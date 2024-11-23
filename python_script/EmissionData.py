## emission data from https://www.eia.gov/environment/emissions/co2_vol_mass.php
# LPG emission data from https://ghgprotocol.org/sites/default/files/Emission_Factors_from_Cross_Sector_Tools_March_2017.xlsx&ved=2ahUKEwjh1ra3nJOJAxX0_7sIHTbCFKoQFnoECBgQAQ&usg=AOvVaw1MOb4QhLTjmQSLtpFXIxFO

r = 1.0550559 #unit conversion 1 KG CO2 per Million Btus = 1.0550559 Kt CO2 per PJ

GHG_fuels = {
    "COKE": 113.67/r,
    "COAL": 95.99/r,
    "KEROSENE": 73.19/r,
    "OIL": 74.14/r,
    "LFO": 74.14/r,
    "HCO": 74.14/r,
    "LPG": 63.1/r,
    "InorganicWaste": 35.55/r,
    "NGA": 52.91/r
}
