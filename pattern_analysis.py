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

# Rename columns for consistency
oni.columns = ['Fecha', 'ONI']
tsm.columns = ['Fecha', 'TSM_Calida', 'TSM_Fria', 'Anomalias_Aportes']
precip.columns = ['Fecha', 'Precipitacion']

# Merge all datasets
df = oni.merge(tsm, on='Fecha', how='outer')
df = df.merge(precip, on='Fecha', how='outer')
df = df.sort_values('Fecha').reset_index(drop=True)

# Convert dates
df['Fecha'] = pd.to_datetime(df['Fecha'])
df['Year'] = df['Fecha'].dt.year
df['Month'] = df['Fecha'].dt.month

# Classify phenomenon
def classify_phenomenon(row):
    oni_val = row['ONI']
    tsm_calida = row['TSM_Calida']
    tsm_fria = row['TSM_Fria']
    
    if oni_val < 0 and tsm_fria < 0:
        return 'La Niña'
    elif oni_val > 0 and tsm_calida > 0:
        return 'El Niño'
    else:
        return 'Neutral'

df['Fenomeno'] = df.apply(classify_phenomenon, axis=1)

# Create comprehensive visualization
fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(5, 2, hspace=0.4, wspace=0.3)

# Color mapping for phenomena
color_map = {'La Niña': '#3498db', 'El Niño': '#e74c3c', 'Neutral': '#95a5a6'}

# 1. Time series of all variables
ax1 = fig.add_subplot(gs[0, :])
ax1_twin = ax1.twinx()

# Plot precipitation on primary axis
ax1.plot(df['Fecha'], df['Precipitacion'], color='#2c3e50', linewidth=2, 
         label='Precipitación', marker='o', markersize=4)
ax1.set_ylabel('Precipitación (mm)', fontweight='bold', fontsize=11, color='#2c3e50')
ax1.tick_params(axis='y', labelcolor='#2c3e50')
ax1.grid(True, alpha=0.3)

# Plot indices on secondary axis
ax1_twin.plot(df['Fecha'], df['ONI'], color='#e67e22', linewidth=2, 
              label='ONI', marker='s', markersize=3, alpha=0.7)
ax1_twin.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax1_twin.set_ylabel('Índices ONI', fontweight='bold', fontsize=11, color='#e67e22')
ax1_twin.tick_params(axis='y', labelcolor='#e67e22')

# Add phenomenon background
for idx, row in df.iterrows():
    color = color_map[row['Fenomeno']]
    ax1.axvspan(row['Fecha'], row['Fecha'] + pd.Timedelta(days=30), 
                alpha=0.15, color=color, zorder=0)

ax1.set_xlabel('Fecha', fontweight='bold', fontsize=11)
ax1.set_title('Serie Temporal: Precipitación e Índice ONI', 
              fontweight='bold', fontsize=13, pad=10)
ax1.legend(loc='upper left')
ax1_twin.legend(loc='upper right')

# 2. TSM indices and precipitation
ax2 = fig.add_subplot(gs[1, :])
ax2_twin = ax2.twinx()

ax2.plot(df['Fecha'], df['Precipitacion'], color='#2c3e50', linewidth=2, 
         label='Precipitación', marker='o', markersize=4)
ax2.set_ylabel('Precipitación (mm)', fontweight='bold', fontsize=11, color='#2c3e50')
ax2.tick_params(axis='y', labelcolor='#2c3e50')
ax2.grid(True, alpha=0.3)

ax2_twin.plot(df['Fecha'], df['TSM_Calida'], color='#e74c3c', linewidth=2, 
              label='TSM Cálida', marker='^', markersize=3, alpha=0.7)
ax2_twin.plot(df['Fecha'], df['TSM_Fria'], color='#3498db', linewidth=2, 
              label='TSM Fría', marker='v', markersize=3, alpha=0.7)
ax2_twin.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax2_twin.set_ylabel('Índices TSM (°C)', fontweight='bold', fontsize=11)

ax2.set_xlabel('Fecha', fontweight='bold', fontsize=11)
ax2.set_title('Serie Temporal: Precipitación e Índices TSM', 
              fontweight='bold', fontsize=13, pad=10)
ax2.legend(loc='upper left')
ax2_twin.legend(loc='upper right')

# 3. Scatter: ONI vs Precipitation
ax3 = fig.add_subplot(gs[2, 0])
for fenomeno in ['La Niña', 'El Niño', 'Neutral']:
    data = df[df['Fenomeno'] == fenomeno]
    ax3.scatter(data['ONI'], data['Precipitacion'], 
                c=color_map[fenomeno], label=fenomeno, s=80, alpha=0.6, edgecolors='black', linewidth=0.5)

