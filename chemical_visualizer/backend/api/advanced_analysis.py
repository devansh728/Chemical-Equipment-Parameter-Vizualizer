"""
Advanced Analysis Module for AI-Enhanced Chemical Equipment Parameter Visualization

This module provides deep statistical analysis capabilities including:
- Dynamic column type detection
- Comprehensive descriptive statistics
- Outlier detection using IQR method
- Correlation analysis
- Data quality profiling
"""

import pandas as pd
import numpy as np
from scipy import stats
import logging

logger = logging.getLogger(__name__)


def profile_columns(df):
    """
    Analyze all columns to detect types, missing values, and metadata.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Column profile information
    """
    profile = {
        'total_columns': len(df.columns),
        'total_rows': len(df),
        'columns': []
    }
    
    for col in df.columns:
        col_info = {
            'name': col,
            'type': None,
            'missing_count': int(df[col].isna().sum()),
            'missing_percent': round(float(df[col].isna().sum() / len(df) * 100), 2),
            'unique_count': int(df[col].nunique()),
            'sample_values': []
        }
        
        # Determine column type
        if pd.api.types.is_numeric_dtype(df[col]):
            col_info['type'] = 'numeric'
            col_info['sample_values'] = df[col].dropna().head(3).tolist()
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            col_info['type'] = 'temporal'
            col_info['sample_values'] = df[col].dropna().head(3).astype(str).tolist()
        elif df[col].nunique() < len(df) * 0.5:  # Less than 50% unique = categorical
            col_info['type'] = 'categorical'
            col_info['sample_values'] = df[col].dropna().unique()[:5].tolist()
        else:
            col_info['type'] = 'text'
            col_info['sample_values'] = df[col].dropna().head(3).tolist()
        
        profile['columns'].append(col_info)
    
    return profile


def calculate_statistics(df, numeric_cols):
    """
    Calculate comprehensive descriptive statistics for numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        numeric_cols (list): List of numeric column names
        
    Returns:
        dict: Statistical summary for each numeric column
    """
    stats_summary = {}
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
            
        col_data = df[col].dropna()
        
        if len(col_data) == 0:
            stats_summary[col] = {'error': 'No valid data'}
            continue
        
        stats_summary[col] = {
            'count': int(len(col_data)),
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'std': float(col_data.std()),
            'min': float(col_data.min()),
            'max': float(col_data.max()),
            'q1': float(col_data.quantile(0.25)),
            'q3': float(col_data.quantile(0.75)),
            'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25)),
            'range': float(col_data.max() - col_data.min()),
            'variance': float(col_data.var()),
            'skewness': float(col_data.skew()) if len(col_data) > 2 else 0,
            'kurtosis': float(col_data.kurtosis()) if len(col_data) > 3 else 0,
        }
    
    return stats_summary


def detect_outliers(df, numeric_cols):
    """
    Detect outliers using the Interquartile Range (IQR) method.
    
    Outliers are defined as:
    - Below Q1 - 1.5 * IQR
    - Above Q3 + 1.5 * IQR
    
    Args:
        df (pd.DataFrame): Input dataframe
        numeric_cols (list): List of numeric column names
        
    Returns:
        dict: Outlier information including detected values and statistics
    """
    outliers_data = {
        'total_outliers': 0,
        'by_column': {},
        'outlier_records': []
    }
    
    for col in numeric_cols:
        if col not in df.columns:
            continue
            
        col_data = df[col].dropna()
        
        if len(col_data) < 4:  # Need at least 4 points for quartiles
            continue
        
        # Calculate IQR bounds
        q1 = col_data.quantile(0.25)
        q3 = col_data.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Identify outliers
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_indices = df[outlier_mask].index.tolist()
        outlier_count = len(outlier_indices)
        
        if outlier_count > 0:
            outliers_data['total_outliers'] += outlier_count
            outliers_data['by_column'][col] = {
                'count': outlier_count,
                'percent': round(float(outlier_count / len(df) * 100), 2),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'outlier_values': df.loc[outlier_indices, col].tolist()[:10]  # Max 10 examples
            }
            
            # Store detailed outlier records (limit to 20 total)
            for idx in outlier_indices[:20]:
                outlier_record = {
                    'row_index': int(idx),
                    'column': col,
                    'value': float(df.loc[idx, col]),
                    'expected_range': [float(lower_bound), float(upper_bound)],
                    'deviation_percent': round(
                        float(abs(df.loc[idx, col] - col_data.median()) / col_data.median() * 100), 2
                    )
                }
                
                # Add equipment identifier if available
                if 'Equipment Name' in df.columns:
                    outlier_record['equipment_id'] = str(df.loc[idx, 'Equipment Name'])
                elif 'Type' in df.columns:
                    outlier_record['equipment_type'] = str(df.loc[idx, 'Type'])
                
                outliers_data['outlier_records'].append(outlier_record)
    
    return outliers_data


