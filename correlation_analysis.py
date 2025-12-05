import pandas as pd
import numpy as np
from pathlib import Path

# Load the data
data_dir = Path('Data/IDEAM')
oni = pd.read_csv(data_dir / 'IndicesONI.csv', parse_dates=['DATE'])
tsm = pd.read_csv(data_dir / 'IndicesTSM.csv', parse_dates=['Fecha'])
precip = pd.read_csv(data_dir / 'ChivorPrecipitacion.csv', parse_dates=['Fecha'])
caudal = pd.read_csv(data_dir / 'LengupaCaudal.csv', parse_dates=['Fecha'])

# Rename columns for consistency
oni.columns = ['Fecha', 'ONI']
tsm.columns = ['Fecha', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes']
precip.columns = ['Fecha', 'Precipitacion']
caudal.columns = ['Fecha', 'Caudal']

# Multiply precipitation by conversion factor
precip['Precipitacion'] = precip['Precipitacion'] * 10.502715

# Merge all datasets
df = oni.merge(tsm, on='Fecha', how='outer')
df = df.merge(precip, on='Fecha', how='outer')
df = df.merge(caudal, on='Fecha', how='outer')

# Extract month from date
df['Month'] = pd.to_datetime(df['Fecha']).dt.month

# Sort by date
df = df.sort_values('Fecha')

# Create correlation matrices for each month
months = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']

print("=" * 80)
print("CORRELATION MATRICES BY MONTH")
print("=" * 80)
print("\nIndependent Variables: ONI, TSM_Calida, TSM_Fria, Anomalias_Aportes")
print("Dependent Variables: Precipitacion (scaled by 10.502715), Caudal")
print("=" * 80)

for month_num in range(1, 13):
    month_data = df[df['Month'] == month_num].copy()
    
    if len(month_data) > 1:
        # Select relevant columns for correlation
        corr_cols = ['ONI', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes', 'Precipitacion', 'Caudal']
        month_subset = month_data[corr_cols].dropna()
        
        if len(month_subset) > 1:
            print(f"\n{'=' * 80}")
            print(f"Month: {months[month_num-1]} (n={len(month_subset)} observations)")
            print(f"{'=' * 80}")
            
            # Calculate correlation matrix
            corr_matrix = month_subset.corr()
            
            # Display full correlation matrix
            print("\nFull Correlation Matrix:")
            print(corr_matrix.round(3))
            
            # Highlight correlations with dependent variables
            print(f"\n{'-' * 80}")
            print("Correlations with Precipitacion (dependent):")
            print(f"{'-' * 80}")
            precip_corr = corr_matrix['Precipitacion'].drop('Precipitacion')
            for var, corr in precip_corr.items():
                print(f"  {var:25s}: {corr:7.3f}")
            
            print(f"\n{'-' * 80}")
            print("Correlations with Caudal (dependent):")
            print(f"{'-' * 80}")
            caudal_corr = corr_matrix['Caudal'].drop('Caudal')
            for var, corr in caudal_corr.items():
                print(f"  {var:25s}: {corr:7.3f}")

# Summary statistics
print("\n\n" + "=" * 80)
print("OVERALL SUMMARY (All months combined)")
print("=" * 80)

# Select relevant columns
summary_cols = ['ONI', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes', 'Precipitacion', 'Caudal']
overall_data = df[summary_cols].dropna()

print(f"\nTotal observations: {len(overall_data)}")
print("\nOverall Correlation Matrix:")
overall_corr = overall_data.corr()
print(overall_corr.round(3))

print(f"\n{'-' * 80}")
print("Overall Correlations with Precipitacion (dependent):")
print(f"{'-' * 80}")
precip_corr_overall = overall_corr['Precipitacion'].drop('Precipitacion')
for var, corr in precip_corr_overall.items():
    print(f"  {var:25s}: {corr:7.3f}")

print(f"\n{'-' * 80}")
print("Overall Correlations with Caudal (dependent):")
print(f"{'-' * 80}")
caudal_corr_overall = overall_corr['Caudal'].drop('Caudal')
for var, corr in caudal_corr_overall.items():
    print(f"  {var:25s}: {corr:7.3f}")

print("\n" + "=" * 80)
print("Analysis complete!")
print("=" * 80)
