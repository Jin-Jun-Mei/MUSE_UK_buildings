import pandas as pd

def non_heat_capacity_share(df_non_heat_techdata, df_ofgem,non_heat_enduses_mapping):
    """
    Processes non-heating and heating data to create a merged DataFrame with capacity shares.

    Parameters:
        df_non_heat_techdata (pd.DataFrame): DataFrame containing non-heating end-use data.
        df_ofgem (pd.DataFrame): DataFrame containing heating data to process.

    Returns:
        pd.DataFrame: Merged DataFrame with processed capacity shares.
    """
    
    # # Step 1: Define mappings
    # non_heat_enduses_mapping = {
    #     'RES.COOKING': 'Cooking',
    #     'RES.COOLING': 'Cold appliances',
    #     'RES.CONSUMER-ELECTRONICS.TV': 'Audiovisual',
    #     'RES.LIGHTING': 'Lighting',
    #     'RES.REFRIGERATORS': 'Cold appliances',
    #     'RES.FREEZERS': 'Cold appliances',
    #     'RES.COMPUTERS': 'ICT',
    #     'RES.WET.APPLIANCES': 'Washing/Drying',
    #     'RES.OTHER': 'Other'
    # }


    # Step 2: Create multipliers DataFrame
    # this data is taken from Household Electricity Survey Final Report 
    # From: Department of Energy & Climate Change, Published 20 June 2013. GOV.UK.
    def create_enduse_multipliers():
        data = [
            ["Enduse", "without_elc_heating", "with_addition_elc_heating", "with_primary_elc_heating"],
            ["Cold appliances", "16.20%", "13.40%", "4.70%"],
            ["Cooking", "13.80%", "11.70%", "7.20%"],
            ["Lighting", "15.40%", "10.00%", "5.80%"],
            ["Audiovisual", "14.40%", "10.40%", "3.40%"],
            ["ICT", "6.10%", "3.60%", "2.60%"],
            ["Washing/Drying", "13.60%", "10.70%", "3.10%"],
            ["Heating", "0", "22.50%", "64.20%"],
            ["Water heating", "7.10%", "4.00%", "6.30%"],
            ["Other", "3.70%", "5.80%", "1.50%"],
            ["Not_known", "9.70%", "7.90%", "1.20%"]
        ]
        df = pd.DataFrame(data[1:], columns=data[0]).set_index('Enduse')
        return df.map(lambda x: float(x.strip('%')) / 100 if isinstance(x, str) and '%' in x else x)

    enduse_multipliers = create_enduse_multipliers()

    # Step 3: Categorize heating types
    def categorize_heating(fuel):
        if fuel == "Mains gas":
            return "without_elc_heating"
        elif fuel == "Electricity":
            return "with_primary_elc_heating"
        else:
            return "with_addition_elc_heating"

    df_ofgem['heating type'] = df_ofgem['Main heating Fuel'].apply(categorize_heating)

    # Step 4: Calculate shares for non-heating enduses
    def calculate_shares(df_ofgem, non_heat_enduses_mapping):
        for item, enduse in non_heat_enduses_mapping.items():
            # Calculate consumption based on multipliers
            consumption = df_ofgem['Average Annual Elec consumption (kWh)'] * df_ofgem['heating type'].apply(
                lambda x: enduse_multipliers.loc[enduse, x]
            )
            total_consumption = consumption.sum()
            # Normalize shares
            df_ofgem[item] = consumption / total_consumption
            # Adjust for shared categories
            if item in ['RES.REFRIGERATORS', 'RES.FREEZERS']:
                df_ofgem[item] /= 2

    # the non-heating end-use shares are calculated for each archetype in df_ofgem
    calculate_shares(df_ofgem, non_heat_enduses_mapping)

    # Step 5: Create enduse shares DataFrame
    def create_enduse_shares(df_ofgem):
        col_to_ignore = [
            'Average Annual Elec consumption (kWh)', 
            'Average Annual Gas consumption (kWh)', 
            'Main heating Fuel', 
            'heating type'
        ]
        columns_to_keep = [col for col in df_ofgem.columns if col not in col_to_ignore]
        return df_ofgem[columns_to_keep].set_index('Archetype').T

    enduse_shares_df = create_enduse_shares(df_ofgem)

    # Step 6: Merge with non-heating data
    def find_containing_category(enduse_value, categories):
        for category in categories:
            if category in str(enduse_value):
                return category
        return None

    # get unique categories
    enduse_shares_categories = enduse_shares_df.index.unique()


    # make a copy to ensure the DataFrame is independent
    df_non_heat_techdata = df_non_heat_techdata.copy()

    # Apply the transformation
    df_non_heat_techdata.loc[:, 'mapped_category'] = df_non_heat_techdata['EndUse'].apply(
        lambda x: find_containing_category(x, enduse_shares_categories)
    )

    # Perform the merge
    merged_df = pd.merge(
        df_non_heat_techdata,
        enduse_shares_df,
        left_on='mapped_category',
        right_index=True,
        how='left'
    )

    # Optionally drop the temporary column if no longer needed
    merged_df = merged_df.drop(columns='mapped_category')

    return merged_df
