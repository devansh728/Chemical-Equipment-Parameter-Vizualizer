import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import Dataset
from .serializers import DatasetListSerializer, DatasetDetailSerializer
from .tasks import phase1_profile_and_suggest, explain_outlier_task, get_recommendations_task
from .analysis import analyze_csv
from .pdf_generator_enhanced import generate_enhanced_report


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated users to sign up

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            'user': serializer.data,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)
        
class FileUploadView(APIView):
    """
    API endpoint for uploading CSV files.
    Triggers async processing with Celery and manages dataset history (max 5).
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        # Check if file is provided
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file extension
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'Only CSV files are allowed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create dataset with PROCESSING status
        dataset = Dataset.objects.create(
            user=request.user,
            file=file,
            status='PROCESSING'
        )
        
        # Trigger new multi-phase async processing pipeline
        phase1_profile_and_suggest.delay(dataset.id)
        
        # History management: Keep only the 5 most recent datasets
        user_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')
        
        if user_datasets.count() > 5:
            # Delete datasets beyond the 5 most recent
            datasets_to_delete = user_datasets[5:]
            for old_dataset in datasets_to_delete:
                # Delete the file from storage
                if old_dataset.file:
                    try:
                        if os.path.isfile(old_dataset.file.path):
                            os.remove(old_dataset.file.path)
                    except Exception as e:
                        print(f"Error deleting file: {e}")
                # Delete the dataset object
                old_dataset.delete()
        
        # Return accepted response with dataset info
        return Response(
            {
                'message': 'File uploaded successfully. Processing started.',
                'dataset_id': dataset.id,
                'status': dataset.status
            },
            status=status.HTTP_202_ACCEPTED
        )


class HistoryListView(generics.ListAPIView):
    """
    API endpoint to list the last 5 datasets for the authenticated user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetListSerializer
    
    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]


class DatasetDetailView(APIView):
    """
    API endpoint to retrieve detailed information about a specific dataset.
    Includes full data (re-analyzed) and summary.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Serialize basic info
        serializer = DatasetDetailSerializer(dataset)
        response_data = serializer.data
        
        # If analysis is completed, get full data
        if dataset.status == 'COMPLETED' and dataset.file:
            try:
                summary, data, error = analyze_csv(dataset.file.path)
                if not error:
                    response_data['data'] = data
                else:
                    response_data['data'] = []
            except Exception as e:
                response_data['data'] = []
                response_data['data_error'] = str(e)
        else:
            response_data['data'] = []
        
        return Response(response_data)


class ReportDownloadView(APIView):
    """
    API endpoint to download a PDF report for a completed dataset.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Check if analysis is completed
        if dataset.status != 'COMPLETED':
            return Response(
                {'error': 'Dataset analysis is not completed yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not dataset.summary:
            return Response(
                {'error': 'No summary data available for this dataset'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get full data for the report
            summary, data, error = analyze_csv(dataset.file.path)
            
            if error:
                return Response(
                    {'error': f'Error reading dataset: {error}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Generate PDF with AI insights
            pdf_buffer = generate_enhanced_report(summary, data, dataset=dataset)
            
            # Create HTTP response with PDF
            response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="dataset_{pk}_report.pdf"'
            
            return response
            
        except Exception as e:
            return Response(
                {'error': f'Error generating report: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExplainOutlierView(APIView):
    """
    API endpoint to get AI explanation for a specific outlier.
    
    POST /api/dataset/<id>/explain-outlier/
    Body: {
        "equipment_name": "HE-101",
        "equipment_type": "Heat Exchanger",
        "parameter": "Temperature",
        "value": 450.5,
        "expected_range": [200, 400]
    }
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Validate required fields
        required_fields = ['equipment_name', 'equipment_type', 'parameter', 'value', 'expected_range']
        missing = [f for f in required_fields if f not in request.data]
        
        if missing:
            return Response(
                {'error': f'Missing required fields: {", ".join(missing)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Trigger async task
            result = explain_outlier_task.delay(dataset.id, request.data)
            
            # Wait for result (max 60 seconds for Gemini API)
            explanation = result.get(timeout=60)
            
            return Response({
                'explanation': explanation,
                'outlier': request.data
            })
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate explanation: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class OptimizationView(APIView):
    """
    API endpoint to get process optimization recommendations.
    
    GET /api/dataset/<id>/optimize/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Check if analysis is completed
        if not dataset.analysis_complete:
            return Response(
                {'error': 'Analysis not completed yet. Please wait for deep analysis to finish.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Trigger async task
            result = get_recommendations_task.delay(dataset.id)
            
            # Wait for result (max 60 seconds for Gemini API)
            recommendations = result.get(timeout=60)
            
            return Response(recommendations)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to generate recommendations: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CorrelationHeatmapView(APIView):
    """
    API endpoint to get correlation matrix data for heatmap visualization.
    
    GET /api/dataset/<id>/correlation/
    
    Returns:
    {
        "correlation_matrix": [[1.0, 0.85, ...], ...],
        "column_names": ["Temperature", "Pressure", ...],
        "strong_correlations": [
            {"param1": "Temperature", "param2": "Pressure", "coefficient": 0.92}
        ]
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Check if analysis is completed
        if not dataset.analysis_complete:
            return Response(
                {'error': 'Analysis not completed yet. Please wait for deep analysis to finish.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not dataset.correlation_matrix:
            return Response(
                {'error': 'No correlation data available for this dataset'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(dataset.correlation_matrix)


class DatasetStatsView(APIView):
    """
    API endpoint to get calculated statistics for stats cards.
    
    GET /api/dataset/<id>/stats/
    
    Returns:
    {
        "total_records": 100,
        "avg_pressure": 250.5,
        "avg_temperature": 350.2,
        "avg_flowrate": 120.8
    }
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        # Get the dataset and ensure it belongs to the user
        dataset = get_object_or_404(Dataset, pk=pk, user=request.user)
        
        # Initialize default stats
        stats = {
            'total_records': 0,
            'avg_pressure': 0,
            'avg_temperature': 0,
            'avg_flowrate': 0
        }
        
        # Extract from enhanced_summary if available
        if dataset.enhanced_summary:
            stats['total_records'] = dataset.enhanced_summary.get('total_records', 0)
            
            # Extract averages from numeric columns
            numeric_cols = dataset.enhanced_summary.get('numeric_columns', {})
            
            # Check for common parameter names (case-insensitive)
            for col_name, col_stats in numeric_cols.items():
                col_lower = col_name.lower()
                if 'pressure' in col_lower:
                    stats['avg_pressure'] = col_stats.get('mean', 0)
                elif 'temperature' in col_lower:
                    stats['avg_temperature'] = col_stats.get('mean', 0)
                elif 'flowrate' in col_lower or 'flow' in col_lower:
                    stats['avg_flowrate'] = col_stats.get('mean', 0)
        
        # Fallback to legacy summary if enhanced_summary not available
        elif dataset.summary:
            stats['total_records'] = dataset.summary.get('total_count', 0)
            averages = dataset.summary.get('averages', {})
            stats['avg_pressure'] = averages.get('pressure', 0)
            stats['avg_temperature'] = averages.get('temperature', 0)
            stats['avg_flowrate'] = averages.get('flowrate', 0)
        
        return Response(stats)
