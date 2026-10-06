# SWYNEX-Final-Data-Analytics-Project

**SWYNEX Technologies Data Analytics Internship – Final Project (Task 4)**

A complete end-to-end data analytics case study on the **Titanic Passenger Dataset**.

---

## 📌 Project Overview

This project combines all stages of a data analytics workflow:

1. **Problem Statement**
2. **Dataset Information**
3. **Data Cleaning**
4. **Exploratory Data Analysis (EDA)**
5. **Interactive Dashboard**
6. **Key Business Insights**

**Goal:** Understand the factors that influenced passenger survival during the Titanic disaster and present findings through clean analysis and an interactive dashboard.

---

## 1. Problem Statement

The RMS Titanic sank on April 15, 1912 after hitting an iceberg. Of the 891 passengers in this dataset, only **38.4%** survived.

**Questions we aim to answer:**

- Who had a higher chance of survival?
- How did **gender**, **passenger class**, and **age** affect survival?
- Did **ticket fare** and **embarkation port** play a role?
- Were passengers traveling with family more likely to survive?

These insights help us understand social and economic factors that determined survival during the disaster.

---

## 2. Dataset Information

| Item | Details |
|------|---------|
| **Dataset** | Titanic Passenger Data |
| **Source** | Public dataset (Kaggle / Data Science Dojo) |
| **Rows** | 891 passengers |
| **Original Columns** | 12 (PassengerId, Survived, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked) |
| **Target Variable** | `Survived` (0 = Did not survive, 1 = Survived) |

### Key Columns
- **Survived** – Survival status
- **Pclass** – Ticket class (1 = Upper, 2 = Middle, 3 = Lower)
- **Sex** – Gender
- **Age** – Age in years
- **SibSp / Parch** – Family members aboard
- **Fare** – Passenger fare
- **Embarked** – Port of Embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)

---

## 3. Data Cleaning Process

**Script:** `notebooks/01_data_cleaning.py`

### Issues Found
| Column | Missing Values | Action Taken |
|--------|----------------|--------------|
| Age | 177 (19.9%) | Filled with median age (28.0) |
| Embarked | 2 (0.2%) | Filled with mode ('S') |
| Fare | 0 | No action needed |
| Cabin | 687 (77.1%) | Created binary feature `Has_Cabin` instead of dropping |

### Feature Engineering
- `FamilySize` = SibSp + Parch + 1
- `IsAlone` = 1 if FamilySize == 1 else 0
- `Age_Group` – Child, Teen, Young Adult, Adult, Senior
- `Title` – Extracted from passenger name (Mr, Mrs, Miss, Master, Rare)
- Readable labels: `Survived_Label`, `Pclass_Label`, `Sex_Label`, `Embarked_Label`

**Cleaned file:** `data/cleaned/cleaned_titanic.csv` (891 rows × 21 columns)

---

## 4. Data Analysis (EDA)

**Script:** `notebooks/02_data_analysis.py`  
**Report:** `reports/analysis_summary.txt`

### Key Findings

| Factor | Insight | Survival Rate |
|--------|---------|---------------|
| **Gender** | Strongest predictor | Female: **74.2%** / Male: **18.9%** |
| **Passenger Class** | Higher class → higher survival | 1st: **63.0%** / 2nd: **47.3%** / 3rd: **24.2%** |
| **Age Group** | Children had better odds | Child (0-12): **58.0%** |
| **Embarked Port** | Cherbourg highest | Cherbourg: **55.4%** |
| **Family** | Traveling with family better | With Family: **50.6%** / Alone: **30.4%** |
| **Fare** | Higher fare → better survival | Survivors avg fare: **$48.40** vs Non-survivors: **$22.12** |

**Overall Survival Rate: 38.4%**

---

## 5. Interactive Dashboard

**Location:** `dashboard/app.py`  
**Tools:** Streamlit + Plotly

### Features
- **KPI Cards:** Total Passengers, Survivors, Survival Rate, Avg Age, Avg Fare
- **Charts:**
  - Survival by Gender
  - Survival by Passenger Class
  - Survival by Embarked Port
  - Age Distribution by Survival
  - Survival Rate Heatmap (Age Group × Class)
  - Fare Distribution (Box Plot)
  - Overall Survival Donut Chart
- **Interactive Filters:** Gender, Class, Embarked Port, Age Range

### How to Run the Dashboard
```bash
cd dashboard
streamlit run app.py
```
The dashboard will open at `http://localhost:8501`.

---

## 6. Key Business Insights

1. **Gender was the strongest predictor of survival**  
   Women survived at ~74% compared to only ~19% of men — reflecting the “Women and children first” policy.

2. **Socio-economic status mattered significantly**  
   1st Class passengers had a 63% survival rate while 3rd Class passengers had only 24%.

3. **Children were prioritized**  
   Children (0–12 years) had a 58% survival rate, higher than most adult groups.

4. **Higher ticket fares correlated with better survival**  
   Survivors paid more than double the average fare of non-survivors, indicating better access to lifeboats and upper-deck cabins.

5. **Family presence improved survival chances**  
   Passengers traveling with family had a 50.6% survival rate vs 30.4% for those traveling alone.

6. **Most passengers were young adults**  
   The largest group was aged 19–35 years.

---

## 📂 Project Structure

```
SWYNEX-Final-Data-Analytics-Project/
├── data/
│   ├── raw/
│   │   └── titanic.csv                 # Original raw dataset
│   └── cleaned/
│       └── cleaned_titanic.csv         # Cleaned & feature-engineered data
├── notebooks/
│   ├── 01_data_cleaning.py             # Data cleaning script
│   └── 02_data_analysis.py             # EDA & insights script
├── dashboard/
│   └── app.py                          # Interactive Streamlit dashboard
├── reports/
│   └── analysis_summary.txt            # Key findings report
├── assets/                             # Screenshots (add your own)
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

- **Python** (Pandas, NumPy)
- **Streamlit** – Interactive dashboard
- **Plotly** – Interactive visualizations
- **GitHub** – Project hosting

---

## 🚀 How to Run the Full Project

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/SWYNEX-Final-Data-Analytics-Project.git
cd SWYNEX-Final-Data-Analytics-Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run data cleaning (optional – cleaned data already included)
cd notebooks
python 01_data_cleaning.py

# 4. Run analysis
python 02_data_analysis.py

# 5. Launch interactive dashboard
cd ../dashboard
streamlit run app.py
```

---

## 📸 Screenshots

> After running the dashboard, add screenshots here:
> - Full dashboard view
> - Filtered view examples
> - KPI cards close-up

---

## 📝 LinkedIn Post Suggestion

```
Completed Task 4 (Final Data Analytics Project) of my internship with @SWYNEX Technologies.

I built a complete end-to-end Titanic Survival Analysis project covering:
• Problem Statement & Dataset Exploration
• Data Cleaning & Feature Engineering
• Exploratory Data Analysis with key insights
• Interactive Dashboard (Streamlit + Plotly)

Key Finding: Gender and passenger class were the strongest predictors of survival.

#SWYNEX #Internship #DataAnalytics #Python #Streamlit #Dashboard #Titanic
```

---

## 👤 Author

Created as part of the **SWYNEX Technologies Data Analytics Internship**.

---

## 📄 License

This project is for educational purposes as part of the SWYNEX internship program.
