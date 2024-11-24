# This script contains the functions that are used in the other script.
from difflib import get_close_matches


# Define a generalized function that can fill missing values for any specified column based on similar "ProcessName"
def fill_missing_column_value(row, data, target_column):
    """
    This function takes a row, the complete data frame, and a target column name.
    It finds similar processes (based on ProcessName) with non-missing values in the target column
    and returns the value from the most similar process.
    """
    # Extract the process name for the current row
    process_name = row['ProcessName']
    
    # Filter out rows with non-missing values in the target column
    available_data = data.dropna(subset=[target_column])
    
    # Find similar process names using the difflib's get_close_matches function
    similar_names = get_close_matches(process_name, available_data['ProcessName'], n=1, cutoff=0.5)
    
    # If a similar name is found, return the corresponding value in the target column
    if similar_names:
        similar_row = available_data[available_data['ProcessName'] == similar_names[0]]
        return similar_row[target_column].values[0]
    return None






