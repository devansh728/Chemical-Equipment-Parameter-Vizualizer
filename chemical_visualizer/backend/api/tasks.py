from celery import shared_task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Dataset
from .analysis import analyze_csv
from .advanced_analysis import analyze_csv_enhanced
from .gemini_cache import get_cached_gemini_service
import logging

logger = logging.getLogger(__name__)


def send_websocket_notification(user_id, message):
    """Helper function to send WebSocket notifications"""
    try:
        channel_layer = get_channel_layer()
        
        # Send to user-specific group
        async_to_sync(channel_layer.group_send)(
            f"user_{user_id}",
            {
                'type': 'analysis_message',
                'message': message
            }
        )
        
        # Also send to broadcast group for unauthenticated users
        async_to_sync(channel_layer.group_send)(
            "broadcast_group",
            {
                'type': 'analysis_message',
                'message': message
            }
        )
    except Exception as e:
        logger.error(f"Failed to send WebSocket notification: {str(e)}")


@shared_task
def phase1_profile_and_suggest(dataset_id):
    """
    Phase 1: Column profiling + AI suggestions (5-10 seconds)
    
    - Analyzes CSV column structure
    - Sends column info to Gemini for smart suggestions
    - Saves to dataset.column_profile and dataset.ai_suggestions
    - Triggers Phase 2
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        logger.info(f"[Phase 1] Profiling dataset {dataset_id}")
        
        dataset.status = 'PROFILING'
        dataset.save()
        
        # Run basic analysis for backward compatibility
        summary, data, error = analyze_csv(dataset.file.path)
        
        if error:
            dataset.status = 'FAILED'
            dataset.error_message = error
            dataset.save()
            send_websocket_notification(dataset.user.id, {
                'dataset_id': dataset.id,
                'status': 'FAILED',
                'error': error
            })
            return f"Dataset {dataset_id} failed in Phase 1: {error}"
        
        # Save legacy summary for backward compatibility
        dataset.summary = summary
        
        # Run enhanced analysis - Phase 1: Column profiling only
        from .advanced_analysis import profile_columns
        import pandas as pd
        
        df = pd.read_csv(dataset.file.path)
        column_profile = profile_columns(df)
        
        dataset.column_profile = column_profile
        
        # Get AI suggestions with caching
        try:
            gemini_service = get_cached_gemini_service()
            ai_suggestions = gemini_service.get_analysis_suggestions(column_profile)
            dataset.ai_suggestions = ai_suggestions
            logger.info(f"[Phase 1] AI suggestions generated for dataset {dataset_id}")
        except Exception as e:
            logger.warning(f"[Phase 1] AI suggestions failed: {str(e)}, using fallback")
            dataset.ai_suggestions = {'suggestions': []}
        
        dataset.profiling_complete = True
        dataset.save()
        
        # Notify frontend
        send_websocket_notification(dataset.user.id, {
            'dataset_id': dataset.id,
            'status': 'profiling_complete',
            'column_profile': column_profile,
            'ai_suggestions': dataset.ai_suggestions
        })
        
        # Trigger Phase 2
        phase2_deep_analysis.delay(dataset_id)
        
        return f"Dataset {dataset_id} Phase 1 complete"
        
    except Exception as e:
        logger.error(f"[Phase 1] Error: {str(e)}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            dataset.status = 'FAILED'
            dataset.error_message = f"Phase 1 error: {str(e)}"
            dataset.save()
        except:
            pass
        return f"Phase 1 failed: {str(e)}"


@shared_task
def phase2_deep_analysis(dataset_id):
    """
    Phase 2: Deep statistical analysis (10-20 seconds)
    
    - Calculates comprehensive statistics
    - Detects outliers using IQR
    - Calculates correlation matrix
    - Saves to enhanced_summary, correlation_matrix, outliers
    - Triggers Phase 3
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        logger.info(f"[Phase 2] Deep analysis for dataset {dataset_id}")
        
        dataset.status = 'ANALYZING'
        dataset.save()
        
        # Run enhanced analysis
        column_profile, enhanced_summary, correlation_matrix, outliers, error = \
            analyze_csv_enhanced(dataset.file.path)
        
        if error:
            dataset.status = 'FAILED'
            dataset.error_message = error
            dataset.save()
            send_websocket_notification(dataset.user.id, {
                'dataset_id': dataset.id,
                'status': 'FAILED',
                'error': error
            })
            return f"Dataset {dataset_id} failed in Phase 2: {error}"
        
        # Save results
        dataset.enhanced_summary = enhanced_summary
        dataset.correlation_matrix = correlation_matrix
        dataset.outliers = outliers
        dataset.analysis_complete = True
        dataset.save()
        
        logger.info(f"[Phase 2] Analysis complete for dataset {dataset_id}")
        
        # Notify frontend
        send_websocket_notification(dataset.user.id, {
            'dataset_id': dataset.id,
            'status': 'analysis_complete',
            'enhanced_summary': enhanced_summary,
            'outliers_count': outliers.get('total_outliers', 0)
        })
        
        # Trigger Phase 3
        phase3_ai_insights.delay(dataset_id)
        
        return f"Dataset {dataset_id} Phase 2 complete"
        
    except Exception as e:
        logger.error(f"[Phase 2] Error: {str(e)}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            dataset.status = 'FAILED'
            dataset.error_message = f"Phase 2 error: {str(e)}"
            dataset.save()
        except:
            pass
        return f"Phase 2 failed: {str(e)}"


@shared_task
def phase3_ai_insights(dataset_id):
    """
    Phase 3: AI Executive Summary (5-10 seconds)
    
    - Sends statistics to Gemini
    - Gets natural language insights
    - Provides recommendations
    - Saves to ai_insights
    - Marks dataset as COMPLETED
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        logger.info(f"[Phase 3] Generating AI insights for dataset {dataset_id}")
        
        dataset.status = 'AI_PROCESSING'
        dataset.save()
        
        # Generate AI insights with caching
        try:
            gemini_service = get_cached_gemini_service()
            ai_insights = gemini_service.generate_executive_summary(
                dataset.enhanced_summary or {},
                dataset.outliers or {},
                dataset.correlation_matrix or {}
            )
            dataset.ai_insights = ai_insights
            logger.info(f"[Phase 3] AI insights generated for dataset {dataset_id}")
        except Exception as e:
            logger.warning(f"[Phase 3] AI insights failed: {str(e)}, using fallback")
            dataset.ai_insights = {
                'executive_summary': 'AI insights unavailable. Please review the statistical analysis.',
                'risk_level': 'unknown',
                'recommendations': []
            }
        
        dataset.ai_complete = True
        dataset.status = 'COMPLETED'
        dataset.save()
        
        logger.info(f"[Phase 3] All phases complete for dataset {dataset_id}")
        
        # Final notification
        send_websocket_notification(dataset.user.id, {
            'dataset_id': dataset.id,
            'status': 'COMPLETED',
            'ai_insights': dataset.ai_insights
        })
        
        return f"Dataset {dataset_id} fully processed"
        
    except Exception as e:
        logger.error(f"[Phase 3] Error: {str(e)}")
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            # Don't mark as FAILED if only AI insights failed
            # Mark as COMPLETED since analysis is done
            dataset.status = 'COMPLETED'
            dataset.ai_complete = True
            dataset.save()
        except:
            pass
        return f"Phase 3 completed with warnings: {str(e)}"


@shared_task
def explain_outlier_task(dataset_id, outlier_data):
    """
    On-demand: Explain a specific outlier using AI
    
    Args:
        dataset_id (int): Dataset ID
        outlier_data (dict): {
            'equipment_name': str,
            'equipment_type': str,
            'parameter': str,
            'value': float,
            'expected_range': [lower, upper]
        }
    
    Returns:
        str: AI explanation
    """
    try:
        logger.info(f"[Explain Outlier] Dataset {dataset_id}")
        
        gemini_service = get_cached_gemini_service()
        explanation = gemini_service.explain_anomaly(
            equipment_type=outlier_data.get('equipment_type', 'Equipment'),
            parameter=outlier_data.get('parameter', 'Parameter'),
            value=outlier_data.get('value', 0),
            expected_range=outlier_data.get('expected_range', [0, 0])
        )
        
        return explanation
        
    except Exception as e:
        logger.error(f"[Explain Outlier] Error: {str(e)}")
        return f"Unable to generate explanation: {str(e)}"


@shared_task
def get_recommendations_task(dataset_id):
    """
    On-demand: Get process optimization recommendations
    
    Args:
        dataset_id (int): Dataset ID
    
    Returns:
        dict: Optimization recommendations
    """
    try:
        dataset = Dataset.objects.get(id=dataset_id)
        logger.info(f"[Recommendations] Dataset {dataset_id}")
        
        gemini_service = get_cached_gemini_service()
        recommendations = gemini_service.get_optimization_recommendations(
            dataset.enhanced_summary or {},
            dataset.outliers or {},
            dataset.correlation_matrix or {}
        )
        
        return recommendations
        
    except Exception as e:
        logger.error(f"[Recommendations] Error: {str(e)}")
        return {
            'optimizations': [],
            'error': str(e)
        }


# Legacy task for backward compatibility
@shared_task
def process_csv_task(dataset_id):
    """
    Legacy task - redirects to new multi-phase pipeline
    Kept for backward compatibility
    """
    logger.info(f"Legacy task called, redirecting to new pipeline for dataset {dataset_id}")
    return phase1_profile_and_suggest.delay(dataset_id)

