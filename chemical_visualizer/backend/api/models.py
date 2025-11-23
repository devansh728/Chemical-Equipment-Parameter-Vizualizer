from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    STATUS_CHOICES = [
        ('PROCESSING', 'Processing'),
        ('PROFILING', 'Profiling Columns'),
        ('ANALYZING', 'Deep Analysis'),
        ('AI_PROCESSING', 'Generating AI Insights'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Legacy field (keep for backward compatibility)
    summary = models.JSONField(null=True, blank=True)
    
    # AI-Enhanced Fields
    enhanced_summary = models.JSONField(null=True, blank=True, help_text='Deep statistical analysis with quartiles, std, etc.')
    column_profile = models.JSONField(null=True, blank=True, help_text='Column types, missing values, unique counts')
    ai_suggestions = models.JSONField(null=True, blank=True, help_text='Gemini-generated analysis suggestions')
    ai_insights = models.JSONField(null=True, blank=True, help_text='AI executive summary and recommendations')
    correlation_matrix = models.JSONField(null=True, blank=True, help_text='Correlation matrix for numeric columns')
    outliers = models.JSONField(null=True, blank=True, help_text='Detected outliers with IQR method')
    
    # Status tracking for multi-phase processing
    profiling_complete = models.BooleanField(default=False)
    analysis_complete = models.BooleanField(default=False)
    ai_complete = models.BooleanField(default=False)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PROCESSING')
    error_message = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.file.name} - {self.status}"

