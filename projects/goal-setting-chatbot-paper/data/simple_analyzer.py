#!/usr/bin/env python3
"""
Simple Chatbot Data Analyzer
Processes Excel data to count logins, chat rounds, and word counts
Created: September 6, 2025
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

def load_excel_data(file_path):
    """Load Excel data and display structure"""
    print(f"📊 Loading Excel file: {file_path}")
    
    try:
        # Load all sheets to see structure
        excel_file = pd.ExcelFile(file_path)
        print(f"Found {len(excel_file.sheet_names)} sheet(s): {excel_file.sheet_names}")
        
        # Load the first sheet
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"✅ Loaded sheet with {df.shape[0]} rows and {df.shape[1]} columns")
        
        print("\n📋 Column names:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        print(f"\n📊 First 3 rows preview:")
        print(df.head(3).to_string())
        
        return df
        
    except Exception as e:
        print(f"❌ Error loading Excel: {e}")
        return None

def analyze_student_usage(df):
    """Analyze student usage patterns"""
    print("\n" + "="*60)
    print("📈 ANALYZING STUDENT USAGE PATTERNS")
    print("="*60)
    
    # Try to identify key columns automatically
    columns = df.columns.str.lower()
    
    # Look for student identifier
    student_cols = [col for col in df.columns if any(word in col.lower() 
                   for word in ['student', 'user', 'name', 'id'])]
    
    # Look for content/message columns
    content_cols = [col for col in df.columns if any(word in col.lower() 
                   for word in ['content', 'message', 'chat', 'text', 'response'])]
    
    # Look for time/date columns
    time_cols = [col for col in df.columns if any(word in col.lower() 
                for word in ['time', 'date', 'timestamp', 'created'])]
    
    print(f"🔍 Identified columns:")
    print(f"   Student ID candidates: {student_cols}")
    print(f"   Content candidates: {content_cols}")
    print(f"   Time candidates: {time_cols}")
    
    # Use the first found columns or ask user to specify
    if not student_cols:
        print("❌ Could not identify student ID column")
        return None
    
    student_col = student_cols[0]
    content_col = content_cols[0] if content_cols else None
    time_col = time_cols[0] if time_cols else None
    
    print(f"\n✅ Using columns:")
    print(f"   Student: {student_col}")
    print(f"   Content: {content_col}")
    print(f"   Time: {time_col}")
    
    # Process data
    analysis_data = []
    
    for student in df[student_col].unique():
        if pd.isna(student):
            continue
            
        student_data = df[df[student_col] == student]
        
        # Count logins (unique dates if time column exists)
        if time_col:
            try:
                student_data[time_col] = pd.to_datetime(student_data[time_col])
                login_count = student_data[time_col].dt.date.nunique()
            except:
                login_count = 1  # Fallback
        else:
            login_count = 1  # Assume one login if no time data
        
        # Count chat rounds
        chat_rounds = len(student_data)
        
        # Count words
        total_words = 0
        if content_col:
            for content in student_data[content_col]:
                if pd.notna(content):
                    total_words += len(str(content).split())
        
        analysis_data.append({
            'Student': str(student),
            'Login_Count': login_count,
            'Chat_Rounds': chat_rounds,
            'Total_Words': total_words
        })
    
    # Create results DataFrame
    results_df = pd.DataFrame(analysis_data)
    
    # Display summary
    print(f"\n📊 ANALYSIS RESULTS")
    print(f"Total students analyzed: {len(results_df)}")
    print(f"Average logins per student: {results_df['Login_Count'].mean():.2f}")
    print(f"Average chat rounds per student: {results_df['Chat_Rounds'].mean():.2f}")
    print(f"Average words per student: {results_df['Total_Words'].mean():.2f}")
    print(f"Total chat interactions: {results_df['Chat_Rounds'].sum()}")
    
    return results_df

def save_results(results_df, output_path):
    """Save results to CSV"""
    try:
        results_df.to_csv(output_path, index=False)
        print(f"✅ Results saved to: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving CSV: {e}")
        return False

def create_charts(results_df, output_dir):
    """Create visualization charts"""
    print(f"\n📈 Creating charts...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Chatbot Usage Analysis - Goal Setting Study', fontsize=16, fontweight='bold')
    
    # 1. Login counts
    axes[0, 0].bar(range(len(results_df)), results_df['Login_Count'], 
                   color='skyblue', alpha=0.7)
    axes[0, 0].set_title('Login Count per Student')
    axes[0, 0].set_xlabel('Student Index')
    axes[0, 0].set_ylabel('Number of Logins')
    axes[0, 0].grid(True, alpha=0.3)
    
    # 2. Chat rounds
    axes[0, 1].bar(range(len(results_df)), results_df['Chat_Rounds'], 
                   color='lightgreen', alpha=0.7)
    axes[0, 1].set_title('Chat Rounds per Student')
    axes[0, 1].set_xlabel('Student Index')
    axes[0, 1].set_ylabel('Number of Chat Rounds')
    axes[0, 1].grid(True, alpha=0.3)
    
    # 3. Word counts
    axes[1, 0].bar(range(len(results_df)), results_df['Total_Words'], 
                   color='salmon', alpha=0.7)
    axes[1, 0].set_title('Total Words per Student')
    axes[1, 0].set_xlabel('Student Index')
    axes[1, 0].set_ylabel('Total Word Count')
    axes[1, 0].grid(True, alpha=0.3)
    
    # 4. Correlation plot
    axes[1, 1].scatter(results_df['Chat_Rounds'], results_df['Total_Words'], 
                       color='purple', alpha=0.6)
    axes[1, 1].set_title('Chat Rounds vs Total Words')
    axes[1, 1].set_xlabel('Chat Rounds')
    axes[1, 1].set_ylabel('Total Words')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Add correlation
    correlation = results_df['Chat_Rounds'].corr(results_df['Total_Words'])
    axes[1, 1].text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                   transform=axes[1, 1].transAxes,
                   bbox=dict(boxstyle="round", facecolor="white", alpha=0.8))
    
    plt.tight_layout()
    
    # Save chart
    chart_path = os.path.join(output_dir, 'chatbot_usage_analysis.png')
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    print(f"✅ Chart saved to: {chart_path}")
    
    # Summary stats chart
    plt.figure(figsize=(10, 6))
    
    stats = ['Average Logins', 'Average Chat Rounds', 'Average Words']
    values = [
        results_df['Login_Count'].mean(),
        results_df['Chat_Rounds'].mean(),
        results_df['Total_Words'].mean()
    ]
    
    bars = plt.bar(stats, values, color=['skyblue', 'lightgreen', 'salmon'], alpha=0.7)
    plt.title('Overall Usage Statistics', fontsize=14, fontweight='bold')
    plt.ylabel('Average Count')
    plt.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}', ha='center', va='bottom')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    summary_path = os.path.join(output_dir, 'usage_summary.png')
    plt.savefig(summary_path, dpi=300, bbox_inches='tight')
    print(f"✅ Summary chart saved to: {summary_path}")
    
    return True

def main():
    """Main execution"""
    print("🤖 Simple Chatbot Data Analyzer")
    print("="*50)
    
    # File paths
    base_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/goal-setting-chatbot-paper"
    excel_file = os.path.join(base_dir, "data", "final_report_fulfill.xlsx")
    csv_output = os.path.join(base_dir, "data", "usage_analysis_results.csv")
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ Excel file not found: {excel_file}")
        return
    
    # Load data
    df = load_excel_data(excel_file)
    if df is None:
        return
    
    # Analyze data
    results = analyze_student_usage(df)
    if results is None:
        return
    
    # Show top students
    print(f"\n🏆 Top 5 Most Active Students (by chat rounds):")
    top_students = results.nlargest(5, 'Chat_Rounds')
    for _, row in top_students.iterrows():
        print(f"   {row['Student']}: {row['Login_Count']} logins, "
              f"{row['Chat_Rounds']} rounds, {row['Total_Words']} words")
    
    # Save results
    save_results(results, csv_output)
    
    # Create charts
    create_charts(results, os.path.join(base_dir, "data"))
    
    print(f"\n🎉 Analysis completed!")
    print(f"   📊 CSV: {csv_output}")
    print(f"   📈 Charts: {base_dir}/data/")

if __name__ == "__main__":
    main()
