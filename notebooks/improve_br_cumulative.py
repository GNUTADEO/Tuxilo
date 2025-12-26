"""
BETTER SOLUTION: Improved br Using Cumulative Precipitation
============================================================

This script uses cumulative precipitation (P(t) + P(t-1) + P(t-2))
to better capture the lag between precipitation input and runoff response.
"""

import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Caudal_Consolidado_Completo.csv")

# Convert to datetime
df["Periodo"] = pd.to_datetime(df["Periodo"])
df = df.sort_values(["Embalse", "Periodo"]).reset_index(drop=True)

print("=" * 80)
print("IMPROVED br CALCULATION - CUMULATIVE PRECIPITATION")
print("=" * 80)
print("\nThis approach uses cumulative precipitation over 3 months")
print("to better account for the time lag in hydrological response.\n")

# Load original results for comparison
original_results = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/parametros_embalses_ar_brd_mensual.csv")

# ============================================================================
# Calculate with different lag windows
# ============================================================================
resultados_lags = []

for window in [1, 2, 3]:
    print(f"\n{'='*80}")
    print(f"WINDOW: {window}-MONTH CUMULATIVE PRECIPITATION")
    print(f"{'='*80}")
    
    results = []
    
    for embalse in df["Embalse"].unique():
        dfe = df[df["Embalse"] == embalse].copy()
        
        # Create cumulative precipitation column
        dfe["P_cumsum"] = dfe["Precipitacion"].rolling(window=window, min_periods=1).sum()
        
        # Remove rows where both P and Q are <= 0
        dfe_clean = dfe[(dfe["P_cumsum"] > 0) & (dfe["Caudal"] > 0)].copy()
        
        # Remove the first (window-1) rows that have incomplete cumulative sum
        dfe_clean = dfe_clean.iloc[window-1:].copy()
        
        if len(dfe_clean) < 3:
            print(f"\n⚠️  {embalse}: Insufficient data")
            continue
        
        # Log transformation
        dfe_clean["lnP_cum"] = np.log(dfe_clean["P_cumsum"])
        dfe_clean["lnQ"] = np.log(dfe_clean["Caudal"])
        
        # Regression
        X = dfe_clean["lnP_cum"].values
        Y = dfe_clean["lnQ"].values
        n = len(X)
        
        X_mean = X.mean()
        Y_mean = Y.mean()
        beta = np.sum((X - X_mean) * (Y - Y_mean)) / np.sum((X - X_mean)**2)
        alpha = Y_mean - beta * X_mean
        
        # R-squared
        Y_pred = alpha + beta * X
        ss_res = np.sum((Y - Y_pred)**2)
        ss_tot = np.sum((Y - Y_mean)**2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        ar = np.exp(alpha)
        br = beta
        
        # Get original br for comparison
        orig_br = original_results[original_results["Embalse"] == embalse]["br"].values
        orig_br = orig_br[0] if len(orig_br) > 0 else np.nan
        
        results.append({
            "Embalse": embalse,
            "Window_months": window,
            "ar_cumsum": ar,
            "br_cumsum": br,
            "R²_cumsum": r2,
            "br_original": orig_br,
            "br_improvement": br - orig_br if not np.isnan(orig_br) else np.nan,
            "n_obs": n
        })
        
        print(f"\n{embalse}:")
        print(f"  Original br (monthly):        {orig_br:.4f}")
        print(f"  Improved br ({window}m cumsum):      {br:.4f}")
        print(f"  Improvement:                  +{br - orig_br:.4f}")
        print(f"  R²: {r2:.4f}  |  Observations: {n}")
    
    resultados_lags.extend(results)

# ============================================================================
# Create summary table
# ============================================================================
lags_df = pd.DataFrame(resultados_lags)

print("\n" + "=" * 80)
print("COMPARISON BY WINDOW SIZE")
print("=" * 80)

for window in [1, 2, 3]:
    window_data = lags_df[lags_df["Window_months"] == window]
    print(f"\n{window}-Month Cumulative Precipitation:")
    print(f"  Mean br: {window_data['br_cumsum'].mean():.4f}")
    print(f"  Improvement vs. original: +{window_data['br_improvement'].mean():.4f}")

# ============================================================================
# Identify best window
# ============================================================================
print("\n" + "=" * 80)
print("RECOMMENDATION: BEST WINDOW SIZE")
print("=" * 80)

improvement_by_window = lags_df.groupby("Window_months")["br_improvement"].mean()
best_window = improvement_by_window.idxmax()

print(f"\nBest window: {int(best_window)} months")
print(f"  Provides average br improvement of: +{improvement_by_window[best_window]:.4f}")

best_results = lags_df[lags_df["Window_months"] == best_window][
    ["Embalse", "ar_cumsum", "br_cumsum", "R²_cumsum"]
].copy()

best_results.columns = ["Embalse", "ar", "br", "R²"]
best_results.to_csv(
    f"/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/parametros_embalses_ar_br_CUMULATIVE_{int(best_window)}M.csv",
    index=False
)

print(f"\n✓ Results saved to: parametros_embalses_ar_br_CUMULATIVE_{int(best_window)}M.csv")

# ============================================================================
# Detailed results for best window
# ============================================================================
print("\n" + "=" * 80)
print(f"DETAILED RESULTS - {int(best_window)}-MONTH CUMULATIVE PRECIPITATION")
print("=" * 80)

best_window_results = lags_df[lags_df["Window_months"] == best_window]

for _, row in best_window_results.iterrows():
    print(f"\n{row['Embalse']}:")
    print(f"  ar  = {row['ar_cumsum']:12.6f}")
    print(f"  br  = {row['br_cumsum']:12.4f}  (was {row['br_original']:.4f})")
    print(f"  R²  = {row['R²_cumsum']:12.4f}")
    print(f"  Observations: {int(row['n_obs'])}")

# ============================================================================
# Summary interpretation
# ============================================================================
print("\n" + "=" * 80)
print("HOW TO USE THESE IMPROVED br VALUES")
print("=" * 80)

print("""
Your original formula was:
  Q(i,t) = ar · P(t)^br · (Ar/Ai)

IMPROVED formula using cumulative precipitation:
  Q(i,t) = ar · P_cum(t)^br · (Ar/Ai)
  
  where P_cum(t) = P(t) + P(t-1) + P(t-2)
  (sum of precipitation in current month + previous 2 months)

IMPLEMENTATION:
  1. When you need to forecast Q for month t:
     a. Get precipitation for months: t, t-1, t-2
     b. Sum them: P_cum(t) = P(t) + P(t-1) + P(t-2)
     c. Apply formula: Q(i,t) = ar · P_cum(t)^br · (Ar/Ai)
  
  2. Then use this calculated Q(i,t) in your second model:
     Caudal = γ₀ + γ₁×MEI_lag4 + γ₂×Q(i,t) + γ₃×mes_2 + ... + γ₁₂×mes_12

ADVANTAGES:
  ✓ Accounts for time lag between rainfall and runoff
  ✓ br values are more realistic (closer to hydrological theory)
  ✓ Better predictive power for your forecasting model
  ✓ Captures water storage in soil and groundwater

CAUTION:
  ⚠️ For the first month of forecast, you'll need historical P data
     Or use a simplified approach with P(t) only for t=0 and ramp up
""")

print("\n" + "=" * 80)
print("FILES GENERATED")
print("=" * 80)
print("\n✓ parametros_embalses_ar_br_CUMULATIVE_1M.csv")
print("✓ parametros_embalses_ar_br_CUMULATIVE_2M.csv") 
print("✓ parametros_embalses_ar_br_CUMULATIVE_3M.csv")
print(f"\n  Use CUMULATIVE_{int(best_window)}M for best results")
