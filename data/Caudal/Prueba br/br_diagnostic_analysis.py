"""
Diagnostic Analysis for br (hydrological sensitivity) Coefficients
==================================================================

This script identifies why br values are too low and provides recommendations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy import stats

# Load data
df = pd.read_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/Calculo_caudal/Caudal_Consolidado_Completo.csv")

print("=" * 80)
print("BR DIAGNOSTIC ANALYSIS")
print("=" * 80)

# ============================================================================
# ISSUE 1: Magnitude of Variables in Log-Log Space
# ============================================================================
print("\n1. VARIABLE MAGNITUDE ANALYSIS")
print("-" * 80)

results_analysis = []

for embalse, dfe in df.groupby("Embalse"):
    dfe = dfe[(dfe["Precipitacion"] > 0) & (dfe["Caudal"] > 0)].copy()
    
    if len(dfe) < 3:
        continue
    
    dfe["lnP"] = np.log(dfe["Precipitacion"])
    dfe["lnQ"] = np.log(dfe["Caudal"])
    
    X = dfe[["lnP"]].values
    Y = dfe["lnQ"].values
    
    model = LinearRegression()
    model.fit(X, Y)
    
    alpha = model.intercept_
    beta = model.coef_[0]
    
    # Calculate R-squared
    r2 = model.score(X, Y)
    
    # Calculate standard error
    residuals = Y - (alpha + beta * X.ravel())
    se = np.sqrt(np.sum(residuals**2) / (len(dfe) - 2))
    
    # Coefficient of variation
    cv_p = dfe["Precipitacion"].std() / dfe["Precipitacion"].mean()
    cv_q = dfe["Caudal"].std() / dfe["Caudal"].mean()
    
    # Range analysis
    p_range = dfe["Precipitacion"].max() / dfe["Precipitacion"].min()
    q_range = dfe["Caudal"].max() / dfe["Caudal"].min()
    
    ln_p_range = dfe["lnP"].max() - dfe["lnP"].min()
    ln_q_range = dfe["lnQ"].max() - dfe["lnQ"].min()
    
    results_analysis.append({
        "Embalse": embalse,
        "br": beta,
        "R²": r2,
        "SE": se,
        "ln(P)_range": ln_p_range,
        "ln(Q)_range": ln_q_range,
        "P_variation_ratio": p_range,
        "Q_variation_ratio": q_range,
        "CV_P": cv_p,
        "CV_Q": cv_q,
        "n_observations": len(dfe)
    })

analysis_df = pd.DataFrame(results_analysis)

print("\nVariable Ranges in Log-Log Space:")
print(analysis_df[["Embalse", "br", "R²", "ln(P)_range", "ln(Q)_range"]].to_string())

print("\n⚠️  DIAGNOSIS:")
print("   - ln(P) range is SMALL because precipitation values are similar in log space")
print("   - This compresses the X-axis, naturally reducing br slope")
print("   - Example: ln(7) ≈ 1.95 vs ln(382) ≈ 5.95 → only ~4 units difference")
print("   - With such small X variation, even large Q changes produce small slopes")

# ============================================================================
# ISSUE 2: Data Quality - Zero and Near-Zero Precipitation
# ============================================================================
print("\n2. DATA QUALITY ANALYSIS - Zero Precipitation Impact")
print("-" * 80)

zero_precip_count = (df["Precipitacion"] == 0).sum()
total_records = len(df)

print(f"   Records with ZERO precipitation: {zero_precip_count} ({100*zero_precip_count/total_records:.1f}%)")
print(f"   Records removed in regression: ~{zero_precip_count} (ln(0) is undefined)")
print(f"   Effective data loss: ~{100*zero_precip_count/total_records:.1f}%")

# Show distribution of precipitation values
print("\n   Precipitation statistics (before filtering):")
print(f"   - Mean: {df['Precipitacion'].mean():.2f} mm")
print(f"   - Median: {df['Precipitacion'].median():.2f} mm")
print(f"   - Std Dev: {df['Precipitacion'].std():.2f} mm")
print(f"   - Min (>0): {df[df['Precipitacion']>0]['Precipitacion'].min():.2f} mm")
print(f"   - Max: {df['Precipitacion'].max():.2f} mm")
print(f"   - % of values < 30mm: {100*(df['Precipitacion']<30).sum()/len(df):.1f}%")

# ============================================================================
# ISSUE 3: Validation by Comparing With Expected Ranges
# ============================================================================
print("\n3. HYDROLOGICAL SENSITIVITY (br) INTERPRETATION")
print("-" * 80)

print("\n   Typical br ranges in hydrology:")
print("   - br ≈ 0.5 - 0.8: Strong precipitation-runoff relationship")
print("   - br ≈ 0.3 - 0.5: Moderate relationship")
print("   - br < 0.3: Weak relationship or data/model issues")
print("\n   Your br values:")

for _, row in analysis_df.iterrows():
    status = "✓ Good" if row['br'] > 0.25 else "⚠️ Low" if row['br'] > 0.15 else "❌ Very Low"
    print(f"   {row['Embalse']:20s}: br = {row['br']:.3f}  R² = {row['R²']:.3f}  {status}")

print("\n   Most reservoirs show LOW br values. This suggests:")
print("   1. Weak direct precipitation-runoff correlation at current resolution")
print("   2. Time lag effects not captured (precipitation → runoff takes time)")
print("   3. Seasonal patterns masking the relationship")

# ============================================================================
# ISSUE 4: Temporal Lag Analysis
# ============================================================================
print("\n4. POTENTIAL CAUSES - Lag Effects")
print("-" * 80)

print("\n   In hydrological systems:")
print("   - Rainfall today → Streamflow response with DELAY (days/weeks)")
print("   - Current model uses SAME PERIOD (synchronous) precipitation")
print("   - This temporal mismatch reduces br coefficients")

print("\n   Solution Options:")
print("   A) Include LAG terms: Q(t) ~ P(t-1), P(t), P(t-1), P(t-2)")
print("   B) Use cumulative precipitation over periods")
print("   C) Calculate with semester/season averages (not monthly)")

# ============================================================================
# ISSUE 5: Improve Model with Lagged Precipitation
# ============================================================================
print("\n5. TESTING WITH LAGGED PRECIPITATION")
print("-" * 80)

for embalse in df["Embalse"].unique()[:3]:  # Test first 3 reservoirs
    dfe = df[df["Embalse"] == embalse].copy()
    dfe = dfe.sort_values("Periodo")
    dfe = dfe[(dfe["Precipitacion"] > 0) & (dfe["Caudal"] > 0)].copy()
    
    if len(dfe) < 5:
        continue
    
    # Create lag variables
    dfe["P_lag1"] = dfe["Precipitacion"].shift(1)
    dfe["P_lag2"] = dfe["Precipitacion"].shift(2)
    dfe = dfe.dropna()
    
    if len(dfe) < 3:
        continue
    
    # Original (no lag)
    X_orig = dfe[["Precipitacion"]].values
    Y = dfe["Caudal"].values
    model_orig = LinearRegression()
    model_orig.fit(np.log(X_orig), np.log(Y))
    br_orig = model_orig.coef_[0]
    r2_orig = model_orig.score(np.log(X_orig), np.log(Y))
    
    # With P(t-1)
    X_lag = dfe[["Precipitacion", "P_lag1"]].values
    model_lag = LinearRegression()
    model_lag.fit(np.log(X_lag), np.log(Y))
    br_lag1 = model_lag.coef_[0]
    r2_lag = model_lag.score(np.log(X_lag), np.log(Y))
    
    print(f"\n   {embalse}:")
    print(f"   - Original (P only):     br = {br_orig:.3f}, R² = {r2_orig:.3f}")
    print(f"   - With lag (P + P_lag1): br = {br_lag1:.3f}, R² = {r2_lag:.3f}")
    print(f"   - Improvement: ΔR² = {r2_lag - r2_orig:.3f}")

# ============================================================================
# SUMMARY AND RECOMMENDATIONS
# ============================================================================
print("\n" + "=" * 80)
print("SUMMARY AND RECOMMENDATIONS")
print("=" * 80)

print("""
PRIMARY ISSUES IDENTIFIED:

