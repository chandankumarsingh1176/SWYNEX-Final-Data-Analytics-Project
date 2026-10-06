"""
SWYNEX Final Data Analytics Project
Task 2 Style - Exploratory Data Analysis & Insights
Dataset: Cleaned Titanic Passenger Data
"""

import pandas as pd
import numpy as np
import os

CLEANED_PATH = "../data/cleaned/cleaned_titanic.csv"
REPORT_PATH = "../reports/analysis_summary.txt"

def load_cleaned_data(path):
    df = pd.read_csv(path)
    print("=" * 70)
    print("CLEANED DATA LOADED FOR ANALYSIS")
    print("=" * 70)
    print(f"Shape: {df.shape}")
    return df


def overall_statistics(df):
    print("\n" + "=" * 70)
    print("1. OVERALL STATISTICS")
    print("=" * 70)
    
    total = len(df)
    survivors = df["Survived"].sum()
    survival_rate = survivors / total * 100
    
    print(f"Total Passengers     : {total}")
    print(f"Total Survivors      : {survivors}")
    print(f"Overall Survival Rate: {survival_rate:.1f}%")
    print(f"Average Age          : {df['Age'].mean():.1f} years")
    print(f"Median Age           : {df['Age'].median():.1f} years")
    print(f"Average Fare         : ${df['Fare'].mean():.2f}")
    print(f"Median Fare          : ${df['Fare'].median():.2f}")
    
    return {
        "total": total,
        "survivors": survivors,
        "survival_rate": round(survival_rate, 1)
    }


def survival_by_gender(df):
    print("\n" + "=" * 70)
    print("2. SURVIVAL BY GENDER")
    print("=" * 70)
    
    gender_stats = df.groupby("Sex_Label").agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    gender_stats["Survival_Rate"] = (gender_stats["Survival_Rate"] * 100).round(1)
    print(gender_stats)
    
    print("\nInsight: Women had a significantly higher survival rate than men.")
    print("         This reflects the 'Women and children first' policy.")


def survival_by_class(df):
    print("\n" + "=" * 70)
    print("3. SURVIVAL BY PASSENGER CLASS")
    print("=" * 70)
    
    class_stats = df.groupby("Pclass_Label").agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    class_stats["Survival_Rate"] = (class_stats["Survival_Rate"] * 100).round(1)
    # Order properly
    class_stats = class_stats.reindex(["1st Class", "2nd Class", "3rd Class"])
    print(class_stats)
    
    print("\nInsight: Higher passenger class = higher survival rate.")
    print("         Socio-economic status strongly influenced survival chances.")


def survival_by_embarked(df):
    print("\n" + "=" * 70)
    print("4. SURVIVAL BY EMBARKED PORT")
    print("=" * 70)
    
    port_stats = df.groupby("Embarked_Label").agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    port_stats["Survival_Rate"] = (port_stats["Survival_Rate"] * 100).round(1)
    print(port_stats)
    
    print("\nInsight: Passengers from Cherbourg had the highest survival rate.")


def survival_by_age_group(df):
    print("\n" + "=" * 70)
    print("5. SURVIVAL BY AGE GROUP")
    print("=" * 70)
    
    age_stats = df.groupby("Age_Group", observed=True).agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    age_stats["Survival_Rate"] = (age_stats["Survival_Rate"] * 100).round(1)
    print(age_stats)
    
    print("\nInsight: Children had relatively better survival odds.")
    print("         Most passengers were Young Adults (19-35).")


def survival_by_family(df):
    print("\n" + "=" * 70)
    print("6. SURVIVAL BY FAMILY SIZE / ALONE STATUS")
    print("=" * 70)
    
    alone_stats = df.groupby("IsAlone").agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    alone_stats.index = alone_stats.index.map({0: "With Family", 1: "Alone"})
    alone_stats["Survival_Rate"] = (alone_stats["Survival_Rate"] * 100).round(1)
    print(alone_stats)
    
    print("\nInsight: Passengers traveling with family had slightly better survival rates.")


def fare_analysis(df):
    print("\n" + "=" * 70)
    print("7. FARE ANALYSIS")
    print("=" * 70)
    
    print("Average Fare by Class:")
    print(df.groupby("Pclass_Label")["Fare"].mean().round(2).reindex(["1st Class", "2nd Class", "3rd Class"]))
    
    print("\nAverage Fare by Survival Status:")
    print(df.groupby("Survived_Label")["Fare"].mean().round(2))
    
    print("\nInsight: Higher ticket fares were associated with better survival chances.")
    print("         Wealthier passengers had better access to lifeboats and upper decks.")


def title_analysis(df):
    print("\n" + "=" * 70)
    print("8. SURVIVAL BY TITLE")
    print("=" * 70)
    
    title_stats = df.groupby("Title").agg(
        Total=("Survived", "count"),
        Survivors=("Survived", "sum"),
        Survival_Rate=("Survived", "mean")
    )
    title_stats["Survival_Rate"] = (title_stats["Survival_Rate"] * 100).round(1)
    print(title_stats.sort_values("Survival_Rate", ascending=False))
    
    print("\nInsight: Titles like Mrs, Miss, Master had high survival rates.")
    print("         'Mr' title (adult males) had the lowest survival rate.")


def generate_report(df, overall):
    """Save a text summary report"""
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("SWYNEX FINAL DATA ANALYTICS PROJECT\n")
        f.write("Titanic Survival Analysis - Key Findings Report\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("OVERALL STATISTICS\n")
        f.write(f"- Total Passengers : {overall['total']}\n")
        f.write(f"- Total Survivors  : {overall['survivors']}\n")
        f.write(f"- Survival Rate    : {overall['survival_rate']}%\n\n")
        
        f.write("KEY BUSINESS INSIGHTS\n")
        f.write("-" * 40 + "\n")
        f.write("1. Gender was the strongest predictor of survival.\n")
        f.write("   Women survived at ~74% vs Men at ~19%.\n\n")
        f.write("2. Socio-economic status (Passenger Class) significantly\n")
        f.write("   affected survival chances (1st: ~63%, 3rd: ~24%).\n\n")
        f.write("3. Children and women had priority access to lifeboats\n")
        f.write("   ('Women and children first' policy).\n\n")
        f.write("4. Higher fare passengers had better survival odds due to\n")
        f.write("   better cabin locations and access to lifeboats.\n\n")
        f.write("5. Most passengers were young adults (19-35 years old).\n\n")
        f.write("6. Passengers traveling with family had slightly better\n")
        f.write("   survival rates than those traveling alone.\n")
    
    print(f"\n✅ Analysis summary saved to: {REPORT_PATH}")


def main():
    df = load_cleaned_data(CLEANED_PATH)
    
    overall = overall_statistics(df)
    survival_by_gender(df)
    survival_by_class(df)
    survival_by_embarked(df)
    survival_by_age_group(df)
    survival_by_family(df)
    fare_analysis(df)
    title_analysis(df)
    
    generate_report(df, overall)
    
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
