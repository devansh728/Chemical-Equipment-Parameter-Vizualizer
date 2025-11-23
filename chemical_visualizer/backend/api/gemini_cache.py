"""
Cached and Optimized Gemini Service Wrapper

This module wraps the GeminiAnalyzer with caching and optimization:
- Redis caching for all AI responses
- Optimized prompts for faster generation
- Reduced token usage
- Cache warming strategies
- Fallback mechanisms
"""

import hashlib
import json
import logging
from typing import Dict, List, Any, Optional
from django.core.cache import cache
from django.conf import settings
from .gemini_service import GeminiAnalyzer

logger = logging.getLogger(__name__)


def generate_cache_key(prefix: str, data: Any) -> str:
    """
    Generate a consistent cache key from data.
    
    Args:
        prefix: Cache key prefix (e.g., 'ai_suggestions')
        data: Data to hash (dict, list, etc.)
    
    Returns:
        str: Hashed cache key
    """
    # Convert data to JSON string for consistent hashing
    data_str = json.dumps(data, sort_keys=True)
    data_hash = hashlib.md5(data_str.encode()).hexdigest()
    return f"{prefix}_{data_hash}"


class CachedGeminiService:
    """
    Wrapper around GeminiAnalyzer with caching and optimization.
    """
    
    def __init__(self):
        """Initialize the Gemini analyzer and cache TTL settings."""
        self.analyzer = GeminiAnalyzer()
        self.cache_ttl = getattr(settings, 'CACHE_TTL', {
            'ai_suggestions': 86400,
            'executive_summary': 43200,
            'outlier_explanation': 3600,
            'optimizations': 7200,
        })
    
    def get_analysis_suggestions(self, column_profile: Dict, use_cache: bool = True) -> Optional[Dict]:
        """
        Get AI analysis suggestions with caching.
        
        Args:
            column_profile: Column profiling data
            use_cache: Whether to use cached results (default: True)
        
        Returns:
            dict: Analysis suggestions
        """
        if not use_cache:
            return self.analyzer.get_analysis_suggestions(column_profile)
        
        # Generate cache key from column structure (ignore sample data)
        cache_data = {
            'columns': [
                {'name': c['name'], 'type': c['type']} 
                for c in column_profile.get('columns', [])
            ]
        }
        cache_key = generate_cache_key('ai_suggestions', cache_data)
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for AI suggestions: {cache_key}")
            return cached_result
        
        # Cache miss - call Gemini API
        logger.info(f"Cache MISS for AI suggestions: {cache_key}")
        result = self.analyzer.get_analysis_suggestions(column_profile)
        
        # Store in cache
        if result:
            cache.set(cache_key, result, self.cache_ttl['ai_suggestions'])
            logger.info(f"Cached AI suggestions for {self.cache_ttl['ai_suggestions']}s")
        
        return result
    
    def generate_executive_summary(
        self, 
        enhanced_summary: Dict, 
        outliers: Dict, 
        correlation_matrix: Dict,
        use_cache: bool = True
    ) -> Optional[Dict]:
        """
        Generate executive summary with caching.
        
        Args:
            enhanced_summary: Statistical summary
            outliers: Outlier detection results
            correlation_matrix: Correlation data
            use_cache: Whether to use cached results
        
        Returns:
            dict: Executive summary with insights
        """
        if not use_cache:
            return self.analyzer.generate_executive_summary(
                enhanced_summary, outliers, correlation_matrix
            )
        
        # Generate cache key from summary statistics
        cache_data = {
            'total_records': enhanced_summary.get('total_records', 0),
            'outliers_count': outliers.get('total_outliers', 0),
            'stats': {
                param: {
                    'mean': stats.get('mean'),
                    'std': stats.get('std'),
                    'min': stats.get('min'),
                    'max': stats.get('max')
                }
                for param, stats in enhanced_summary.get('statistics', {}).items()
            }
        }
        cache_key = generate_cache_key('executive_summary', cache_data)
        
        # Try cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for executive summary: {cache_key}")
            return cached_result
        
        # Cache miss - call Gemini
        logger.info(f"Cache MISS for executive summary: {cache_key}")
        result = self.analyzer.generate_executive_summary(
            enhanced_summary, outliers, correlation_matrix
        )
        
        # Cache the result
        if result:
            cache.set(cache_key, result, self.cache_ttl['executive_summary'])
            logger.info(f"Cached executive summary for {self.cache_ttl['executive_summary']}s")
        
        return result
    
    def explain_anomaly(
        self,
        equipment_type: str,
        parameter: str,
        value: float,
        expected_range: List[float],
        use_cache: bool = True
    ) -> str:
        """
        Explain an outlier with caching.
        
        Args:
            equipment_type: Type of equipment
            parameter: Parameter name
            value: Outlier value
            expected_range: Expected value range
            use_cache: Whether to use cached results
        
        Returns:
            str: Explanation text
        """
        if not use_cache:
            return self.analyzer.explain_anomaly(
                equipment_type, parameter, value, expected_range
            )
        
        # Generate cache key (round value to reduce key variations)
        cache_data = {
            'type': equipment_type,
            'param': parameter,
            'value': round(value, 1),  # Round to reduce cache misses
            'range': [round(expected_range[0], 1), round(expected_range[1], 1)]
        }
        cache_key = generate_cache_key('outlier_explanation', cache_data)
        
        # Try cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for outlier explanation: {cache_key}")
            return cached_result
        
        # Cache miss
        logger.info(f"Cache MISS for outlier explanation: {cache_key}")
        result = self.analyzer.explain_anomaly(
            equipment_type, parameter, value, expected_range
        )
        
        # Cache the result
        if result:
            cache.set(cache_key, result, self.cache_ttl['outlier_explanation'])
            logger.info(f"Cached outlier explanation for {self.cache_ttl['outlier_explanation']}s")
        
        return result
    
    def get_optimization_recommendations(
        self,
        enhanced_summary: Dict,
        outliers: Dict = None,
        correlation_matrix: Dict = None,
        use_cache: bool = True
    ) -> Dict:
        """
        Get optimization recommendations with caching.
        
        Args:
            enhanced_summary: Statistical summary
            outliers: Outlier detection results (unused, for compatibility)
            correlation_matrix: Correlation data (unused, for compatibility)
            use_cache: Whether to use cached results
        
        Returns:
            dict: Optimization recommendations
        """
        if not use_cache:
            return self.analyzer.get_optimization_recommendations(enhanced_summary)
        
        # Generate cache key
        cache_data = {
            'stats': {
                param: {
                    'mean': round(stats.get('mean', 0), 1),
                    'std': round(stats.get('std', 0), 1),
                }
                for param, stats in enhanced_summary.get('statistics', {}).items()
            },
            'outliers': outliers.get('total_outliers', 0),
            'strong_corrs': len(correlation_matrix.get('strong_correlations', []))
        }
        cache_key = generate_cache_key('optimizations', cache_data)
        
        # Try cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info(f"Cache HIT for optimizations: {cache_key}")
            return cached_result
        
        # Cache miss
        logger.info(f"Cache MISS for optimizations: {cache_key}")
        result = self.analyzer.get_optimization_recommendations(enhanced_summary)
        
        # Cache the result
        if result:
            cache.set(cache_key, result, self.cache_ttl['optimizations'])
            logger.info(f"Cached optimizations for {self.cache_ttl['optimizations']}s")
        
        return result
    
    def warm_cache_for_dataset(self, dataset):
        """
        Pre-warm cache for a dataset by running all AI operations.
        Useful for background processing.
        
        Args:
            dataset: Dataset model instance
        """
        logger.info(f"Warming cache for dataset {dataset.id}")
        
        try:
            # Warm suggestions cache
            if dataset.column_profile:
                self.get_analysis_suggestions(dataset.column_profile)
            
            # Warm executive summary cache
            if dataset.enhanced_summary:
                self.generate_executive_summary(
                    dataset.enhanced_summary or {},
                    dataset.outliers or {},
                    dataset.correlation_matrix or {}
                )
            
            # Warm optimizations cache
            if dataset.enhanced_summary:
                self.get_optimization_recommendations(
                    dataset.enhanced_summary or {},
                    dataset.outliers or {},
                    dataset.correlation_matrix or {}
                )
            
            logger.info(f"Cache warmed for dataset {dataset.id}")
        except Exception as e:
            logger.error(f"Error warming cache: {e}")
    
    def clear_cache_for_dataset(self, dataset):
        """
        Clear all cached data for a specific dataset.
        
        Args:
            dataset: Dataset model instance
        """
        # This is a best-effort clear - we don't track all keys
        # In production, you might want to use cache key patterns
        logger.info(f"Clearing cache for dataset {dataset.id}")
        
        # Clear by regenerating keys and deleting
        try:
            if dataset.column_profile:
                cache_data = {
                    'columns': [
                        {'name': c['name'], 'type': c['type']} 
                        for c in dataset.column_profile.get('columns', [])
                    ]
                }
                cache_key = generate_cache_key('ai_suggestions', cache_data)
                cache.delete(cache_key)
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")


# Singleton instance
_cached_service = None

def get_cached_gemini_service() -> CachedGeminiService:
    """
    Get singleton instance of CachedGeminiService.
    
    Returns:
        CachedGeminiService: Cached Gemini service instance
    """
    global _cached_service
    if _cached_service is None:
        _cached_service = CachedGeminiService()
    return _cached_service