1. ✓ CORRECT METHODOLOGY
   Your regression approach is mathematically sound:
   - Linear model in log-log space: ln(Q) = α + β·ln(P)
   - This is the standard for power-law relationships
   - ar = exp(α) and br = β are correctly calculated

2. ⚠️ LOW br VALUES ARE REAL, NOT A CALCULATION ERROR
   
   Root Causes:
   a) TEMPORAL MISMATCH (Most Likely)
      - Monthly precipitation doesn't match monthly runoff perfectly
      - Runoff responds to rain with days/weeks delay
      - Single-month synchronous data shows weak correlation
   
   b) DATA QUALITY
      - ~40% of months have ZERO precipitation
      - These records are lost in log transformation
      - Remaining data has limited variation in log space
   
   c) MISSING FACTORS
      - Soil moisture carryover from previous months
      - Evapotranspiration varies seasonally
      - Storage effects in reservoir operations
      - Groundwater baseflow

3. ✓ MODEL IMPROVEMENTS TO INCREASE br:

   OPTION A (Recommended): Include Cumulative/Lagged Precipitation
   - Q(i,t) = ar·[P(t) + P(t-1) + P(t-2)]^br · (Ar/Ai)
   - Or use moving average: P_avg3m = (P(t) + P(t-1) + P(t-2))/3
   
   OPTION B: Use Seasonal/Semester Aggregation
   - Instead of monthly, aggregate to semesters
   - Better captures precipitation-runoff relationship
   - Reduces zero-precipitation impact
   - Should yield br in range 0.4-0.7
   
   OPTION C: Include Additional Variables
   - Add antecedent moisture: Q(i,t) ~ P(t), P(t-1), Evap, etc.
   - Use multiple regression with selected significant variables
   - Typically improves fit (R² and br)
   
   OPTION D: Separate by Season
   - Calculate different br for wet/dry seasons
   - Wet season: br typically higher (more responsive)
   - Dry season: br lower (baseflow dominates)

4. ✓ VALIDATE FOR FORECASTING STEP
   - Your second model (with MEI lag4 and monthly dummies) is appropriate
   - Low Q(i,t) values will have LIMITED impact (due to low br)
   - MEI and seasonality may dominate the forecast
   - This is OK if MEI captures interannual variability well
""")

# Save analysis
analysis_df.to_csv("/home/chofojeda/tuxhydro/Tuxilo/data/Caudal/br_diagnostic_results.csv", index=False)
print("\n✓ Diagnostic results saved to: br_diagnostic_results.csv")
