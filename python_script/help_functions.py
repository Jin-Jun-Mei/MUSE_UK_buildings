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

def bring_row_to_top(df, identifier, column_name=None):
    """
    Reorders the DataFrame so that the row with the specified identifier
    is moved to the top. The identifier can either be in the index or a specific column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - identifier: The value to identify the row to move to the top.
    - column_name (str, optional): The column name to search for the identifier
                                   if it's not in the index. Defaults to None.

    Returns:
    - pd.DataFrame: A reordered DataFrame with the specified row at the top.
    """
    if column_name:  # If searching within a column
        if identifier in df[column_name].values:
            # Select the row(s) where the column matches the identifier
            target_row = df[df[column_name] == identifier]
            # Drop the identified row(s) from the original DataFrame
            remaining_rows = df[df[column_name] != identifier]
        else:
            # If the identifier is not found, return the original DataFrame
            return df
    else:  # If searching in the index
        if identifier in df.index:
            # Extract the row with the identifier in the index
            target_row = df.loc[[identifier]]
            # Drop the specified row from the original DataFrame
            remaining_rows = df.drop(identifier)
        else:
            # If the identifier is not found, return the original DataFrame
            return df

    # Concatenate the target row on top of the remaining rows
    df_reordered = pd.concat([target_row, remaining_rows])
    return df_reordered

def reorder_columns(dataframe, first_column):
    """
    Reorders the columns of a DataFrame, placing the specified column first.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to reorder.
        first_column (str): The column to place first.

    Returns:
        pd.DataFrame: The reordered DataFrame.
    """
    if first_column not in dataframe.columns:
        raise ValueError(f"Column '{first_column}' not found in DataFrame.")
    # Create the new column order
    columns = [first_column] + [col for col in dataframe.columns if col != first_column]
    # Reorder and return the DataFrame
    return dataframe[columns]




def merge_by_column(file1, file2, column_name, output_file=None):
    """
    Merges two specific CSV files based on a common column, saving the result.
    
    Parameters:
    - df1: str - Path to the first CSV file, e.g. residential_file_path.
    - file2: str - Path to the second CSV file, e.g. service_file_path.
    - column_name: str - Column name to merge on.
    - output_file_path: str - Path to save the merged CSV file.
    
    Returns:
    - merged_df
    """
    # Load the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Merge on the specified column
    merged_df = pd.merge(df1, df2, on=column_name, how='outer', suffixes=('', '_drop'))
 
    # Drop duplicated columns
    merged_df = merged_df[[col for col in merged_df.columns if not col.endswith('_drop')]]
    
    if output_file is not None:
        # Save the merged DataFrame to the specified output file
        merged_df.to_csv(output_file, index=False)
    
        print(f"Merged files saved to {output_file}")
   

    return merged_df



def merge_by_row(file1, file2, output_file=None):
    """
    Merges two CSV files by adding rows together, removes duplicate rows, and saves the result.
    
    Parameters:
    - file1: str - Path to the first CSV file, e.g. residential_file_path.
    - file2: str - Path to the second CSV file, e.g. service_file_path.
    - output_file: str - Path to save the merged CSV file, e.g. Building_file_path.
    
    Returns:
    -None
    or - merged_df: pd.DataFrame - The resulting merged DataFrame with duplicate rows removed.
    """
    # Load the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Concatenate the DataFrames along rows
    merged_df = pd.concat([df1, df2], axis=0, ignore_index=True)
    
    # Drop duplicate rows
    merged_df = merged_df.drop_duplicates()
    
    if output_file is not None:
        # Save the merged DataFrame to the specified output file
        merged_df.to_csv(output_file, index=False)
    
        print(f"Merged files saved to {output_file} with duplicates removed.")
    
    return merged_df


def split_agent_column(df, keyword="new"):
    """
    Splits a DataFrame into two parts based on whether a specified keyword is present
    in the first row (Unit).

    Parameters:
    - df (pd.DataFrame): The input DataFrame to split.
    - keyword (str): The keyword to check for in the specified column.

    Returns:
    - df_with_keyword (pd.DataFrame): DataFrame with columns where the keyword is found.
    - df_without_keyword (pd.DataFrame): DataFrame with columns where the keyword is not found.
    """

    # Set 'ProcessName' as the index
    if df.index.name != "ProcessName":
        df = df.set_index("ProcessName")

    # Identify the first row corresponding to "Unit"
    if "Unit" not in df.index:
        raise ValueError("No 'Unit' row found in the index.")
    
    first_row = df.loc["Unit"]

    # Identify columns with and without the keyword
    columns_with_keyword = df.columns[first_row.str.contains(keyword, na=False)]
    columns_without_keyword = df.columns[~first_row.str.contains(keyword, na=False)]

    # Split the DataFrame
    df_with_keyword = df[columns_with_keyword]
    df_without_keyword = df[columns_without_keyword]

    return df_with_keyword, df_without_keyword




