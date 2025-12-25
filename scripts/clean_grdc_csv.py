#!/usr/bin/env python3
"""
Script to remove all backslash-comma occurrences from grdc_stations.csv
"""

import sys
from pathlib import Path

def clean_grdc_csv(input_file, output_file=None):
    """Remove all backslash-comma sequences from the CSV file."""
    
    if output_file is None:
        output_file = input_file
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove all '\,' occurrences
    cleaned_content = content.replace('\\,', '')
    
    # Write back to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)
    
    print(f"Cleaned '{input_file}'")
    print(f"Removed all '\\,' sequences")

if __name__ == '__main__':
    # Default path to grdc_stations.csv
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    csv_file = repo_root / 'data' / 'GRDC' / 'grdc_stations.csv'
    
    if len(sys.argv) > 1:
        csv_file = Path(sys.argv[1])
    
    if not csv_file.exists():
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)
    
    clean_grdc_csv(csv_file)
