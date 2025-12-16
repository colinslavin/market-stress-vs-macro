# Executive Summary  
**Macro Regimes vs Market Stress: A Systems-Level Comparison**

## Overview
Macro regimes and market stress signals operate on different clocks.  
Macro data estimates the economic state with structural lag, while market stress indicators react in real time to changes in uncertainty, correlation, liquidity, and tail risk.

This project compares **slow macro regime signals** and **fast market stress signals** across sudden shocks and prolonged stress periods. Rather than treating them as competing indicators, the analysis frames them as **complementary layers in a risk monitoring system**.

The objective is not to generate alpha or optimize portfolios, but to understand **timing, persistence, and failure modes** in risk signals used for governance, monitoring, and decision support.

---

## Key Questions
1. Which signals detect stress earliest?
2. Which signals confirm that stress is persistent?
3. Where does each signal fail?
4. How should these signals be used together in practice?

---

## Approach
- Construct a **Composite Stress Index (CSI)** from fast market-based indicators:
  - Volatility (VIX, realized volatility)
  - Correlation (diversification breakdown across sector ETFs)
  - Dispersion (cross-sectional disagreement)
  - Volume (liquidity stress)
  - Tail risk (downside event frequency)
- Normalize indicators using rolling statistics (no lookahead)
- Combine indicators with equal weights to avoid parameter tuning
- Define stress regimes using expanding percentiles
- Compare CSI behavior against lagged macro regime proxies across predefined stress events

No performance metrics (Sharpe, CAGR, returns) are used.

---

## Core Findings

### 1. Detection Timing
- **CSI responds immediately** during sudden shocks (e.g., COVID)
- **Macro regimes lag materially** or do not trigger during short-lived stress
- This is a structural limitation of macro data, not a modeling failure

### 2. Persistence & Confirmation
- During prolonged stress (e.g., GFC, 2022 tightening), macro regimes eventually align
- Macro regimes remain active longer, confirming that stress is structural rather than transient
- CSI captures onset; macro confirms persistence

### 3. Failure Modes
- CSI can overreact to short-lived shocks if used alone
- Macro regimes miss fast instability entirely if used alone
- Treating either signal as a standalone solution is a category error

---

## Key Insight
> Macro regimes are slow state estimators.  
> Market stress indicators are fast instability detectors.  
> They solve different problems and should be used together, not compared as substitutes.

---

## Practical Implications
- **Risk monitoring:** Use CSI for early warning and escalation
- **Governance:** Use macro regimes to validate persistence before structural decisions
- **Communication:** Separate “instability detected” from “economic regime shift confirmed”

---

## What This Project Is Not
- A trading strategy
- An asset allocation model
- An optimized signal
- A claim of return improvement

This is a **systems and decision-support analysis**.

---

## Takeaway
Effective risk systems require both **fast sensors** and **slow confirmations**.  
The mistake is evaluating them on the same axis.
