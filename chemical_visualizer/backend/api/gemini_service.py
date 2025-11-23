"""
Gemini AI Service for Intelligent Chemical Equipment Analysis

This module integrates Google's Gemini API to provide:
- Smart analysis suggestions based on CSV column structure
- Executive summaries in natural language
- Anomaly explanations for outliers
- Process optimization recommendations
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("google-generativeai not installed. AI features will be disabled.")

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    """
    AI-powered analyzer using Google's Gemini API for chemical equipment insights.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client with API key from environment or parameter.
        
        Args:
            api_key (str, optional): Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        if not GEMINI_AVAILABLE:
            self.enabled = False
            logger.warning("Gemini AI features disabled - library not installed")
            return
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            self.enabled = False
            logger.warning("GEMINI_API_KEY not found. AI features will be disabled.")
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                'models/gemini-2.5-flash',
                generation_config={
                    'temperature': 0.7,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 2048,  # Limit token output for faster response
                }
            )
            self.enabled = True
            logger.info("Gemini AI service initialized successfully")
        except Exception as e:
            self.enabled = False
            logger.error(f"Failed to initialize Gemini: {str(e)}")
    
    def get_analysis_suggestions(self, column_profile: Dict) -> Optional[Dict]:
        """
        Generate smart analysis suggestions based on CSV column structure.
        
        This is Phase 1 - helps users understand what analyses to run.
        
        Args:
            column_profile (dict): Column profiling data from advanced_analysis.py
            
        Returns:
            dict: Analysis suggestions with chart types and priorities
        """
        if not self.enabled:
            return self._get_fallback_suggestions(column_profile)
        
        try:
            columns_info = column_profile.get('columns', [])
            
            # Create a concise description of the dataset
            numeric_cols = [c['name'] for c in columns_info if c['type'] == 'numeric']
            categorical_cols = [c['name'] for c in columns_info if c['type'] == 'categorical']
            temporal_cols = [c['name'] for c in columns_info if c['type'] == 'temporal']
            
            prompt = f"""You are an expert chemical process engineer analyzing equipment data.

Dataset Structure:
- Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}
- Categorical columns: {', '.join(categorical_cols) if categorical_cols else 'None'}
- Time-based columns: {', '.join(temporal_cols) if temporal_cols else 'None'}

Task: Suggest 3-5 most valuable analyses to run on this data.

For each suggestion, provide:
1. A descriptive title
2. Why this analysis is important for chemical equipment monitoring
3. Which chart type to use (scatter, line, bar, heatmap, box)
4. Which columns to analyze (x_axis, y_axis, or group_by)
5. Priority level (high, medium, low)

Return ONLY valid JSON in this format:
{{
  "suggestions": [
    {{
      "title": "Temperature-Pressure Correlation",
      "description": "Analyze relationship between reactor temperature and system pressure",
      "chart_type": "scatter",
      "x_axis": "Temperature",
      "y_axis": "Pressure",
      "priority": "high",
      "reasoning": "Strong correlations indicate...",
    }}
  ]
}}"""
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON from response
            response_text = response.text.strip()
            
            # Clean up markdown code blocks if present
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            suggestions = json.loads(response_text)
            logger.info(f"Generated {len(suggestions.get('suggestions', []))} AI suggestions")
            
            return suggestions
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {str(e)}")
            return self._get_fallback_suggestions(column_profile)
        except Exception as e:
            logger.error(f"Error getting AI suggestions: {str(e)}")
            return self._get_fallback_suggestions(column_profile)
    
    def generate_executive_summary(self, enhanced_summary: Dict, outliers: Dict, correlations: Dict) -> Optional[Dict]:
        """
        Generate AI-powered executive summary from statistical analysis.
        
        This is Phase 3 - converts numbers into actionable insights.
        
        Args:
            enhanced_summary (dict): Statistical analysis results
            outliers (dict): Detected outliers
            correlations (dict): Correlation matrix
            
        Returns:
            dict: Executive summary with insights and recommendations
        """
        if not self.enabled:
            return self._get_fallback_summary(enhanced_summary, outliers)
        
        try:
            prompt = f"""You are a senior chemical process engineer reviewing equipment data.

Statistical Summary:
- Total Records: {enhanced_summary.get('total_records', 0)}
- Numeric Columns: {enhanced_summary.get('numeric_columns_count', 0)}
- Outliers Detected: {outliers.get('total_outliers', 0)}
- Strong Correlations: {len(correlations.get('strong_correlations', []))}

Detailed Data:
{json.dumps(enhanced_summary.get('numeric_columns', {}), indent=2)[:1500]}

Outliers:
{json.dumps(outliers.get('by_column', {}), indent=2)[:800]}

Strong Correlations:
{json.dumps(correlations.get('strong_correlations', []), indent=2)[:800]}

Task: Write a concise 3-paragraph executive summary for a plant manager.

Paragraph 1: Overall data quality and key statistics
Paragraph 2: Critical anomalies and their potential implications
Paragraph 3: Notable correlations and what they mean for operations

Then provide 3 specific, actionable recommendations.

Return ONLY valid JSON:
{{
  "executive_summary": "**Overall Assessment:**\\n\\n[paragraph 1]\\n\\n**Critical Findings:**\\n\\n[paragraph 2]\\n\\n**Process Insights:**\\n\\n[paragraph 3]",
  "risk_level": "low|medium|high",
  "key_metrics": [
    {{"metric": "Average Temperature", "value": "325.5°C", "status": "normal|warning|critical"}}
  ],
  "recommendations": [
    "Inspect equipment X for...",
    "Monitor parameter Y...",
    "Consider process optimization..."
  ],
  "anomalies_count": 3,
  "correlations_count": 2
}}"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean markdown
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            insights = json.loads(response_text)
            logger.info("Generated AI executive summary")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return self._get_fallback_summary(enhanced_summary, outliers)
    
    def explain_anomaly(self, equipment_name: str, equipment_type: str, parameter: str, 
                       value: float, expected_range: List[float]) -> Optional[str]:
        """
        Explain a specific outlier/anomaly using AI.
        
        This is called on-demand when user clicks "Why?" on an outlier.
        
        Args:
            equipment_name (str): Equipment identifier
            equipment_type (str): Type of equipment (Pump, Reactor, etc.)
            parameter (str): Parameter name (Pressure, Temperature, etc.)
            value (float): Actual outlier value
            expected_range (list): [lower_bound, upper_bound]
            
        Returns:
            str: Plain text explanation
        """
        if not self.enabled:
            return self._get_fallback_explanation(equipment_type, parameter, value, expected_range)
        
        try:
            prompt = f"""You are a chemical equipment maintenance expert.

