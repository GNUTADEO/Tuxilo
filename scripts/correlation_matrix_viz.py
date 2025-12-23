import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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
df = df.sort_values('Fecha')

# Month names
months = ['January', 'February', 'March', 'April', 'May', 'June', 
          'July', 'August', 'September', 'October', 'November', 'December']

# Create a figure with subplots for each month
fig, axes = plt.subplots(4, 3, figsize=(20, 24))
fig.suptitle('Correlation Matrices by Month\n(Independent: ONI, TSM | Dependent: Precipitation, Caudal)', 
             fontsize=16, fontweight='bold', y=0.995)

axes = axes.flatten()

# Variables for correlation
corr_cols = ['ONI', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes', 'Precipitacion', 'Caudal']
var_labels = ['ONI', 'TSM\nCalida', 'TSM\nFria', 'Anomalias\nAportes', 'Precipitacion\n(x10.5)', 'Caudal']

for month_num in range(1, 13):
    ax = axes[month_num - 1]
    month_data = df[df['Month'] == month_num].copy()
    
    month_subset = month_data[corr_cols].dropna()
    
    if len(month_subset) > 1:
        # Calculate correlation matrix
        corr_matrix = month_subset.corr()
        
        # Create heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', 
                    center=0, vmin=-1, vmax=1, 
                    square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                    ax=ax, xticklabels=var_labels, yticklabels=var_labels)
        
        ax.set_title(f'{months[month_num-1]} (n={len(month_subset)})', 
                     fontsize=12, fontweight='bold', pad=10)
    else:
        ax.text(0.5, 0.5, f'{months[month_num-1]}\nInsufficient data', 
                ha='center', va='center', fontsize=12, transform=ax.transAxes)
        ax.axis('off')

plt.tight_layout()
plt.savefig('results/correlation_matrices_monthly.png', dpi=300, bbox_inches='tight')
print("Saved: results/correlation_matrices_monthly.png")

# Create overall correlation matrix
fig2, ax2 = plt.subplots(figsize=(10, 8))
overall_data = df[corr_cols].dropna()
overall_corr = overall_data.corr()

sns.heatmap(overall_corr, annot=True, fmt='.2f', cmap='RdBu_r', 
            center=0, vmin=-1, vmax=1, 
            square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
            ax=ax2, xticklabels=var_labels, yticklabels=var_labels)

ax2.set_title(f'Overall Correlation Matrix (All Months)\nn={len(overall_data)} observations', 
              fontsize=14, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('results/correlation_matrix_overall.png', dpi=300, bbox_inches='tight')
print("Saved: results/correlation_matrix_overall.png")

# Create focused view on dependent variables
fig3, axes3 = plt.subplots(2, 6, figsize=(24, 10))
fig3.suptitle('Correlations with Dependent Variables by Month', 
              fontsize=14, fontweight='bold', y=0.98)

independent_vars = ['ONI', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes']
independent_labels = ['ONI', 'TSM Calida', 'TSM Fria', 'Anomalias Aportes']

for month_num in range(1, 13):
    month_data = df[df['Month'] == month_num].copy()
    month_subset = month_data[corr_cols].dropna()
    
    row = (month_num - 1) // 6
    col = (month_num - 1) % 6
    
    if len(month_subset) > 1:
        corr_matrix = month_subset.corr()
        
        # Precipitation correlations
        precip_corr = [corr_matrix.loc[var, 'Precipitacion'] for var in independent_vars]
        ax1 = axes3[0, col]
        colors = ['red' if x < 0 else 'green' for x in precip_corr]
        ax1.bar(range(len(precip_corr)), precip_corr, color=colors, alpha=0.7)
        ax1.set_ylim(-1, 1)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax1.set_xticks(range(len(independent_vars)))
        ax1.set_xticklabels(independent_labels, rotation=45, ha='right', fontsize=8)
        ax1.set_title(months[month_num-1][:3], fontsize=10, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        if col == 0:
            ax1.set_ylabel('Correlation with\nPrecipitation', fontsize=10, fontweight='bold')
        
        # Caudal correlations
        caudal_corr = [corr_matrix.loc[var, 'Caudal'] for var in independent_vars]
        ax2 = axes3[1, col]
        colors = ['red' if x < 0 else 'green' for x in caudal_corr]
        ax2.bar(range(len(caudal_corr)), caudal_corr, color=colors, alpha=0.7)
        ax2.set_ylim(-1, 1)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax2.set_xticks(range(len(independent_vars)))
        ax2.set_xticklabels(independent_labels, rotation=45, ha='right', fontsize=8)
        ax2.grid(axis='y', alpha=0.3)
        if col == 0:
            ax2.set_ylabel('Correlation with\nCaudal', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('results/correlation_dependent_vars_monthly.png', dpi=300, bbox_inches='tight')
print("Saved: results/correlation_dependent_vars_monthly.png")

print("\n" + "="*60)
print("All correlation matrix visualizations generated successfully!")
print("="*60)
