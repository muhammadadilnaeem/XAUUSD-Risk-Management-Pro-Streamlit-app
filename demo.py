import streamlit as st
import pandas as pd
import numpy as np
import textwrap

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="XAUUSD Pro Suite v3",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def html(raw: str):
    st.markdown(textwrap.dedent(raw).strip(), unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --navy-900:      #060D1F;
    --navy-800:      #0A1628;
    --navy-700:      #0D1F3C;
    --gold:          #D4AF37;
    --gold-light:    #FFE082;
    --gold-dim:      #FFD54F;
    --blue-accent:   #82B1FF;
    --green-accent:  #69F0AE;
    --red-accent:    #FF8A80;
    --text-primary:  #E8EAF0;
    --text-secondary:#8899AA;
    --text-muted:    #566A80;
    --glass-bg:      rgba(13,31,60,0.7);
    --glass-border:  rgba(212,175,55,0.12);
    --card-shadow:   0 8px 32px rgba(0,0,0,0.45), 0 1px 0 rgba(212,175,55,0.07) inset;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    background-color: var(--navy-900) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0D1F3C 0%, #060D1F 50%, #060D1F 100%);
    background-attachment: fixed;
}
body::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(212,175,55,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(212,175,55,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #060D1F 100%);
    border-right: 1px solid rgba(212,175,55,0.15);
}
[data-testid="stSidebar"] label {
    color: #B8C4D4 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: rgba(212,175,55,0.05) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 8px !important;
    color: #E8EAF0 !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(212,175,55,0.6) !important;
    box-shadow: 0 0 0 2px rgba(212,175,55,0.12) !important;
}

.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
}
.stSlider > div > div > div > div > div {
    background: #fff !important;
    border: 2px solid var(--gold) !important;
    box-shadow: 0 0 12px rgba(212,175,55,0.55) !important;
    width: 18px !important; height: 18px !important;
}

.stSelectbox > div > div {
    background: rgba(212,175,55,0.05) !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
.stSelectbox > div > div:hover { border-color: rgba(212,175,55,0.5) !important; }
.stSelectbox svg { color: var(--gold) !important; }

.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #1a3a6e 0%, #D4AF37 100%) !important;
    color: #fff !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 15px 32px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(212,175,55,0.25) !important;
    margin-top: 8px !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(212,175,55,0.4) !important;
    background: linear-gradient(135deg, #1a3a6e 0%, #FFE082 100%) !important;
}

/* Toggle pills for pip mode */
.pip-mode-bar {
    display: flex; gap: 8px; margin: 10px 0 18px 0;
}
.pip-pill {
    flex: 1; text-align: center; padding: 8px 4px;
    border-radius: 10px; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.1em; text-transform: uppercase;
    cursor: pointer; transition: all 0.18s;
    font-family: 'Poppins', sans-serif;
}
.pip-pill-active {
    background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(212,175,55,0.08));
    border: 1px solid rgba(212,175,55,0.5); color: #D4AF37;
}
.pip-pill-inactive {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); color: #566A80;
}

.section-label {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--gold);
    border-left: 3px solid var(--gold); padding-left: 0.75rem;
    margin: 0 0 1rem 0; display: block;
}
.section-title {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.16em;
    text-transform: uppercase; color: var(--gold);
    border-left: 3px solid var(--gold); padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* KPI Grid */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 2rem; }