def merge_by_column_and_row(file1, file2, output_file):
    """
    Merges two CSV files by keeping all unique columns and rows, combines "Unit" rows into one,
    and fills missing values with 0 for columns that are not present in one of the files.
    
    Parameters:
    - file1: str - Path to the first CSV file.
    - file2: str - Path to the second CSV file.
    - output_file: str - Path to save the merged CSV file.
    
    Returns:
    - None
    """
    # Load the CSV files as strings for consistency
    df1 = pd.read_csv(file1, dtype=str)
    df2 = pd.read_csv(file2, dtype=str)
    
    # Concatenate along rows with an outer join to keep all columns
    merged_df = pd.concat([df1, df2], axis=0, ignore_index=True)
    
    # Separate "Unit" rows
    unit_rows = merged_df[merged_df['ProcessName'] == 'Unit']
    merged_df = merged_df[merged_df['ProcessName'] != 'Unit']
    
    # If there are multiple "Unit" rows, combine them
    if len(unit_rows) > 1:
        combined_unit_row = unit_rows.iloc[0].copy()  # Start with the first "Unit" row
        
        # Iterate over columns to combine values from all "Unit" rows
        for idx in range(1, len(unit_rows)):
            for col in unit_rows.columns:
                # Keep the non-zero, non-empty value if they differ
                current_value = combined_unit_row[col]
                new_value = unit_rows.iloc[idx][col]
                
                # Check for zero or empty before replacing
                
                if(pd.isna(current_value) or current_value == '') and not pd.isna(new_value) and new_value != '':
                    combined_unit_row[col] = new_value
        
        # Use only the combined "Unit" row
        unit_row_df = pd.DataFrame([combined_unit_row])

    elif len(unit_rows) == 1:
        # If only one "Unit" row exists, retain it
        unit_row_df = unit_rows
    else:
        print("No 'Unit' row found in either file.")
        unit_row_df = pd.DataFrame()  # Empty DataFrame if no "Unit" row exists

    # Fill missing values across the entire DataFrame with 0
    merged_df = merged_df.fillna(0)
    
    # Concatenate the "Unit" row back on top, if it exists
    if not unit_row_df.empty:
        merged_df = pd.concat([unit_row_df, merged_df], ignore_index=True)
    
    # Drop duplicate rows based on all columns
    merged_df = merged_df.drop_duplicates()
    
    # Save the result to a CSV file
    merged_df.to_csv(output_file, index=False)
    
    print(f"Merged files saved to {output_file} with duplicates removed, 'Unit' rows combined, and missing values filled with 0.")


# 
def split_agent_columns(df, keyword="new"):
    """
    Splits a DataFrame into two parts based on whether a specified keyword is present
    in the first row (Unit).

    Parameters:
    - df (pd.DataFrame): The input DataFrame to split.
    - keyword (str): The keyword to check for in the specified column.

    Returns:
    - df_with_keyword (pd.DataFrame): DataFrame with columns where the keyword is found.
    - df_without_keyword (pd.DataFrame): DataFrame with columns where the keyword is not found.
    """
    
    # Set 'ProcessName' as the index
    
    if df.index.name != "ProcessName":
        df = df.set_index("ProcessName")
    

    # Identify the first row corresponding to "Unit"
    if "Unit" not in df.index:
        raise ValueError("No 'Unit' row found in the index.")
    
    first_row = df.loc["Unit"]

    # Identify columns with and without the keyword
    columns_with_keyword = df.columns[first_row.str.contains(keyword, na=False)]
    columns_without_keyword = df.columns[~first_row.str.contains(keyword, na=False)]

    # Split the DataFrame
    df_with_keyword = df[columns_with_keyword]
    df_without_keyword = df[columns_without_keyword]

    return df_with_keyword, df_without_keyword


# 
def merge_by_row_technodata(file1, file2, output_file=None):
    """
   Similar to the merge_by_row function, but this function is specifically for merging two Technodata files.
   As technodata files have a specific structure (have a Unit row and agent columns), this function is designed to handle that structure.
    """
    # Load the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    

    # Separate the columns into two parts based on whether the first row (index "Unit") contains "new" (which indicates agent columns)
    df1_with_agents, df1_without_agents = split_agent_columns(df1)
    df2_with_agents, df2_without_agents = split_agent_columns(df2)

    # Merge on ProcessName
    # (1) merge agent columns 
    merged_agent_columns = pd.merge(df1_with_agents, df2_with_agents, on='ProcessName', how='outer').fillna(0)
    # print(merged_agent_columns.shape)
    # (2) merge non-agent columns (a.ka. technology data)
    merged_non_agents_columns = pd.concat([df1_without_agents, df2_without_agents], axis=0, ignore_index=False)
    # print(merged_non_agents_columns.shape)
    # merged (1) and (2)
    merged_all_columns = pd.merge(merged_non_agents_columns, merged_agent_columns, left_index=True, right_index=True, how='outer')
    
    # bring the "Unit" row to the top row
    merged_all_columns = bring_row_to_top(merged_all_columns, 'Unit')

    # remove duplicates (this comment out as it is not necessary)
    merged_all_columns.reset_index(drop=False, inplace=True)
    merged_all_columns.drop_duplicates(inplace=True)
    print(merged_all_columns.shape)

    if output_file is not None:
        # Save the merged DataFrame to the specified output file
        merged_all_columns.to_csv(output_file, index=False)
    
        print(f"Merged files saved to {output_file}.")

    return merged_all_columns




def combine_tech(dataframe, columns_to_ignore, combine_column):
    """
    Groups a DataFrame by all columns except specified ones, combining values in a specified column.

    Parameters:
        dataframe (pd.DataFrame): The DataFrame to process.
        columns_to_ignore (list): Columns to ignore during grouping.
        combine_column (str): The column whose values should be combined for identical rows.

    Returns:
        pd.DataFrame: The grouped and combined DataFrame.
    """
    # Validate inputs
    if combine_column not in dataframe.columns:
        raise ValueError(f"Combine column '{combine_column}' not found in DataFrame.")
    
    # Define columns to group by (all except ignored ones)
    columns_to_group_by = [col for col in dataframe.columns if col not in columns_to_ignore]
    
    # Group data and combine the specified column
    grouped_data = dataframe.groupby(columns_to_group_by, dropna=False).agg({
        combine_column: lambda x: ', '.join(x)  # Combine values in the specified column
    }).reset_index()

    print(f"Data grouped by columns: {columns_to_group_by} and values in '{combine_column}' combined.")
    
    return grouped_data
