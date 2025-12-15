## Macro regimes and market stress signals operate on different clocks.
Macro data estimates the economic state with structural lag, making it ill-suited for detecting sudden market stress. Market stress indicators react to fast-moving mechanisms such as volatility repricing, correlation breakdown, and liquidity withdrawal. This project compares the timing, behavior, and failure modes of slow macro regimes versus fast market stress detectors during sudden and prolonged stress episodes, framing both as complementary layers in a risk monitoring system rather than alpha-generating strategies.

## What this project is/is not
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

## Market Stress: Conceptual Definition
Market stress is defined as a rapid deterioration in market functioning, characterized by uncertainty repricing, correlation convergence, liquidity withdrawal, and nonlinear return behavior. Stress is a property of the market system, not simply poor returns.

- Uncertainty / convexity demand
- Diversification breakdown
- Forced trading and liquidity stress
- Tail-risk amplification

| Mechanism               | Indicator Family | Examples (not exhaustive)          |
| ----------------------- | ---------------- | ---------------------------------- |
| Uncertainty repricing   | Volatility       | VIX level, VIX momentum            |
| Diversification failure | Correlation      | Avg pairwise correlation           |
| Disagreement / herding  | Dispersion       | Cross-sectional return dispersion  |
| Liquidity stress        | Volume           | Volume spikes, down/up volume      |
| Nonlinearity            | Tails            | Skewness, kurtosis, tail frequency |

- All indicators must be observable in real time
- No future information
- No optimization across indicators
- Higher value = more stress

## Composite Stress Index (CSI) Philosophy
The composite stress index is designed as a structural monitoring tool, not an optimized signal. Indicators are normalized to a common scale and equally weighted to avoid parameter mining. The objective is robustness and interpretability rather than performance maximization.
- Z-score normalization
- Equal weights
- Percentile-based regimes (not thresholds)
The CSI is evaluated on detection timing, stability, and interpretability rather than return outcomes.

## Macro Regimes as Slow State Estimation
Macro regimes are treated as slow-moving state estimators of the economic environment. Their value lies in identifying persistence and structural backdrops, not in detecting abrupt market stress.
- Monthly or quarterly frequency
- Explicit publication lag
- Designed to capture persistence, not onset
- Evaluated on duration alignment, not early warning
In this framework, macro regimes are not expected to lead stress events, but to contextualize and validate their persistence.

## Design Constraints
- No lookahead or revised data
- Indicators must be computable in real time
- No parameter tuning based on outcomes
- All regime boundaries fixed ex ante

## Evaluation Framework
No performance metrics (Sharpe, CAGR) are used. Performance metrics are intentionally excluded to avoid conflating stress detection quality with portfolio construction choices.
### Timing & detection
- Stress onset → signal trigger latency
- Signal trigger → drawdown trough
- Signal trigger → recovery
### Quality
- False positive rate
- Persistence in stress states
- Stability across parameter variations
### Conditioning
- Forward volatility by state
- Tail loss probability by state
- Correlation levels by state

## Stress Taxonomy
- Sudden shocks (fast onset, fast resolution)
- Prolonged stress (slow burn, persistent)