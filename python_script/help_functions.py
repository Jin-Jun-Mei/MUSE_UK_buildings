# This script contains the functions that are used in the other script.
from difflib import get_close_matches
import pandas as pd


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




# Define a function to explicitly calculate linear interpolation between start (year) and cutoff years (the year where the residual capacity reaches 0)
# because the data in TIMES data set is not complete. As you can see in the above table, the residual capacity is not available for all years (as indicated by NaN values).

def explicit_interpolation(row):
    # Identify year columns (assumes numeric column names for years)
    year_columns = [col for col in row.index if isinstance(col, int)]
    
    # Convert year values to numeric
    row[year_columns] = pd.to_numeric(row[year_columns], errors='coerce')
    
    # Starting point
    start_year = year_columns[0]
    start_value = row[start_year]
    
    # Identify cutoff year
    cutoff_year = None
    for year in year_columns:
        if row[year] == 0:
            cutoff_year = year
            break
    
    # Interpolation between start and cutoff
    if cutoff_year:
        start_idx = year_columns.index(start_year)
        cutoff_idx = year_columns.index(cutoff_year)
        
        # Calculate interpolated values
        for i in range(start_idx + 1, cutoff_idx):
            year = year_columns[i]
            row[year] = start_value + (row[cutoff_year] - start_value) * (i - start_idx) / (cutoff_idx - start_idx)
        
        # Set values after cutoff to 0
        for year in year_columns[cutoff_idx + 1:]:
            row[year] = 0
    else:
        # If no cutoff, set all years after start to 0
        row.loc[year_columns[1:]] = 0

    return row



# def explicit_interpolation(row):
#     # Identify year columns and convert them to numeric
#     year_columns = [col for col in Residual_Capacity.columns if isinstance(col, int)]
#     row[year_columns] = row[year_columns].apply(pd.to_numeric, errors='coerce')
    
#     # Starting point
#     start_year = year_columns[0]
#     start_value = row[start_year]
    
#     # Identify cutoff year
#     cutoff_year = None
#     for year in year_columns:
#         if row[year] == 0:
#             cutoff_year = year
#             break
    
#     # Interpolation between start and cutoff
#     if cutoff_year:
#         start_idx = year_columns.index(start_year)
#         cutoff_idx = year_columns.index(cutoff_year)
        
#         # Calculate interpolated values
#         for i in range(start_idx + 1, cutoff_idx):
#             year = year_columns[i]
#             row[year] = start_value + (row[cutoff_year] - start_value) * (i - start_idx) / (cutoff_idx - start_idx)
        
#         # Set values after cutoff to 0
#         for year in year_columns[cutoff_idx + 1:]:
#             row[year] = 0
#     else:
#         # If no cutoff, set all years after start to 0
#         row.loc[year_columns[1:]] = 0

#     return row


