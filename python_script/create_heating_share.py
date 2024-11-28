import pandas as pd

def heating_capacity_share(technodata,df_ofgem):
    """
    Processes Ofgem data and merges it with Technodata to calculate agent shares.

    Parameters:
        df_ofgem (pd.DataFrame): DataFrame containing Ofgem data on fuel consumption and archetypes.
        technodata (pd.DataFrame): DataFrame containing Technodata with fuel types.

    Returns:
        pd.DataFrame: Updated Technodata with agent shares.
    """

    # Step 1: Calculate fuel consumption ratios
    def calculate_main_fuel_ratios(data, heating_fuel, consumption_column):
        """
        Calculate consumption ratios for a specific heating fuel.
        """
        # Filter data where 'Main heating Fuel' contains the given type
        filtered_data = data[data['Main heating Fuel'].str.contains(heating_fuel, case=False, na=False, regex=False)].copy()
        total_consumption = filtered_data[consumption_column].sum()

        # Avoid division by zero
        if total_consumption == 0:
            raise ValueError(f"Total consumption for {heating_fuel} is zero.")

        # Calculate the ratio
        filtered_data['Fuel Consumption Ratio'] = filtered_data[consumption_column] / total_consumption
        return filtered_data[['Archetype', 'Fuel Consumption Ratio']]

    # Calculate ratios for each fuel type
    def build_agent_dataframe(df_ofgem):
        """
        Build a DataFrame to store agent shares by fuel type and archetype.
        """
        fuel_types = ['Mains gas', 'Oil', 'Other (solid fuel/LPG)', 'Electricity']
        consumption_columns = {
            'Mains gas': 'Average Annual Gas consumption (kWh)',
            'Oil': 'Average Annual Elec consumption (kWh)',
            'Other (solid fuel/LPG)': 'Average Annual Elec consumption (kWh)',
            'Electricity': 'Average Annual Elec consumption (kWh)'
        }
        agent_df = pd.DataFrame(index=fuel_types)

        for fuel_type, column in consumption_columns.items():
            fuel_ratios = calculate_main_fuel_ratios(df_ofgem, fuel_type, column)
            for _, row in fuel_ratios.iterrows():
                archetype = row['Archetype']
                ratio = row['Fuel Consumption Ratio']
                agent_df.loc[fuel_type, archetype] = ratio

        return agent_df.fillna(0)

    # Build the Ofgem agent DataFrame
    ofgem_agent_df = build_agent_dataframe(df_ofgem)

    # Add a unit row ("new")
    new_row = pd.DataFrame([["new"] * ofgem_agent_df.shape[1]], columns=ofgem_agent_df.columns)
    ofgem_agent_df_with_unit_row = pd.concat([new_row, ofgem_agent_df])

    # Step 2: Map fuel types in Technodata
    def map_fuel_to_type(fuel):
        """
        Map fuel codes to Ofgem agent DataFrame index.
        """
        fuel_mapping = {
            "NGA": "Mains gas",
            "OIL": "Oil",
            "HCO": "Oil",
            "ELC": "Electricity",
            "HYDROGEN": None,
            "SOLAR": None,
            "-": 0
        }
        return fuel_mapping.get(fuel, "Other (solid fuel/LPG)")

    technodata.loc[:, 'MappedFuelType'] = technodata['Fuel'].apply(map_fuel_to_type)

    # Step 3: Merge Technodata with agent shares
    technodata_add_agents = technodata.merge(
        ofgem_agent_df_with_unit_row,
        left_on='MappedFuelType',
        right_index=True,
        how='left'
    )

    # Step 4: Handle missing values for specific fuels
    def handle_missing_values(data, fuels, columns):
        """
        Fill missing values in specified columns for given fuel types.
        """
        rows = data['Fuel'].isin(fuels)
        data.loc[rows, columns] = data.loc[rows, columns].fillna(0)
        
    archetype_columns = [col for col in technodata_add_agents.columns if col in ofgem_agent_df.columns]
    handle_missing_values(technodata_add_agents, ['HYDROGEN', 'SOLAR'], archetype_columns)

    # Step 5: Clean up unnecessary columns
    columns_to_drop = [col for col in technodata_add_agents.columns if "Agent" in col or "agent" in col or col == "MappedFuelType"]
    technodata_add_agents.drop(columns=columns_to_drop, inplace=True)

    return technodata_add_agents