# Add trend line
valid_data = df[['ONI', 'Precipitacion']].dropna()
z = np.polyfit(valid_data['ONI'], valid_data['Precipitacion'], 1)
p = np.poly1d(z)
x_line = np.linspace(valid_data['ONI'].min(), valid_data['ONI'].max(), 100)
ax3.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label=f'Tendencia: y={z[0]:.1f}x+{z[1]:.1f}')

# Calculate correlation
corr = valid_data['ONI'].corr(valid_data['Precipitacion'])
ax3.text(0.05, 0.95, f'Correlación: {corr:.3f}', transform=ax3.transAxes, 
         fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax3.set_xlabel('Índice ONI', fontweight='bold', fontsize=11)
ax3.set_ylabel('Precipitación (mm)', fontweight='bold', fontsize=11)
ax3.set_title('Relación: ONI vs Precipitación', fontweight='bold', fontsize=12)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Scatter: TSM vs Precipitation
ax4 = fig.add_subplot(gs[2, 1])

# Create TSM index (use Calida when positive ONI, Fria when negative)
df['TSM_Dominante'] = df.apply(lambda row: row['TSM_Calida'] if row['ONI'] > 0 else row['TSM_Fria'], axis=1)

for fenomeno in ['La Niña', 'El Niño', 'Neutral']:
    data = df[df['Fenomeno'] == fenomeno]
    ax4.scatter(data['TSM_Dominante'], data['Precipitacion'], 
                c=color_map[fenomeno], label=fenomeno, s=80, alpha=0.6, edgecolors='black', linewidth=0.5)

# Add trend line
valid_data2 = df[['TSM_Dominante', 'Precipitacion']].dropna()
z2 = np.polyfit(valid_data2['TSM_Dominante'], valid_data2['Precipitacion'], 1)
p2 = np.poly1d(z2)
x_line2 = np.linspace(valid_data2['TSM_Dominante'].min(), valid_data2['TSM_Dominante'].max(), 100)
ax4.plot(x_line2, p2(x_line2), "r--", alpha=0.8, linewidth=2, label=f'Tendencia: y={z2[0]:.1f}x+{z2[1]:.1f}')

corr2 = valid_data2['TSM_Dominante'].corr(valid_data2['Precipitacion'])
ax4.text(0.05, 0.95, f'Correlación: {corr2:.3f}', transform=ax4.transAxes, 
         fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

ax4.set_xlabel('TSM Dominante (°C)', fontweight='bold', fontsize=11)
ax4.set_ylabel('Precipitación (mm)', fontweight='bold', fontsize=11)
ax4.set_title('Relación: TSM vs Precipitación', fontweight='bold', fontsize=12)
ax4.legend()
ax4.grid(True, alpha=0.3)

# 5. Monthly pattern analysis
ax5 = fig.add_subplot(gs[3, 0])
monthly_precip = df.groupby('Month')['Precipitacion'].mean()
monthly_oni = df.groupby('Month')['ONI'].mean()

ax5_twin = ax5.twinx()

months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
x_pos = np.arange(1, 13)

bars = ax5.bar(x_pos, monthly_precip.values, alpha=0.7, color='#3498db', label='Precipitación Media')
ax5.set_xlabel('Mes', fontweight='bold', fontsize=11)
ax5.set_ylabel('Precipitación Media (mm)', fontweight='bold', fontsize=11, color='#3498db')
ax5.tick_params(axis='y', labelcolor='#3498db')
ax5.set_xticks(x_pos)
ax5.set_xticklabels(months, rotation=45)

line = ax5_twin.plot(x_pos, monthly_oni.values, color='#e74c3c', marker='o', 
                     linewidth=2, markersize=8, label='ONI Medio')
ax5_twin.set_ylabel('ONI Medio', fontweight='bold', fontsize=11, color='#e74c3c')
ax5_twin.tick_params(axis='y', labelcolor='#e74c3c')
ax5_twin.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

ax5.set_title('Patrón Mensual: Precipitación y ONI', fontweight='bold', fontsize=12)
ax5.legend(loc='upper left')
ax5_twin.legend(loc='upper right')
ax5.grid(True, alpha=0.3, axis='y')

# 6. Precipitation by phenomenon
ax6 = fig.add_subplot(gs[3, 1])
fenomeno_precip = df.groupby('Fenomeno')['Precipitacion'].agg(['mean', 'std', 'count'])

colors_box = [color_map[f] for f in ['La Niña', 'El Niño', 'Neutral']]
bp = ax6.boxplot([df[df['Fenomeno'] == 'La Niña']['Precipitacion'].dropna(),
                   df[df['Fenomeno'] == 'El Niño']['Precipitacion'].dropna(),
                   df[df['Fenomeno'] == 'Neutral']['Precipitacion'].dropna()],
                  labels=['La Niña', 'El Niño', 'Neutral'],
                  patch_artist=True, notch=True, showmeans=True)

for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax6.set_ylabel('Precipitación (mm)', fontweight='bold', fontsize=11)
ax6.set_title('Distribución de Precipitación por Fenómeno', fontweight='bold', fontsize=12)
ax6.grid(True, alpha=0.3, axis='y')

# Add mean values as text
for i, fenomeno in enumerate(['La Niña', 'El Niño', 'Neutral']):
    mean_val = fenomeno_precip.loc[fenomeno, 'mean']
    ax6.text(i+1, mean_val, f'{mean_val:.1f}', ha='center', va='bottom', fontweight='bold')

# 7. Lag correlation analysis
ax7 = fig.add_subplot(gs[4, :])

lags = range(-6, 7)
oni_corrs = []
tsm_corrs = []

for lag in lags:
    if lag < 0:
        oni_shifted = df['ONI'].shift(-lag)
        tsm_shifted = df['TSM_Dominante'].shift(-lag)
    else:
        oni_shifted = df['ONI'].shift(lag)
        tsm_shifted = df['TSM_Dominante'].shift(lag)
    
    oni_corr = df['Precipitacion'].corr(oni_shifted)
    tsm_corr = df['Precipitacion'].corr(tsm_shifted)
    
    oni_corrs.append(oni_corr)
    tsm_corrs.append(tsm_corr)

ax7.bar([l-0.2 for l in lags], oni_corrs, width=0.4, alpha=0.7, color='#e67e22', label='ONI')
ax7.bar([l+0.2 for l in lags], tsm_corrs, width=0.4, alpha=0.7, color='#9b59b6', label='TSM')
ax7.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax7.axvline(x=0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Sin desfase')

ax7.set_xlabel('Desfase (meses) - Negativo: Índices adelantados | Positivo: Índices retrasados', 
               fontweight='bold', fontsize=11)
ax7.set_ylabel('Correlación', fontweight='bold', fontsize=11)
ax7.set_title('Análisis de Correlación con Desfase Temporal (Lag Correlation)', 
              fontweight='bold', fontsize=12)
ax7.legend()
ax7.grid(True, alpha=0.3, axis='y')
ax7.set_xticks(lags)

# Add max correlation annotations
max_oni_idx = np.argmax(np.abs(oni_corrs))
max_tsm_idx = np.argmax(np.abs(tsm_corrs))
ax7.annotate(f'Max ONI: {oni_corrs[max_oni_idx]:.3f}\n(lag={list(lags)[max_oni_idx]})', 
             xy=(list(lags)[max_oni_idx]-0.2, oni_corrs[max_oni_idx]), 
             xytext=(10, 20), textcoords='offset points', 
             bbox=dict(boxstyle='round', facecolor='#e67e22', alpha=0.5),
             arrowprops=dict(arrowstyle='->', color='#e67e22'))

plt.suptitle('Análisis de Patrones y Ciclos: Influencia de Índices ENSO en Precipitación Chivor', 
             fontsize=16, fontweight='bold', y=0.998)

plt.savefig('results/pattern_analysis_precipitation.png', dpi=300, bbox_inches='tight')
print("=" * 80)
print("Gráfico guardado: results/pattern_analysis_precipitation.png")
print("=" * 80)

# Print summary statistics
print("\nRESUMEN DE CORRELACIONES:")
print("-" * 80)
print(f"Correlación ONI vs Precipitación: {corr:.3f}")
print(f"Correlación TSM vs Precipitación: {corr2:.3f}")
print(f"\nMáxima correlación ONI (con desfase): {oni_corrs[max_oni_idx]:.3f} (lag={list(lags)[max_oni_idx]} meses)")
print(f"Máxima correlación TSM (con desfase): {tsm_corrs[max_tsm_idx]:.3f} (lag={list(lags)[max_tsm_idx]} meses)")
print("\nPRECIPITACIÓN MEDIA POR FENÓMENO:")
print("-" * 80)
print(fenomeno_precip)
print("=" * 80)
