# Credit Score Dataset — EDA & Data Quality Assessment

**Prepared by:** Hassan Warraich  
**Course:** Artificial Intelligence (Machine Learning, Deep Learning & Communication) — Batch I  
**Project Type:** Exploratory Data Analysis (EDA) & Data Quality Assessment  
**Language:** Python

---

## 📌 Project Overview

This project focuses on performing a comprehensive Exploratory Data Analysis (EDA) and Data Quality Assessment of the Credit Score dataset.

The dataset contains 150,000 records and 13 variables, with `SeriousDlqin2yrs` as the target variable. The objective is to understand the data, identify quality issues, explore meaningful patterns, and prepare the dataset for future machine learning applications.

The project emphasizes not only writing code but also interpreting visualizations, documenting observations, and justifying important data-cleaning decisions.

## 🎯 Objectives

- Understand the dataset structure, variables, and data types.
- Identify missing values, duplicate records, and suspicious observations.
- Perform univariate and bivariate exploratory data analysis.
- Analyze the distribution of the target variable.
- Investigate relationships between financial indicators and serious delinquency.
- Create meaningful visualizations and a numerical correlation heatmap.
- Clean and prepare the dataset using justified methods.
- Compare the original and cleaned datasets.
- Document key findings and recommendations for future machine learning.

## 📂 Dataset Description

**Dataset file:** `CreditScore.csv`

| Attribute | Description |
|---|---|
| Original records | 150,000 |
| Variables | 13 |
| Target variable | `SeriousDlqin2yrs` |
| Problem type | Binary classification |
| Primary focus | Data quality, EDA, and preprocessing |

### Target Variable

`SeriousDlqin2yrs`

- `0` — No serious delinquency within two years.
- `1` — Experienced serious delinquency within two years.

The target distribution will be analyzed to determine whether class imbalance exists and how it may influence future model evaluation.

### Important Features

- `Age`
- `Gender`
- `MonthlyIncome`
- `DebtRatio`
- `RevolvingUtilizationOfUnsecuredLines`
- `NumberOfOpenCreditLinesAndLoans`
- `NumberOfTimes90DaysLate`
- `NumberOfTime60-89DaysPastDueNotWorse`
- `NumberOfTime30-59DaysPastDueNotWorse`
- `NumberRealEstateLoansOrLines`
- `NumberOfDependents`

All remaining variables will also be included in the initial data inspection.

## 🛠️ Tools & Libraries

- **Python** — Programming and analysis
- **Pandas** — Data manipulation and cleaning
- **NumPy** — Numerical operations
- **Matplotlib** — Visualization
- **Seaborn** — Statistical plots
- **Jupyter Notebook** — Interactive analysis

## 🔍 Project Workflow

### 1. Data Understanding

- Load the dataset and inspect its dimensions.
- Review column names, data types, and sample records.
- Generate descriptive statistics.
- Identify numerical and categorical variables.
- Examine the target variable and its distribution.

### 2. Data Quality Assessment

Investigate potential issues involving:

- Missing and null values.
- Duplicate records.
- Incorrect data types.
- Invalid or unexpected values.
- Extreme observations and potential outliers.
- Inconsistent categorical values, where applicable.

A concise Data Quality Report will document observed issues, their potential impact, and recommended actions.

### 3. Exploratory Data Analysis

**Univariate Analysis**

Use histograms, KDE plots, count plots, boxplots, and descriptive statistics to understand individual variable distributions.

**Bivariate Analysis**

Investigate relationships between important features and `SeriousDlqin2yrs`, particularly:

- Age and serious delinquency.
- Monthly income and serious delinquency.
- Debt ratio and serious delinquency.
- Revolving credit utilization and serious delinquency.
- Previous delinquency indicators and serious delinquency.

**Correlation Analysis**

Create a correlation matrix and heatmap to examine relationships between numerical variables and identify potential redundancy or multicollinearity.

Each important visualization will include a short explanation of its key insight.

### 4. Data Cleaning & Preparation

| Issue | Planned approach |
|---|---|
| Missing values | Investigate patterns and select an appropriate imputation strategy. |
| Duplicates | Identify duplicate rows and assess whether removal is justified. |
| Data types | Correct inappropriate types where necessary. |
| Categorical inconsistencies | Standardize values if inconsistencies exist. |
| Outliers | Investigate and retain, cap, or remove based on evidence. |
| Suspicious values | Verify their meaning before modifying or removing them. |
| Target validity | Confirm that target values match the expected binary classes. |

Cleaning decisions will be justified using statistical evidence and domain understanding. Missing values will not automatically be replaced with zero, and extreme values will not automatically be removed.

### 5. Original vs. Cleaned Dataset

The final analysis will compare the original and cleaned datasets based on:

- Number of rows and columns.
- Missing values before and after cleaning.
- Duplicate records.
- Data types and corrected values.
- Treatment of suspicious observations.
- Final dataset readiness for machine learning.

## 📊 Key Findings

The completed notebook will report:

**Data Quality Findings**
- The 3–5 most important issues identified during inspection.
- Their potential impact on analysis.
- The actions taken and the reasons behind them.

**EDA Insights**
- Distribution and imbalance of the target variable.
- Differences in delinquency rates across age groups.
- Income-related patterns.
- Relationship between debt ratio and delinquency.
- Association between credit utilization, previous delinquencies, and the target.

All final findings will be based on the actual analysis rather than assumptions.

## 🤖 Considerations for Future Machine Learning

Before building a predictive model, the following should be evaluated:

1. **Class imbalance:** Consider stratified splitting and appropriate evaluation metrics.
2. **Data leakage:** Fit preprocessing steps on training data only.
3. **Feature quality:** Investigate invalid values, extreme observations, and feature meanings.
4. **Model evaluation:** Consider precision, recall, F1-score, ROC-AUC, and precision-recall AUC.
5. **Fairness and privacy:** Evaluate demographic bias and applicable data-protection requirements.

## 📁 Project Structure

```text
Credit-Score-EDA-Data-Quality-Assessment/
│
├── CreditScore.csv
├── Credit_Score_EDA.ipynb
├── README.md
│
└── outputs/
    ├── visualizations/
    └── reports/
```

The `outputs` directory is optional and can be created to organize saved charts and reports.

## ▶️ How to Run

Install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn jupyter
```

Run Jupyter Notebook:

```bash
jupyter notebook
```

Open `Credit_Score_EDA.ipynb` and execute the notebook cells in sequence. Ensure that `CreditScore.csv` is available at the path specified in the notebook.

## ✅ Expected Deliverables

- Exploratory Data Analysis notebook.
- Data Quality Assessment report.
- Visualizations with written interpretations.
- Documented cleaning decisions.
- Original and cleaned dataset comparison.
- Final cleaned dataset.
- Key findings and machine learning recommendations.

## 🏁 Conclusion

This project establishes a structured understanding of the Credit Score dataset through systematic data inspection, exploratory analysis, and evidence-based preprocessing.

The main goal is to identify data limitations, discover meaningful patterns, and prepare a reliable foundation for future credit-risk machine learning applications.

**Prepared by: Hassan Warraich**

**Course:** Artificial Intelligence (Machine Learning, Deep Learning & Communication) — Batch I