def calculate_correlations(df, numeric_cols):
    """
    Calculate Pearson correlation matrix for numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
        numeric_cols (list): List of numeric column names
        
    Returns:
        dict: Correlation matrix with column names and values
    """
    if len(numeric_cols) < 2:
        return {'error': 'Need at least 2 numeric columns for correlation'}
    
    # Filter to only numeric columns that exist
    valid_cols = [col for col in numeric_cols if col in df.columns]
    
    if len(valid_cols) < 2:
        return {'error': 'Insufficient numeric columns'}
    
    # Calculate correlation matrix
    corr_matrix = df[valid_cols].corr(method='pearson')
    
    # Convert to JSON-friendly format
    correlation_data = {
        'columns': valid_cols,
        'matrix': corr_matrix.values.tolist(),
        'strong_correlations': []  # |r| > 0.7
    }
    
    # Find strong correlations
    for i, col1 in enumerate(valid_cols):
        for j, col2 in enumerate(valid_cols):
            if i < j:  # Only upper triangle
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) > 0.7:
                    correlation_data['strong_correlations'].append({
                        'column1': col1,
                        'column2': col2,
                        'correlation': round(float(corr_value), 3),
                        'strength': 'very strong' if abs(corr_value) > 0.9 else 'strong'
                    })
    
    return correlation_data


def analyze_csv_enhanced(file_path):
    """
    Main orchestrator for enhanced CSV analysis.
    
    This function performs a complete analysis pipeline:
    1. Load and validate CSV
    2. Profile columns (types, missing data)
    3. Calculate comprehensive statistics
    4. Detect outliers
    5. Calculate correlations
    
    Args:
        file_path (str): Path to CSV file
        
    Returns:
        tuple: (column_profile, enhanced_summary, correlation_matrix, outliers, error)
    """
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        if df.empty:
            return None, None, None, None, "CSV file is empty"
        
        # Step 1: Profile columns
        logger.info(f"Profiling columns for {file_path}")
        column_profile = profile_columns(df)
        
        # Identify numeric columns
        numeric_cols = [
            col_info['name'] for col_info in column_profile['columns']
            if col_info['type'] == 'numeric'
        ]
        
        # Identify categorical columns
        categorical_cols = [
            col_info['name'] for col_info in column_profile['columns']
            if col_info['type'] == 'categorical'
        ]
        
        # Step 2: Calculate statistics
        logger.info(f"Calculating statistics for {len(numeric_cols)} numeric columns")
        numeric_stats = calculate_statistics(df, numeric_cols)
        
        # Step 3: Categorical distributions
        categorical_stats = {}
        for col in categorical_cols:
            if col in df.columns:
                categorical_stats[col] = {
                    'distribution': df[col].value_counts().to_dict(),
                    'unique_count': int(df[col].nunique())
                }
        
        # Step 4: Build enhanced summary
        enhanced_summary = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'numeric_columns_count': len(numeric_cols),
            'categorical_columns_count': len(categorical_cols),
            'numeric_columns': numeric_stats,
            'categorical_columns': categorical_stats,
        }
        
        # Step 5: Detect outliers
        logger.info("Detecting outliers using IQR method")
        outliers = detect_outliers(df, numeric_cols)
        
        # Step 6: Calculate correlations
        logger.info("Calculating correlation matrix")
        correlation_matrix = calculate_correlations(df, numeric_cols)
        
        return column_profile, enhanced_summary, correlation_matrix, outliers, None
        
    except pd.errors.EmptyDataError:
        return None, None, None, None, "CSV file is empty"
    except pd.errors.ParserError as e:
        return None, None, None, None, f"Error parsing CSV: {str(e)}"
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {str(e)}")
        return None, None, None, None, f"Analysis error: {str(e)}"
