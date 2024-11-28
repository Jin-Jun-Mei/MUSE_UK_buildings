import pandas as pd
from calculate_non_heat_share import non_heat_capacity_share
from calculate_heating_share import heating_capacity_share


def add_agents_to_technodata(df_ofgem, technodata_df, output_folder_path=None):
    """
    Processes Technodata and Ofgem data, integrates AgentShare parameters, 
    and saves the final dataframe to Technodata.csv.

    Parameters:
        df_ofgem (pd.DataFrame): The Ofgem data.
        technodata_df (pd.DataFrame): The Technodata dataframe.
        output_folder_path (Path): The path where the output will be saved.

    Returns:
        pd.DataFrame: The final merged dataframe.
    """
    # Define enduse mappings
    non_heat_enduses_mapping = {
        'RES.COOKING': 'Cooking',
        'RES.COOLING': 'Cold appliances',
        'RES.CONSUMER-ELECTRONICS.TV': 'Audiovisual',
        'RES.LIGHTING': 'Lighting',
        'RES.REFRIGERATORS': 'Cold appliances',
        'RES.FREEZERS': 'Cold appliances',
        'RES.COMPUTERS': 'ICT',
        'RES.WET.APPLIANCES': 'Washing/Drying',
        'RES.OTHER': 'Other'
    }

    heating_enduses_mapping = {
        'RES.HOT-WATER': 'Water heating',
        'RES.SPACE-HEAT': 'Heating'
    }

    non_heat_enduses = list(non_heat_enduses_mapping.keys())
    heating_enduses = list(heating_enduses_mapping.keys())

    # Step 1: Identify columns with "new" in the "Unit" row
    columns_to_drop = technodata_df.loc[0][technodata_df.loc[0] == "new"].index

    # Step 2: Drop these old Agent columns from the DataFrame
    technodata_df.drop(columns=columns_to_drop, inplace=True)

    # Step 3: Extract the "Unit" row, which will be added back to the DataFrame later
    unit_row = technodata_df.iloc[[0]]

    # Step 5: Split the DataFrame into two based on the "EndUse" column
    non_heat_use = technodata_df['EndUse'].str.contains('|'.join(non_heat_enduses), case=False, na=False)
    heating_use = technodata_df['EndUse'].str.contains('|'.join(heating_enduses), case=False, na=False)

    df_non_heat = technodata_df[non_heat_use]
    df_heating = technodata_df[heating_use]

    # Process non-heat enduse
    df1 = non_heat_capacity_share(df_non_heat, df_ofgem, non_heat_enduses_mapping)

    # Process heating enduse
    df2 = heating_capacity_share(df_heating, df_ofgem)

    # Combine dataframes together
    new_columns = set(df1.columns) - set(unit_row.columns)

    # Update the Unit row with the new columns
    unit_row = unit_row.copy()
    for col in new_columns:
        unit_row[col] = 'new'

    # Add the updated Unit row back to the top
    final_merged_df = pd.concat([unit_row, df1, df2], ignore_index=True)

    # Save the final dataframe
    # output_folder = Path(output_folder_path)
    # output_folder.mkdir(parents=True, exist_ok=True)
    # output_file = output_folder / "Technodata.csv"
    # final_merged_df.to_csv(output_file, index=False)

    # print(f"Technodata.csv is successfully saved to {output_file}")
    return final_merged_df
