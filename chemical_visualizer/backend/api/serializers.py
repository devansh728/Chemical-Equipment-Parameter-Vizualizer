from rest_framework import serializers
from .models import Dataset
import os
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class DatasetListSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    total_records = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'status', 
            'total_records', 'profiling_complete', 
            'analysis_complete', 'ai_complete'
        ]
    
    def get_filename(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None
    
    def get_total_records(self, obj):
        """Extract total records from summary or enhanced_summary"""
        if obj.enhanced_summary and 'total_records' in obj.enhanced_summary:
            return obj.enhanced_summary['total_records']
        elif obj.summary and 'total_count' in obj.summary:
            return obj.summary['total_count']
        return 0


class DatasetDetailSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'status', 'error_message',
            # Legacy
            'summary',
            # AI-Enhanced Fields
            'enhanced_summary', 'column_profile', 'ai_suggestions',
            'ai_insights', 'correlation_matrix', 'outliers',
            # Status flags
            'profiling_complete', 'analysis_complete', 'ai_complete'
        ]
    
    def get_filename(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return None

