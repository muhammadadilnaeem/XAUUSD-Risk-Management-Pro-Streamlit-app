import streamlit as st
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="XAUUSD Risk Management Pro",
    page_icon="🥇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Deep Navy Fintech Premium Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Poppins:wght@400;500;600;700;800&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #060D1F;
    color: #E8EAF0;
}

/* ── App Background ── */
.stApp {
    background: radial-gradient(ellipse at 20% 0%, #0D1F3C 0%, #060D1F 50%, #060D1F 100%);
    background-attachment: fixed;
}

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1628 0%, #060D1F 100%);
    border-right: 1px solid rgba(212, 175, 55, 0.15);
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* ── Sidebar Labels ── */
[data-testid="stSidebar"] label {
    color: #B8C4D4 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

/* ── Number Inputs & Sliders ── */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input {
    background: rgba(212, 175, 55, 0.05) !important;
    border: 1px solid rgba(212, 175, 55, 0.2) !important;
    border-radius: 8px !important;
    color: #E8EAF0 !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: rgba(212, 175, 55, 0.6) !important;
    box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.12) !important;
}

/* Slider thumb color */
[data-testid="stSlider"] [class*="thumb"] {
    background: #D4AF37 !important;
}
[data-testid="stSlider"] [class*="track"] {
    background: rgba(212, 175, 55, 0.3) !important;
}

/* ── Main Metric Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    padding: 1.5rem 1.2rem;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 16px 16px 0 0;
}
.kpi-gold   { background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(212,175,55,0.04)); }
.kpi-gold::before { background: linear-gradient(90deg, #D4AF37, #FFE082); }

.kpi-blue   { background: linear-gradient(135deg, rgba(41,98,255,0.15), rgba(41,98,255,0.04)); }
.kpi-blue::before { background: linear-gradient(90deg, #2962FF, #82B1FF); }

.kpi-green  { background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,200,83,0.04)); }
.kpi-green::before { background: linear-gradient(90deg, #00C853, #69F0AE); }

.kpi-red    { background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.04)); }
.kpi-red::before { background: linear-gradient(90deg, #FF1744, #FF8A80); }

.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8899AA;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.9rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-gold .kpi-value   { color: #FFD54F; }
.kpi-blue .kpi-value   { color: #82B1FF; }
.kpi-green .kpi-value  { color: #69F0AE; }
.kpi-red .kpi-value    { color: #FF8A80; }
.kpi-sub {
    font-size: 0.72rem;
    color: #566A80;
    font-family: 'Space Mono', monospace;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Poppins', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #D4AF37;
    border-left: 3px solid #D4AF37;
    padding-left: 0.75rem;
    margin: 2rem 0 1rem 0;
}

/* ── RRR Badge ── */
.rrr-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.05));
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 50px;
    padding: 0.5rem 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    color: #D4AF37;
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* ── Lot Suggestion Cards ── */
.lot-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.lot-card {
    background: rgba(255,255,255,0.03);
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.07);
    padding: 1.1rem 1rem;
    text-align: center;
    transition: border-color 0.2s;
}
.lot-card:hover { border-color: rgba(212,175,55,0.35); }
.lot-card .lc-label {
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.4rem;
}
.lot-card .lc-value {
    font-family: 'Space Mono', monospace;
    font-size: 1.35rem;
    font-weight: 700;
    line-height: 1;
}
.lot-card .lc-risk {
    font-size: 0.68rem;
    color: #566A80;
    margin-top: 0.3rem;
    font-family: 'Space Mono', monospace;
}
.lc-conservative .lc-label { color: #69F0AE; }
.lc-conservative .lc-value { color: #69F0AE; }
.lc-moderate     .lc-label { color: #FFD54F; }
.lc-moderate     .lc-value { color: #FFD54F; }
.lc-aggressive   .lc-label { color: #FF8A80; }
.lc-aggressive   .lc-value { color: #FF8A80; }

/* ── Trade Summary Panel ── */
.summary-panel {
    background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.5rem;
}
.summary-panel h3 {
    font-family: 'Poppins', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #D4AF37;
    margin: 0 0 1rem 0;
}
.summary-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.88rem;
}
.summary-row:last-child { border-bottom: none; }
.summary-row .sr-label { color: #8899AA; }
.summary-row .sr-val   { font-family: 'Space Mono', monospace; font-weight: 700; }

/* ── Risk-o-Meter Bar ── */
.risk-bar-wrap {
    background: rgba(255,255,255,0.04);
    border-radius: 8px;
    height: 10px;
    overflow: hidden;
    margin: 0.6rem 0 0.3rem 0;
}
.risk-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.4s ease;
}
.risk-safe     { background: linear-gradient(90deg, #00C853, #69F0AE); }
.risk-moderate { background: linear-gradient(90deg, #FFD54F, #FFA000); }
.risk-danger   { background: linear-gradient(90deg, #FF6D00, #FF1744); }

/* ── Drawdown Table ── */
.dd-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.82rem;
    font-family: 'Space Mono', monospace;
}
.dd-table th {
    background: rgba(212,175,55,0.08);
    color: #D4AF37;
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.6rem 0.8rem;
    text-align: left;
    border-bottom: 1px solid rgba(212,175,55,0.2);
}
.dd-table td {
    padding: 0.55rem 0.8rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    color: #C0CDD8;
}
.dd-table tr:hover td { background: rgba(212,175,55,0.04); }
.dd-table .loss-val { color: #FF8A80; }
.dd-table .safe-val { color: #69F0AE; }

/* ── Warning/Info Boxes ── */
.warn-box {
    background: rgba(255,167,38,0.08);
    border: 1px solid rgba(255,167,38,0.25);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #FFB74D;
    margin-bottom: 0.8rem;
}
.info-box {
    background: rgba(41,98,255,0.08);
    border: 1px solid rgba(41,98,255,0.25);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    font-size: 0.82rem;
    color: #82B1FF;
    margin-bottom: 0.8rem;
}

/* ── Plotly override ── */
.js-plotly-plot .plotly, .js-plotly-plot .plotly div {
    background: transparent !important;
}

/* ── Sidebar gold header ── */
.sidebar-brand {
    text-align: center;
    padding: 0 0 1.5rem 0;
    border-bottom: 1px solid rgba(212,175,55,0.15);
    margin-bottom: 1.5rem;
}
.sidebar-brand span {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.1rem;
    background: linear-gradient(90deg, #D4AF37, #FFE082);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.04em;
}
.sidebar-brand small {
    display: block;
    font-size: 0.62rem;
    color: #566A80;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.15rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DOMAIN MODEL
# ─────────────────────────────────────────────
class XAUUSDCalculator:
    """Core domain model for XAUUSD risk calculations."""

    PIP_VALUE_PER_LOT = 1.0  # $1 per pip per standard lot for XAUUSD

    def __init__(self, account_balance: float, risk_percent: float,
                 sl_pips: float, tp_pips: float):
        self.account_balance = account_balance
        self.risk_percent    = risk_percent
        self.sl_pips         = sl_pips
        self.tp_pips         = tp_pips

    @property
    def risk_amount(self) -> float:
        return (self.account_balance * self.risk_percent) / 100

    @property
    def lot_size(self) -> float:
        if self.sl_pips <= 0:
            return 0.0
        return self.risk_amount / (self.sl_pips * self.PIP_VALUE_PER_LOT)

    @property
    def profit(self) -> float:
        return self.tp_pips * self.lot_size * self.PIP_VALUE_PER_LOT

    @property
    def loss(self) -> float:
        return self.sl_pips * self.lot_size * self.PIP_VALUE_PER_LOT

    @property
    def rrr(self) -> float:
        if self.sl_pips <= 0:
            return 0.0
        return self.tp_pips / self.sl_pips

    @property
    def account_after_win(self) -> float:
        return self.account_balance + self.profit

    @property
    def account_after_loss(self) -> float:
        return self.account_balance - self.loss

    def lot_for_risk(self, pct: float) -> float:
        if self.sl_pips <= 0:
            return 0.0
        return (self.account_balance * pct / 100) / (self.sl_pips * self.PIP_VALUE_PER_LOT)

    def equity_simulation(self, n_trades: int, win_rate: float = 0.5) -> list:
        equity = self.account_balance
        curve  = [equity]
        for _ in range(n_trades):
            if np.random.rand() < win_rate:
                equity += self.profit
            else:
                equity -= self.loss
            curve.append(equity)
        return curve

    def drawdown_table(self, consecutive_losses: int = 10) -> pd.DataFrame:
        rows = []
        equity = self.account_balance
        for i in range(1, consecutive_losses + 1):
            equity -= self.loss
            dd_pct = ((self.account_balance - equity) / self.account_balance) * 100
            rows.append({
                "Consecutive Losses": i,
                "Account Balance ($)": round(equity, 2),
                "Total Drawdown ($)": round(self.loss * i, 2),
                "Drawdown %": round(dd_pct, 2),
            })
        return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div class='sidebar-brand'>
    <span>⚡ XAUUSD RISK PRO</span>
    <small>Professional Risk Engine</small>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### Trade Parameters")

account_balance = st.sidebar.number_input(
    "Account Balance ($)",
    min_value=100.0,
    max_value=10_000_000.0,
    value=10_000.0,
    step=500.0,
    format="%.2f"
)

risk_percent = st.sidebar.number_input(
    "Risk % per Trade",
    min_value=0.1,
    max_value=10.0,
    value=2.0,
    step=0.1,
    format="%.1f"
)

sl_pips = st.sidebar.number_input(
    "Stop Loss (pips)",
    min_value=1,
    max_value=500,
    value=50,
    step=1
)

tp_pips = st.sidebar.number_input(
    "Take Profit (pips)",
    min_value=1,
    max_value=5000,
    value=100,
    step=1
)

# ─────────────────────────────────────────────
# VALIDATION
# ─────────────────────────────────────────────
calc = XAUUSDCalculator(account_balance, risk_percent, sl_pips, tp_pips)

if sl_pips <= 0:
    st.sidebar.error("❌ Stop Loss must be > 0")
if tp_pips <= sl_pips:
    st.sidebar.warning("⚠️ TP < SL — negative risk-reward detected")
if risk_percent >= 5:
    st.sidebar.warning("⚠️ Risk ≥ 5% — high-risk territory")


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<h1 style='
    font-family: Poppins, sans-serif;
    font-weight: 800;
    font-size: 1.7rem;
    background: linear-gradient(90deg, #D4AF37 0%, #FFE082 50%, #D4AF37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
    letter-spacing: -0.01em;
'>XAUUSD Risk Management Pro</h1>
<p style='color:#566A80; font-size:0.82rem; letter-spacing:0.1em;
    text-transform:uppercase; margin-top:0.3rem; margin-bottom:2rem;'>
    Precision Risk Engine &nbsp;·&nbsp; Gold Trading &nbsp;·&nbsp; Professional Grade
</p>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
st.markdown(f"""
<div class='kpi-grid'>
    <div class='kpi-card kpi-blue'>
        <div class='kpi-label'>Lot Size</div>
        <div class='kpi-value'>{calc.lot_size:.3f}</div>
        <div class='kpi-sub'>Standard Lots</div>
    </div>
    <div class='kpi-card kpi-gold'>
        <div class='kpi-label'>Risk Amount</div>
        <div class='kpi-value'>${calc.risk_amount:,.2f}</div>
        <div class='kpi-sub'>{risk_percent}% of account</div>
    </div>
    <div class='kpi-card kpi-green'>
        <div class='kpi-label'>Profit if TP Hit</div>
        <div class='kpi-value'>${calc.profit:,.2f}</div>
        <div class='kpi-sub'>+{(calc.profit/account_balance*100):.2f}% return</div>
    </div>
    <div class='kpi-card kpi-red'>
        <div class='kpi-label'>Loss if SL Hit</div>
        <div class='kpi-value'>${calc.loss:,.2f}</div>
        <div class='kpi-sub'>-{(calc.loss/account_balance*100):.2f}% drawdown</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# RRR + RISK BAR
# ─────────────────────────────────────────────
col_rrr, col_riskbar = st.columns([1, 2])

with col_rrr:
    rrr_color = "#69F0AE" if calc.rrr >= 2 else ("#FFD54F" if calc.rrr >= 1 else "#FF8A80")
    st.markdown(f"""
    <div style='padding:1rem 0;'>
        <div class='section-title'>Risk / Reward</div>
        <div style='font-family:Space Mono,monospace; font-size:2.4rem;
                    font-weight:700; color:{rrr_color}; line-height:1;'>
            1 : {calc.rrr:.2f}
        </div>
        <div style='color:#566A80; font-size:0.75rem; margin-top:0.4rem;'>
            {"✅ Excellent RRR" if calc.rrr >= 2 else ("⚠️ Acceptable RRR" if calc.rrr >= 1 else "❌ Negative RRR")}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_riskbar:
    bar_class = "risk-safe" if risk_percent <= 2 else ("risk-moderate" if risk_percent <= 4 else "risk-danger")
    bar_label = "🟢 Safe Zone" if risk_percent <= 2 else ("🟡 Caution Zone" if risk_percent <= 4 else "🔴 Danger Zone")
    st.markdown(f"""
    <div style='padding:1rem 0;'>
        <div class='section-title'>Risk-o-Meter</div>
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
            <span style='font-size:0.78rem; color:#8899AA;'>{bar_label}</span>
            <span style='font-family:Space Mono,monospace; font-size:0.9rem; color:#D4AF37; font-weight:700;'>{risk_percent}%</span>
        </div>
        <div class='risk-bar-wrap'>
            <div class='risk-bar-fill {bar_class}' style='width:{min(risk_percent*10, 100)}%;'></div>
        </div>
        <div style='display:flex; justify-content:space-between; font-size:0.6rem; color:#566A80; margin-top:0.25rem;'>
            <span>0%</span><span>2% Safe</span><span>5% Risky</span><span>10%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TRADE SUMMARY + LOT SUGGESTIONS
# ─────────────────────────────────────────────
col_summ, col_lots = st.columns([1, 1])

with col_summ:
    st.markdown("<div class='section-title'>Trade Summary</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='summary-panel'>
        <h3>📋 Position Overview</h3>
        <div class='summary-row'>
            <span class='sr-label'>Account Balance</span>
            <span class='sr-val' style='color:#E8EAF0;'>${account_balance:,.2f}</span>
        </div>
        <div class='summary-row'>
            <span class='sr-label'>You are risking</span>
            <span class='sr-val' style='color:#FFD54F;'>${calc.risk_amount:,.2f} ({risk_percent}%)</span>
        </div>
        <div class='summary-row'>
            <span class='sr-label'>Position Size</span>
            <span class='sr-val' style='color:#82B1FF;'>{calc.lot_size:.3f} lots</span>
        </div>
        <div class='summary-row'>
            <span class='sr-label'>Stop Loss</span>
            <span class='sr-val' style='color:#FF8A80;'>{sl_pips} pips → -${calc.loss:,.2f}</span>
        </div>
        <div class='summary-row'>
            <span class='sr-label'>Take Profit</span>
            <span class='sr-val' style='color:#69F0AE;'>{tp_pips} pips → +${calc.profit:,.2f}</span>
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
    """, unsafe_allow_html=True)

with col_lots:
    st.markdown("<div class='section-title'>Lot Size Suggestions</div>", unsafe_allow_html=True)
    l1 = calc.lot_for_risk(1)
    l2 = calc.lot_for_risk(2)
    l5 = calc.lot_for_risk(5)
    st.markdown(f"""
    <div class='lot-row'>
        <div class='lot-card lc-conservative'>
            <div class='lc-label'>Conservative</div>
            <div class='lc-value'>{l1:.3f}</div>
            <div class='lc-risk'>1% Risk · ${account_balance*0.01:,.0f}</div>
        </div>
        <div class='lot-card lc-moderate'>
            <div class='lc-label'>Moderate</div>
            <div class='lc-value'>{l2:.3f}</div>
            <div class='lc-risk'>2% Risk · ${account_balance*0.02:,.0f}</div>
        </div>
        <div class='lot-card lc-aggressive'>
            <div class='lc-label'>Aggressive</div>
            <div class='lc-value'>{l5:.3f}</div>
            <div class='lc-risk'>5% Risk · ${account_balance*0.05:,.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formula Reference
    st.markdown("<div class='section-title'>Formula Reference</div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
                border-radius:12px; padding:1rem 1.2rem; font-family:Space Mono,monospace;
                font-size:0.75rem; line-height:2; color:#8899AA;'>
        <span style='color:#D4AF37;'>Risk $</span>    = Balance × Risk% / 100<br>
        <span style='color:#82B1FF;'>Lot Size</span>  = Risk$ / (SL pips × $1)<br>
        <span style='color:#69F0AE;'>Profit</span>    = TP pips × Lot × $1<br>
        <span style='color:#FF8A80;'>Loss</span>      = SL pips × Lot × $1<br>
        <span style='color:#FFD54F;'>RRR</span>       = TP pips / SL pips
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:2.5rem 0 1rem 0; color:#2A3A4A;
            font-size:0.7rem; letter-spacing:0.12em; text-transform:uppercase;'>
    XAUUSD Risk Management Pro &nbsp;·&nbsp; For Educational Purposes Only &nbsp;·&nbsp;
    Not Financial Advice
</div>
""", unsafe_allow_html=True)