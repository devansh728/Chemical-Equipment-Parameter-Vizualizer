from django.urls import path
from .views import (
    FileUploadView,
    HistoryListView,
    DatasetDetailView,
    ReportDownloadView,
    ExplainOutlierView,
    OptimizationView,
    CorrelationHeatmapView,
    DatasetStatsView,
    SignupView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('history/', HistoryListView.as_view(), name='history-list'),
    path('dataset/<int:pk>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('dataset/<int:pk>/report/', ReportDownloadView.as_view(), name='dataset-report'),
    path('dataset/<int:pk>/stats/', DatasetStatsView.as_view(), name='dataset-stats'),
    
    # AI Enhancement Endpoints
    path('dataset/<int:pk>/explain-outlier/', ExplainOutlierView.as_view(), name='explain-outlier'),
    path('dataset/<int:pk>/optimize/', OptimizationView.as_view(), name='optimization'),
    path('dataset/<int:pk>/correlation/', CorrelationHeatmapView.as_view(), name='correlation-heatmap'),
]
