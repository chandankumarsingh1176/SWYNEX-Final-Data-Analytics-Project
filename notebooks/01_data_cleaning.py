"""
SWYNEX Final Data Analytics Project
Task 1 Style - Data Cleaning Script
Dataset: Titanic Passenger Data
"""

import pandas as pd
import numpy as np
import os

# Paths
RAW_PATH = "../data/raw/titanic.csv"
CLEANED_PATH = "../data/cleaned/cleaned_titanic.csv"

def load_raw_data(path):
    """Load the raw Titanic dataset"""
    df = pd.read_csv(path)
    print("=" * 60)
    print("RAW DATA LOADED")
    print("=" * 60)
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head())
    print("\nData Types:")
    print(df.dtypes)
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())
    return df


def clean_data(df):
    """Perform data cleaning steps"""
    print("\n" + "=" * 60)
    print("DATA CLEANING PROCESS")
    print("=" * 60)
    
    df_clean = df.copy()
    
    # 1. Handle missing Age values - fill with median
    age_median = df_clean["Age"].median()
    missing_age = df_clean["Age"].isnull().sum()
    df_clean["Age"] = df_clean["Age"].fillna(age_median)
    print(f"1. Age: Filled {missing_age} missing values with median ({age_median})")
    
    # 2. Handle missing Embarked - fill with mode
    embarked_mode = df_clean["Embarked"].mode()[0]
    missing_embarked = df_clean["Embarked"].isnull().sum()
    df_clean["Embarked"] = df_clean["Embarked"].fillna(embarked_mode)
    print(f"2. Embarked: Filled {missing_embarked} missing values with mode ('{embarked_mode}')")
    
    # 3. Handle missing Fare - fill with median
    fare_median = df_clean["Fare"].median()
    missing_fare = df_clean["Fare"].isnull().sum()
    df_clean["Fare"] = df_clean["Fare"].fillna(fare_median)
    print(f"3. Fare: Filled {missing_fare} missing values with median ({fare_median})")
    
    # 4. Cabin has too many missing values - create binary feature instead of dropping
    df_clean["Has_Cabin"] = df_clean["Cabin"].notnull().astype(int)
    print(f"4. Cabin: Created 'Has_Cabin' feature (1 = has cabin info, 0 = missing). Original Cabin column kept for reference.")
    
    # 5. Feature Engineering for better analysis
    df_clean["FamilySize"] = df_clean["SibSp"] + df_clean["Parch"] + 1
    df_clean["IsAlone"] = (df_clean["FamilySize"] == 1).astype(int)
    
    # Age groups
    df_clean["Age_Group"] = pd.cut(
        df_clean["Age"],
        bins=[0, 12, 18, 35, 50, 100],
        labels=["Child (0-12)", "Teen (13-18)", "Young Adult (19-35)", "Adult (36-50)", "Senior (51+)"]
    )
    
    # Title extraction from Name (useful feature)
    df_clean["Title"] = df_clean["Name"].str.extract(r',\s*([^\.]+)\.', expand=False)
    # Simplify rare titles
    title_map = {
        "Mr": "Mr", "Miss": "Miss", "Mrs": "Mrs", "Master": "Master",
        "Dr": "Rare", "Rev": "Rare", "Col": "Rare", "Major": "Rare",
        "Mlle": "Miss", "Mme": "Mrs", "Ms": "Miss", "Lady": "Rare",
        "Sir": "Rare", "Capt": "Rare", "Countess": "Rare", "Jonkheer": "Rare",
        "Don": "Rare", "Dona": "Rare"
    }
    df_clean["Title"] = df_clean["Title"].map(title_map).fillna("Rare")
    
    # Readable labels
    df_clean["Survived_Label"] = df_clean["Survived"].map({0: "Did Not Survive", 1: "Survived"})
    df_clean["Pclass_Label"] = df_clean["Pclass"].map({1: "1st Class", 2: "2nd Class", 3: "3rd Class"})
    df_clean["Sex_Label"] = df_clean["Sex"].str.title()
    df_clean["Embarked_Label"] = df_clean["Embarked"].map({
        "C": "Cherbourg", "Q": "Queenstown", "S": "Southampton"
    })
    
    print("5. Feature Engineering completed:")
    print("   - FamilySize, IsAlone")
    print("   - Age_Group")
    print("   - Title (extracted from Name)")
    print("   - Readable labels (Survived_Label, Pclass_Label, etc.)")
    
    # Final check
    print("\n" + "=" * 60)
    print("CLEANED DATA SUMMARY")
    print("=" * 60)
    print(f"Shape: {df_clean.shape}")
    print("\nMissing Values after cleaning:")
    print(df_clean.isnull().sum())
    print("\nNew columns added:", [c for c in df_clean.columns if c not in df.columns])
    
    return df_clean


def main():
    # Ensure directories exist
    os.makedirs(os.path.dirname(CLEANED_PATH), exist_ok=True)
    
    # Load
    df = load_raw_data(RAW_PATH)
    
    # Clean
    df_clean = clean_data(df)
    
    # Save
    df_clean.to_csv(CLEANED_PATH, index=False)
    print(f"\n✅ Cleaned data saved to: {CLEANED_PATH}")
    print(f"   Total rows: {len(df_clean)}")
    print(f"   Total columns: {len(df_clean.columns)}")


if __name__ == "__main__":
    main()
