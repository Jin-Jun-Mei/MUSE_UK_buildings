# Python Scripts in `python_script` Folder

This folder contains Python scripts and Jupyter Notebooks used to generate MUSE input files as described in the [main README](../README.md). 

- **Jupyter Notebooks** (`.ipynb`): These are executed to create MUSE input files.
- **Python Scripts** (`.py`): These helper scripts are called by the Jupyter Notebooks to process data and generate the MUSE input files.

---

## Helper Functions

The following Python scripts contain functions that assist in generating MUSE input files:

- **`fun_add_agents_to_technodata.py`**
- **`fun_create_ofgem_agents.py`**
- **`help_functions.py`**

For detailed functionality, refer to the inline comments and docstrings in the code.

---

## Data, Parameter, and Class Settings

These scripts define data, parameters, and classes used during input file generation:

- **`name_mapping.py`**
- **`price_projection.py`**
- **`cls_Agent.py`**
- **`emission_data.py`**

For detailed functionality, refer to the inline comments and docstrings in the code.

---

## Execution Instructions

1. Run the Jupyter Notebooks in this folder to create MUSE input files. 
2. Ensure all dependencies are installed, including any Python libraries required by the scripts.
3. The `.py` scripts in this folder will be automatically called by the Jupyter Notebooks during execution.

---

## Notes

- Each script is designed/aims to handle specific tasks in the data generation pipeline.
- For more details on how the generated input files are used, refer to the [main README](../README.md).
