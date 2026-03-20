
---

# ⚡ XAUUSD Pro Suite

> A professional-grade, single-file Streamlit application for gold trading risk management — combining a Position Size Calculator and a full Risk Management Dashboard under one roof.

---

## Overview

XAUUSD Pro Suite merges two standalone trading tools into a unified three-page app with a shared sidebar, a consistent navy/gold design system, and a clean domain model at its core. It is built for traders who want to size positions precisely, understand their risk-reward profile, and model the impact of losing streaks — all without leaving a single interface.

---

## Pages

### 📖 Page 1 — Explainer
A complete knowledge-base reference covering every formula and concept used in the app. Includes:
- What position sizing is and why it matters
- A full step-by-step worked example (balance → risk → lot size)
- Risk tier classification (Conservative / Moderate / Aggressive)
- Risk-Reward Ratio deep dive with break-even win-rate math
- Consecutive loss drawdown concept with formulas

### 🧮 Page 2 — Position Calculator
An interactive calculator focused on answering one question: *how large should this trade be?*

| Input | Description |
|---|---|
| Instrument Type | XAUUSD (Gold), Forex Pair, or Other |
| Account Balance | Your total trading capital in USD |
| Stop Loss (pips) | Distance to your stop-loss level |
| Risk % | Percentage of account to risk per trade |

**Outputs:** recommended lot size, capital at risk, pip value per lot, and risk profile classification.

### 📊 Page 3 — Risk Management Pro
A full risk dashboard that goes beyond lot sizing to give you the complete picture of any trade.

- **KPI Cards** — Lot size, risk amount, profit if TP hit, loss if SL hit
- **Risk-Reward Ratio** — Live 1:N display with qualitative rating
- **Risk-o-Meter** — Visual bar spanning Safe → Caution → Danger zones
- **Trade Summary Panel** — All key figures in one place, including post-trade account balances
- **Lot Size Suggestions** — Conservative (1%), Moderate (2%), and Aggressive (5%) presets side by side
- **Drawdown Table** — Models 10 consecutive losses with colour-coded balance and drawdown % progression

---

## Architecture

The app follows a domain-first approach. All financial logic lives in a single class, `XAUUSDCalculator`, which is instantiated once from sidebar inputs and shared across all pages.

```python
class XAUUSDCalculator:
    PIP_VALUE_PER_LOT = 1.0  # $1 per pip per standard lot (XAUUSD)

    # Core properties
    risk_amount        → Balance × Risk% / 100
    lot_size           → Risk$ / (SL pips × pip value)
    profit             → TP pips × lot size × pip value
    loss               → SL pips × lot size × pip value
    rrr                → TP pips / SL pips
    account_after_win  → Balance + profit
    account_after_loss → Balance − loss

    # Methods
    lot_for_risk(pct)    → lot size at any given risk %
    drawdown_table(n)    → DataFrame of n consecutive losses
```

The UI layer is intentionally separated from this model — pages read from `calc.*` properties and render HTML/CSS components independently.

---

## Formulas Reference

```
Risk Amount ($)   = Account Balance × Risk% ÷ 100
Lot Size          = Risk Amount ÷ (Stop Loss pips × $1)
Profit            = Take Profit pips × Lot Size × $1
Loss              = Stop Loss pips × Lot Size × $1
Risk-Reward Ratio = Take Profit pips ÷ Stop Loss pips
```

> **XAUUSD constant:** 1 standard lot = 100 oz of XAU. Pip value = **$1.00 per pip per lot**.

---

## Project Structure

```
xauusd_pro_app/
├── app.py        # Single-file Streamlit application
└── README.md     # This file
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

```bash
# 1. Clone or download the project
git clone https://github.com/your-username/xauusd-pro-suite.git
cd xauusd-pro-suite

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install streamlit pandas numpy

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `pandas` | Drawdown table construction |
| `numpy` | Numeric utilities |

No external APIs or data feeds are required. All calculations are performed locally and in real time.

---

## Design System

The app uses a custom CSS design system injected via `st.markdown`. Key tokens:

| Token | Value | Usage |
|---|---|---|
| `--navy-900` | `#060D1F` | App background |
| `--gold` | `#D4AF37` | Primary accent, borders, labels |
| `--gold-light` | `#FFE082` | Gradient highlights |
| `--green-accent` | `#69F0AE` | Conservative / profit / safe |
| `--red-accent` | `#FF8A80` | Aggressive / loss / danger |
| `--blue-accent` | `#82B1FF` | Lot size / neutral data |

Typography: **Poppins** (UI, headings) + **Space Mono** (numbers, data, monospaced values) via Google Fonts.

---

## Customisation

**Adding a new instrument** — extend the `pip_value_map` dictionary in Page 2 and update `XAUUSDCalculator.PIP_VALUE_PER_LOT` if needed for a default.

**Changing the drawdown depth** — pass a different `consecutive_losses` argument to `calc.drawdown_table()` on Page 3.

**Adjusting risk tier thresholds** — the Conservative / Moderate / Aggressive cutoffs (2% and 4%) appear in both the Page 2 result card and the Page 3 risk-o-meter. Update the conditional blocks in each section to change them globally.

**Adding more pages** — extend the `page` radio widget in the sidebar and add a new `elif` branch at the bottom of `app.py`.

---

## Disclaimer

> This application is built **for educational purposes only**. It does not constitute financial advice. Trading leveraged instruments such as gold (XAUUSD) carries significant risk of loss. Past performance does not guarantee future results. Always trade responsibly and within your means.

---

*XAUUSD Pro Suite · Professional Risk Engine · v2.0*

---
