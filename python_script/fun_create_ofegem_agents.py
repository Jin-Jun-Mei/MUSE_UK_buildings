from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from cls_Agent import Agent  # Import the Agent class

def create_ofgem_agents(df):
    """
    Process the input DataFrame and create agents DataFrame for MUSE input.

    Parameters:
        df (pd.DataFrame): Input DataFrame containing archetype data.

    Returns:
        pd.DataFrame: Processed DataFrame containing agent information.
    """
    # Ensure the required columns are present in the DataFrame
    required_columns = [
        'Archetype', 'Main heating Fuel', 'Average Annual Elec consumption (kWh)', 
        'Average Annual Gas consumption (kWh)'
    ]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

    # Filter rows for 'Mains gas' to train the model
    filtered_df = df[df['Main heating Fuel'] == 'Mains gas'].dropna(
        subset=['Average Annual Elec consumption (kWh)', 'Average Annual Gas consumption (kWh)']
    )

    if filtered_df.empty:
        raise ValueError("No valid data found for training the regression model.")

    # Prepare data for linear regression
    X = filtered_df[['Average Annual Elec consumption (kWh)']]
    y = filtered_df['Average Annual Gas consumption (kWh)'].values

    # Train the linear regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict for rows where 'Main heating Fuel' is not 'Mains gas', 'Electricity', or other excluded categories
    non_main_fuel_rows = df[
        ~df['Main heating Fuel'].isin(['Mains gas', 'Electricity', 'Electricity/Other (Solid fuel/LPG)'])
    ].copy()
    if not non_main_fuel_rows.empty:
        non_main_fuel_rows['Predicted Consumption (kWh)'] = model.predict(
            non_main_fuel_rows[['Average Annual Elec consumption (kWh)']]
        )

    # Add predictions to the original DataFrame
    df['Predicted Consumption (kWh)'] = np.nan
    if not non_main_fuel_rows.empty:
        df.loc[non_main_fuel_rows.index, 'Predicted Consumption (kWh)'] = non_main_fuel_rows[
            'Predicted Consumption (kWh)'
        ]

    # Calculate 'demand_share'
    df['demand_share'] = np.where(
        df['Predicted Consumption (kWh)'].notna(),
        df['Predicted Consumption (kWh)'] + df['Average Annual Elec consumption (kWh)'],
        df['Average Annual Gas consumption (kWh)'] + df['Average Annual Elec consumption (kWh)']
    )

    # Normalize 'demand_share'
    total_consumption_sum = df['demand_share'].sum()
    df['demand_share'] = df['demand_share'] / total_consumption_sum

    # Clear existing Agent instances (important for multiple runs)
    Agent.instances.clear()

    # Create Agent instances for each row in the DataFrame
    # At this point, the agents are identical except for the 'Name' and 'Quantity' attributes.
    # But this can be modified to include other attributes
    for _, row in df.iterrows():
        name = row['Archetype']
        agent_share = row['Archetype']
        quantity = row['demand_share']
        Agent(
            Name=name,
            AgentShare=agent_share,
            Quantity=quantity
        )

    # Convert the Agent instances to a DataFrame
    agents_data = [vars(agent) for agent in Agent.instances]
    agents_df = pd.DataFrame(agents_data)

    # Rename 'AgentType' to 'Type' for MUSE compatibility
    if 'AgentType' in agents_df.columns:
        agents_df.rename(columns={'AgentType': 'Type'}, inplace=True)

    return agents_df
