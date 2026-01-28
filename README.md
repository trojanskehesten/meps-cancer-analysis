# MEPS Cancer Analysis (2019)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://meps-cancer-analysis.streamlit.app/)

This project explores differences between individuals **with and without cancer**, as well as **across different types of cancer**, using data from the Medical Expenditure Panel Survey (MEPS).

The analysis focuses on demographic differences associated with cancer status and cancer type, with particular attention to key population characteristics that are central to cancer epidemiology and health disparities research:

- **Age**
- **Sex**
- **Race**

All analyses are descriptive and exploratory, aiming to highlight potential disparities and patterns among cancer patients.

---

## Data Source

This project utilizes data from the **Medical Expenditure Panel Survey (MEPS) 2019 Full Year Consolidated Data File (HC-216)**. This dataset provides comprehensive information on a nationally representative sample of the U.S. civilian noninstitutionalized population for the calendar year 2019.

* [MEPS HC-216 Data File](https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-216)

The HC-216 file includes a wide range of variables, such as:

- **Demographics**: age, sex, race/ethnicity, education level, income.
- **Health Status**: self-reported health status, limitations in activities of daily living (ADLs), instrumental activities of daily living (IADLs).
- **Healthcare Access and Utilization**: insurance coverage, usual source of care, number of medical visits.
- **Expenditures**: total healthcare expenditures, out-of-pocket costs, payments by source.
- **Employment and Disability Days**: employment status, number of workdays missed due to illness or injury.
- **Priority Conditions**: indicators for various health conditions, including cancer.

In this project, the analysis is restricted to demographic variables and cancer-related indicators, providing a focused overview of cancer prevalence and demographic heterogeneity in the 2019 MEPS sample. 
That is why a minimal subset of the original MEPS file is used.

The subset keeps only the variables required for the cancer-focused analysis:

- **Cancer-related variables**:  
  `CABLADDR`, `CABREAST`, `CACERVIX`, `CACOLON`, `CALUNG`, `CALYMPH`, `CAMELANO`,  
  `CAOTHER`, `CAPROSTA`, `CASKINNM`, `CASKINDK`, `CAUTERUS`, `CANCERDX`

- **Demographic variables**:  
  `AGELAST`, `SEX`, `RACEV1X`

All other columns from the original `h216.dta` (≈75 MB) are omitted, resulting in a compact file (≈0.5 MB) containing only the variables used in this project.

---

## Data File

The repository expects a Stata file named:

```text
data/h216.dta
```

In this project, `data/h216.dta` is already a **reduced subset** of the original MEPS HC‑216 file, containing only the cancer-related and demographic columns listed above.

If you want to recreate the subset yourself, you can download the full file from MEPS:

- `h216.dta` - [Download from MEPS](https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-216)

Then extract only the required columns before use.

---

## Project Structure

- `app/`  
  - `dashboard.py` - main Streamlit app (layout, controls, and dashboard logic)  
  - `utils.py` - helper functions for data loading and plotting
- `data/`  - input datasets
  - `h216.dta` - reduced MEPS dataset (subset with cancer and demographic variables only)
- `docs/` - documentation and exported results *(not tracked in git)*
- `modules/` - utility functions for data processing and visualization
- [`MEPS Cancer analysis 2019.ipynb`](MEPS%20Cancer%20analysis%202019.ipynb) - main notebook for exploratory analysis of MEPS 2019 data with a demographic focus.  
  It includes:
  - an overview of cancer types represented in the dataset,
  - comparisons between individuals with and without cancer,
  - descriptive analyses stratified by:
    - **Age**
    - **Sex**
    - **Race**
  - summary tables and visualizations highlighting demographic patterns and disparities.

---

## Dashboard

**Live Demo**: [https://meps-cancer-analysis.streamlit.app/](https://meps-cancer-analysis.streamlit.app/)

An interactive dashboard is provided to explore cancer-related patterns by age, sex, and race.

The dashboard:

- visualizes distributions of key demographic variables,
- shows how cancer diagnosis and cancer types depend on demographics,
- allows filtering by cancer type and demographic groups.

To run the dashboard from the **project root**:

```bash
streamlit run app/dashboard.py
```

- Make sure that python dependencies are installed (see below).

---

## Requirements

- Python 3.12

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## License

This project is released under the [MIT License](LICENSE).
