#!/usr/bin/env python3
"""
Chatbot Usage Data Analysis Script
Analyzes student login patterns, chat rounds, and word counts from goal-setting chatbot study
Created: September 6, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

class ChatbotDataAnalyzer:
    """Analyze chatbot usage data for goal-setting study"""
    
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.data = None
        self.analysis_results = {}
        
    def load_data(self):
        """Load and examine the Excel file structure"""
        try:
            # Try to read all sheets first to understand structure
            excel_file = pd.ExcelFile(self.excel_file_path)
            print(f"📊 Excel file contains {len(excel_file.sheet_names)} sheets:")
            for i, sheet in enumerate(excel_file.sheet_names):
                print(f"   {i+1}. {sheet}")
            
            # Load the main sheet (assuming first sheet or most relevant)
            if len(excel_file.sheet_names) == 1:
                self.data = pd.read_excel(self.excel_file_path)
                sheet_name = excel_file.sheet_names[0]
            else:
                # Try to find the main data sheet
                main_sheet = None
                for sheet in excel_file.sheet_names:
                    if any(keyword in sheet.lower() for keyword in ['data', 'main', 'chat', 'log', 'fulfill']):
                        main_sheet = sheet
                        break
                
                if main_sheet:
                    self.data = pd.read_excel(self.excel_file_path, sheet_name=main_sheet)
                    sheet_name = main_sheet
                else:
                    # Default to first sheet
                    self.data = pd.read_excel(self.excel_file_path, sheet_name=excel_file.sheet_names[0])
                    sheet_name = excel_file.sheet_names[0]
            
            print(f"✅ Loaded data from sheet: '{sheet_name}'")
            print(f"📈 Data shape: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
            print(f"🔍 Column names: {list(self.data.columns)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading Excel file: {e}")
            return False
    
    def examine_data_structure(self):
        """Examine and display data structure"""
        if self.data is None:
            print("❌ No data loaded")
            return
        
        print("\n" + "="*50)
        print("📋 DATA STRUCTURE ANALYSIS")
        print("="*50)
        
        # Display basic info
        print(f"Dataset shape: {self.data.shape}")
        print(f"Memory usage: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Display column information
        print("\n🔍 Column Details:")
        for i, col in enumerate(self.data.columns):
            dtype = self.data[col].dtype
            null_count = self.data[col].isnull().sum()
            unique_count = self.data[col].nunique()
            print(f"   {i+1:2d}. {col:<25} | Type: {dtype:<12} | Nulls: {null_count:>4} | Unique: {unique_count:>6}")
        
        # Display first few rows
        print("\n📊 First 5 rows:")
        display_cols = self.data.columns[:8]  # Show first 8 columns to avoid overflow
        print(self.data[display_cols].head().to_string(index=False))
        
        if len(self.data.columns) > 8:
            print(f"\n... and {len(self.data.columns) - 8} more columns")
        
        # Look for key columns related to our analysis
        key_patterns = {
            'student_id': ['student', 'user', 'id', 'name'],
            'login_time': ['login', 'time', 'timestamp', 'date'],
            'chat_content': ['chat', 'message', 'content', 'text'],
            'session': ['session', 'round', 'conversation']
        }
        
        print("\n🔍 Potential Key Columns for Analysis:")
        for category, patterns in key_patterns.items():
            matching_cols = []
            for col in self.data.columns:
                if any(pattern in col.lower() for pattern in patterns):
                    matching_cols.append(col)
            if matching_cols:
                print(f"   {category}: {matching_cols}")
    
    def identify_analysis_columns(self):
        """Automatically identify relevant columns for analysis"""
        if self.data is None:
            return None
        
        columns = self.data.columns.str.lower()
        
        # Try to identify key columns
        student_col = None
        time_col = None
        content_col = None
        session_col = None
        
        # Find student identifier column
        for col in self.data.columns:
            if any(pattern in col.lower() for pattern in ['student', 'user', 'name', 'id']):
                student_col = col
                break
        
        # Find timestamp column
        for col in self.data.columns:
            if any(pattern in col.lower() for pattern in ['time', 'date', 'timestamp', 'login']):
                if self.data[col].dtype in ['datetime64[ns]', 'object']:
                    time_col = col
                    break
        
        # Find content column
        for col in self.data.columns:
            if any(pattern in col.lower() for pattern in ['content', 'message', 'chat', 'text', 'response']):
                content_col = col
                break
        
        # Find session column
        for col in self.data.columns:
            if any(pattern in col.lower() for pattern in ['session', 'round', 'conversation']):
                session_col = col
                break
        
        identified = {
            'student_id': student_col,
            'timestamp': time_col,
            'content': content_col,
            'session': session_col
        }
        
        print("\n🎯 Auto-identified columns:")
        for key, col in identified.items():
            print(f"   {key}: {col if col else 'Not found'}")
        
        return identified
    
    def analyze_usage_patterns(self, student_col, time_col, content_col, session_col=None):
        """Analyze student usage patterns"""
        print("\n" + "="*50)
        print("📈 USAGE PATTERN ANALYSIS")
        print("="*50)
        
        # Create a copy for analysis
        df = self.data.copy()
        
        # Convert timestamp if needed
        if time_col and df[time_col].dtype == 'object':
            try:
                df[time_col] = pd.to_datetime(df[time_col])
            except:
                print(f"⚠️  Could not convert {time_col} to datetime")
        
        # Calculate word counts if content column exists
        if content_col:
            df['word_count'] = df[content_col].astype(str).apply(lambda x: len(str(x).split()) if pd.notna(x) else 0)
        
        # Group by student to analyze patterns
        if session_col:
            # If we have session information
            student_stats = df.groupby([student_col, session_col]).agg({
                time_col: 'first' if time_col else 'count',
                content_col: 'count' if content_col else 'count',
                'word_count': 'sum' if content_col else 'count'
            }).reset_index()
            
            # Aggregate by student
            final_stats = student_stats.groupby(student_col).agg({
                session_col: 'nunique',  # Number of sessions (logins)
                content_col: 'sum',      # Total chat rounds
                'word_count': 'sum'      # Total word count
            }).reset_index()
            
            final_stats.columns = [student_col, 'login_count', 'chat_rounds', 'total_words']
            
        else:
            # If no session info, group by student and date
            if time_col:
                df['date'] = df[time_col].dt.date
                student_stats = df.groupby([student_col, 'date']).agg({
                    content_col: 'count' if content_col else 'count',
                    'word_count': 'sum' if content_col else 'count'
                }).reset_index()
                
                final_stats = student_stats.groupby(student_col).agg({
                    'date': 'nunique',         # Number of login days
                    content_col: 'sum',        # Total chat rounds
                    'word_count': 'sum'        # Total word count
                }).reset_index()
                
                final_stats.columns = [student_col, 'login_count', 'chat_rounds', 'total_words']
            else:
                # Fallback: just count by student
                final_stats = df.groupby(student_col).agg({
                    content_col: 'count' if content_col else 'count',
                    'word_count': 'sum' if content_col else 'count'
                }).reset_index()
                
                final_stats.columns = [student_col, 'chat_rounds', 'total_words']
                final_stats['login_count'] = 1  # Assume 1 login per student
        
        self.analysis_results = final_stats
        
        # Display summary statistics
        print(f"📊 Analysis Results for {len(final_stats)} students:")
        print(f"   • Average logins per student: {final_stats['login_count'].mean():.2f}")
        print(f"   • Average chat rounds per student: {final_stats['chat_rounds'].mean():.2f}")
        print(f"   • Average words per student: {final_stats['total_words'].mean():.2f}")
        print(f"   • Total chat rounds: {final_stats['chat_rounds'].sum()}")
        print(f"   • Total words: {final_stats['total_words'].sum()}")
        
        return final_stats
    
    def save_results_csv(self, output_path):
        """Save analysis results to CSV"""
        if self.analysis_results is None or len(self.analysis_results) == 0:
            print("❌ No analysis results to save")
            return False
        
        try:
            self.analysis_results.to_csv(output_path, index=False)
            print(f"✅ Results saved to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return False
    
    def create_visualizations(self, output_dir):
        """Create visualization charts"""
        if self.analysis_results is None or len(self.analysis_results) == 0:
            print("❌ No analysis results to visualize")
            return False
        
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Chatbot Usage Analysis - Goal Setting Study', fontsize=16, fontweight='bold')
        
        df = self.analysis_results
        student_col = df.columns[0]
        
        # 1. Login Count Distribution
        axes[0, 0].bar(range(len(df)), df['login_count'], color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Login Count per Student', fontweight='bold')
        axes[0, 0].set_xlabel('Student')
        axes[0, 0].set_ylabel('Number of Logins')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Chat Rounds Distribution
        axes[0, 1].bar(range(len(df)), df['chat_rounds'], color='lightgreen', alpha=0.7)
        axes[0, 1].set_title('Chat Rounds per Student', fontweight='bold')
        axes[0, 1].set_xlabel('Student')
        axes[0, 1].set_ylabel('Number of Chat Rounds')
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Word Count Distribution
        axes[1, 0].bar(range(len(df)), df['total_words'], color='salmon', alpha=0.7)
        axes[1, 0].set_title('Total Words per Student', fontweight='bold')
        axes[1, 0].set_xlabel('Student')
        axes[1, 0].set_ylabel('Total Word Count')
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Correlation Plot
        axes[1, 1].scatter(df['chat_rounds'], df['total_words'], color='purple', alpha=0.6, s=60)
        axes[1, 1].set_title('Chat Rounds vs Total Words', fontweight='bold')
        axes[1, 1].set_xlabel('Chat Rounds')
        axes[1, 1].set_ylabel('Total Words')
        axes[1, 1].grid(True, alpha=0.3)
        
        # Add correlation coefficient
        correlation = df['chat_rounds'].corr(df['total_words'])
        axes[1, 1].text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
                       transform=axes[1, 1].transAxes, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
        
        plt.tight_layout()
        
        # Save the plot
        chart_path = os.path.join(output_dir, 'chatbot_usage_analysis.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        print(f"✅ Charts saved to: {chart_path}")
        
        # Create summary statistics chart
        fig2, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        # Summary statistics
        stats_data = {
            'Metric': ['Average Logins', 'Average Chat Rounds', 'Average Words per Student'],
            'Value': [
                df['login_count'].mean(),
                df['chat_rounds'].mean(), 
                df['total_words'].mean()
            ]
        }
        
        bars = ax.bar(stats_data['Metric'], stats_data['Value'], 
                     color=['skyblue', 'lightgreen', 'salmon'], alpha=0.7)
        ax.set_title('Overall Usage Statistics', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Count')
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        summary_path = os.path.join(output_dir, 'usage_summary.png')
        plt.savefig(summary_path, dpi=300, bbox_inches='tight')
        print(f"✅ Summary chart saved to: {summary_path}")
        
        plt.show()
        return True

def main():
    """Main execution function"""
    print("🤖 Chatbot Usage Data Analyzer")
    print("="*50)
    
    # File paths
    base_dir = "/Users/simonwang/Documents/Usage/VibeCoding/DailyAssistant/projects/goal-setting-chatbot-paper"
    excel_file = os.path.join(base_dir, "data", "final_report_fulfill.xlsx")
    output_csv = os.path.join(base_dir, "data", "usage_analysis_results.csv")
    
    # Create analyzer
    analyzer = ChatbotDataAnalyzer(excel_file)
    
    # Load and examine data
    if not analyzer.load_data():
        return
    
    analyzer.examine_data_structure()
    identified_cols = analyzer.identify_analysis_columns()
    
    if not identified_cols:
        print("❌ Could not identify required columns automatically")
        return
    
    # Manual override if auto-detection fails
    print("\n" + "="*50)
    print("🔧 COLUMN CONFIGURATION")
    print("="*50)
    
    # You can manually specify columns here if auto-detection doesn't work
    student_col = identified_cols['student_id']
    time_col = identified_cols['timestamp'] 
    content_col = identified_cols['content']
    session_col = identified_cols['session']
    
    if not student_col:
        print("❌ Could not identify student ID column")
        print("Available columns:", list(analyzer.data.columns))
        return
    
    # Perform analysis
    results = analyzer.analyze_usage_patterns(student_col, time_col, content_col, session_col)
    
    if results is not None and len(results) > 0:
        # Save CSV results
        analyzer.save_results_csv(output_csv)
        
        # Create visualizations
        analyzer.create_visualizations(os.path.join(base_dir, "data"))
        
        print(f"\n🎉 Analysis completed successfully!")
        print(f"   📊 CSV results: {output_csv}")
        print(f"   📈 Charts: {base_dir}/data/")
        
        # Display top students
        print(f"\n🏆 Top 5 Most Active Students:")
        top_students = results.nlargest(5, 'chat_rounds')
        for i, row in top_students.iterrows():
            print(f"   {row[student_col]}: {row['login_count']} logins, {row['chat_rounds']} rounds, {row['total_words']} words")
    
    else:
        print("❌ Analysis failed - no results generated")

if __name__ == "__main__":
    main()