.kpi-card {
    position: relative; overflow: hidden; border-radius: 16px;
    padding: 1.5rem 1.2rem; border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
}
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 16px 16px 0 0;
}
.kpi-gold  { background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(212,175,55,0.04)); }
.kpi-gold::before  { background: linear-gradient(90deg, #D4AF37, #FFE082); }
.kpi-blue  { background: linear-gradient(135deg, rgba(41,98,255,0.15), rgba(41,98,255,0.04)); }
.kpi-blue::before  { background: linear-gradient(90deg, #2962FF, #82B1FF); }
.kpi-green { background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,200,83,0.04)); }
.kpi-green::before { background: linear-gradient(90deg, #00C853, #69F0AE); }
.kpi-red   { background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.04)); }
.kpi-red::before   { background: linear-gradient(90deg, #FF1744, #FF8A80); }
.kpi-purple{ background: linear-gradient(135deg, rgba(170,0,255,0.13), rgba(170,0,255,0.04)); }
.kpi-purple::before{ background: linear-gradient(90deg, #AA00FF, #CE93D8); }
.kpi-cyan  { background: linear-gradient(135deg, rgba(0,229,255,0.12), rgba(0,229,255,0.04)); }
.kpi-cyan::before  { background: linear-gradient(90deg, #00B8D4, #80DEEA); }
.kpi-label { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #8899AA; margin-bottom: 0.5rem; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 1.7rem; font-weight: 700; line-height: 1; margin-bottom: 0.3rem; }
.kpi-gold .kpi-value   { color: #FFD54F; }
.kpi-blue .kpi-value   { color: #82B1FF; }
.kpi-green .kpi-value  { color: #69F0AE; }
.kpi-red .kpi-value    { color: #FF8A80; }
.kpi-purple .kpi-value { color: #CE93D8; }
.kpi-cyan .kpi-value   { color: #80DEEA; }
.kpi-sub { font-size: 0.72rem; color: #566A80; font-family: 'Space Mono', monospace; }

/* Validation alert badges */
.val-ok      { display:inline-flex; align-items:center; gap:6px; padding:8px 14px; border-radius:8px; font-size:0.75rem; font-weight:600; background:rgba(105,240,174,0.08); border:1px solid rgba(105,240,174,0.25); color:#69F0AE; margin:4px 0; width:100%; }
.val-warn    { display:inline-flex; align-items:center; gap:6px; padding:8px 14px; border-radius:8px; font-size:0.75rem; font-weight:600; background:rgba(255,213,79,0.08); border:1px solid rgba(255,213,79,0.25); color:#FFD54F; margin:4px 0; width:100%; }
.val-danger  { display:inline-flex; align-items:center; gap:6px; padding:8px 14px; border-radius:8px; font-size:0.75rem; font-weight:600; background:rgba(255,138,128,0.08); border:1px solid rgba(255,138,128,0.25); color:#FF8A80; margin:4px 0; width:100%; }

/* Calc card */
.calc-card {
    background: var(--glass-bg); border: 1px solid var(--glass-border);
    border-radius: 20px; padding: 32px 28px; position: relative;
    box-shadow: var(--card-shadow); margin-bottom: 20px;
    backdrop-filter: blur(12px); overflow: hidden;
}
.calc-card::before {
    content: ''; position: absolute; top: 0; left: 20px; right: 20px;
    height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.5), transparent);
}

/* Result card */
.result-outer {
    background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
    border: 1px solid rgba(212,175,55,0.22); border-radius: 20px;
    padding: 36px 28px 32px; position: relative; box-shadow: var(--card-shadow);
    margin-top: 8px; animation: fadeSlideUp 0.35s cubic-bezier(0.22,1,0.36,1);
    backdrop-filter: blur(12px); overflow: hidden;
}
.result-outer::before {
    content: ''; position: absolute; top: 0; left: 20px; right: 20px;
    height: 1px; background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.lot-label { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 5px; color: var(--text-muted); text-align: center; margin-bottom: 4px; }
.lot-value {
    font-family: 'Space Mono', monospace;
    font-size: clamp(54px,12vw,96px); font-weight: 700; line-height: 1; text-align: center;
    background: linear-gradient(135deg, #fff 0%, var(--gold) 55%, var(--gold-dim) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 28px rgba(212,175,55,0.3));
}
.lot-unit { font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 5px; color: var(--text-secondary); text-align: center; text-transform: uppercase; margin-top: 4px; }
.stats-divider { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent); margin: 20px 0; }
.stats-row { display: flex; justify-content: space-around; gap: 8px; flex-wrap: wrap; }
.stat-item { text-align: center; flex: 1; min-width: 80px; background: rgba(212,175,55,0.04); border: 1px solid rgba(212,175,55,0.09); border-radius: 12px; padding: 10px 8px; }
.stat-val { font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; color: var(--text-primary); }
.stat-lbl { font-size: 9px; font-weight: 600; letter-spacing: 0.1em; color: var(--text-muted); text-transform: uppercase; margin-top: 4px; }

/* Cost breakdown */
.cost-row { display: flex; justify-content: space-between; align-items: center; padding: 7px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.82rem; }
.cost-row:last-child { border-bottom: none; font-weight: 700; }
.cost-label { color: #8899AA; }
.cost-val { font-family: 'Space Mono', monospace; }

/* Summary panel */
.summary-panel {
    background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
    border: 1px solid rgba(212,175,55,0.2); border-radius: 16px;
    padding: 1.4rem 1.6rem; margin-bottom: 1.5rem;
}
.summary-panel h3 { font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: #D4AF37; margin: 0 0 0.9rem 0; }
.summary-row { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.87rem; }
.summary-row:last-child { border-bottom: none; }
.summary-row .sr-label { color: #8899AA; }
.summary-row .sr-val   { font-family: 'Space Mono', monospace; font-weight: 700; }

/* Lot suggestion cards */
.lot-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 1.5rem; }
.lot-card { background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.07); padding: 1.1rem 1rem; text-align: center; transition: border-color 0.2s; }
.lot-card:hover { border-color: rgba(212,175,55,0.35); }
.lot-card .lc-label { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem; }
.lot-card .lc-value { font-family: 'Space Mono', monospace; font-size: 1.3rem; font-weight: 700; line-height: 1; }
.lot-card .lc-risk  { font-size: 0.68rem; color: #566A80; margin-top: 0.3rem; font-family: 'Space Mono', monospace; }
.lc-conservative .lc-label, .lc-conservative .lc-value { color: #69F0AE; }
.lc-moderate     .lc-label, .lc-moderate     .lc-value { color: #FFD54F; }
.lc-aggressive   .lc-label, .lc-aggressive   .lc-value { color: #FF8A80; }

/* Risk bar */
.risk-bar-wrap { background: rgba(255,255,255,0.04); border-radius: 8px; height: 10px; overflow: hidden; margin: 0.6rem 0 0.3rem 0; }
.risk-bar-fill  { height: 100%; border-radius: 8px; transition: width 0.4s ease; }
.risk-safe      { background: linear-gradient(90deg, #00C853, #69F0AE); }
.risk-moderate  { background: linear-gradient(90deg, #FFD54F, #FFA000); }
.risk-danger    { background: linear-gradient(90deg, #FF6D00, #FF1744); }

/* Explainer cards */
.exp-section {
    background: var(--glass-bg); border: 1px solid var(--glass-border);
    border-radius: 20px; padding: 28px; margin-bottom: 20px;
    position: relative; overflow: hidden;
}
.exp-section::before {
    content: ''; position: absolute; top: 0; left: 20px; right: 20px;
    height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
}
.exp-title    { font-size: 1.1rem; font-weight: 700; color: var(--gold-light); margin-bottom: 0.5rem; }
.exp-subtitle { font-family: 'Space Mono', monospace; font-size: 0.68rem; letter-spacing: 0.14em; color: var(--text-muted); text-transform: uppercase; margin-bottom: 1.2rem; }
.exp-body     { font-size: 0.88rem; line-height: 1.8; color: var(--text-secondary); }
.formula-block {
    background: rgba(6,13,31,0.9); border: 1px solid rgba(212,175,55,0.15);
    border-radius: 12px; padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace; font-size: 0.8rem; line-height: 2.2; color: #8899AA; margin-top: 1rem;
}

/* New mode badge */
.new-badge {
    display: inline-block; font-size: 0.55rem; font-weight: 800; letter-spacing: 0.12em;
    text-transform: uppercase; background: linear-gradient(90deg, #D4AF37, #FFE082);
    color: #060D1F; padding: 2px 7px; border-radius: 4px; vertical-align: middle; margin-left: 6px;
}

/* Sidebar brand */
.sidebar-brand {
    text-align: center; padding: 0 0 1.5rem 0;
    border-bottom: 1px solid rgba(212,175,55,0.15); margin-bottom: 1.5rem;
}
.sidebar-brand span {
    font-family: 'Poppins', sans-serif; font-weight: 800; font-size: 1.05rem;
    background: linear-gradient(90deg, #D4AF37, #FFE082);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 0.04em;
}
.sidebar-brand small {
    display: block; font-size: 0.6rem; color: #566A80; letter-spacing: 0.18em;
    text-transform: uppercase; margin-top: 0.15rem;
}

@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

.warning-strip {
    background: rgba(212,175,55,0.05); border: 1px solid rgba(212,175,55,0.14);
    border-left: 3px solid var(--gold); border-radius: 10px;
    padding: 12px 16px; margin-top: 16px;
    font-size: 11px; color: var(--text-muted); line-height: 1.7;
}

.footer {
    text-align: center; margin-top: 44px;
    font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 3px;
    color: var(--text-muted); opacity: 0.4; text-transform: uppercase; padding-bottom: 2rem;
}

/* Live indicator */
.live-dot {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(105,240,174,0.08); border: 1px solid rgba(105,240,174,0.22);
    border-radius: 999px; padding: 4px 14px;
    font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 3px; color: #69F0AE; text-transform: uppercase;
}
.live-dot-inner {
    width: 6px; height: 6px; border-radius: 50%; background: #69F0AE;
    box-shadow: 0 0 8px #69F0AE; animation: pulse 1.5s ease infinite;
}

/* Margin meter */
.margin-meter { background: rgba(255,255,255,0.04); border-radius: 8px; height: 8px; overflow: hidden; margin: 6px 0; }
.margin-fill  { height: 100%; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DOMAIN MODEL  (v3 — fully upgraded)
# ─────────────────────────────────────────────
class XAUUSDCalculatorV3:
    """
    Institutional-grade domain model.

    Calculation modes
    ─────────────────
    1. Price-based  : uses entry_price + sl_price   → most accurate, broker-agnostic
    2. Pip-based    : uses sl_pips + pip_mode toggle → backward-compatible

    Pip modes (pip-based only)
    ──────────────────────────
    • standard : 1 pip = 0.01 → $1  per standard lot  (cTrader definition)
    • broker   : 1 pip = 0.10 → $10 per standard lot  (MT4/MT5 definition)
    """

    CONTRACT_SIZE = 100   # oz per standard lot for XAUUSD

    def __init__(
        self,
        account_balance: float,
        risk_percent:    float,
        sl_pips:         float,
        tp_pips:         float,
        pip_mode:        str   = "standard",   # "standard" | "broker"
        spread_points:   float = 0.0,
        commission_lot:  float = 0.0,
        leverage:        int   = 100,
        entry_price:     float = 0.0,
        sl_price:        float = 0.0,
        tp_price:        float = 0.0,
        use_price_mode:  bool  = False,
        trade_direction: str   = "buy",        # "buy" | "sell"
    ):
        self.account_balance = account_balance
        self.risk_percent    = risk_percent
        self.sl_pips_raw     = sl_pips
        self.tp_pips_raw     = tp_pips
        self.pip_mode        = pip_mode
        self.spread_points   = spread_points
        self.commission_lot  = commission_lot
        self.leverage        = leverage
        self.entry_price     = entry_price
        self.sl_price        = sl_price
        self.tp_price        = tp_price
        self.use_price_mode  = use_price_mode
        self.trade_direction = trade_direction

    # ── Pip value per lot based on mode ──────────────────────────
    @property
    def pip_value_per_lot(self) -> float:
        return 10.0 if self.pip_mode == "broker" else 1.0

    # ── Price-based distance (in price units) ─────────────────────
    @property
    def sl_distance_price(self) -> float:
        """Absolute price distance from entry to SL."""
        if self.use_price_mode and self.entry_price > 0 and self.sl_price > 0:
            return abs(self.entry_price - self.sl_price)
        return 0.0

    @property
    def tp_distance_price(self) -> float:
        """Absolute price distance from entry to TP."""
        if self.use_price_mode and self.entry_price > 0 and self.tp_price > 0:
            return abs(self.entry_price - self.tp_price)
        return 0.0

    # ── Effective SL after spread adjustment ─────────────────────
    @property
    def effective_sl_pips(self) -> float:
        """
        Spread widens the effective stop-loss.
        spread_points / 10 converts points→pips (standard pip) or /1 for broker pip.
        """
        if self.use_price_mode:
            # In price mode spread is added as points → convert to price units (0.01 per point)
            spread_price = self.spread_points * 0.01
            return self.sl_distance_price + spread_price
        else:
            spread_pips = self.spread_points / (10.0 if self.pip_mode == "standard" else 1.0)
            return self.sl_pips_raw + spread_pips

    @property
    def effective_tp_pips(self) -> float:
        if self.use_price_mode:
            return self.tp_distance_price
        return self.tp_pips_raw

    # ── Core calculations ─────────────────────────────────────────
    @property
    def risk_amount(self) -> float:
        return (self.account_balance * self.risk_percent) / 100

    @property
    def lot_size(self) -> float:
        if self.use_price_mode:
            if self.sl_distance_price <= 0:
                return 0.0
            # Institutional formula: Lot = Risk$ / (SL_distance × contract_size)
            return self.risk_amount / (self.effective_sl_pips * self.CONTRACT_SIZE)
        else:
            if self.effective_sl_pips <= 0:
                return 0.0
            return self.risk_amount / (self.effective_sl_pips * self.pip_value_per_lot)

    @property
    def profit(self) -> float:
        if self.use_price_mode:
            return self.effective_tp_pips * self.lot_size * self.CONTRACT_SIZE
        return self.effective_tp_pips * self.lot_size * self.pip_value_per_lot

    @property
    def loss(self) -> float:
        return self.risk_amount  # by definition when sizing correctly

    @property
    def commission_total(self) -> float:
        return self.commission_lot * self.lot_size

    @property
    def net_profit(self) -> float:
        return self.profit - self.commission_total

    @property
    def net_loss(self) -> float:
        return self.loss + self.commission_total

    @property
    def rrr(self) -> float:
        if self.effective_sl_pips <= 0:
            return 0.0
        if self.use_price_mode:
            return self.tp_distance_price / self.sl_distance_price if self.sl_distance_price > 0 else 0
        return self.effective_tp_pips / self.effective_sl_pips

    @property
    def required_margin(self) -> float:
        """Required margin = (Lot × contract_size × entry_price) / leverage."""
        price = self.entry_price if self.use_price_mode and self.entry_price > 0 else 2330.0  # fallback gold price
        return (self.lot_size * self.CONTRACT_SIZE * price) / self.leverage

    @property
    def margin_usage_pct(self) -> float:
        return (self.required_margin / self.account_balance) * 100 if self.account_balance > 0 else 0

    @property
    def account_after_win(self) -> float:
        return self.account_balance + self.net_profit

    @property
    def account_after_loss(self) -> float:
        return self.account_balance - self.net_loss

    @property
    def breakeven_win_rate(self) -> float:
        if self.rrr <= 0:
            return 100.0
        return (1 / (1 + self.rrr)) * 100

    # ── Risk-tier classification ──────────────────────────────────
    @property
    def risk_tier(self) -> str:
        if self.risk_percent <= 2:
            return "CONSERVATIVE"
        elif self.risk_percent <= 4:
            return "MODERATE"
        return "AGGRESSIVE"

    @property
    def risk_color(self) -> str:
        return {"CONSERVATIVE": "#69F0AE", "MODERATE": "#FFD54F", "AGGRESSIVE": "#FF8A80"}[self.risk_tier]

    # ── Trade validations ─────────────────────────────────────────
    def validate(self) -> list[dict]:
        """Returns list of {level: 'ok'|'warn'|'danger', msg: str}."""
        alerts = []
        lot = self.lot_size
        margin_pct = self.margin_usage_pct

        if lot <= 0:
            alerts.append({"level": "danger", "msg": "❌ Lot size is zero — check your SL distance"})
            return alerts

        if lot < 0.01:
            alerts.append({"level": "warn", "msg": "⚠️ Lot size < 0.01 — may be below broker minimum"})
        elif lot > 100:
            alerts.append({"level": "danger", "msg": "❌ Lot size too large — verify inputs"})
        else:
            alerts.append({"level": "ok", "msg": f"✅ Lot size {lot:.3f} within normal range"})

        if self.risk_percent > 5:
            alerts.append({"level": "danger", "msg": f"❌ Risk {self.risk_percent}% is DANGEROUS — professionals use ≤2%"})
        elif self.risk_percent > 2:
            alerts.append({"level": "warn", "msg": f"⚠️ Risk {self.risk_percent}% is elevated — consider reducing"})
        else:
            alerts.append({"level": "ok", "msg": f"✅ Risk {self.risk_percent}% is within safe range"})

        if self.use_price_mode and self.sl_distance_price < 0.50:
            alerts.append({"level": "danger", "msg": "❌ SL too tight (< 50 pts) — high stop-out risk"})
        elif not self.use_price_mode and self.effective_sl_pips < 5:
            alerts.append({"level": "danger", "msg": "❌ SL too tight — vulnerable to spread/slippage"})

        if margin_pct > 50:
            alerts.append({"level": "danger", "msg": f"❌ Margin usage {margin_pct:.1f}% — account at high risk"})
        elif margin_pct > 20:
            alerts.append({"level": "warn", "msg": f"⚠️ Margin usage {margin_pct:.1f}% — monitor closely"})
        else:
            alerts.append({"level": "ok", "msg": f"✅ Margin usage {margin_pct:.1f}% is acceptable"})

        if self.rrr > 0 and self.rrr < 1:
            alerts.append({"level": "danger", "msg": "❌ RRR < 1:1 — statistically negative edge"})
        elif self.rrr < 2:
            alerts.append({"level": "warn", "msg": f"⚠️ RRR 1:{self.rrr:.2f} — aim for ≥ 1:2"})
        else:
            alerts.append({"level": "ok", "msg": f"✅ RRR 1:{self.rrr:.2f} is excellent"})

        return alerts

    # ── Lot for given risk pct ────────────────────────────────────
    def lot_for_risk(self, pct: float) -> float:
        if self.use_price_mode:
            if self.sl_distance_price <= 0:
                return 0.0
            return (self.account_balance * pct / 100) / (self.effective_sl_pips * self.CONTRACT_SIZE)
        else:
            if self.effective_sl_pips <= 0:
                return 0.0
            return (self.account_balance * pct / 100) / (self.effective_sl_pips * self.pip_value_per_lot)

    # ── Drawdown table ────────────────────────────────────────────
    def drawdown_table(self, consecutive_losses: int = 10) -> pd.DataFrame:
        rows = []
        equity = self.account_balance
        for i in range(1, consecutive_losses + 1):
            equity -= self.net_loss
            dd_pct = ((self.account_balance - equity) / self.account_balance) * 100
            rows.append({
                "# Losses":            i,
                "Account Balance ($)": round(max(equity, 0), 2),
                "Total Drawdown ($)":  round(self.net_loss * i, 2),
                "Drawdown %":          round(min(dd_pct, 100), 2),
                "Commission Drag ($)": round(self.commission_total * i, 2),
            })
        return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# SIDEBAR — Navigation + Shared Params
# ─────────────────────────────────────────────
with st.sidebar:
    html("""
    <div class='sidebar-brand'>
        <span>⚡ XAUUSD PRO SUITE</span>
        <small>v3 · Real-Time Engine</small>
    </div>
    """)

    page = st.radio(
        "Navigate",
        options=["📖  Explainer", "🧮  Position Calculator", "📊  Risk Management Pro"],
        index=1,
    )

    st.markdown("---")
    st.markdown("### ⚙️ Shared Parameters")

    account_balance = st.number_input(
        "Account Balance ($)", min_value=100.0, max_value=10_000_000.0,
        value=10_000.0, step=500.0, format="%.2f"
    )
    risk_percent_sidebar = st.number_input(
        "Risk % per Trade", min_value=0.1, max_value=20.0,
        value=2.0, step=0.1, format="%.1f"
    )
    leverage_sidebar = st.selectbox(
        "Leverage", options=[10, 20, 30, 50, 100, 200, 400, 500], index=4
    )

    st.markdown("---")
    st.markdown("### 📐 SL / TP")

    sl_pips_sidebar = st.number_input(
        "Stop Loss (pips)", min_value=1, max_value=500, value=50, step=1
    )
    tp_pips_sidebar = st.number_input(
        "Take Profit (pips)", min_value=1, max_value=5000, value=100, step=1
    )

    st.markdown("---")
    st.markdown("### 🔧 Broker Costs")

    spread_sidebar = st.number_input(
        "Spread (points)", min_value=0.0, max_value=200.0, value=20.0, step=1.0,
        help="Typical XAUUSD spread: 20–50 points. 10 points = 1 pip (standard)."
    )
    commission_sidebar = st.number_input(
        "Commission per Lot ($)", min_value=0.0, max_value=50.0, value=0.0, step=0.5,
        help="ECN brokers charge per round-turn lot. E.g. $7/lot."
    )

    # Quick sidebar validations
    if sl_pips_sidebar <= 0:
        st.error("❌ Stop Loss must be > 0")
    if risk_percent_sidebar >= 5:
        st.warning("⚠️ Risk ≥ 5% — high-risk territory")


# ─────────────────────────────────────────────
# DEFAULT CALC (sidebar params, pip-based)
# ─────────────────────────────────────────────
calc = XAUUSDCalculatorV3(
    account_balance = account_balance,
    risk_percent    = risk_percent_sidebar,
    sl_pips         = sl_pips_sidebar,
    tp_pips         = tp_pips_sidebar,
    spread_points   = spread_sidebar,
    commission_lot  = commission_sidebar,
    leverage        = leverage_sidebar,
    use_price_mode  = False,
)


# ══════════════════════════════════════════════════════════════════
#  PAGE 1 — EXPLAINER
# ══════════════════════════════════════════════════════════════════
if page == "📖  Explainer":

    html("""
    <div style='padding:40px 0 32px;'>
        <div style='display:inline-flex; align-items:center; gap:6px;
                    background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.22);
                    border-radius:999px; padding:5px 16px; font-family:Space Mono,monospace;
                    font-size:10px; letter-spacing:3px; color:#D4AF37; text-transform:uppercase; margin-bottom:20px;'>
            <span style='width:6px;height:6px;border-radius:50%;background:#D4AF37;
                         box-shadow:0 0 8px #D4AF37;animation:pulse 2s ease infinite;display:inline-block;'></span>
            Knowledge Base · v3
        </div>
        <h1 style='font-family:Poppins,sans-serif; font-size:clamp(28px,5vw,46px); font-weight:800;
                   background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   margin:0 0 10px; line-height:1.1;'>How It All Works</h1>
        <p style='color:#8899AA; font-size:13px;'>
            Complete formula reference for XAUUSD Pro Suite v3 — including new price-mode, spread, commission &amp; margin modules.
        </p>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v3 Upgrade · Pip Definition Problem</div>
        <div class='exp-title'>🔍 Why Pip Definitions Matter</div>
        <div class='exp-body'>
            The most dangerous mistake in XAUUSD trading tools is ambiguous pip definitions.
            There are <strong style='color:#E8EAF0;'>two industry conventions</strong> — and confusing them gives you a lot size
            that is <strong style='color:#FF8A80;'>10× too small or 10× too large</strong>.
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem;'>
            <div style='background:rgba(130,177,255,0.07); border:1px solid rgba(130,177,255,0.22);
                        border-radius:12px; padding:1.2rem;'>
                <div style='color:#82B1FF; font-weight:700; font-size:0.85rem; letter-spacing:0.08em; margin-bottom:0.5rem;'>📌 Standard / cTrader</div>
                <div style='font-family:Space Mono,monospace; font-size:0.82rem; color:#8899AA; line-height:2;'>
                    1 pip = 0.01 price move<br>
                    Pip value = $1 per standard lot<br>
                    SL of 50 pips = 0.50 move
                </div>
            </div>
            <div style='background:rgba(255,213,79,0.07); border:1px solid rgba(255,213,79,0.22);
                        border-radius:12px; padding:1.2rem;'>
                <div style='color:#FFD54F; font-weight:700; font-size:0.85rem; letter-spacing:0.08em; margin-bottom:0.5rem;'>📌 Broker / MT4·MT5</div>
                <div style='font-family:Space Mono,monospace; font-size:0.82rem; color:#8899AA; line-height:2;'>
                    1 pip = 0.10 price move<br>
                    Pip value = $10 per standard lot<br>
                    SL of 50 pips = 5.00 move
                </div>
            </div>
        </div>
        <div class='formula-block' style='margin-top:1rem;'>
            <span style='color:#FFD54F;'>Always verify</span> which convention your broker uses before entering positions.<br>
            Best practice: use <span style='color:#69F0AE;'>Price-Based Mode</span> to eliminate ambiguity entirely.
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v3 Upgrade · Institutional Approach</div>
        <div class='exp-title'>🏦 Price-Based Calculation (Most Accurate)</div>
        <div class='exp-body'>
            Instead of entering pips, you enter actual <strong style='color:#E8EAF0;'>price levels</strong>.
            The calculator derives the dollar distance automatically — completely broker-agnostic.
        </div>
        <div class='formula-block'>
            <span style='color:#8899AA;'>Given: Entry = 2330.00 · SL = 2320.00 · TP = 2360.00</span><br><br>
            <span style='color:#FFD54F;'>SL Distance</span>  = |Entry − SL|   = |2330 − 2320| = <span style='color:#FF8A80;'>10.00 pts</span><br>
            <span style='color:#69F0AE;'>TP Distance</span>  = |Entry − TP|   = |2330 − 2360| = <span style='color:#69F0AE;'>30.00 pts</span><br>
            <span style='color:#82B1FF;'>Lot Size</span>      = Risk$ ÷ (SL Distance × 100) = 200 ÷ (10 × 100) = <span style='color:#82B1FF;'>0.200 lots</span><br>
            <span style='color:#FFD54F;'>RRR</span>           = TP Distance ÷ SL Distance = 30 ÷ 10 = <span style='color:#D4AF37;'>1:3.00</span>
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v3 Upgrade · Hidden Costs</div>
        <div class='exp-title'>💸 Spread &amp; Commission Impact</div>
        <div class='exp-body'>
            Every trade has two hidden costs that inflate your real risk beyond the calculated amount.
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem;'>
            <div style='background:rgba(206,147,216,0.07); border:1px solid rgba(206,147,216,0.2); border-radius:12px; padding:1.2rem;'>
                <div style='color:#CE93D8; font-weight:700; font-size:0.85rem; margin-bottom:0.5rem;'>📊 Spread</div>
                <div style='color:#8899AA; font-size:0.82rem; line-height:1.8;'>
                    Typical XAUUSD spread: 20–50 points.<br>
                    Effective SL = your SL + spread<br>
                    Means your stop is hit earlier than intended.
                </div>
            </div>
            <div style='background:rgba(128,222,234,0.07); border:1px solid rgba(128,222,234,0.2); border-radius:12px; padding:1.2rem;'>
                <div style='color:#80DEEA; font-weight:700; font-size:0.85rem; margin-bottom:0.5rem;'>💰 Commission</div>
                <div style='color:#8899AA; font-size:0.82rem; line-height:1.8;'>
                    ECN brokers: typically $3–7 per lot round-turn.<br>
                    Adds to net loss on SL hits.<br>
                    Reduces net profit on TP hits.
                </div>
            </div>
        </div>
        <div class='formula-block'>
            <span style='color:#CE93D8;'>Effective SL</span>  = SL pips + (Spread ÷ pip_divisor)<br>
            <span style='color:#80DEEA;'>Net Profit</span>    = Gross Profit − (Commission × Lots)<br>
            <span style='color:#FF8A80;'>Net Loss</span>      = Risk Amount + (Commission × Lots)
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v3 Upgrade · Margin Awareness</div>
        <div class='exp-title'>📈 Margin &amp; Leverage</div>
        <div class='exp-body'>
            Knowing your required margin keeps you from over-leveraging and facing a margin call.
        </div>
        <div class='formula-block'>
            <span style='color:#80DEEA;'>Required Margin</span> = (Lot × 100 oz × Gold Price) ÷ Leverage<br>
            <span style='color:#CE93D8;'>Margin Usage %</span>  = Required Margin ÷ Account Balance × 100<br><br>
            <span style='color:#8899AA;'>Example: 0.20 lots · Gold @ $2,330 · 1:100 leverage</span><br>
            Margin = (0.20 × 100 × 2330) ÷ 100 = <span style='color:#80DEEA;'>$466</span>  (4.66% of $10,000)
        </div>
    </div>
    """)

    html('<div class="footer">XAUUSD Pro Suite v3 · Knowledge Base · For Educational Purposes Only</div>')


# ══════════════════════════════════════════════════════════════════
#  PAGE 2 — POSITION CALCULATOR (v3, live)
# ══════════════════════════════════════════════════════════════════
elif page == "🧮  Position Calculator":

    html("""
    <div style='text-align:center; padding:40px 24px 28px;'>
        <div class='live-dot' style='margin:0 auto 16px; width:fit-content;'>
            <span class='live-dot-inner'></span> Live · Auto-Calculates
        </div>
        <div style='font-family:Poppins,sans-serif; font-size:clamp(28px,6vw,48px); font-weight:800;
                    background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1;'>
            Position Calculator
        </div>
        <div style='color:#8899AA; font-size:13px; margin-top:10px;'>
            XAU/USD · Professional Risk Management · v3
        </div>
    </div>
    """)

    col_inputs, col_results = st.columns([1, 1], gap="large")

    with col_inputs:
        html('<div class="calc-card">')
        html('<span class="section-label">01 · Calculation Mode</span>')

        calc_mode = st.radio(
            "Mode",
            options=["📍 Price-Based (Recommended)", "📏 Pip-Based"],
            index=0,
            horizontal=True,
            help="Price-Based is broker-agnostic and most accurate. Pip-Based requires knowing your broker's pip convention."
        )
        use_price_mode = calc_mode.startswith("📍")

        if not use_price_mode:
            html('<span class="section-label" style="margin-top:16px;">Pip Convention</span>')
            pip_mode_sel = st.radio(
                "Pip Definition",
                options=["Standard (0.01 = $1/lot)", "Broker MT4/MT5 (0.10 = $10/lot)"],
                index=0, horizontal=True
            )
            pip_mode = "broker" if "Broker" in pip_mode_sel else "standard"
        else:
            pip_mode = "standard"

        html('<span class="section-label" style="margin-top:20px;">02 · Account</span>')
        c1, c2 = st.columns(2)
        with c1:
            balance_p2 = st.number_input("Account Balance ($)", value=account_balance,
                                          step=500.0, min_value=100.0, key="bal_p2")
        with c2:
            risk_pct_p2 = st.number_input("Risk % per Trade", value=risk_percent_sidebar,
                                           step=0.1, min_value=0.1, max_value=20.0, key="risk_p2")

        html('<span class="section-label" style="margin-top:20px;">03 · Trade Levels</span>')

        if use_price_mode:
            c1, c2, c3 = st.columns(3)
            with c1:
                direction_p2 = st.selectbox("Direction", ["Buy", "Sell"], key="dir_p2")
            with c2:
                entry_p2 = st.number_input("Entry Price", value=2330.00, step=0.10, format="%.2f", key="entry_p2")
            with c3:
                sl_price_p2 = st.number_input("SL Price", value=2310.00, step=0.10, format="%.2f", key="slprice_p2")
            tp_price_p2 = st.number_input("TP Price", value=2370.00, step=0.10, format="%.2f", key="tpprice_p2")
            sl_pips_p2 = 0.0
            tp_pips_p2 = 0.0
        else:
            c1, c2 = st.columns(2)
            with c1:
                sl_pips_p2 = st.number_input("Stop Loss (pips)", value=float(sl_pips_sidebar),
                                               step=1.0, min_value=1.0, key="sl_p2")
            with c2:
                tp_pips_p2 = st.number_input("Take Profit (pips)", value=float(tp_pips_sidebar),
                                               step=1.0, min_value=1.0, key="tp_p2")
            entry_p2 = 0.0; sl_price_p2 = 0.0; tp_price_p2 = 0.0
            direction_p2 = "Buy"

        html('<span class="section-label" style="margin-top:20px;">04 · Broker Costs</span>')
        c1, c2, c3 = st.columns(3)
        with c1:
            spread_p2 = st.number_input("Spread (pts)", value=spread_sidebar, step=1.0,
                                         min_value=0.0, max_value=200.0, key="spread_p2")
        with c2:
            comm_p2 = st.number_input("Commission/Lot ($)", value=commission_sidebar,
                                       step=0.5, min_value=0.0, max_value=50.0, key="comm_p2")
        with c3:
            lev_p2 = st.selectbox("Leverage", options=[10,20,30,50,100,200,400,500],
                                    index=4, key="lev_p2")

        html("</div>")  # end calc-card

    # ── Live calculation ──────────────────────────────────────────
    with col_results:
        c2_obj = XAUUSDCalculatorV3(
            account_balance = balance_p2,
            risk_percent    = risk_pct_p2,
            sl_pips         = sl_pips_p2,
            tp_pips         = tp_pips_p2,
            pip_mode        = pip_mode,
            spread_points   = spread_p2,
            commission_lot  = comm_p2,
            leverage        = lev_p2,
            entry_price     = entry_p2 if use_price_mode else 2330.0,
            sl_price        = sl_price_p2 if use_price_mode else 0.0,
            tp_price        = tp_price_p2 if use_price_mode else 0.0,
            use_price_mode  = use_price_mode,
            trade_direction = direction_p2.lower() if use_price_mode else "buy",
        )

        lot  = c2_obj.lot_size
        risk = c2_obj.risk_amount
        net_p = c2_obj.net_profit
        net_l = c2_obj.net_loss
        rrr   = c2_obj.rrr
        margin = c2_obj.required_margin
        margin_pct = c2_obj.margin_usage_pct

        if lot > 0:
            html(f"""
            <div class='result-outer' style='margin-top:16px;'>
                <div class='lot-label'>Recommended Lot Size</div>
                <div class='lot-value'>{lot:.3f}</div>
                <div class='lot-unit'>Standard Lots</div>
                <div class='stats-divider'></div>
                <div class='stats-row'>
                    <div class='stat-item'>
                        <div class='stat-val' style='color:#FFD54F;'>${risk:,.2f}</div>
                        <div class='stat-lbl'>Capital at Risk</div>
                    </div>
                    <div class='stat-item'>
                        <div class='stat-val' style='color:#69F0AE;'>${net_p:,.2f}</div>
                        <div class='stat-lbl'>Net Profit</div>
                    </div>
                    <div class='stat-item'>
                        <div class='stat-val' style='color:#FF8A80;'>${net_l:,.2f}</div>
                        <div class='stat-lbl'>Net Loss</div>
                    </div>
                    <div class='stat-item'>
                        <div class='stat-val' style='color:#D4AF37;'>1:{rrr:.2f}</div>
                        <div class='stat-lbl'>RRR</div>
                    </div>
                </div>
                <div class='stats-divider'></div>
                <div style='padding: 0 4px;'>
                    <div style='display:flex; justify-content:space-between; font-size:0.75rem; color:#8899AA; margin-bottom:4px;'>
                        <span>Margin Required</span>
                        <span style='font-family:Space Mono,monospace; color:#80DEEA;'>${margin:,.2f} ({margin_pct:.1f}%)</span>
                    </div>
                    <div class='margin-meter'>
                        <div class='margin-fill' style='width:{min(margin_pct,100):.1f}%;
                             background: {"linear-gradient(90deg,#00C853,#69F0AE)" if margin_pct<20 else ("linear-gradient(90deg,#FFD54F,#FFA000)" if margin_pct<50 else "linear-gradient(90deg,#FF6D00,#FF1744)")};'></div>
                    </div>
                    <div style='display:flex; justify-content:space-between; font-size:0.75rem; color:#8899AA; margin-bottom:8px;'>
                        <span>Cost Breakdown</span>
                        <span style='font-family:Space Mono,monospace; color:#CE93D8;'>Spread + Commission</span>
                    </div>
                    <div style='background:rgba(0,0,0,0.2); border-radius:10px; padding:10px 12px;'>
                        <div class='cost-row'>
                            <span class='cost-label'>Spread cost</span>
                            <span class='cost-val' style='color:#CE93D8;'>${(spread_p2 * 0.01 * lot * 100 if use_price_mode else spread_p2 / (10 if pip_mode=="standard" else 1) * lot * c2_obj.pip_value_per_lot):,.3f}</span>
                        </div>
                        <div class='cost-row'>
                            <span class='cost-label'>Commission</span>
                            <span class='cost-val' style='color:#80DEEA;'>${c2_obj.commission_total:,.3f}</span>
                        </div>
                        <div class='cost-row' style='border-top:1px solid rgba(255,255,255,0.08); margin-top:4px; padding-top:8px;'>
                            <span class='cost-label'>Break-even win rate</span>
                            <span class='cost-val' style='color:#FFD54F;'>{c2_obj.breakeven_win_rate:.1f}%</span>
                        </div>
                    </div>
                </div>
            </div>
            """)

            # Validation alerts
            html('<div style="margin-top:16px;">')
            alerts = c2_obj.validate()
            for a in alerts:
                css = {"ok": "val-ok", "warn": "val-warn", "danger": "val-danger"}[a["level"]]
                html(f'<div class="{css}">{a["msg"]}</div>')
            html('</div>')
        else:
            html("""
            <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;
                        height:320px; opacity:0.35; text-align:center;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>⚡</div>
                <div style='font-family:Space Mono,monospace; font-size:0.75rem; letter-spacing:0.2em;
                            text-transform:uppercase; color:#566A80;'>
                    Adjust parameters above — results update live
                </div>
            </div>
            """)

    html('<div class="footer">XAUUSD Position Calculator · v3 · Live Engine · Not Financial Advice</div>')


# ══════════════════════════════════════════════════════════════════
#  PAGE 3 — RISK MANAGEMENT PRO
# ══════════════════════════════════════════════════════════════════
elif page == "📊  Risk Management Pro":

    html("""
    <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:1.5rem; flex-wrap:wrap; gap:12px;'>
        <div>
            <h1 style='font-family:Poppins,sans-serif; font-weight:800; font-size:1.65rem;
                       background:linear-gradient(90deg,#D4AF37 0%,#FFE082 50%,#D4AF37 100%);
                       -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                       margin:0; letter-spacing:-0.01em;'>XAUUSD Risk Management Pro</h1>
            <p style='color:#566A80; font-size:0.78rem; letter-spacing:0.1em; text-transform:uppercase; margin:0.3rem 0 0;'>
                Precision Risk Engine · Gold Trading · Professional Grade
            </p>
        </div>
        <div class='live-dot'>
            <span class='live-dot-inner'></span> Auto-Updating · Live
        </div>
    </div>
    """)

    # ── 6-up KPI cards ────────────────────────────────────────────
    html(f"""
    <div style='display:grid; grid-template-columns:repeat(6,1fr); gap:0.85rem; margin-bottom:1.8rem;'>
        <div class='kpi-card kpi-blue'>
            <div class='kpi-label'>Lot Size</div>
            <div class='kpi-value' style='font-size:1.5rem;'>{calc.lot_size:.3f}</div>
            <div class='kpi-sub'>Std Lots</div>
        </div>
        <div class='kpi-card kpi-gold'>
            <div class='kpi-label'>Risk $</div>
            <div class='kpi-value' style='font-size:1.5rem;'>${calc.risk_amount:,.0f}</div>
            <div class='kpi-sub'>{risk_percent_sidebar}% of acct</div>
        </div>
        <div class='kpi-card kpi-green'>
            <div class='kpi-label'>Net Profit</div>
            <div class='kpi-value' style='font-size:1.5rem;'>${calc.net_profit:,.0f}</div>
            <div class='kpi-sub'>+{(calc.net_profit/account_balance*100):.2f}%</div>
        </div>
        <div class='kpi-card kpi-red'>
            <div class='kpi-label'>Net Loss</div>
            <div class='kpi-value' style='font-size:1.5rem;'>${calc.net_loss:,.0f}</div>
            <div class='kpi-sub'>-{(calc.net_loss/account_balance*100):.2f}%</div>
        </div>
        <div class='kpi-card kpi-purple'>
            <div class='kpi-label'>Margin</div>
            <div class='kpi-value' style='font-size:1.5rem;'>${calc.required_margin:,.0f}</div>
            <div class='kpi-sub'>{calc.margin_usage_pct:.1f}% usage</div>
        </div>
        <div class='kpi-card kpi-cyan'>
            <div class='kpi-label'>Break-even WR</div>
            <div class='kpi-value' style='font-size:1.5rem;'>{calc.breakeven_win_rate:.0f}%</div>
            <div class='kpi-sub'>to be profitable</div>
        </div>
    </div>
    """)

    # ── RRR + Risk-o-Meter + Margin Meter ────────────────────────
    col_rrr, col_risk, col_margin = st.columns([1, 1.5, 1.5])

    with col_rrr:
        rc = "#69F0AE" if calc.rrr >= 2 else ("#FFD54F" if calc.rrr >= 1 else "#FF8A80")
        label = "✅ Excellent" if calc.rrr >= 2 else ("⚠️ Acceptable" if calc.rrr >= 1 else "❌ Avoid")
        html(f"""
        <div style='padding:1rem 0;'>
            <div class='section-title'>Risk / Reward</div>
            <div style='font-family:Space Mono,monospace; font-size:2.2rem; font-weight:700; color:{rc}; line-height:1;'>1 : {calc.rrr:.2f}</div>
            <div style='color:#566A80; font-size:0.75rem; margin-top:0.4rem;'>{label}</div>
        </div>
        """)

    with col_risk:
        bar_cls = "risk-safe" if risk_percent_sidebar <= 2 else ("risk-moderate" if risk_percent_sidebar <= 4 else "risk-danger")
        bar_lbl = "🟢 Safe Zone" if risk_percent_sidebar <= 2 else ("🟡 Caution Zone" if risk_percent_sidebar <= 4 else "🔴 Danger Zone")
        html(f"""
        <div style='padding:1rem 0;'>
            <div class='section-title'>Risk-o-Meter</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
                <span style='font-size:0.78rem; color:#8899AA;'>{bar_lbl}</span>
                <span style='font-family:Space Mono,monospace; font-size:0.9rem; color:#D4AF37; font-weight:700;'>{risk_percent_sidebar}%</span>
            </div>
            <div class='risk-bar-wrap'>
                <div class='risk-bar-fill {bar_cls}' style='width:{min(risk_percent_sidebar*10,100)}%;'></div>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.6rem; color:#566A80; margin-top:0.25rem;'>
                <span>0%</span><span>2% Safe</span><span>5% Risky</span><span>10%</span>
            </div>
        </div>
        """)

    with col_margin:
        m_pct = calc.margin_usage_pct
        m_cls = "risk-safe" if m_pct < 20 else ("risk-moderate" if m_pct < 50 else "risk-danger")
        m_lbl = "🟢 Low" if m_pct < 20 else ("🟡 Moderate" if m_pct < 50 else "🔴 High Risk")
        html(f"""
        <div style='padding:1rem 0;'>
            <div class='section-title'>Margin Usage</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
                <span style='font-size:0.78rem; color:#8899AA;'>{m_lbl}</span>
                <span style='font-family:Space Mono,monospace; font-size:0.9rem; color:#80DEEA; font-weight:700;'>{m_pct:.1f}%</span>
            </div>
            <div class='risk-bar-wrap'>
                <div class='risk-bar-fill {m_cls}' style='width:{min(m_pct,100):.1f}%;'></div>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.6rem; color:#566A80; margin-top:0.25rem;'>
                <span>0%</span><span>20% OK</span><span>50% High</span><span>100%</span>
            </div>
        </div>
        """)

    # ── Live Validation Panel ─────────────────────────────────────
    html('<div class="section-title">Live Trade Validation</div>')
    val_cols = st.columns(2)
    alerts = calc.validate()
    for i, a in enumerate(alerts):
        css = {"ok": "val-ok", "warn": "val-warn", "danger": "val-danger"}[a["level"]]
        with val_cols[i % 2]:
            html(f'<div class="{css}">{a["msg"]}</div>')

    # ── Trade Summary + Lot Suggestions ──────────────────────────
    col_summ, col_lots = st.columns([1, 1])

    with col_summ:
        html("<div class='section-title'>Trade Summary</div>")
        html(f"""
        <div class='summary-panel'>
            <h3>📋 Position Overview</h3>
            <div class='summary-row'>
                <span class='sr-label'>Account Balance</span>
                <span class='sr-val' style='color:#E8EAF0;'>${account_balance:,.2f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Capital at Risk</span>
                <span class='sr-val' style='color:#FFD54F;'>${calc.risk_amount:,.2f} ({risk_percent_sidebar}%)</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Position Size</span>
                <span class='sr-val' style='color:#82B1FF;'>{calc.lot_size:.3f} lots</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Stop Loss</span>
                <span class='sr-val' style='color:#FF8A80;'>{sl_pips_sidebar} pips (eff. {calc.effective_sl_pips:.1f})</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Take Profit</span>
                <span class='sr-val' style='color:#69F0AE;'>{tp_pips_sidebar} pips → +${calc.net_profit:,.2f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Spread Impact</span>
                <span class='sr-val' style='color:#CE93D8;'>{spread_sidebar:.0f} pts → extra SL</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Commission Cost</span>
                <span class='sr-val' style='color:#80DEEA;'>${calc.commission_total:,.3f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Required Margin</span>
                <span class='sr-val' style='color:#80DEEA;'>${calc.required_margin:,.2f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Risk / Reward</span>
                <span class='sr-val' style='color:#D4AF37;'>1 : {calc.rrr:.2f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Account after Win</span>
                <span class='sr-val' style='color:#69F0AE;'>${calc.account_after_win:,.2f}</span>
            </div>
            <div class='summary-row'>
                <span class='sr-label'>Account after Loss</span>
                <span class='sr-val' style='color:#FF8A80;'>${calc.account_after_loss:,.2f}</span>
            </div>
        </div>
        """)

    with col_lots:
        html("<div class='section-title'>Lot Size Suggestions</div>")
        l1 = calc.lot_for_risk(1)
        l2 = calc.lot_for_risk(2)
        l5 = calc.lot_for_risk(5)
        html(f"""
        <div class='lot-row'>
            <div class='lot-card lc-conservative'>
                <div class='lc-label'>Conservative</div>
                <div class='lc-value'>{l1:.3f}</div>
                <div class='lc-risk'>1% · ${account_balance*0.01:,.0f}</div>
            </div>
            <div class='lot-card lc-moderate'>
                <div class='lc-label'>Moderate</div>
                <div class='lc-value'>{l2:.3f}</div>
                <div class='lc-risk'>2% · ${account_balance*0.02:,.0f}</div>
            </div>
            <div class='lot-card lc-aggressive'>
                <div class='lc-label'>Aggressive</div>
                <div class='lc-value'>{l5:.3f}</div>
                <div class='lc-risk'>5% · ${account_balance*0.05:,.0f}</div>
            </div>
        </div>
        """)

        html("<div class='section-title'>Formula Reference (v3)</div>")
        pip_v = 10.0 if calc.pip_mode == "broker" else 1.0
        html(f"""
        <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
                    border-radius:12px; padding:1rem 1.2rem; font-family:Space Mono,monospace;
                    font-size:0.72rem; line-height:2.1; color:#8899AA;'>
            <span style='color:#D4AF37;'>Risk $</span>         = ${account_balance:,.0f} × {risk_percent_sidebar}% = ${calc.risk_amount:,.2f}<br>
            <span style='color:#82B1FF;'>Lot Size</span>       = ${calc.risk_amount:,.2f} ÷ ({calc.effective_sl_pips:.1f} × ${pip_v}) = {calc.lot_size:.3f}<br>
            <span style='color:#69F0AE;'>Gross Profit</span>   = {tp_pips_sidebar} × {calc.lot_size:.3f} × ${pip_v} = ${calc.profit:,.2f}<br>
            <span style='color:#CE93D8;'>Net Profit</span>     = ${calc.profit:,.2f} − ${calc.commission_total:,.3f} = ${calc.net_profit:,.2f}<br>
            <span style='color:#80DEEA;'>Margin</span>         = ${calc.required_margin:,.2f} ({calc.margin_usage_pct:.1f}% of acct)<br>
            <span style='color:#FFD54F;'>Break-even WR</span>  = {calc.breakeven_win_rate:.1f}%
        </div>
        """)

    # ── Drawdown Table ────────────────────────────────────────────
    html("<div class='section-title'>Consecutive Loss Drawdown Analysis (with Commission Drag)</div>")

    dd_df = calc.drawdown_table(10)

    def color_row(row):
        dd = row["Drawdown %"]
        c = "#69F0AE" if dd < 10 else ("#FFD54F" if dd < 25 else "#FF8A80")
        return [f"color: {c}"] * len(row)

    styled = (
        dd_df.style
        .apply(color_row, axis=1)
        .format({
            "Account Balance ($)":  "${:,.2f}",
            "Total Drawdown ($)":   "${:,.2f}",
            "Drawdown %":           "{:.2f}%",
            "Commission Drag ($)":  "${:,.2f}",
        })
        .set_properties(**{
            "background-color": "rgba(13,31,60,0.6)",
            "border":           "1px solid rgba(212,175,55,0.1)",
            "font-family":      "Space Mono, monospace",
            "font-size":        "0.82rem",
            "text-align":       "center",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "rgba(212,175,55,0.12)"),
                ("color", "#D4AF37"),
                ("font-family", "Poppins, sans-serif"),
                ("font-size", "0.68rem"),
                ("letter-spacing", "0.1em"),
                ("text-transform", "uppercase"),
                ("border", "1px solid rgba(212,175,55,0.2)"),
            ]},
            {"selector": "tr:hover td", "props": [
                ("background-color", "rgba(212,175,55,0.05)"),
            ]},
        ])
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    html("""
    <div class='warning-strip'>
        ⚠️ RISK DISCLOSURE — All calculations are for educational purposes only. 
        Actual results depend on your broker's execution, slippage, and market conditions. 
        Commission drag compounds over time — always factor broker costs into your strategy.
        Past performance does not guarantee future results. Trade responsibly.
    </div>
    """)

    html("""
    <div class='footer'>XAUUSD Risk Management Pro v3 · Live Engine · Not Financial Advice</div>
    """)
