#!/usr/bin/env python3
"""
Script to clean CSV files by removing problematic comma patterns.
Handles both backslash-comma and comma-space issues in river names.
"""

import sys
import csv
from pathlib import Path

def clean_csv_file(input_file, output_file=None):
    """
    Clean CSV file by:
    1. Removing backslash-comma sequences (\\,)
    2. Fixing river names like 'SAN JUAN, RIO' -> 'SAN JUAN RIO'
    """
    
    if output_file is None:
        output_file = input_file
    
    # Read all lines
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    fixes_count = 0
    
    for line in lines:
        original = line
        
        # Remove backslash-comma sequences
        line = line.replace('\\,', '')
        
        # Fix patterns like "SAN JUAN, RIO" where comma-space creates extra column
        # Pattern: word(s), RIO -> word(s) RIO (remove comma-space before RIO)
        line = line.replace(', RIO,', ' RIO,')
        
        if line != original:
            fixes_count += 1
        
        cleaned_lines.append(line)
    
    # Write cleaned content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)
    
    print(f"Cleaned '{input_file}'")
    print(f"Fixed {fixes_count} line(s)")

if __name__ == '__main__':
    # Default path to caudal_stations.csv
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_file = repo_root / 'data' / 'Caudal' / 'caudal_stations.csv'
    
    if len(sys.argv) > 1:
        csv_file = Path(sys.argv[1])
    
    if not csv_file.exists():
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    
    clean_csv_file(csv_file)
