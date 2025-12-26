"""
RECALIBRATE ar COEFFICIENTS
============================

Since ar values were calculated with wrong area ratio,
we need to recalibrate them using historical data.

Formula: Q(i,t) = ar · P^br · (Ar/Ai)
We'll solve for ar using historical data and fixed br.
"""

import pandas as pd
import numpy as np

# Load data
df_hist = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Caudal_Consolidado.csv")
df_areas = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Areas_hidrologia.csv")
df_param = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Prueba br/RECOMMENDED_BR_VALUES.csv")

# Clean columns
def clean_cols(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

df_hist = clean_cols(df_hist)
df_areas = clean_cols(df_areas)
df_param = clean_cols(df_param)

print("="*80)
print("RECALIBRATING ar COEFFICIENTS")
print("="*80)

# Prepare historical data with cumulative precipitation
df_hist['periodo_dt'] = pd.to_datetime(df_hist['periodo'])
df_hist = df_hist.sort_values(['embalse', 'periodo_dt'])

# Calculate 3-month cumulative precipitation
df_hist['p_cum'] = df_hist.groupby('embalse')['precipitacion'].transform(
    lambda x: x.rolling(window=3, min_periods=1).sum()
)

# Merge with areas
df_hist = df_hist.merge(
    df_areas[['embalse', 'ar_km2', 'ai_km2']],
    on='embalse',
    how='left'
)

# Merge with br values
df_hist = df_hist.merge(
    df_param[['embalse', 'br']],
    on='embalse',
    how='left'
)

# Filter valid data
df_hist = df_hist[
    (df_hist['caudal'] > 0) & 
    (df_hist['p_cum'] > 0) & 
    (df_hist['br'].notna())
].copy()

print("\nRecalibrating ar for each reservoir:\n")

new_ar_values = []

for embalse in df_hist['embalse'].unique():
    subset = df_hist[df_hist['embalse'] == embalse].copy()
    
    if len(subset) < 5:
        print(f"{embalse}: Insufficient data, skipping")
        continue
    
    # Extract parameters
    br = subset['br'].iloc[0]
    ar_area = subset['ar_km2'].iloc[0]
    ai_area = subset['ai_km2'].iloc[0]
    area_ratio = ar_area / ai_area
    
    # Solve for ar using least squares
    # Q = ar · P^br · (Ar/Ai)
    # ar = Q / (P^br · (Ar/Ai))
    
    # Calculate ar for each observation
    ar_observations = subset['caudal'] / (
        np.power(subset['p_cum'], br) * area_ratio
    )
    
    # Use median to minimize outliers
    ar_new = ar_observations.median()
    ar_mean = ar_observations.mean()
    
    # Calculate R² with new ar
    q_pred = ar_new * np.power(subset['p_cum'], br) * area_ratio
    ss_res = np.sum((subset['caudal'] - q_pred)**2)
    ss_tot = np.sum((subset['caudal'] - subset['caudal'].mean())**2)
    r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    
    new_ar_values.append({
        'embalse': embalse,
        'ar_old': df_param[df_param['embalse'] == embalse]['ar'].values[0],
        'ar_new': ar_new,
        'ar_mean': ar_mean,
        'br': br,
        'r2': r2,
        'n_obs': len(subset)
    })
    
    print(f"{embalse}:")
    print(f"  Old ar (wrong):     {ar_observations.iloc[0]:.6f}")
    print(f"  New ar (median):    {ar_new:.6f}")
    print(f"  New ar (mean):      {ar_mean:.6f}")
    print(f"  br:                 {br:.4f}")
    print(f"  R²:                 {r2:.4f}")
    print(f"  Observations:       {len(subset)}")
    
    # Show sample predictions
    sample_idx = subset.sample(min(3, len(subset))).index
    for idx in sample_idx:
        q_obs = subset.loc[idx, 'caudal']
        p = subset.loc[idx, 'p_cum']
        q_pred = ar_new * np.power(p, br) * area_ratio
        error_pct = 100 * (q_pred - q_obs) / q_obs
        print(f"    P={p:6.0f}mm → Q_obs={q_obs:7.1f} Q_pred={q_pred:7.1f} ({error_pct:+6.1f}%)")
    print()

# Create new parameter file
df_new_params = pd.DataFrame(new_ar_values)
df_new_params_out = df_new_params[['embalse', 'ar_new', 'br']].copy()
df_new_params_out.columns = ['Embalse', 'ar', 'br']
df_new_params_out.to_csv(
    "/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/RECALIBRATED_BR_VALUES.csv",
    index=False
)

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

print("\nComparison (old vs new ar):\n")
print(f"{'Embalse':<20} {'ar_old':<15} {'ar_new':<15} {'Ratio':<10} {'R²':<8}")
print("-" * 70)
for _, row in df_new_params.iterrows():
    ratio = row['ar_new'] / row['ar_old']
    print(f"{row['embalse']:<20} {row['ar_old']:<15.6f} {row['ar_new']:<15.6f} {ratio:<10.3f} {row['r2']:<8.4f}")

print("\n✓ New parameters saved to: RECALIBRATED_BR_VALUES.csv")
print("\nThis new file has ar values calibrated against historical data.")
print("It should give Q values that match historical caudal ranges.")

