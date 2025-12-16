# Macro Regimes vs Market Stress  
**Fast Instability Detection vs Slow State Estimation**

## Thesis
Macro regimes and market stress signals operate on different clocks.

Macro data estimates the economic state with structural lag, making it ill-suited for detecting sudden market stress. Market stress indicators react to fast-moving mechanisms such as volatility repricing, correlation breakdown, liquidity withdrawal, and tail-risk amplification.

This project compares the timing, behavior, and failure modes of slow macro regimes versus fast market stress detectors across sudden and prolonged stress episodes. The analysis frames them as **complementary layers in a risk monitoring system**, not alpha-generating strategies.

---

## What This Project Is / Is Not

### IS
- Systems-level risk diagnostics  
- Stress detection vs state estimation  
- Timing, latency, persistence, and failure modes  
- Explainable, rule-based signals  

### IS NOT
- A trading strategy  
- Optimized weights or thresholds  
- A Sharpe-maximization exercise  
- A claim of return improvement  

---

## Market Stress: Conceptual Definition
Market stress is defined as a rapid deterioration in market functioning, characterized by:
- Uncertainty repricing
- Correlation convergence and diversification failure
- Liquidity withdrawal and forced trading
- Nonlinear tail-risk amplification

Stress is a property of the market system, not simply poor returns.

| Mechanism               | Indicator Family | Examples |
|------------------------|------------------|----------|
| Uncertainty repricing   | Volatility       | VIX level, realized volatility |
| Diversification failure | Correlation      | Avg pairwise correlation |
| Disagreement / herding  | Dispersion       | Cross-sectional return dispersion |
| Liquidity stress        | Volume           | Volume anomalies |
| Nonlinearity            | Tails            | Downside tail frequency |

Design rules:
- Indicators must be observable in real time
- No future information or revised data
- No parameter optimization
- Higher values always indicate more stress

---

## Composite Stress Index (CSI)
The Composite Stress Index aggregates fast market stress indicators into a single monitoring construct.

**Design principles**
- Rolling normalization (no hindsight)
- Equal weighting (robustness over optimization)
- Percentile-based regimes (adaptive, not hard-coded)

The CSI is evaluated on **timing, stability, and interpretability**, not returns.

---

## Macro Regimes
Macro regimes are treated as **slow-moving state estimators**:
- Monthly frequency
- Explicit publication lag
- Designed to capture persistence, not onset
- Evaluated on duration alignment, not early warning

Macro regimes are not expected to lead stress events, but to contextualize and validate their persistence.

---

## Evaluation Framework

### Timing & Detection
- Stress onset → signal trigger latency
- Signal trigger → drawdown trough
- Signal trigger → recovery

### Quality
- False positive rate
- Persistence in stress states
- Stability across parameter variations

### Conditioning
- Forward volatility by state
- Downside probability by state
- Correlation levels by state

No performance metrics (Sharpe, CAGR) are used.

---

## Stress Taxonomy
- **Sudden shocks:** fast onset, fast resolution (e.g., COVID)
- **Prolonged stress:** slow burn, persistent instability (e.g., GFC, tightening cycles)

---

## Key Insight
> Macro regimes and market stress signals are not substitutes.  
> They are complementary components of a robust risk monitoring system.

---

## Status
Analysis complete.  
No further tuning or optimization planned.
