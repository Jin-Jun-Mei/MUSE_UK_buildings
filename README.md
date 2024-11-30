# MUSE-UK Buildings Sector

Welcome to the **MUSE-UK Buildings** repository! This repository contains input data for the residential, service and buildings sector of the MUSE (ModUlar energy system Simulation Environment) model. It also provides a detailed guide for creating these input files using the TIMES (The Integrated MARKAL-EFOM System) model dataset.

For a comprehensive overview of the MUSE framework, refer to the [MUSE documentation](https://muse-os.readthedocs.io/en/latest/) and the [MUSE GitHub repository](https://github.com/EnergySystemsModellingLab/MUSE_OS).


## Repository Structure

This repository is organized into three main folders:

1. **`MUSE_files`**: Contains the input data for the MUSE-UK buildings sector. This folder includes three subfolders — `Residential`, `Service`, and `Buildings` (created by combining the Residential and Service sectors). Each subfolder contains files that can be run as a standalone sector in MUSE.
2. **`python_script`**: Includes Python scripts used to generate the files in `MUSE_files`.
3. **`TIMES_data`**: Holds the TIMES model data, which serves as the basis for generating input files for the MUSE-UK buildings sector. This folder includes two subfolders — `TIMES_data_Residential` and `TIMES_data_Service`, each containing technology data specific to its respective subsector.
4. **`Ofgem_Archetype`**: Contains information extracted from the report [Ofgem energy consumer archetypes update 2024"][./Ofgem_archetypes_update_2024_FinalReport.pdf]. Table 1 of this report is used as a reference for creating consumer archetypes in the residential sector for MUSE, referred to as 'Ofgem_agents'.


---
## Steps to Generate MUSE Buildings Sector Files

![TIMES-MUSE flow](https://github.com/user-attachments/assets/f3b30b89-cc3f-4e39-9e22-500c31dcfeb1)

The files in the `MUSE_files` are generated by running the scripts in `python_script`.

### Prerequisites

To execute the transformation scripts, ensure you have:
- **Installed Tools**: Jupyter Notebook, Python.
- **Required Libraries**: Pandas, NumPy, pathlib, re, difflib, shutil, etc.
- **File Structure**: Ensure the `TIMES_data` folder is in the correct directory relative to your `python_script` folder.

---

### **1. Residential Subsector**

To generate MUSE input files for the Residential subsector:

1. **Agent Configuration** (pre-set step):
   - Configure the `version` parameter in `create_MUSE_Files_Residential.ipynb`:
     - **`single_agent`**: Generates a single agent.
     - **`Ofgem_agents`**: Generates 24 agents representing the _Ofgem archetype_ with different name and initial capacity share. (see MUSE documentation for details on "initial capacity share"). _Ofgem archetype_ is explained [here]
     ```python
     version = 'single_agent'  # or 'Ofgem_agents'
     ```

2. **Run the Script**:
   - Open and execute the `create_MUSE_Files_Residential.ipynb` notebook.
   - This script will generate:
     - `Consumption*.csv`
     - `Technodata.csv`
     - `TechnodataTimeslices.csv`
     - `GlobalCommodities.csv`
     - `CommIn.csv`
     - `CommOut.csv`
     - `Projections.csv`
     - `ExistingCapacity.csv`
     - `Agent.csv`

3. **Finalize Configuration**:
   - Add the `settings_Residential.toml` file. This allows the Residential subsector to be run as a standalone sector in MUSE. This setting file is already in this repo. Make sure to have the correct directory relative to your MUSE input folder.

---

### **2. Service Subsector**

To generate MUSE input files for the Service subsector:

1. **Run the Script**:
   - Open and execute the `create_MUSE_Files_Service.ipynb` notebook. Similar to the Residential Subsector above, this script generates all the input files required by MUSE for this sector.
   - Unlike the Residential subsector, this notebook does not include an _Ofgem archetype_ option. However, you can generate multiple agents if needed (default: one agent).

2. **Finalize Configuration**:
   - Add the `settings_Service.toml` file. This allows the Service subsector to be run as a standalone sector in MUSE. This setting file is already in this repo. Make sure to have the correct directory relative to your MUSE input folder.

---

### **3. Building sector (Combine Residential and Service Subsectors)**

To create input files for the Buildings sector:
1. **Agent Configuration** (pre-set step):
   - similar to the Residential subsector, first open and configure the `version` parameter in `combine_Residential+Service.ipynb`:
     - **`single_agent`**: Combine 2 agents, a single agent from Residential and Service Subsectors respectively.
     - **`Ofgem_agents`**: Combine 25 agents (24 from Residential and 1 from the Service Subsectors).

2. **Run the Script**:
   - Execute the `combine_Residential+Service.ipynb` notebook.
   ```python
   if  version = 'single_agent' 
     
   # This script combines corresponding CSV files from `MUSE_files/Residential/single_agent` and `MUSE_files/Service`, removing duplicates.
   ```
   
   ```python
    if version = 'Ofgem_agents' 
     
   # This script combines corresponding CSV files from `MUSE_files/Residential/Ofgem_agents` and `MUSE_files/Service`, removing duplicates.
   ```

2. **Finalize Configuration**:
   - Add the `settings_Buildings.toml` file. This allows the Buildings sector to be run as a standalone sector in MUSE. This setting file is already in this repo. Make sure to have the correct directory relative to your MUSE input folder.

---

### **4. Simplify Technologies (Optional)**

To reduce the number of technologies in the Buildings sector (to decrease runtime or avoid out of memory issues):

1. **Run the Script**:
   - Open and execute the `simplify_technologies.ipynb` notebook.
   - This script regenerates input files in step 3 with a reduced set of technologies.

2. **Configuration**:
   - The `settings_Buildings.toml` file remains unchanged.

---

We hope this repository serves as a valuable resource for understanding and using the MUSE-UK buildings sector model. For questions or contributions, feel free to submit an issue or reach out!

---
