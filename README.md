# Workforce Quality & Governance Dashboard

**Live Dashboard:** https://workforce-quality-governance-clunam.streamlit.app/  
Interactive visualization for workforce-quality metrics, recruitment patterns, manager effectiveness, and department turnover indicators.

---

## Project Overview

This project processes three HR datasets and produces governance-style metrics for evaluating workforce stability, recruitment quality, and manager performance.  
All outputs are integrated into a lightweight Streamlit dashboard.

The pipeline includes:

- Data cleaning & standardization  
- Performance and tenure engineering  
- Recruitment source quality scoring  
- Manager Effectiveness Index (MEI) construction  
- Department turnover calculation  
- Exporting model-ready & dashboard-ready CSV outputs  

---

## 📊 Input Datasets

### **1. Employee Master Data** — `staff_particulars.csv`
Contains core HR fields:
- hire/termination dates  
- performance scores  
- pay rate  
- department & manager  
- recruitment source  

### **2. Salary Structure Grid** — `salary_grid.csv`
Job-level pay ranges used for salary exploration.

### **3. Recruitment Cost Data** — `recruitment_costs.csv`
Costs per hiring channel (used to contextualize recruitment performance).

---

## 🧠 What the Pipeline Computes

### **1. Recruitment Source Summary**
For each hiring channel:
- number of hires  
- average tenure  
- average performance  
- retention rate  
- average pay  

**Output:** `recruitment_source_summary.csv`

---

### **2. Manager Effectiveness Index (MEI)**
Built from three normalized metrics:
- average team performance  
- median team tenure  
- retention rate  

Scores are z-normalized and averaged into a composite index.  
**Output:** `manager_summary.csv`

---

### **3. Department Turnover Indicators**
Department-level churn signals:
- headcount  
- number of exits  
- turnover rate  

**Output:** `turnover_by_dept.csv` 

---

## 🎛️ Dashboard Features

The Streamlit app includes:

### 1) Recruitment Source Scorecard  
Bar chart + downloadable table of recruitment quality metrics.

### 2) Manager Effectiveness Index  
Ranked MEI visualization to surface high- and low-stability managers.

### 3) Department Turnover View  
Simple bar chart showing department-level turnover rates.

### 4) Salary Grid Explorer  
Displays top salary ranges from the salary grid dataset.

---

## 🛠️ Tech Stack

- **Python**  
- **pandas** — data cleaning & engineering  
- **scikit-learn** — performance normalization utilities  
- **Plotly** — interactive charts  
- **Streamlit** — dashboard interface  

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

## Repo Structure

```bash
workforce-quality-governance/
│
├── streamlit_app.py
├── output/
│   ├── recruitment_source_summary.csv
│   ├── manager_summary.csv
│   ├── turnover_by_dept.csv
│   └── salary_grid.csv
└── README.md
```

---

### Notes

This project focuses on clean feature engineering and governance-ready metrics, not predictive modeling.
All computations are transparent and reproducible through the included Python scripts.