Equipment: {equipment_name} (Type: {equipment_type})
Parameter: {parameter}
Measured Value: {value}
Expected Range: {expected_range[0]} to {expected_range[1]}

This value is OUTSIDE the normal range.

Provide 3 possible causes for this anomaly in a chemical plant context.
Be specific to the equipment type and parameter.
Keep each explanation to 1-2 sentences.

Format as a numbered list."""
            
            response = self.model.generate_content(prompt)
            explanation = response.text.strip()
            
            logger.info(f"Generated anomaly explanation for {equipment_name}")
            return explanation
            
        except Exception as e:
            logger.error(f"Error explaining anomaly: {str(e)}")
            return self._get_fallback_explanation(equipment_type, parameter, value, expected_range)
    
    def get_optimization_recommendations(self, enhanced_summary: Dict) -> Optional[Dict]:
        """
        Get process optimization recommendations using AI.
        
        This is called on-demand when user clicks "Optimize" button.
        
        Args:
            enhanced_summary (dict): Statistical analysis results
            
        Returns:
            dict: Optimization suggestions
        """
        if not self.enabled:
            return self._get_fallback_optimization()
        
        try:
            prompt = f"""You are a process optimization consultant for chemical plants.

Equipment Data Summary:
{json.dumps(enhanced_summary.get('numeric_columns', {}), indent=2)[:1200]}

Task: Suggest 2-3 specific areas for process optimization or energy savings.

For each suggestion:
1. Title (concise)
2. Description (2-3 sentences)
3. Expected benefit (energy savings %, quality improvement, etc.)
4. Implementation difficulty (easy, medium, hard)

Return ONLY valid JSON:
{{
  "optimizations": [
    {{
      "title": "Heat Recovery Optimization",
      "description": "...",
      "expected_benefit": "15-20% steam savings",
      "difficulty": "medium",
      "priority": "high|medium|low"
    }}
  ]
}}"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            optimizations = json.loads(response_text)
            logger.info("Generated optimization recommendations")
            
            return optimizations
            
        except Exception as e:
            logger.error(f"Error generating optimizations: {str(e)}")
            return self._get_fallback_optimization()
    
    # Fallback methods (when Gemini is unavailable)
    
    def _get_fallback_suggestions(self, column_profile: Dict) -> Dict:
        """Provide basic suggestions without AI"""
        columns = column_profile.get('columns', [])
        numeric_cols = [c['name'] for c in columns if c['type'] == 'numeric']
        
        suggestions = []
        
        if len(numeric_cols) >= 2:
            suggestions.append({
                'title': f'{numeric_cols[0]} vs {numeric_cols[1]} Analysis',
                'description': 'Scatter plot analysis',
                'chart_type': 'scatter',
                'x_axis': numeric_cols[0],
                'y_axis': numeric_cols[1],
                'priority': 'high'
            })
        
        return {'suggestions': suggestions}
    
    def _get_fallback_summary(self, enhanced_summary: Dict, outliers: Dict) -> Dict:
        """Provide basic summary without AI"""
        return {
            'executive_summary': f"Analysis of {enhanced_summary.get('total_records', 0)} records complete. {outliers.get('total_outliers', 0)} outliers detected.",
            'risk_level': 'medium',
            'recommendations': ['Review data for quality', 'Investigate outliers'],
            'anomalies_count': outliers.get('total_outliers', 0)
        }
    
    def _get_fallback_explanation(self, equipment_type: str, parameter: str, value: float, expected_range: List) -> str:
        """Provide basic explanation without AI"""
        return f"The {parameter} value of {value} is outside the expected range [{expected_range[0]}, {expected_range[1]}]. Common causes: sensor malfunction, process upset, or equipment degradation."
    
    def _get_fallback_optimization(self) -> Dict:
        """Provide basic optimization without AI"""
        return {
            'optimizations': [
                {
                    'title': 'Data Quality Review',
                    'description': 'Review equipment sensors for calibration',
                    'expected_benefit': 'Improved data reliability',
                    'difficulty': 'easy',
                    'priority': 'medium'
                }
            ]
        }
