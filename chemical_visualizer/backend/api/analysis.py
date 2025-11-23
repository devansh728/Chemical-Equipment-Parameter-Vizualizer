import pandas as pd


def analyze_csv(file_path):
    """
    Analyze CSV file containing chemical equipment parameters.
    
    Returns:
        tuple: (summary_dict, data_list_of_dicts, error_string)
               If error occurs, summary_dict and data_list_of_dicts will be None
    """
    required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
    
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Validate required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return None, None, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Remove rows with missing values in critical columns
        df = df.dropna(subset=required_columns)
        
        if df.empty:
            return None, None, "No valid data found in CSV file after removing rows with missing values"
        
        # Calculate summary statistics
        summary = {
            'total_count': len(df),
            'averages': {
                'flowrate': float(df['Flowrate'].mean()),
                'pressure': float(df['Pressure'].mean()),
                'temperature': float(df['Temperature'].mean()),
            },
            'type_distribution': df['Type'].value_counts().to_dict(),
            'min_values': {
                'flowrate': float(df['Flowrate'].min()),
                'pressure': float(df['Pressure'].min()),
                'temperature': float(df['Temperature'].min()),
            },
            'max_values': {
                'flowrate': float(df['Flowrate'].max()),
                'pressure': float(df['Pressure'].max()),
                'temperature': float(df['Temperature'].max()),
            },
        }
        
        # Convert dataframe to list of dictionaries
        data_list = df.to_dict(orient='records')
        
        return summary, data_list, None
        
    except pd.errors.EmptyDataError:
        return None, None, "CSV file is empty"
    except pd.errors.ParserError as e:
        return None, None, f"Error parsing CSV file: {str(e)}"
    except Exception as e:
        return None, None, f"Unexpected error during analysis: {str(e)}"

