import pandas as pd
import os

def load_and_clean_data(file_path):
    """
    Loads the defect dataset and performs basic cleaning.
    """
    print(f"Loading dataset from: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find the dataset at {file_path}")
        
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        print(f"Original dataset shape: {df.shape}")
        
        # Drop rows where critical columns (like long_description) are missing
        critical_columns = ['long_description', 'short_description', 'bug_id']
        
        # Check which critical columns actually exist in the dataframe
        existing_cols = [col for col in critical_columns if col in df.columns]
        
        df_cleaned = df.dropna(subset=existing_cols)
        print(f"Cleaned dataset shape (removed nulls): {df_cleaned.shape}")
        
        return df_cleaned
        
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    # Test the function assuming the file starts with 'DATASET'
    
    # Find the CSV file in the current directory that starts with 'DATASET'
    dataset_files = [f for f in os.listdir('.') if f.upper().startswith('DATASET') and f.endswith('.csv')]
    
    if dataset_files:
        file_to_load = dataset_files[0]
        cleaned_data = load_and_clean_data(file_to_load)
        
        if cleaned_data is not None:
            print("\nPreview of the cleaned data:")
            print(cleaned_data.head(2))
    else:
        print("No CSV file starting with 'DATASET' found in the current directory.")
