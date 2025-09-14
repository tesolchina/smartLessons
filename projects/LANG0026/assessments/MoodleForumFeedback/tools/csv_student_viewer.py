#!/usr/bin/env python3
"""
CSV Student List Viewer
=======================

Simple script to view and analyze the student enrollment CSV file.
"""

import pandas as pd

def view_student_list(csv_file: str):
    """View student enrollment data from CSV"""
    print("📋 LANG0026 Student Enrollment Data")
    print("=" * 50)
    
    # Load CSV
    df = pd.read_csv(csv_file)
    
    print(f"✅ Total Students: {len(df)}")
    print(f"📊 Columns: {list(df.columns)}")
    print()
    
    # Section breakdown
    section_counts = df['Section Code'].value_counts().sort_index()
    print("📈 Students by Section:")
    for section, count in section_counts.items():
        print(f"   Section {section}: {count} students")
    print()
    
    # Program breakdown
    program_counts = df['Study Programme'].value_counts()
    print("🎓 Students by Program:")
    for program, count in program_counts.head(10).items():
        print(f"   {program}: {count} students")
    print()
    
    # Sample data
    print("👥 Sample Student Records:")
    print(df[['Section Code', 'Student Name', 'Study Programme']].head(10).to_string(index=False))
    print()
    
    # Missing data check
    print("🔍 Data Quality Check:")
    for col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            print(f"   {col}: {missing} missing values")
    
    return df

def main():
    csv_file = "../../0036students.csv"
    df = view_student_list(csv_file)

if __name__ == "__main__":
    main()