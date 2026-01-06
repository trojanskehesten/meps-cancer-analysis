# MEPS Cancer Analysis (2019)

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

---

## Data File

To run the analysis, download the following data file and place it in the `data/` folder:
- `h216.dta` - [Download from MEPS](https://meps.ahrq.gov/data_stats/download_data_files_detail.jsp?cboPufNumber=HC-216)

On the download page, scroll to the **"Data"** section and select the file in **Data File, Stata format (.dta)**.

The notebook expects this file to be located at:  
```
data/h216.dta
```

---

## Structure

- `data/` - input datasets (not tracked in git)
- `docs/` - documentation and exported results
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

## Requirements

- Python 3.12

See [`requirements.txt`](requirements.txt) for details.

---

## License

This project is released under the [MIT License](LICENSE).
