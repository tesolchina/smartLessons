#!/usr/bin/env python3
"""
Word Count Analyzer for Donald's Geography Coursework
Analyzes word count by section to help with manuscript length management.
"""

import re
import os
from pathlib import Path

def clean_text_for_counting(text):
    """Clean text for accurate word counting"""
    # Remove markdown formatting
    text = re.sub(r'#+\s*', '', text)  # Remove headers
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)  # Remove italic
    text = re.sub(r'`(.*?)`', r'\1', text)  # Remove code formatting
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # Remove links but keep text
    text = re.sub(r'!\[\]\(\)', '', text)  # Remove empty image placeholders
    text = re.sub(r'\|.*?\|', '', text)  # Remove table separators
    text = re.sub(r'^[-=]+$', '', text, flags=re.MULTILINE)  # Remove table dividers
    
    # Remove URLs and citations
    text = re.sub(r'http[s]?://\S+', '', text)
    text = re.sub(r'www\.\S+', '', text)
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def count_words(text):
    """Count words in cleaned text"""
    if not text:
        return 0
    cleaned = clean_text_for_counting(text)
    words = cleaned.split()
    return len([word for word in words if word.strip()])

def analyze_manuscript_sections(file_path):
    """Analyze word count by section"""
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    print("📊 IGCSE Geography Coursework - Word Count Analysis")
    print("=" * 60)
    print(f"📄 File: {os.path.basename(file_path)}")
    print("=" * 60)
    
    # Define section patterns
    sections = {
        "Title and Contents": r"^(.*?)(?=# Introduction)",
        "Introduction": r"# Introduction(.*?)(?=# Methodology)",
        "Methodology": r"# Methodology(.*?)(?=# Data Presentation)",
        "Data Presentation & Analysis": r"# Data Presentation(.*?)(?=# Conclusion)",
        "Conclusion": r"# Conclusion(.*?)(?=# Evaluation)",
        "Evaluation": r"# Evaluation(.*?)(?=# Bibliography)",
        "Bibliography": r"# Bibliography(.*?)(?=# Appendix)",
        "Appendix": r"# Appendix(.*?)$"
    }
    
    total_words = 0
    section_counts = {}
    
    for section_name, pattern in sections.items():
        matches = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if matches:
            section_text = matches.group(1) if matches.lastindex and matches.lastindex >= 1 else matches.group(0)
            word_count = count_words(section_text)
            section_counts[section_name] = word_count
            total_words += word_count
            
            # Visual progress bar
            bar_length = 30
            percentage = (word_count / 3000) * 100 if word_count < 3000 else 100
            filled_length = int(bar_length * word_count / 3000) if word_count < 3000 else bar_length
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            print(f"{section_name:<25} │ {word_count:>4} words │ {bar} │ {percentage:5.1f}%")
        else:
            section_counts[section_name] = 0
            print(f"{section_name:<25} │    0 words │ {'░' * 30} │   0.0%")
    
    print("=" * 60)
    print(f"{'TOTAL WORD COUNT':<25} │ {total_words:>4} words")
    print("=" * 60)
    
    # IGCSE Guidelines Analysis
    print("\n📋 IGCSE Geography Coursework Requirements:")
    print("-" * 40)
    
    target_range = (1800, 2500)  # Typical IGCSE range
    if target_range[0] <= total_words <= target_range[1]:
        print(f"✅ Word count: {total_words} (WITHIN target range {target_range[0]}-{target_range[1]})")
    elif total_words < target_range[0]:
        shortage = target_range[0] - total_words
        print(f"⚠️  Word count: {total_words} (BELOW target by {shortage} words)")
    else:
        excess = total_words - target_range[1]
        print(f"⚠️  Word count: {total_words} (ABOVE target by {excess} words)")
    
    # Section recommendations
    print("\n💡 Section Analysis & Recommendations:")
    print("-" * 40)
    
    recommendations = {
        "Introduction": (200, 400),
        "Methodology": (150, 300),
        "Data Presentation & Analysis": (800, 1200),
        "Conclusion": (150, 250),
        "Evaluation": (200, 350),
    }
    
    for section, (min_words, max_words) in recommendations.items():
        if section in section_counts:
            current = section_counts[section]
            if min_words <= current <= max_words:
                status = "✅ Good"
            elif current < min_words:
                status = f"📈 Expand (+{min_words - current})"
            else:
                status = f"✂️  Trim (-{current - max_words})"
            
            print(f"{section:<25} │ {current:>4} │ Target: {min_words}-{max_words} │ {status}")
    
    # Percentage breakdown
    print("\n📊 Section Distribution:")
    print("-" * 40)
    
    for section_name, word_count in section_counts.items():
        if section_name not in ["Title and Contents", "Bibliography", "Appendix"]:
            percentage = (word_count / total_words * 100) if total_words > 0 else 0
            print(f"{section_name:<25} │ {percentage:5.1f}% of total")
    
    return section_counts, total_words

def main():
    """Main function to analyze Donald's coursework"""
    
    # Try different possible file locations
    possible_files = [
        "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo/SampleAssignments/DonaldDraftLatest.md",
        "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo/DraftDonaldWong.md",
        "/Users/simonwang/Documents/Usage/VibeCodingMac/DailyAssistant/projects/Donald/Geo/shortenManuscript/current.md"
    ]
    
    file_found = False
    
    for file_path in possible_files:
        if os.path.exists(file_path):
            print(f"📄 Found file: {file_path}")
            analyze_manuscript_sections(file_path)
            file_found = True
            print("\n" + "=" * 60)
            break
    
    if not file_found:
        print("❌ No manuscript files found in expected locations:")
        for path in possible_files:
            print(f"   • {path}")
        print("\n💡 Please check file paths or run from the correct directory.")

if __name__ == "__main__":
    main()