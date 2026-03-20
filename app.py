
import streamlit as st
import pandas as pd
import numpy as np
import textwrap

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="XAUUSD Pro Suite v4",
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
# GLOBAL CSS — v4: Full dark-mode widget override
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* ── CSS VARIABLES ───────────────────────────────────────── */
:root {
    --navy-950:      #03080F;
    --navy-900:      #060D1F;
    --navy-800:      #091628;
    --navy-700:      #0D1F3C;
    --navy-600:      #122845;
    --gold:          #D4AF37;
    --gold-light:    #FFE082;
    --gold-dim:      #FFD54F;
    --gold-muted:    rgba(212,175,55,0.15);
    --blue:          #82B1FF;
    --green:         #69F0AE;
    --red:           #FF8A80;
    --purple:        #CE93D8;
    --cyan:          #80DEEA;
    --text-1:        #EDF0F7;
    --text-2:        #8899AA;
    --text-3:        #4A5C70;
    --glass:         rgba(9,22,40,0.85);
    --glass-border:  rgba(212,175,55,0.10);
    --input-bg:      #091628;
    --input-border:  rgba(212,175,55,0.18);
    --input-border-focus: rgba(212,175,55,0.65);
    --shadow-card:   0 8px 40px rgba(0,0,0,0.6), 0 1px 0 rgba(212,175,55,0.06) inset;
}

/* ── RESET ──────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
    background-color: var(--navy-950) !important;
    color: var(--text-1) !important;
}

/* ── APP BACKGROUND ─────────────────────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 10% -10%, rgba(13,31,60,0.9) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(212,175,55,0.04) 0%, transparent 60%),
        var(--navy-950);
    background-attachment: fixed;
}

/* Subtle grid overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(212,175,55,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(212,175,55,0.018) 1px, transparent 1px);
    background-size: 52px 52px;
    pointer-events: none;
    z-index: 0;
}

#MainMenu, footer, header { visibility: hidden; }

/* ── SIDEBAR ────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060D1F 0%, #03080F 100%) !important;
    border-right: 1px solid rgba(212,175,55,0.12) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stRadio label {
    color: #8899AA !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px !important;
}
[data-testid="stSidebar"] .stRadio > div > label {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
    color: #8899AA !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    text-transform: none !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}
[data-testid="stSidebar"] .stRadio > div > label:hover {
    border-color: rgba(212,175,55,0.35) !important;
    color: #D4AF37 !important;
    background: rgba(212,175,55,0.05) !important;
}
[data-testid="stSidebar"] .stRadio > div > label[data-baseweb="radio"] input:checked + div,
[data-testid="stSidebar"] .stRadio [aria-checked="true"] {
    color: #D4AF37 !important;
}

/* ── ALL INPUT FIELDS — DARK OVERRIDE ──────────────────── */
/* Number inputs */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
input[type="number"],
input[type="text"] {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 10px !important;
    color: var(--text-1) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    box-shadow: none !important;
    -webkit-text-fill-color: var(--text-1) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: var(--input-border-focus) !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.10) !important;
    outline: none !important;
}
/* Number input +/- button area */
[data-testid="stNumberInput"] > div {
    background: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}
[data-testid="stNumberInput"] > div > div {
    background: transparent !important;
}
[data-testid="stNumberInput"] button {
    background: rgba(212,175,55,0.08) !important;
    border: none !important;
    border-left: 1px solid rgba(212,175,55,0.1) !important;
    color: var(--gold) !important;
    transition: background 0.15s !important;
}
[data-testid="stNumberInput"] button:hover {
    background: rgba(212,175,55,0.18) !important;
}
[data-testid="stNumberInput"] button svg {
    fill: var(--gold) !important;
    color: var(--gold) !important;
}

/* ── SELECTBOX — DARK OVERRIDE ──────────────────────────── */
[data-testid="stSelectbox"] > div > div,
.stSelectbox > div > div,
div[data-baseweb="select"] > div {
    background: var(--input-bg) !important;
    background-color: var(--input-bg) !important;
    border: 1px solid var(--input-border) !important;
    border-radius: 10px !important;
    color: var(--text-1) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}
[data-testid="stSelectbox"] > div > div:hover,
div[data-baseweb="select"] > div:hover {
    border-color: rgba(212,175,55,0.45) !important;
}
div[data-baseweb="select"] svg {
    fill: var(--gold) !important;
    color: var(--gold) !important;
}
/* Dropdown menu itself */
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[data-baseweb="menu"] {
    background: #0A1628 !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 12px !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.7) !important;
}
li[role="option"],
[data-baseweb="menu"] li {
    background: transparent !important;
    color: var(--text-2) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 10px 16px !important;
    transition: all 0.15s !important;
}
li[role="option"]:hover,
[data-baseweb="menu"] li:hover {
    background: rgba(212,175,55,0.08) !important;
    color: var(--gold) !important;
}
li[aria-selected="true"] {
    background: rgba(212,175,55,0.12) !important;
    color: var(--gold) !important;
}

/* ── RADIO BUTTONS ──────────────────────────────────────── */
.stRadio > div {
    gap: 8px !important;
}
.stRadio > div > label {
    background: rgba(9,22,40,0.7) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    color: var(--text-2) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    text-transform: none !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.18s ease !important;
}
.stRadio > div > label:hover {
    border-color: rgba(212,175,55,0.4) !important;
    color: var(--gold) !important;
    background: rgba(212,175,55,0.06) !important;
}
/* Radio circle */
.stRadio > div > label > div:first-child {
    border-color: rgba(212,175,55,0.4) !important;
}
.stRadio > div > label > div:first-child > div {
    background: var(--gold) !important;
}

/* ── SLIDERS ────────────────────────────────────────────── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
}
.stSlider > div > div > div > div > div {
    background: #fff !important;
    border: 2px solid var(--gold) !important;
    box-shadow: 0 0 14px rgba(212,175,55,0.6) !important;
    width: 18px !important;
    height: 18px !important;
}

/* ── BUTTONS ────────────────────────────────────────────── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #122845 0%, rgba(212,175,55,0.85) 100%) !important;
    color: #fff !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    cursor: pointer !important;
    transition: all 0.22s ease !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(212,175,55,0.38) !important;
    background: linear-gradient(135deg, #122845 0%, #FFE082 100%) !important;
}

/* ── DATAFRAME ──────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden !important;
    border: 1px solid rgba(212,175,55,0.1) !important;
}
[data-testid="stDataFrame"] table {
    background: rgba(6,13,31,0.9) !important;
}
[data-testid="stDataFrame"] th {
    background: rgba(212,175,55,0.08) !important;
    color: #D4AF37 !important;
}
[data-testid="stDataFrame"] td {
    color: var(--text-1) !important;
    background: transparent !important;
}

/* ── DIVIDERS ───────────────────────────────────────────── */
hr { border-color: rgba(212,175,55,0.1) !important; }

/* ── SECTION LABELS ─────────────────────────────────────── */
.section-label {
    display: block;
    font-size: 0.63rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    border-left: 3px solid var(--gold);
    padding-left: 0.75rem;
    margin: 1.4rem 0 0.85rem 0;
    opacity: 0.9;
}
.section-title {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--gold);
    border-left: 3px solid var(--gold);
    padding-left: 0.75rem;
    margin: 2rem 0 1.1rem 0;
    display: block;
}

/* ── CARDS ──────────────────────────────────────────────── */
.calc-card {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 28px 24px;
    position: relative;
    box-shadow: var(--shadow-card);
    margin-bottom: 16px;
    backdrop-filter: blur(16px);
}
.calc-card::after {
    content: '';
    position: absolute;
    top: 0; left: 24px; right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.45), transparent);
    border-radius: 1px;
}

.result-outer {
    background: linear-gradient(145deg, rgba(212,175,55,0.07) 0%, rgba(6,13,31,0.97) 100%);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 20px;
    padding: 32px 24px 28px;
    position: relative;
    box-shadow: var(--shadow-card);
    margin-top: 0;
    animation: fadeSlideUp 0.3s cubic-bezier(0.22,1,0.36,1);
    backdrop-filter: blur(16px);
}
.result-outer::after {
    content: '';
    position: absolute;
    top: 0; left: 24px; right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── LOT SIZE DISPLAY ───────────────────────────────────── */
.lot-label { font-family: 'Space Mono', monospace; font-size: 9px; letter-spacing: 6px; color: var(--text-3); text-align: center; margin-bottom: 6px; text-transform: uppercase; }
.lot-value {
    font-family: 'Space Mono', monospace;
    font-size: clamp(52px,10vw,88px);
    font-weight: 700;
    line-height: 1;
    text-align: center;
    background: linear-gradient(140deg, #fff 0%, #FFE082 45%, var(--gold-dim) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 32px rgba(212,175,55,0.28));
    letter-spacing: -2px;
}
.lot-unit { font-family: 'Poppins', sans-serif; font-size: 10px; font-weight: 700; letter-spacing: 6px; color: var(--text-2); text-align: center; text-transform: uppercase; margin-top: 6px; }

/* ── STATS ROW ──────────────────────────────────────────── */
.stats-divider { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.18), transparent); margin: 20px 0; }
.stats-row { display: flex; justify-content: space-around; gap: 6px; flex-wrap: wrap; }
.stat-item { text-align: center; flex: 1; min-width: 70px; background: rgba(212,175,55,0.03); border: 1px solid rgba(212,175,55,0.08); border-radius: 10px; padding: 10px 6px; transition: border-color 0.2s; }
.stat-item:hover { border-color: rgba(212,175,55,0.2); }
.stat-val { font-family: 'Space Mono', monospace; font-size: 13px; font-weight: 700; color: var(--text-1); }
.stat-lbl { font-size: 8px; font-weight: 600; letter-spacing: 0.12em; color: var(--text-3); text-transform: uppercase; margin-top: 4px; }

/* ── COST BREAKDOWN ─────────────────────────────────────── */
.cost-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.8rem; }
.cost-row:last-child { border-bottom: none; }
.cost-label { color: var(--text-2); }
.cost-val { font-family: 'Space Mono', monospace; font-weight: 700; }
.cost-block { background: rgba(0,0,0,0.25); border-radius: 12px; padding: 12px 14px; border: 1px solid rgba(255,255,255,0.04); }

/* ── VALIDATION BADGES ──────────────────────────────────── */
.val-ok    { display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:9px;font-size:0.72rem;font-weight:600;background:rgba(105,240,174,0.07);border:1px solid rgba(105,240,174,0.2);color:#69F0AE;margin:4px 0;width:100%; }
.val-warn  { display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:9px;font-size:0.72rem;font-weight:600;background:rgba(255,213,79,0.07);border:1px solid rgba(255,213,79,0.22);color:#FFD54F;margin:4px 0;width:100%; }
.val-danger{ display:inline-flex;align-items:center;gap:8px;padding:9px 14px;border-radius:9px;font-size:0.72rem;font-weight:600;background:rgba(255,138,128,0.07);border:1px solid rgba(255,138,128,0.22);color:#FF8A80;margin:4px 0;width:100%; }

/* ── KPI CARDS ──────────────────────────────────────────── */
.kpi-card {
    position: relative; overflow: hidden; border-radius: 14px;
    padding: 1.3rem 1.1rem; border: 1px solid rgba(255,255,255,0.05);
    transition: transform 0.2s, border-color 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); }
.kpi-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; border-radius:14px 14px 0 0; }
.kpi-gold  { background: linear-gradient(135deg, rgba(212,175,55,0.11), rgba(212,175,55,0.03)); }
.kpi-gold::before  { background: linear-gradient(90deg, #D4AF37, #FFE082); }
.kpi-blue  { background: linear-gradient(135deg, rgba(41,98,255,0.14), rgba(41,98,255,0.03)); }
.kpi-blue::before  { background: linear-gradient(90deg, #2962FF, #82B1FF); }
.kpi-green { background: linear-gradient(135deg, rgba(0,200,83,0.13), rgba(0,200,83,0.03)); }
.kpi-green::before { background: linear-gradient(90deg, #00C853, #69F0AE); }
.kpi-red   { background: linear-gradient(135deg, rgba(255,23,68,0.13), rgba(255,23,68,0.03)); }
.kpi-red::before   { background: linear-gradient(90deg, #FF1744, #FF8A80); }
.kpi-purple{ background: linear-gradient(135deg, rgba(170,0,255,0.12), rgba(170,0,255,0.03)); }
.kpi-purple::before{ background: linear-gradient(90deg, #AA00FF, #CE93D8); }
.kpi-cyan  { background: linear-gradient(135deg, rgba(0,229,255,0.11), rgba(0,229,255,0.03)); }
.kpi-cyan::before  { background: linear-gradient(90deg, #00B8D4, #80DEEA); }
.kpi-label { font-size: 0.62rem; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--text-2); margin-bottom: 0.45rem; }
.kpi-value { font-family: 'Space Mono', monospace; font-size: 1.45rem; font-weight: 700; line-height: 1; margin-bottom: 0.3rem; }
.kpi-gold .kpi-value   { color: #FFD54F; }
.kpi-blue .kpi-value   { color: #82B1FF; }
.kpi-green .kpi-value  { color: #69F0AE; }
.kpi-red .kpi-value    { color: #FF8A80; }
.kpi-purple .kpi-value { color: #CE93D8; }
.kpi-cyan .kpi-value   { color: #80DEEA; }
.kpi-sub { font-size: 0.67rem; color: var(--text-3); font-family: 'Space Mono', monospace; }

/* ── RISK BAR ───────────────────────────────────────────── */
.risk-bar-wrap { background: rgba(255,255,255,0.05); border-radius: 99px; height: 9px; overflow: hidden; margin: 0.55rem 0 0.3rem 0; }
.risk-bar-fill  { height: 100%; border-radius: 99px; transition: width 0.5s ease; }
.risk-safe    { background: linear-gradient(90deg, #00C853, #69F0AE); }
.risk-moderate{ background: linear-gradient(90deg, #FFD54F, #FFA000); }
.risk-danger  { background: linear-gradient(90deg, #FF6D00, #FF1744); }

/* ── MARGIN METER ───────────────────────────────────────── */
.margin-meter { background: rgba(255,255,255,0.05); border-radius: 99px; height: 7px; overflow: hidden; margin: 6px 0; }
.margin-fill  { height: 100%; border-radius: 99px; }

/* ── SUMMARY PANEL ──────────────────────────────────────── */
.summary-panel {
    background: linear-gradient(145deg, rgba(212,175,55,0.06), rgba(6,13,31,0.98));
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 16px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1.4rem;
}
.summary-panel h3 { font-size: 0.7rem; letter-spacing: 0.14em; text-transform: uppercase; color: #D4AF37; margin: 0 0 0.85rem 0; }
.summary-row { display: flex; justify-content: space-between; align-items: center; padding: 0.45rem 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.84rem; }
.summary-row:last-child { border-bottom: none; }
.summary-row .sr-label { color: var(--text-2); }
.summary-row .sr-val   { font-family: 'Space Mono', monospace; font-weight: 700; }

/* ── LOT SUGGESTION CARDS ───────────────────────────────── */
.lot-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 0.85rem; margin-bottom: 1.4rem; }
.lot-card { background: rgba(255,255,255,0.025); border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); padding: 1.1rem 0.9rem; text-align: center; transition: all 0.2s; }
.lot-card:hover { transform: translateY(-2px); }
.lot-card .lc-label { font-size: 0.6rem; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem; }
.lot-card .lc-value { font-family: 'Space Mono', monospace; font-size: 1.25rem; font-weight: 700; line-height: 1; }
.lot-card .lc-risk  { font-size: 0.64rem; color: var(--text-3); margin-top: 0.35rem; font-family: 'Space Mono', monospace; }
.lc-conservative { border-color: rgba(105,240,174,0.2) !important; }
.lc-conservative:hover { border-color: rgba(105,240,174,0.45) !important; }
.lc-conservative .lc-label, .lc-conservative .lc-value { color: #69F0AE; }
.lc-moderate { border-color: rgba(255,213,79,0.2) !important; }
.lc-moderate:hover { border-color: rgba(255,213,79,0.45) !important; }
.lc-moderate .lc-label, .lc-moderate .lc-value { color: #FFD54F; }
.lc-aggressive { border-color: rgba(255,138,128,0.2) !important; }
.lc-aggressive:hover { border-color: rgba(255,138,128,0.45) !important; }
.lc-aggressive .lc-label, .lc-aggressive .lc-value { color: #FF8A80; }

/* ── EXPLAINER SECTIONS ─────────────────────────────────── */
.exp-section {
    background: var(--glass);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 26px 24px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
}
.exp-section::after {
    content: '';
    position: absolute;
    top: 0; left: 24px; right: 24px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(212,175,55,0.38), transparent);
}
.exp-title    { font-size: 1.05rem; font-weight: 700; color: var(--gold-light); margin-bottom: 0.4rem; }
.exp-subtitle { font-family: 'Space Mono', monospace; font-size: 0.64rem; letter-spacing: 0.16em; color: var(--text-3); text-transform: uppercase; margin-bottom: 1.1rem; }
.exp-body     { font-size: 0.86rem; line-height: 1.85; color: var(--text-2); }
.formula-block {
    background: rgba(3,8,15,0.9);
    border: 1px solid rgba(212,175,55,0.13);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    line-height: 2.3;
    color: var(--text-2);
    margin-top: 1rem;
}

/* ── LIVE INDICATOR ─────────────────────────────────────── */
.live-dot {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(105,240,174,0.07);
    border: 1px solid rgba(105,240,174,0.2);
    border-radius: 999px;
    padding: 5px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    color: #69F0AE;
    text-transform: uppercase;
}
.live-dot-inner {
    width: 6px; height: 6px; border-radius: 50%;
    background: #69F0AE;
    box-shadow: 0 0 8px #69F0AE;
    animation: pulse 1.6s ease infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.3; transform: scale(0.8); }
}

/* ── SIDEBAR BRAND ──────────────────────────────────────── */
.sidebar-brand {
    text-align: center;
    padding: 0 0 1.4rem 0;
    border-bottom: 1px solid rgba(212,175,55,0.12);
    margin-bottom: 1.4rem;
}
.sidebar-brand span {
    font-family: 'Poppins', sans-serif;
    font-weight: 800;
    font-size: 1.0rem;
    background: linear-gradient(90deg, #D4AF37, #FFE082);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 0.03em;
}
.sidebar-brand small {
    display: block;
    font-size: 0.58rem;
    color: var(--text-3);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-top: 0.18rem;
}

/* ── WARNING / FOOTER ───────────────────────────────────── */
.warning-strip {
    background: rgba(212,175,55,0.04);
    border: 1px solid rgba(212,175,55,0.12);
    border-left: 3px solid rgba(212,175,55,0.5);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 16px;
    font-size: 11px;
    color: var(--text-3);
    line-height: 1.75;
}
.footer {
    text-align: center;
    margin-top: 48px;
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 4px;
    color: var(--text-3);
    opacity: 0.5;
    text-transform: uppercase;
    padding-bottom: 2rem;
}

/* ── EMPTY STATE ────────────────────────────────────────── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 300px;
    opacity: 0.3;
    text-align: center;
    border: 1px dashed rgba(212,175,55,0.15);
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DOMAIN MODEL
# ─────────────────────────────────────────────
class XAUUSDCalculatorV4:
    CONTRACT_SIZE = 100  # oz per standard lot

    def __init__(
        self,
        account_balance: float,
        risk_percent:    float,
        sl_pips:         float,
        tp_pips:         float,
        pip_mode:        str   = "standard",
        spread_points:   float = 0.0,
        commission_lot:  float = 0.0,
        leverage:        int   = 100,
        entry_price:     float = 0.0,
        sl_price:        float = 0.0,
        tp_price:        float = 0.0,
        use_price_mode:  bool  = False,
        trade_direction: str   = "buy",
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

    @property
    def pip_value_per_lot(self) -> float:
        return 10.0 if self.pip_mode == "broker" else 1.0

    @property
    def sl_distance_price(self) -> float:
        if self.use_price_mode and self.entry_price > 0 and self.sl_price > 0:
            return abs(self.entry_price - self.sl_price)
        return 0.0

    @property
    def tp_distance_price(self) -> float:
        if self.use_price_mode and self.entry_price > 0 and self.tp_price > 0:
            return abs(self.entry_price - self.tp_price)
        return 0.0

    @property
    def effective_sl_pips(self) -> float:
        if self.use_price_mode:
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

    @property
    def risk_amount(self) -> float:
        return (self.account_balance * self.risk_percent) / 100

    @property
    def lot_size(self) -> float:
        if self.use_price_mode:
            if self.sl_distance_price <= 0:
                return 0.0
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
        return self.risk_amount

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
        if self.use_price_mode:
            return self.tp_distance_price / self.sl_distance_price if self.sl_distance_price > 0 else 0.0
        return self.effective_tp_pips / self.effective_sl_pips if self.effective_sl_pips > 0 else 0.0

    @property
    def required_margin(self) -> float:
        price = self.entry_price if self.use_price_mode and self.entry_price > 0 else 2330.0
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
        return (1 / (1 + self.rrr)) * 100 if self.rrr > 0 else 100.0

    @property
    def risk_tier(self) -> str:
        if self.risk_percent <= 2: return "CONSERVATIVE"
        elif self.risk_percent <= 4: return "MODERATE"
        return "AGGRESSIVE"

    def validate(self) -> list:
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

    def lot_for_risk(self, pct: float) -> float:
        if self.use_price_mode:
            if self.sl_distance_price <= 0: return 0.0
            return (self.account_balance * pct / 100) / (self.effective_sl_pips * self.CONTRACT_SIZE)
        else:
            if self.effective_sl_pips <= 0: return 0.0
            return (self.account_balance * pct / 100) / (self.effective_sl_pips * self.pip_value_per_lot)

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
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    html("""
    <div class='sidebar-brand'>
        <span>⚡ XAUUSD PRO SUITE</span>
        <small>v4 · Dark Engine</small>
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
        help="Typical XAUUSD spread: 20–50 points."
    )
    commission_sidebar = st.number_input(
        "Commission per Lot ($)", min_value=0.0, max_value=50.0, value=0.0, step=0.5,
        help="ECN brokers charge per round-turn lot."
    )

    if sl_pips_sidebar <= 0:
        st.error("❌ Stop Loss must be > 0")
    if risk_percent_sidebar >= 5:
        st.warning("⚠️ Risk ≥ 5% — high-risk territory")


# Default calc
calc = XAUUSDCalculatorV4(
    account_balance=account_balance,
    risk_percent=risk_percent_sidebar,
    sl_pips=sl_pips_sidebar,
    tp_pips=tp_pips_sidebar,
    spread_points=spread_sidebar,
    commission_lot=commission_sidebar,
    leverage=leverage_sidebar,
    use_price_mode=False,
)


# ══════════════════════════════════════════════════════════════════
#  PAGE 1 — EXPLAINER
# ══════════════════════════════════════════════════════════════════
if page == "📖  Explainer":

    html("""
    <div style='padding:36px 0 28px;'>
        <div style='display:inline-flex; align-items:center; gap:6px;
                    background:rgba(212,175,55,0.07); border:1px solid rgba(212,175,55,0.2);
                    border-radius:999px; padding:5px 16px; font-family:Space Mono,monospace;
                    font-size:9px; letter-spacing:3px; color:#D4AF37; text-transform:uppercase; margin-bottom:18px;'>
            <span style='width:5px;height:5px;border-radius:50%;background:#D4AF37;
                         box-shadow:0 0 8px #D4AF37; animation:pulse 2s ease infinite; display:inline-block;'></span>
            Knowledge Base · v4
        </div>
        <h1 style='font-family:Poppins,sans-serif; font-size:clamp(26px,5vw,44px); font-weight:800;
                   background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   margin:0 0 10px; line-height:1.1;'>How It All Works</h1>
        <p style='color:#566A80; font-size:13px; max-width:560px;'>
            Complete formula reference for XAUUSD Pro Suite v4 — price-mode, spread, commission & margin modules.
        </p>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v4 · Pip Definition Problem</div>
        <div class='exp-title'>🔍 Why Pip Definitions Matter</div>
        <div class='exp-body'>
            The most dangerous mistake in XAUUSD trading tools is ambiguous pip definitions.
            There are <strong style='color:#E8EAF0;'>two industry conventions</strong> — confusing them gives you a lot size
            that is <strong style='color:#FF8A80;'>10× too small or too large</strong>.
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem;'>
            <div style='background:rgba(130,177,255,0.06); border:1px solid rgba(130,177,255,0.18); border-radius:12px; padding:1.2rem;'>
                <div style='color:#82B1FF; font-weight:700; font-size:0.82rem; letter-spacing:0.07em; margin-bottom:0.5rem;'>📌 Standard / cTrader</div>
                <div style='font-family:Space Mono,monospace; font-size:0.78rem; color:#8899AA; line-height:2.1;'>
                    1 pip = 0.01 price move<br>
                    Value = $1 per standard lot<br>
                    SL 50 pips = 0.50 move
                </div>
            </div>
            <div style='background:rgba(255,213,79,0.06); border:1px solid rgba(255,213,79,0.18); border-radius:12px; padding:1.2rem;'>
                <div style='color:#FFD54F; font-weight:700; font-size:0.82rem; letter-spacing:0.07em; margin-bottom:0.5rem;'>📌 Broker / MT4·MT5</div>
                <div style='font-family:Space Mono,monospace; font-size:0.78rem; color:#8899AA; line-height:2.1;'>
                    1 pip = 0.10 price move<br>
                    Value = $10 per standard lot<br>
                    SL 50 pips = 5.00 move
                </div>
            </div>
        </div>
        <div class='formula-block'>
            <span style='color:#FFD54F;'>Best practice:</span> use <span style='color:#69F0AE;'>Price-Based Mode</span> to eliminate ambiguity entirely.
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v4 · Institutional Approach</div>
        <div class='exp-title'>🏦 Price-Based Calculation (Most Accurate)</div>
        <div class='exp-body'>
            Enter actual <strong style='color:#E8EAF0;'>price levels</strong>. The calculator derives
            the dollar distance automatically — completely broker-agnostic.
        </div>
        <div class='formula-block'>
            <span style='color:#8899AA;'>Given: Entry = 2330.00 · SL = 2320.00 · TP = 2360.00</span><br><br>
            <span style='color:#FFD54F;'>SL Distance</span>  = |Entry − SL| = |2330 − 2320| = <span style='color:#FF8A80;'>10.00 pts</span><br>
            <span style='color:#69F0AE;'>TP Distance</span>  = |Entry − TP| = |2330 − 2360| = <span style='color:#69F0AE;'>30.00 pts</span><br>
            <span style='color:#82B1FF;'>Lot Size</span>      = Risk$ ÷ (SL × 100) = 200 ÷ (10 × 100) = <span style='color:#82B1FF;'>0.200 lots</span><br>
            <span style='color:#FFD54F;'>RRR</span>           = TP ÷ SL = 30 ÷ 10 = <span style='color:#D4AF37;'>1 : 3.00</span>
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v4 · Hidden Costs</div>
        <div class='exp-title'>💸 Spread & Commission Impact</div>
        <div class='exp-body'>Every trade has hidden costs that inflate your real risk.</div>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:1rem;'>
            <div style='background:rgba(206,147,216,0.06); border:1px solid rgba(206,147,216,0.18); border-radius:12px; padding:1.2rem;'>
                <div style='color:#CE93D8; font-weight:700; font-size:0.82rem; margin-bottom:0.5rem;'>📊 Spread</div>
                <div style='color:#8899AA; font-size:0.8rem; line-height:1.8;'>Typical: 20–50 points.<br>Effective SL = your SL + spread.</div>
            </div>
            <div style='background:rgba(128,222,234,0.06); border:1px solid rgba(128,222,234,0.18); border-radius:12px; padding:1.2rem;'>
                <div style='color:#80DEEA; font-weight:700; font-size:0.82rem; margin-bottom:0.5rem;'>💰 Commission</div>
                <div style='color:#8899AA; font-size:0.8rem; line-height:1.8;'>ECN: $3–7 per lot.<br>Reduces net profit on TP hits.</div>
            </div>
        </div>
        <div class='formula-block'>
            <span style='color:#CE93D8;'>Net Profit</span> = Gross Profit − (Commission × Lots)<br>
            <span style='color:#FF8A80;'>Net Loss</span>   = Risk Amount + (Commission × Lots)
        </div>
    </div>
    """)

    html("""
    <div class='exp-section'>
        <div class='exp-subtitle'>v4 · Margin Awareness</div>
        <div class='exp-title'>📈 Margin & Leverage</div>
        <div class='formula-block'>
            <span style='color:#80DEEA;'>Required Margin</span> = (Lot × 100 oz × Gold Price) ÷ Leverage<br>
            <span style='color:#CE93D8;'>Margin Usage %</span>  = Required Margin ÷ Account Balance × 100<br><br>
            <span style='color:#8899AA;'>Example: 0.20 lots · Gold @ $2,330 · 1:100 leverage</span><br>
            Margin = (0.20 × 100 × 2330) ÷ 100 = <span style='color:#80DEEA;'>$466</span>  (4.66%)
        </div>
    </div>
    """)

    html('<div class="footer">XAUUSD Pro Suite v4 · Knowledge Base · For Educational Purposes Only</div>')


# ══════════════════════════════════════════════════════════════════
#  PAGE 2 — POSITION CALCULATOR
# ══════════════════════════════════════════════════════════════════
elif page == "🧮  Position Calculator":

    html("""
    <div style='text-align:center; padding:36px 24px 24px;'>
        <div class='live-dot' style='margin:0 auto 16px; width:fit-content;'>
            <span class='live-dot-inner'></span> Live · Auto-Calculates
        </div>
        <div style='font-family:Poppins,sans-serif; font-size:clamp(26px,6vw,46px); font-weight:800;
                    background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1;'>
            Position Calculator
        </div>
        <div style='color:#4A5C70; font-size:12px; margin-top:8px; letter-spacing:0.06em;'>
            XAU/USD · Professional Risk Management · v4
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
            index=0, horizontal=True,
        )
        use_price_mode = calc_mode.startswith("📍")

        if not use_price_mode:
            html('<span class="section-label" style="margin-top:12px;">Pip Convention</span>')
            pip_mode_sel = st.radio(
                "Pip Definition",
                options=["Standard (0.01 = $1/lot)", "Broker MT4/MT5 (0.10 = $10/lot)"],
                index=0, horizontal=True
            )
            pip_mode = "broker" if "Broker" in pip_mode_sel else "standard"
        else:
            pip_mode = "standard"

        html('<span class="section-label" style="margin-top:16px;">02 · Account</span>')
        c1, c2 = st.columns(2)
        with c1:
            balance_p2 = st.number_input("Account Balance ($)", value=account_balance,
                                          step=500.0, min_value=100.0, key="bal_p2")
        with c2:
            risk_pct_p2 = st.number_input("Risk % per Trade", value=risk_percent_sidebar,
                                           step=0.1, min_value=0.1, max_value=20.0, key="risk_p2")

        html('<span class="section-label" style="margin-top:16px;">03 · Trade Levels</span>')

        if use_price_mode:
            c1, c2, c3 = st.columns(3)
            with c1:
                direction_p2 = st.selectbox("Direction", ["Buy", "Sell"], key="dir_p2")
            with c2:
                entry_p2 = st.number_input("Entry Price", value=2330.00, step=0.10, format="%.2f", key="entry_p2")
            with c3:
                sl_price_p2 = st.number_input("SL Price", value=2310.00, step=0.10, format="%.2f", key="slprice_p2")
            tp_price_p2 = st.number_input("TP Price", value=2370.00, step=0.10, format="%.2f", key="tpprice_p2")
            sl_pips_p2 = 0.0; tp_pips_p2 = 0.0
        else:
            c1, c2 = st.columns(2)
            with c1:
                sl_pips_p2 = st.number_input("Stop Loss (pips)", value=float(sl_pips_sidebar),
                                               step=1.0, min_value=1.0, key="sl_p2")
            with c2:
                tp_pips_p2 = st.number_input("Take Profit (pips)", value=float(tp_pips_sidebar),
                                               step=1.0, min_value=1.0, key="tp_p2")
            entry_p2 = 0.0; sl_price_p2 = 0.0; tp_price_p2 = 0.0; direction_p2 = "Buy"

        html('<span class="section-label" style="margin-top:16px;">04 · Broker Costs</span>')
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

        html("</div>")

    with col_results:
        c2_obj = XAUUSDCalculatorV4(
            account_balance=balance_p2,
            risk_percent=risk_pct_p2,
            sl_pips=sl_pips_p2,
            tp_pips=tp_pips_p2,
            pip_mode=pip_mode,
            spread_points=spread_p2,
            commission_lot=comm_p2,
            leverage=lev_p2,
            entry_price=entry_p2 if use_price_mode else 2330.0,
            sl_price=sl_price_p2 if use_price_mode else 0.0,
            tp_price=tp_price_p2 if use_price_mode else 0.0,
            use_price_mode=use_price_mode,
            trade_direction=direction_p2.lower() if use_price_mode else "buy",
        )

        lot       = c2_obj.lot_size
        risk      = c2_obj.risk_amount
        net_p     = c2_obj.net_profit
        net_l     = c2_obj.net_loss
        rrr       = c2_obj.rrr
        margin    = c2_obj.required_margin
        margin_pct= c2_obj.margin_usage_pct

        if lot > 0:
            # Spread cost calculation
            if use_price_mode:
                spread_cost = spread_p2 * 0.01 * lot * 100
            else:
                spread_cost = (spread_p2 / (10 if pip_mode == "standard" else 1)) * lot * c2_obj.pip_value_per_lot

            margin_color = ("linear-gradient(90deg,#00C853,#69F0AE)" if margin_pct < 20
                            else ("linear-gradient(90deg,#FFD54F,#FFA000)" if margin_pct < 50
                                  else "linear-gradient(90deg,#FF6D00,#FF1744)"))

            html(f"""
            <div class='result-outer' style='margin-top:16px;'>
                <div class='lot-label'>Recommended Lot Size</div>
                <div class='lot-value'>{lot:.3f}</div>
                <div class='lot-unit'>Standard Lots</div>
                <div class='stats-divider'></div>
                <div class='stats-row'>
                    <div class='stat-item'>
                        <div class='stat-val' style='color:#FFD54F;'>${risk:,.2f}</div>
                        <div class='stat-lbl'>At Risk</div>
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
                <div style='padding:0 2px;'>
                    <div style='display:flex; justify-content:space-between; font-size:0.72rem; color:#566A80; margin-bottom:5px;'>
                        <span>Margin Required</span>
                        <span style='font-family:Space Mono,monospace; color:#80DEEA;'>${margin:,.2f} ({margin_pct:.1f}%)</span>
                    </div>
                    <div class='margin-meter'>
                        <div class='margin-fill' style='width:{min(margin_pct,100):.1f}%; background:{margin_color};'></div>
                    </div>
                    <div style='margin-top:14px;'>
                        <div class='cost-block'>
                            <div class='cost-row'>
                                <span class='cost-label'>Spread cost</span>
                                <span class='cost-val' style='color:#CE93D8;'>${spread_cost:,.3f}</span>
                            </div>
                            <div class='cost-row'>
                                <span class='cost-label'>Commission</span>
                                <span class='cost-val' style='color:#80DEEA;'>${c2_obj.commission_total:,.3f}</span>
                            </div>
                            <div class='cost-row'>
                                <span class='cost-label'>Break-even win rate</span>
                                <span class='cost-val' style='color:#FFD54F;'>{c2_obj.breakeven_win_rate:.1f}%</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """)

            html('<div style="margin-top:14px;">')
            alerts = c2_obj.validate()
            for a in alerts:
                css = {"ok": "val-ok", "warn": "val-warn", "danger": "val-danger"}[a["level"]]
                html(f'<div class="{css}">{a["msg"]}</div>')
            html('</div>')

        else:
            html("""
            <div class='empty-state' style='margin-top:16px;'>
                <div style='font-size:2.5rem; margin-bottom:1rem; opacity:0.4;'>⚡</div>
                <div style='font-family:Space Mono,monospace; font-size:0.7rem; letter-spacing:0.2em;
                            text-transform:uppercase; color:#4A5C70;'>
                    Adjust parameters — results update live
                </div>
            </div>
            """)

    html('<div class="footer">XAUUSD Position Calculator · v4 · Live Engine · Not Financial Advice</div>')


# ══════════════════════════════════════════════════════════════════
#  PAGE 3 — RISK MANAGEMENT PRO
# ══════════════════════════════════════════════════════════════════
elif page == "📊  Risk Management Pro":

    html("""
    <div style='display:flex; align-items:center; justify-content:space-between;
                margin-bottom:1.5rem; flex-wrap:wrap; gap:12px;'>
        <div>
            <h1 style='font-family:Poppins,sans-serif; font-weight:800; font-size:1.6rem;
                       background:linear-gradient(90deg,#D4AF37 0%,#FFE082 50%,#D4AF37 100%);
                       -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                       margin:0; letter-spacing:-0.01em;'>XAUUSD Risk Management Pro</h1>
            <p style='color:#4A5C70; font-size:0.72rem; letter-spacing:0.1em; text-transform:uppercase; margin:0.3rem 0 0;'>
                Precision Risk Engine · Gold Trading · Professional Grade
            </p>
        </div>
        <div class='live-dot'>
            <span class='live-dot-inner'></span> Auto-Updating
        </div>
    </div>
    """)

    # 6 KPI Cards
    html(f"""
    <div style='display:grid; grid-template-columns:repeat(6,1fr); gap:0.75rem; margin-bottom:1.6rem;'>
        <div class='kpi-card kpi-blue'>
            <div class='kpi-label'>Lot Size</div>
            <div class='kpi-value'>{calc.lot_size:.3f}</div>
            <div class='kpi-sub'>Std Lots</div>
        </div>
        <div class='kpi-card kpi-gold'>
            <div class='kpi-label'>Risk $</div>
            <div class='kpi-value'>${calc.risk_amount:,.0f}</div>
            <div class='kpi-sub'>{risk_percent_sidebar}% of acct</div>
        </div>
        <div class='kpi-card kpi-green'>
            <div class='kpi-label'>Net Profit</div>
            <div class='kpi-value'>${calc.net_profit:,.0f}</div>
            <div class='kpi-sub'>+{(calc.net_profit/account_balance*100):.2f}%</div>
        </div>
        <div class='kpi-card kpi-red'>
            <div class='kpi-label'>Net Loss</div>
            <div class='kpi-value'>${calc.net_loss:,.0f}</div>
            <div class='kpi-sub'>-{(calc.net_loss/account_balance*100):.2f}%</div>
        </div>
        <div class='kpi-card kpi-purple'>
            <div class='kpi-label'>Margin</div>
            <div class='kpi-value'>${calc.required_margin:,.0f}</div>
            <div class='kpi-sub'>{calc.margin_usage_pct:.1f}% usage</div>
        </div>
        <div class='kpi-card kpi-cyan'>
            <div class='kpi-label'>Break-even WR</div>
            <div class='kpi-value'>{calc.breakeven_win_rate:.0f}%</div>
            <div class='kpi-sub'>to be profitable</div>
        </div>
    </div>
    """)

    # Meters row
    col_rrr, col_risk, col_margin = st.columns([1, 1.5, 1.5])

    with col_rrr:
        rc = "#69F0AE" if calc.rrr >= 2 else ("#FFD54F" if calc.rrr >= 1 else "#FF8A80")
        label = "✅ Excellent" if calc.rrr >= 2 else ("⚠️ Acceptable" if calc.rrr >= 1 else "❌ Avoid")
        html(f"""
        <div style='padding:0.8rem 0;'>
            <div class='section-title' style='margin-top:0;'>Risk / Reward</div>
            <div style='font-family:Space Mono,monospace; font-size:2rem; font-weight:700; color:{rc}; line-height:1;'>1 : {calc.rrr:.2f}</div>
            <div style='color:#4A5C70; font-size:0.72rem; margin-top:0.4rem;'>{label}</div>
        </div>
        """)

    with col_risk:
        bar_cls = "risk-safe" if risk_percent_sidebar <= 2 else ("risk-moderate" if risk_percent_sidebar <= 4 else "risk-danger")
        bar_lbl = "🟢 Safe Zone" if risk_percent_sidebar <= 2 else ("🟡 Caution" if risk_percent_sidebar <= 4 else "🔴 Danger")
        html(f"""
        <div style='padding:0.8rem 0;'>
            <div class='section-title' style='margin-top:0;'>Risk-o-Meter</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
                <span style='font-size:0.76rem; color:#8899AA;'>{bar_lbl}</span>
                <span style='font-family:Space Mono,monospace; font-size:0.88rem; color:#D4AF37; font-weight:700;'>{risk_percent_sidebar}%</span>
            </div>
            <div class='risk-bar-wrap'>
                <div class='risk-bar-fill {bar_cls}' style='width:{min(risk_percent_sidebar*10,100)}%;'></div>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.58rem; color:#4A5C70; margin-top:0.25rem;'>
                <span>0%</span><span>2%</span><span>5%</span><span>10%</span>
            </div>
        </div>
        """)

    with col_margin:
        m_pct = calc.margin_usage_pct
        m_cls = "risk-safe" if m_pct < 20 else ("risk-moderate" if m_pct < 50 else "risk-danger")
        m_lbl = "🟢 Low" if m_pct < 20 else ("🟡 Moderate" if m_pct < 50 else "🔴 High Risk")
        html(f"""
        <div style='padding:0.8rem 0;'>
            <div class='section-title' style='margin-top:0;'>Margin Usage</div>
            <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem;'>
                <span style='font-size:0.76rem; color:#8899AA;'>{m_lbl}</span>
                <span style='font-family:Space Mono,monospace; font-size:0.88rem; color:#80DEEA; font-weight:700;'>{m_pct:.1f}%</span>
            </div>
            <div class='risk-bar-wrap'>
                <div class='risk-bar-fill {m_cls}' style='width:{min(m_pct,100):.1f}%;'></div>
            </div>
            <div style='display:flex; justify-content:space-between; font-size:0.58rem; color:#4A5C70; margin-top:0.25rem;'>
                <span>0%</span><span>20%</span><span>50%</span><span>100%</span>
            </div>
        </div>
        """)

    # Validation panel
    html('<div class="section-title">Live Trade Validation</div>')
    val_cols = st.columns(2)
    alerts = calc.validate()
    for i, a in enumerate(alerts):
        css = {"ok": "val-ok", "warn": "val-warn", "danger": "val-danger"}[a["level"]]
        with val_cols[i % 2]:
            html(f'<div class="{css}">{a["msg"]}</div>')

    # Summary + Lot suggestions
    col_summ, col_lots = st.columns([1, 1])

    with col_summ:
        html("<div class='section-title'>Trade Summary</div>")
        html(f"""
        <div class='summary-panel'>
            <h3>📋 Position Overview</h3>
            <div class='summary-row'><span class='sr-label'>Account Balance</span><span class='sr-val' style='color:#E8EAF0;'>${account_balance:,.2f}</span></div>
            <div class='summary-row'><span class='sr-label'>Capital at Risk</span><span class='sr-val' style='color:#FFD54F;'>${calc.risk_amount:,.2f} ({risk_percent_sidebar}%)</span></div>
            <div class='summary-row'><span class='sr-label'>Position Size</span><span class='sr-val' style='color:#82B1FF;'>{calc.lot_size:.3f} lots</span></div>
            <div class='summary-row'><span class='sr-label'>Stop Loss</span><span class='sr-val' style='color:#FF8A80;'>{sl_pips_sidebar} pips (eff. {calc.effective_sl_pips:.1f})</span></div>
            <div class='summary-row'><span class='sr-label'>Take Profit</span><span class='sr-val' style='color:#69F0AE;'>{tp_pips_sidebar} pips → +${calc.net_profit:,.2f}</span></div>
            <div class='summary-row'><span class='sr-label'>Spread Impact</span><span class='sr-val' style='color:#CE93D8;'>{spread_sidebar:.0f} pts → extra SL</span></div>
            <div class='summary-row'><span class='sr-label'>Commission Cost</span><span class='sr-val' style='color:#80DEEA;'>${calc.commission_total:,.3f}</span></div>
            <div class='summary-row'><span class='sr-label'>Required Margin</span><span class='sr-val' style='color:#80DEEA;'>${calc.required_margin:,.2f}</span></div>
            <div class='summary-row'><span class='sr-label'>Risk / Reward</span><span class='sr-val' style='color:#D4AF37;'>1 : {calc.rrr:.2f}</span></div>
            <div class='summary-row'><span class='sr-label'>Account after Win</span><span class='sr-val' style='color:#69F0AE;'>${calc.account_after_win:,.2f}</span></div>
            <div class='summary-row'><span class='sr-label'>Account after Loss</span><span class='sr-val' style='color:#FF8A80;'>${calc.account_after_loss:,.2f}</span></div>
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

        html("<div class='section-title'>Formula Reference (v4)</div>")
        pip_v = 10.0 if calc.pip_mode == "broker" else 1.0
        html(f"""
        <div style='background:rgba(3,8,15,0.9); border:1px solid rgba(212,175,55,0.1);
                    border-radius:12px; padding:1rem 1.2rem; font-family:Space Mono,monospace;
                    font-size:0.7rem; line-height:2.2; color:#566A80;'>
            <span style='color:#D4AF37;'>Risk $</span>         = ${account_balance:,.0f} × {risk_percent_sidebar}% = ${calc.risk_amount:,.2f}<br>
            <span style='color:#82B1FF;'>Lot Size</span>       = ${calc.risk_amount:,.2f} ÷ ({calc.effective_sl_pips:.1f} × ${pip_v}) = {calc.lot_size:.3f}<br>
            <span style='color:#69F0AE;'>Gross Profit</span>   = {tp_pips_sidebar} × {calc.lot_size:.3f} × ${pip_v} = ${calc.profit:,.2f}<br>
            <span style='color:#CE93D8;'>Net Profit</span>     = ${calc.profit:,.2f} − ${calc.commission_total:,.3f} = ${calc.net_profit:,.2f}<br>
            <span style='color:#80DEEA;'>Margin</span>         = ${calc.required_margin:,.2f} ({calc.margin_usage_pct:.1f}% of acct)<br>
            <span style='color:#FFD54F;'>Break-even WR</span>  = {calc.breakeven_win_rate:.1f}%
        </div>
        """)

    # Drawdown table
    html("<div class='section-title'>Consecutive Loss Drawdown Analysis</div>")
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
            "background-color": "rgba(6,13,31,0.8)",
            "border":           "1px solid rgba(212,175,55,0.08)",
            "font-family":      "Space Mono, monospace",
            "font-size":        "0.8rem",
            "text-align":       "center",
        })
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "rgba(212,175,55,0.10)"),
                ("color", "#D4AF37"),
                ("font-family", "Poppins, sans-serif"),
                ("font-size", "0.65rem"),
                ("letter-spacing", "0.1em"),
                ("text-transform", "uppercase"),
                ("border", "1px solid rgba(212,175,55,0.15)"),
                ("padding", "10px 12px"),
            ]},
            {"selector": "tr:hover td", "props": [
                ("background-color", "rgba(212,175,55,0.04)"),
            ]},
        ])
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    html("""
    <div class='warning-strip'>
        ⚠️ RISK DISCLOSURE — All calculations are for educational purposes only.
        Actual results depend on your broker's execution, slippage, and market conditions.
        Commission drag compounds over time. Past performance does not guarantee future results.
    </div>
    """)

    html('<div class="footer">XAUUSD Risk Management Pro v4 · Dark Engine · Not Financial Advice</div>')

# Stable One 

# import streamlit as st
# import pandas as pd
# import numpy as np
# import textwrap

# # ─────────────────────────────────────────────
# # PAGE CONFIG  (must be first Streamlit call)
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="XAUUSD Pro Suite",
#     page_icon="🥇",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────
# def html(raw: str):
#     st.markdown(textwrap.dedent(raw).strip(), unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # GLOBAL CSS — Risk Pro Navy/Gold Theme
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Poppins:wght@400;500;600;700;800&display=swap');

# /* ── CSS Variables ── */
# :root {
#     --navy-900:      #060D1F;
#     --navy-800:      #0A1628;
#     --navy-700:      #0D1F3C;
#     --gold:          #D4AF37;
#     --gold-light:    #FFE082;
#     --gold-dim:      #FFD54F;
#     --blue-accent:   #82B1FF;
#     --green-accent:  #69F0AE;
#     --red-accent:    #FF8A80;
#     --text-primary:  #E8EAF0;
#     --text-secondary:#8899AA;
#     --text-muted:    #566A80;
#     --glass-bg:      rgba(13,31,60,0.7);
#     --glass-border:  rgba(212,175,55,0.12);
#     --card-shadow:   0 8px 32px rgba(0,0,0,0.45), 0 1px 0 rgba(212,175,55,0.07) inset;
# }

# /* ── Reset & Base ── */
# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
# html, body, [class*="css"] {
#     font-family: 'Poppins', sans-serif !important;
#     background-color: var(--navy-900) !important;
#     color: var(--text-primary) !important;
# }

# /* ── App Background ── */
# .stApp {
#     background: radial-gradient(ellipse at 20% 0%, #0D1F3C 0%, #060D1F 50%, #060D1F 100%);
#     background-attachment: fixed;
# }
# body::after {
#     content: '';
#     position: fixed;
#     inset: 0;
#     background-image:
#         linear-gradient(rgba(212,175,55,0.025) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(212,175,55,0.025) 1px, transparent 1px);
#     background-size: 48px 48px;
#     pointer-events: none;
#     z-index: 0;
# }

# /* ── Hide Streamlit chrome ── */
# #MainMenu, footer, header { visibility: hidden; }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0A1628 0%, #060D1F 100%);
#     border-right: 1px solid rgba(212,175,55,0.15);
# }
# [data-testid="stSidebar"] label {
#     color: #B8C4D4 !important;
#     font-size: 0.78rem !important;
#     font-weight: 600 !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
# }

# /* ── Inputs ── */
# [data-testid="stNumberInput"] input,
# [data-testid="stTextInput"] input {
#     background: rgba(212,175,55,0.05) !important;
#     border: 1px solid rgba(212,175,55,0.2) !important;
#     border-radius: 8px !important;
#     color: #E8EAF0 !important;
#     font-family: 'Space Mono', monospace !important;
# }
# [data-testid="stNumberInput"] input:focus,
# [data-testid="stTextInput"] input:focus {
#     border-color: rgba(212,175,55,0.6) !important;
#     box-shadow: 0 0 0 2px rgba(212,175,55,0.12) !important;
# }

# /* Slider */
# .stSlider > div > div > div > div {
#     background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
# }
# .stSlider > div > div > div > div > div {
#     background: #fff !important;
#     border: 2px solid var(--gold) !important;
#     box-shadow: 0 0 12px rgba(212,175,55,0.55) !important;
#     width: 18px !important; height: 18px !important;
# }

# /* Selectbox */
# .stSelectbox > div > div {
#     background: rgba(212,175,55,0.05) !important;
#     border: 1px solid rgba(212,175,55,0.2) !important;
#     border-radius: 10px !important;
#     color: var(--text-primary) !important;
#     font-family: 'Poppins', sans-serif !important;
# }
# .stSelectbox > div > div:hover { border-color: rgba(212,175,55,0.5) !important; }
# .stSelectbox svg { color: var(--gold) !important; }

# /* ── Calculate / CTA button ── */
# .stButton > button {
#     width: 100% !important;
#     background: linear-gradient(135deg, #1a3a6e 0%, #D4AF37 100%) !important;
#     color: #fff !important;
#     font-family: 'Poppins', sans-serif !important;
#     font-size: 15px !important;
#     font-weight: 700 !important;
#     letter-spacing: 0.08em !important;
#     border: none !important;
#     border-radius: 12px !important;
#     padding: 15px 32px !important;
#     cursor: pointer !important;
#     transition: all 0.2s ease !important;
#     box-shadow: 0 4px 24px rgba(212,175,55,0.25) !important;
#     margin-top: 8px !important;
# }
# .stButton > button:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 8px 32px rgba(212,175,55,0.4) !important;
#     background: linear-gradient(135deg, #1a3a6e 0%, #FFE082 100%) !important;
# }

# /* ── Section label (left gold border) ── */
# .section-label {
#     font-family: 'Poppins', sans-serif;
#     font-size: 0.68rem;
#     font-weight: 700;
#     letter-spacing: 0.16em;
#     text-transform: uppercase;
#     color: var(--gold);
#     border-left: 3px solid var(--gold);
#     padding-left: 0.75rem;
#     margin: 0 0 1rem 0;
#     display: block;
# }
# .section-title {
#     font-family: 'Poppins', sans-serif;
#     font-size: 0.72rem;
#     font-weight: 700;
#     letter-spacing: 0.16em;
#     text-transform: uppercase;
#     color: var(--gold);
#     border-left: 3px solid var(--gold);
#     padding-left: 0.75rem;
#     margin: 2rem 0 1rem 0;
# }

# /* ── KPI Grid ── */
# .kpi-grid {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 1rem;
#     margin-bottom: 2rem;
# }
# .kpi-card {
#     position: relative;
#     overflow: hidden;
#     border-radius: 16px;
#     padding: 1.5rem 1.2rem;
#     border: 1px solid rgba(255,255,255,0.06);
#     backdrop-filter: blur(12px);
# }
# .kpi-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 3px;
#     border-radius: 16px 16px 0 0;
# }
# .kpi-gold   { background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(212,175,55,0.04)); }
# .kpi-gold::before { background: linear-gradient(90deg, #D4AF37, #FFE082); }
# .kpi-blue   { background: linear-gradient(135deg, rgba(41,98,255,0.15), rgba(41,98,255,0.04)); }
# .kpi-blue::before { background: linear-gradient(90deg, #2962FF, #82B1FF); }
# .kpi-green  { background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,200,83,0.04)); }
# .kpi-green::before { background: linear-gradient(90deg, #00C853, #69F0AE); }
# .kpi-red    { background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.04)); }
# .kpi-red::before { background: linear-gradient(90deg, #FF1744, #FF8A80); }
# .kpi-label  { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #8899AA; margin-bottom: 0.5rem; }
# .kpi-value  { font-family: 'Space Mono', monospace; font-size: 1.9rem; font-weight: 700; line-height: 1; margin-bottom: 0.3rem; }
# .kpi-gold .kpi-value  { color: #FFD54F; }
# .kpi-blue .kpi-value  { color: #82B1FF; }
# .kpi-green .kpi-value { color: #69F0AE; }
# .kpi-red .kpi-value   { color: #FF8A80; }
# .kpi-sub { font-size: 0.72rem; color: #566A80; font-family: 'Space Mono', monospace; }

# /* ── Calc card (page 2) ── */
# .calc-card {
#     background: var(--glass-bg);
#     border: 1px solid var(--glass-border);
#     border-radius: 20px;
#     padding: 32px 28px;
#     position: relative;
#     box-shadow: var(--card-shadow);
#     margin-bottom: 20px;
#     backdrop-filter: blur(12px);
#     overflow: hidden;
# }
# .calc-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 20px; right: 20px;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, rgba(212,175,55,0.5), transparent);
# }

# /* ── Risk badge ── */
# .risk-badge {
#     display: inline-block;
#     font-family: 'Space Mono', monospace;
#     font-size: 32px; font-weight: 700;
#     color: var(--gold-dim);
#     background: rgba(212,175,55,0.07);
#     border: 1px solid rgba(212,175,55,0.22);
#     border-radius: 12px;
#     padding: 6px 20px;
#     text-align: center;
#     min-width: 90px;
# }
# .risk-label { font-size: 11px; font-weight: 500; color: var(--text-muted); text-align: center; margin-top: 6px; }

# /* ── Result card (page 2) ── */
# .result-outer {
#     background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
#     border: 1px solid rgba(212,175,55,0.22);
#     border-radius: 20px;
#     padding: 36px 28px 32px;
#     position: relative;
#     box-shadow: var(--card-shadow);
#     margin-top: 8px;
#     animation: fadeSlideUp 0.35s cubic-bezier(0.22,1,0.36,1);
#     backdrop-filter: blur(12px);
#     overflow: hidden;
# }
# .result-outer::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 20px; right: 20px;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, var(--gold), transparent);
# }
# @keyframes fadeSlideUp {
#     from { opacity: 0; transform: translateY(24px); }
#     to   { opacity: 1; transform: translateY(0); }
# }
# .lot-label { font-family: 'Space Mono', monospace; font-size: 10px; letter-spacing: 5px; color: var(--text-muted); text-align: center; text-transform: uppercase; margin-bottom: 4px; }
# .lot-value {
#     font-family: 'Space Mono', monospace;
#     font-size: clamp(64px,15vw,108px);
#     font-weight: 700; line-height: 1; text-align: center;
#     background: linear-gradient(135deg, #fff 0%, var(--gold) 55%, var(--gold-dim) 100%);
#     -webkit-background-clip: text; -webkit-text-fill-color: transparent;
#     filter: drop-shadow(0 0 28px rgba(212,175,55,0.3));
#     letter-spacing: -2px;
# }
# .lot-unit { font-family: 'Poppins', sans-serif; font-size: 12px; font-weight: 600; letter-spacing: 5px; color: var(--text-secondary); text-align: center; text-transform: uppercase; margin-top: 4px; }
# .stats-divider { width: 100%; height: 1px; background: linear-gradient(90deg, transparent, rgba(212,175,55,0.2), transparent); margin: 24px 0; }
# .stats-row { display: flex; justify-content: space-around; gap: 8px; flex-wrap: wrap; }
# .stat-item { text-align: center; flex: 1; min-width: 90px; background: rgba(212,175,55,0.04); border: 1px solid rgba(212,175,55,0.09); border-radius: 12px; padding: 12px 8px; }
# .stat-val { font-family: 'Space Mono', monospace; font-size: 17px; font-weight: 700; color: var(--text-primary); }
# .stat-lbl { font-family: 'Poppins', sans-serif; font-size: 9px; font-weight: 600; letter-spacing: 0.1em; color: var(--text-muted); text-transform: uppercase; margin-top: 5px; }

# /* ── Trade Summary Panel (page 3) ── */
# .summary-panel {
#     background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
#     border: 1px solid rgba(212,175,55,0.2);
#     border-radius: 16px;
#     padding: 1.6rem 1.8rem;
#     margin-bottom: 1.5rem;
# }
# .summary-panel h3 { font-family: 'Poppins', sans-serif; font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: #D4AF37; margin: 0 0 1rem 0; }
# .summary-row { display: flex; justify-content: space-between; align-items: center; padding: 0.55rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.88rem; }
# .summary-row:last-child { border-bottom: none; }
# .summary-row .sr-label { color: #8899AA; }
# .summary-row .sr-val   { font-family: 'Space Mono', monospace; font-weight: 700; }

# /* ── Lot Suggestion Cards ── */
# .lot-row { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 1.5rem; }
# .lot-card { background: rgba(255,255,255,0.03); border-radius: 12px; border: 1px solid rgba(255,255,255,0.07); padding: 1.1rem 1rem; text-align: center; transition: border-color 0.2s; }
# .lot-card:hover { border-color: rgba(212,175,55,0.35); }
# .lot-card .lc-label { font-size: 0.65rem; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem; }
# .lot-card .lc-value { font-family: 'Space Mono', monospace; font-size: 1.35rem; font-weight: 700; line-height: 1; }
# .lot-card .lc-risk  { font-size: 0.68rem; color: #566A80; margin-top: 0.3rem; font-family: 'Space Mono', monospace; }
# .lc-conservative .lc-label, .lc-conservative .lc-value { color: #69F0AE; }
# .lc-moderate     .lc-label, .lc-moderate     .lc-value { color: #FFD54F; }
# .lc-aggressive   .lc-label, .lc-aggressive   .lc-value { color: #FF8A80; }

# /* ── Risk Bar ── */
# .risk-bar-wrap { background: rgba(255,255,255,0.04); border-radius: 8px; height: 10px; overflow: hidden; margin: 0.6rem 0 0.3rem 0; }
# .risk-bar-fill  { height: 100%; border-radius: 8px; transition: width 0.4s ease; }
# .risk-safe      { background: linear-gradient(90deg, #00C853, #69F0AE); }
# .risk-moderate  { background: linear-gradient(90deg, #FFD54F, #FFA000); }
# .risk-danger    { background: linear-gradient(90deg, #FF6D00, #FF1744); }

# /* ── Warning strip ── */
# .warning-strip {
#     background: rgba(212,175,55,0.05);
#     border: 1px solid rgba(212,175,55,0.14);
#     border-left: 3px solid var(--gold);
#     border-radius: 10px;
#     padding: 12px 16px;
#     margin-top: 20px;
#     font-family: 'Poppins', sans-serif;
#     font-size: 11px;
#     color: var(--text-muted);
#     line-height: 1.7;
# }

# /* ── Explainer page cards ── */
# .exp-section {
#     background: var(--glass-bg);
#     border: 1px solid var(--glass-border);
#     border-radius: 20px;
#     padding: 28px 28px 24px;
#     margin-bottom: 20px;
#     position: relative;
#     overflow: hidden;
# }
# .exp-section::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 20px; right: 20px;
#     height: 1px;
#     background: linear-gradient(90deg, transparent, rgba(212,175,55,0.4), transparent);
# }
# .exp-title {
#     font-family: 'Poppins', sans-serif;
#     font-size: 1.1rem;
#     font-weight: 700;
#     color: var(--gold-light);
#     margin-bottom: 0.5rem;
# }
# .exp-subtitle {
#     font-family: 'Space Mono', monospace;
#     font-size: 0.68rem;
#     letter-spacing: 0.14em;
#     color: var(--text-muted);
#     text-transform: uppercase;
#     margin-bottom: 1.2rem;
# }
# .exp-body {
#     font-size: 0.88rem;
#     line-height: 1.8;
#     color: var(--text-secondary);
# }
# .formula-block {
#     background: rgba(6,13,31,0.9);
#     border: 1px solid rgba(212,175,55,0.15);
#     border-radius: 12px;
#     padding: 1rem 1.2rem;
#     font-family: 'Space Mono', monospace;
#     font-size: 0.8rem;
#     line-height: 2.2;
#     color: #8899AA;
#     margin-top: 1rem;
# }

# /* ── Sidebar brand ── */
# .sidebar-brand {
#     text-align: center;
#     padding: 0 0 1.5rem 0;
#     border-bottom: 1px solid rgba(212,175,55,0.15);
#     margin-bottom: 1.5rem;
# }
# .sidebar-brand span {
#     font-family: 'Poppins', sans-serif;
#     font-weight: 800;
#     font-size: 1.1rem;
#     background: linear-gradient(90deg, #D4AF37, #FFE082);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     letter-spacing: 0.04em;
# }
# .sidebar-brand small {
#     display: block;
#     font-size: 0.62rem;
#     color: #566A80;
#     letter-spacing: 0.18em;
#     text-transform: uppercase;
#     margin-top: 0.15rem;
# }

# /* ── Pulse animation ── */
# @keyframes pulse {
#     0%, 100% { opacity: 1; }
#     50%       { opacity: 0.3; }
# }

# /* ── Footer ── */
# .footer {
#     text-align: center;
#     margin-top: 44px;
#     font-family: 'Space Mono', monospace;
#     font-size: 10px;
#     letter-spacing: 3px;
#     color: var(--text-muted);
#     opacity: 0.4;
#     text-transform: uppercase;
#     padding-bottom: 2rem;
# }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # DOMAIN MODEL
# # ─────────────────────────────────────────────
# class XAUUSDCalculator:
#     """Core domain model for XAUUSD risk calculations."""

#     PIP_VALUE_PER_LOT = 1.0  # $1 per pip per standard lot for XAUUSD

#     def __init__(self, account_balance: float, risk_percent: float,
#                  sl_pips: float, tp_pips: float):
#         self.account_balance = account_balance
#         self.risk_percent    = risk_percent
#         self.sl_pips         = sl_pips
#         self.tp_pips         = tp_pips

#     @property
#     def risk_amount(self) -> float:
#         return (self.account_balance * self.risk_percent) / 100

#     @property
#     def lot_size(self) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return self.risk_amount / (self.sl_pips * self.PIP_VALUE_PER_LOT)

#     @property
#     def profit(self) -> float:
#         return self.tp_pips * self.lot_size * self.PIP_VALUE_PER_LOT

#     @property
#     def loss(self) -> float:
#         return self.sl_pips * self.lot_size * self.PIP_VALUE_PER_LOT

#     @property
#     def rrr(self) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return self.tp_pips / self.sl_pips

#     @property
#     def account_after_win(self) -> float:
#         return self.account_balance + self.profit

#     @property
#     def account_after_loss(self) -> float:
#         return self.account_balance - self.loss

#     def lot_for_risk(self, pct: float) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return (self.account_balance * pct / 100) / (self.sl_pips * self.PIP_VALUE_PER_LOT)

#     def drawdown_table(self, consecutive_losses: int = 10) -> pd.DataFrame:
#         rows = []
#         equity = self.account_balance
#         for i in range(1, consecutive_losses + 1):
#             equity -= self.loss
#             dd_pct = ((self.account_balance - equity) / self.account_balance) * 100
#             rows.append({
#                 "# Losses": i,
#                 "Account Balance ($)": round(equity, 2),
#                 "Total Drawdown ($)": round(self.loss * i, 2),
#                 "Drawdown %": round(dd_pct, 2),
#             })
#         return pd.DataFrame(rows)


# # ─────────────────────────────────────────────
# # SIDEBAR — Navigation + Shared Params
# # ─────────────────────────────────────────────
# html("""
# <div class='sidebar-brand'>
#     <span>⚡ XAUUSD PRO SUITE</span>
#     <small>Professional Risk Engine</small>
# </div>
# """)

# page = st.sidebar.radio(
#     "Navigate",
#     options=["📖  Explainer", "🧮  Position Calculator", "📊  Risk Management Pro"],
#     index=0,
# )

# st.sidebar.markdown("---")
# st.sidebar.markdown("### ⚙️ Shared Parameters")

# account_balance = st.sidebar.number_input(
#     "Account Balance ($)",
#     min_value=100.0, max_value=10_000_000.0,
#     value=10_000.0, step=500.0, format="%.2f"
# )

# risk_percent_sidebar = st.sidebar.number_input(
#     "Risk % per Trade",
#     min_value=0.1, max_value=10.0,
#     value=2.0, step=0.1, format="%.1f"
# )

# sl_pips_sidebar = st.sidebar.number_input(
#     "Stop Loss (pips)",
#     min_value=1, max_value=500, value=50, step=1
# )

# tp_pips_sidebar = st.sidebar.number_input(
#     "Take Profit (pips)",
#     min_value=1, max_value=5000, value=100, step=1
# )

# # Sidebar validations
# if sl_pips_sidebar <= 0:
#     st.sidebar.error("❌ Stop Loss must be > 0")
# if tp_pips_sidebar <= sl_pips_sidebar:
#     st.sidebar.warning("⚠️ TP < SL — negative risk-reward detected")
# if risk_percent_sidebar >= 5:
#     st.sidebar.warning("⚠️ Risk ≥ 5% — high-risk territory")

# # Shared domain model instance
# calc = XAUUSDCalculator(account_balance, risk_percent_sidebar, sl_pips_sidebar, tp_pips_sidebar)


# # ══════════════════════════════════════════════════════════════════
# #  PAGE 1 — EXPLAINER
# # ══════════════════════════════════════════════════════════════════
# if page == "📖  Explainer":

#     html("""
#     <div style='padding: 40px 0 32px 0;'>
#         <div style='display:inline-flex; align-items:center; gap:6px;
#                     background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.22);
#                     border-radius:999px; padding:5px 16px; font-family:Space Mono,monospace;
#                     font-size:10px; letter-spacing:3px; color:#D4AF37; text-transform:uppercase; margin-bottom:20px;'>
#             <span style='width:6px;height:6px;border-radius:50%;background:#D4AF37;
#                          box-shadow:0 0 8px #D4AF37;animation:pulse 2s ease infinite;display:inline-block;'></span>
#             Knowledge Base
#         </div>
#         <h1 style='font-family:Poppins,sans-serif; font-size:clamp(28px,5vw,46px); font-weight:800;
#                    background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
#                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
#                    margin:0 0 10px 0; line-height:1.1;'>
#             How It All Works
#         </h1>
#         <p style='color:#8899AA; font-size:13px; letter-spacing:0.4px; margin:0;'>
#             Complete formula reference &amp; concept guide for both tools in the XAUUSD Pro Suite
#         </p>
#     </div>
#     """)

#     # ── Section A: Position Calculator ───────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 01 · Position Size Calculator</div>
#         <div class='exp-title'>📐 What Is Position Sizing?</div>
#         <div class='exp-body'>
#             Position sizing is <strong style='color:#E8EAF0;'>the most critical discipline in trading</strong>.
#             It answers the question: <em style='color:#FFD54F;'>"How large should my trade be?"</em><br><br>
#             The goal is to risk only a fixed percentage of your account on any single trade, so that
#             a string of losses does not wipe out your capital. The <strong style='color:#E8EAF0;'>Position Calculator</strong>
#             takes your account balance, your acceptable risk (%), and the distance to your stop-loss (in pips)
#             and outputs the exact standard-lot size you should trade.
#         </div>
#         <div class='formula-block'>
#             <span style='color:#FFD54F;'>Risk Amount ($)</span>  = Account Balance × Risk% ÷ 100<br>
#             <span style='color:#82B1FF;'>Lot Size</span>         = Risk Amount ÷ (Stop Loss pips × Pip Value per Lot)<br>
#             <br>
#             <span style='color:#8899AA;'>── XAUUSD constants ──</span><br>
#             <span style='color:#69F0AE;'>Pip Value per Lot</span> = $1.00  (1 pip = $1 per standard lot for gold)<br>
#             <span style='color:#69F0AE;'>1 Standard Lot</span>   = 100 oz of XAU<br>
#         </div>
#     </div>
#     """)

#     # ── Section B: Worked example ─────────────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 01 · Worked Example</div>
#         <div class='exp-title'>🔢 Step-by-Step Calculation</div>
#         <div class='exp-body'>
#             Suppose you have a <strong style='color:#E8EAF0;'>$10,000 account</strong>,
#             want to risk <strong style='color:#FFD54F;'>2%</strong>,
#             and your stop-loss is <strong style='color:#FF8A80;'>50 pips</strong> away.
#         </div>
#         <div class='formula-block'>
#             <span style='color:#8899AA;'>Step 1 — Dollar risk</span><br>
#             Risk $ = 10,000 × 2 ÷ 100 = <span style='color:#FFD54F;'>$200</span><br>
#             <br>
#             <span style='color:#8899AA;'>Step 2 — Lot size</span><br>
#             Lot Size = 200 ÷ (50 × 1.00) = <span style='color:#82B1FF;'>0.04 lots</span><br>
#             <br>
#             <span style='color:#8899AA;'>Interpretation</span><br>
#             Trading <span style='color:#82B1FF;'>0.04 standard lots</span> means each pip move = $0.04.<br>
#             If SL is hit: 50 pips × $0.04 = <span style='color:#FF8A80;'>-$200</span> (exactly 2% of $10,000). ✅
#         </div>
#     </div>
#     """)

#     # ── Section C: Risk Profiles ──────────────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 01 · Risk Profiles</div>
#         <div class='exp-title'>🎯 Risk Tier Classification</div>
#         <div class='exp-body'>
#             The calculator automatically classifies your trade into one of three risk tiers
#             based on the percentage of account equity you are exposing.
#         </div>
#         <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1rem;'>
#             <div style='background:rgba(105,240,174,0.07); border:1px solid rgba(105,240,174,0.2);
#                         border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-size:1.5rem; margin-bottom:0.4rem;'>🟢</div>
#                 <div style='color:#69F0AE; font-weight:700; font-size:0.85rem; letter-spacing:0.08em;'>CONSERVATIVE</div>
#                 <div style='color:#566A80; font-size:0.75rem; margin-top:0.3rem;'>Risk ≤ 2%</div>
#                 <div style='color:#8899AA; font-size:0.78rem; margin-top:0.5rem; line-height:1.6;'>
#                     Industry standard. Withstands 50 consecutive losses before account depletion.
#                 </div>
#             </div>
#             <div style='background:rgba(255,213,79,0.07); border:1px solid rgba(255,213,79,0.2);
#                         border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-size:1.5rem; margin-bottom:0.4rem;'>🟡</div>
#                 <div style='color:#FFD54F; font-weight:700; font-size:0.85rem; letter-spacing:0.08em;'>MODERATE</div>
#                 <div style='color:#566A80; font-size:0.75rem; margin-top:0.3rem;'>Risk 2% – 4%</div>
#                 <div style='color:#8899AA; font-size:0.78rem; margin-top:0.5rem; line-height:1.6;'>
#                     Elevated returns possible, but drawdowns accelerate quickly during losing streaks.
#                 </div>
#             </div>
#             <div style='background:rgba(255,138,128,0.07); border:1px solid rgba(255,138,128,0.2);
#                         border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-size:1.5rem; margin-bottom:0.4rem;'>🔴</div>
#                 <div style='color:#FF8A80; font-weight:700; font-size:0.85rem; letter-spacing:0.08em;'>AGGRESSIVE</div>
#                 <div style='color:#566A80; font-size:0.75rem; margin-top:0.3rem;'>Risk &gt; 4%</div>
#                 <div style='color:#8899AA; font-size:0.78rem; margin-top:0.5rem; line-height:1.6;'>
#                     High-variance strategy. Account can halve in fewer than 15 consecutive losses.
#                 </div>
#             </div>
#         </div>
#     </div>
#     """)

#     # ── Section D: Risk Management Pro ───────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 02 · XAUUSD Risk Management Pro</div>
#         <div class='exp-title'>📊 Full Risk Dashboard Explained</div>
#         <div class='exp-body'>
#             The <strong style='color:#E8EAF0;'>Risk Management Pro</strong> dashboard builds on the position
#             calculator with four additional analytical layers: <em style='color:#FFD54F;'>Risk-Reward Ratio</em>,
#             a live <em style='color:#82B1FF;'>Trade Summary</em>, <em style='color:#69F0AE;'>Lot Suggestions</em>
#             at three risk tiers, and a <em style='color:#FF8A80;'>Drawdown Table</em>
#             modelling consecutive losses.
#         </div>
#         <div class='formula-block'>
#             <span style='color:#D4AF37;'>Risk Amount ($)</span>  = Balance × Risk% ÷ 100<br>
#             <span style='color:#82B1FF;'>Lot Size</span>         = Risk$ ÷ (SL pips × $1)<br>
#             <span style='color:#69F0AE;'>Profit (if TP hit)</span> = TP pips × Lot Size × $1<br>
#             <span style='color:#FF8A80;'>Loss (if SL hit)</span>  = SL pips × Lot Size × $1<br>
#             <span style='color:#FFD54F;'>Risk-Reward Ratio</span> = TP pips ÷ SL pips<br>
#             <span style='color:#E8EAF0;'>Account after Win</span> = Balance + Profit<br>
#             <span style='color:#E8EAF0;'>Account after Loss</span>= Balance − Loss<br>
#         </div>
#     </div>
#     """)

#     # ── Section E: RRR deep-dive ──────────────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 02 · Concept Deep-Dive</div>
#         <div class='exp-title'>⚖️ Risk-Reward Ratio (RRR)</div>
#         <div class='exp-body'>
#             RRR tells you <strong style='color:#E8EAF0;'>how much you expect to gain relative to what you risk</strong>.
#             A 1:2 RRR means for every $1 risked, you target $2 in profit.
#             <br><br>
#             At a 1:2 RRR, you only need to win <strong style='color:#69F0AE;'>34% of trades</strong> to break even.
#             At 1:1 you need 50%. Below 1:1 the math permanently works against you regardless of win-rate.
#         </div>
#         <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:1rem; margin-top:1rem;'>
#             <div style='background:rgba(105,240,174,0.06); border:1px solid rgba(105,240,174,0.18); border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-family:Space Mono,monospace; font-size:1.6rem; font-weight:700; color:#69F0AE;'>≥ 1:2</div>
#                 <div style='color:#69F0AE; font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;'>✅ Excellent</div>
#                 <div style='color:#8899AA; font-size:0.76rem; margin-top:0.5rem;'>Break-even at ~34% win-rate</div>
#             </div>
#             <div style='background:rgba(255,213,79,0.06); border:1px solid rgba(255,213,79,0.18); border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-family:Space Mono,monospace; font-size:1.6rem; font-weight:700; color:#FFD54F;'>1:1</div>
#                 <div style='color:#FFD54F; font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;'>⚠️ Acceptable</div>
#                 <div style='color:#8899AA; font-size:0.76rem; margin-top:0.5rem;'>Must win &gt;50% to profit</div>
#             </div>
#             <div style='background:rgba(255,138,128,0.06); border:1px solid rgba(255,138,128,0.18); border-radius:12px; padding:1rem; text-align:center;'>
#                 <div style='font-family:Space Mono,monospace; font-size:1.6rem; font-weight:700; color:#FF8A80;'>&lt; 1:1</div>
#                 <div style='color:#FF8A80; font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; margin-top:4px;'>❌ Avoid</div>
#                 <div style='color:#8899AA; font-size:0.76rem; margin-top:0.5rem;'>Statistically negative edge</div>
#             </div>
#         </div>
#     </div>
#     """)

#     # ── Section F: Drawdown concept ───────────────────────────────
#     html("""
#     <div class='exp-section'>
#         <div class='exp-subtitle'>Module 02 · Drawdown Analysis</div>
#         <div class='exp-title'>📉 Consecutive Loss Modelling</div>
#         <div class='exp-body'>
#             The <strong style='color:#E8EAF0;'>Drawdown Table</strong> in Risk Management Pro
#             simulates what happens to your account if you hit a series of consecutive losses—
#             something every trader will experience.
#             <br><br>
#             At 2% risk, 10 consecutive losses reduce your account by approximately
#             <strong style='color:#FF8A80;'>18.3%</strong> (compound effect).
#             At 5% risk, the same streak costs you <strong style='color:#FF8A80;'>40.1%</strong>.
#             <br><br>
#             Understanding this table helps you choose a risk percentage you can
#             <em style='color:#FFD54F;'>emotionally and financially survive</em>.
#         </div>
#         <div class='formula-block'>
#             <span style='color:#8899AA;'>For each consecutive loss N:</span><br>
#             <span style='color:#FF8A80;'>Balance(N)</span>  = Balance(N-1) − Loss per Trade<br>
#             <span style='color:#FFD54F;'>Drawdown %</span>  = (Initial Balance − Balance(N)) ÷ Initial Balance × 100<br>
#         </div>
#     </div>
#     """)

#     html('<div class="footer">XAUUSD Pro Suite · Knowledge Base · For Educational Purposes Only</div>')


# # ══════════════════════════════════════════════════════════════════
# #  PAGE 2 — POSITION CALCULATOR
# # ══════════════════════════════════════════════════════════════════
# elif page == "🧮  Position Calculator":

#     html("""
#     <div style='text-align:center; padding:48px 24px 36px;'>
#         <div style='display:inline-flex; align-items:center; gap:6px;
#                     background:rgba(212,175,55,0.08); border:1px solid rgba(212,175,55,0.22);
#                     border-radius:999px; padding:5px 16px; font-family:Space Mono,monospace;
#                     font-size:10px; letter-spacing:3px; color:#D4AF37; text-transform:uppercase; margin-bottom:20px;'>
#             <span style='width:6px;height:6px;border-radius:50%;background:#D4AF37;
#                          box-shadow:0 0 8px #D4AF37;animation:pulse 2s ease infinite;display:inline-block;'></span>
#             Live Risk Engine
#         </div>
#         <div style='font-family:Poppins,sans-serif; font-size:clamp(32px,7vw,52px); font-weight:800;
#                     background:linear-gradient(90deg,#D4AF37,#FFE082,#D4AF37);
#                     -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1;'>
#             Position Calculator
#         </div>
#         <div style='color:#8899AA; font-size:13px; margin-top:10px; letter-spacing:0.4px;'>
#             XAU/USD · Forex · Commodities — Professional Risk Management
#         </div>
#     </div>
#     """)

#     # ── Two-column layout ─────────────────────────────────────────
#     col_inputs, col_results = st.columns([1, 1], gap="large")

#     with col_inputs:
#         html('<div class="calc-card">')
#         html('<span class="section-label">01 · Instrument</span>')

#         pair_type = st.selectbox(
#             "Select Instrument Type",
#             options=["XAUUSD (Gold)", "Forex Pair", "Other"],
#             index=0,
#         )

#         html('<span class="section-label" style="margin-top:24px;">02 · Account Parameters</span>')
#         c1, c2 = st.columns(2)
#         with c1:
#             balance_p2 = st.number_input("Account Balance (USD)", value=account_balance,
#                                          step=500.0, min_value=100.0, key="bal_p2")
#         with c2:
#             stop_loss_p2 = st.number_input("Stop Loss (Pips)", value=float(sl_pips_sidebar),
#                                             step=1.0, min_value=1.0, key="sl_p2")

#         html('<span class="section-label" style="margin-top:24px;">03 · Risk Exposure</span>')
#         risk_pct_p2 = st.slider("Risk % per Trade", min_value=0.5, max_value=100.0,
#                                  value=risk_percent_sidebar, step=0.5, key="risk_p2")

#         # Live risk preview
#         rd_preview = balance_p2 * (risk_pct_p2 / 100)
#         _, cb, _ = st.columns([1, 1, 1])
#         with cb:
#             html(f"""
#             <div style='text-align:center; margin:8px 0 4px;'>
#                 <div class='risk-badge'>{risk_pct_p2:.1f}%</div>
#                 <div class='risk-label'>approx ${rd_preview:,.0f} at risk</div>
#             </div>
#             """)

#         html("</div>")

#         _, cbtn, _ = st.columns([0.5, 2, 0.5])
#         with cbtn:
#             calculate = st.button("⚡  Calculate Position Size")

#     with col_results:
#         if calculate:
#             pip_value_map = {"XAUUSD (Gold)": 1.0, "Forex Pair": 10.0, "Other": 1.0}
#             pip_value  = pip_value_map[pair_type]
#             risk_amt   = balance_p2 * (risk_pct_p2 / 100)
#             lot_size_r = risk_amt / (stop_loss_p2 * pip_value)
#             pip_cost   = pip_value * lot_size_r

#             if risk_pct_p2 <= 2:
#                 risk_color = "#69F0AE"; risk_tier = "CONSERVATIVE"
#             elif risk_pct_p2 <= 4:
#                 risk_color = "#FFD54F"; risk_tier = "MODERATE"
#             else:
#                 risk_color = "#FF8A80"; risk_tier = "AGGRESSIVE"

#             html(f"""
#             <div class='result-outer' style='margin-top:80px;'>
#                 <div class='lot-label'>Recommended Lot Size</div>
#                 <div class='lot-value'>{lot_size_r:.2f}</div>
#                 <div class='lot-unit'>Standard Lots</div>
#                 <div class='stats-divider'></div>
#                 <div class='stats-row'>
#                     <div class='stat-item'>
#                         <div class='stat-val' style='color:#FFD54F;'>${risk_amt:,.2f}</div>
#                         <div class='stat-lbl'>Capital at Risk</div>
#                     </div>
#                     <div class='stat-item'>
#                         <div class='stat-val' style='color:#82B1FF;'>${pip_value:.2f}</div>
#                         <div class='stat-lbl'>Pip Value / Lot</div>
#                     </div>
#                     <div class='stat-item'>
#                         <div class='stat-val' style='color:{risk_color};'>{risk_tier}</div>
#                         <div class='stat-lbl'>Risk Profile</div>
#                     </div>
#                     <div class='stat-item'>
#                         <div class='stat-val' style='color:#E8EAF0;'>{int(stop_loss_p2)} pips</div>
#                         <div class='stat-lbl'>Stop Loss</div>
#                     </div>
#                 </div>
#                 <div class='warning-strip'>
#                     ⚠️&nbsp; RISK DISCLOSURE — Trading leveraged instruments carries significant risk.
#                     Position sizes are calculated based on your defined risk parameters only.
#                     Past performance does not guarantee future results. Trade responsibly.
#                 </div>
#             </div>
#             """)
#         else:
#             html("""
#             <div style='display:flex; flex-direction:column; align-items:center; justify-content:center;
#                         height:380px; opacity:0.35; text-align:center;'>
#                 <div style='font-size:3.5rem; margin-bottom:1rem;'>⚡</div>
#                 <div style='font-family:Space Mono,monospace; font-size:0.75rem; letter-spacing:0.2em;
#                             text-transform:uppercase; color:#566A80;'>
#                     Fill in parameters &amp; click calculate
#                 </div>
#             </div>
#             """)

#     html('<div class="footer">XAUUSD Position Calculator · Professional Risk Engine · v2.0</div>')


# # ══════════════════════════════════════════════════════════════════
# #  PAGE 3 — RISK MANAGEMENT PRO
# # ══════════════════════════════════════════════════════════════════
# elif page == "📊  Risk Management Pro":

#     html("""
#     <h1 style='font-family:Poppins,sans-serif; font-weight:800; font-size:1.7rem;
#                background:linear-gradient(90deg,#D4AF37 0%,#FFE082 50%,#D4AF37 100%);
#                -webkit-background-clip:text; -webkit-text-fill-color:transparent;
#                margin-bottom:0; letter-spacing:-0.01em;'>
#         XAUUSD Risk Management Pro
#     </h1>
#     <p style='color:#566A80; font-size:0.82rem; letter-spacing:0.1em; text-transform:uppercase;
#               margin-top:0.3rem; margin-bottom:2rem;'>
#         Precision Risk Engine &nbsp;·&nbsp; Gold Trading &nbsp;·&nbsp; Professional Grade
#     </p>
#     """)

#     # ── KPI Cards ─────────────────────────────────────────────────
#     html(f"""
#     <div class='kpi-grid'>
#         <div class='kpi-card kpi-blue'>
#             <div class='kpi-label'>Lot Size</div>
#             <div class='kpi-value'>{calc.lot_size:.3f}</div>
#             <div class='kpi-sub'>Standard Lots</div>
#         </div>
#         <div class='kpi-card kpi-gold'>
#             <div class='kpi-label'>Risk Amount</div>
#             <div class='kpi-value'>${calc.risk_amount:,.2f}</div>
#             <div class='kpi-sub'>{risk_percent_sidebar}% of account</div>
#         </div>
#         <div class='kpi-card kpi-green'>
#             <div class='kpi-label'>Profit if TP Hit</div>
#             <div class='kpi-value'>${calc.profit:,.2f}</div>
#             <div class='kpi-sub'>+{(calc.profit/account_balance*100):.2f}% return</div>
#         </div>
#         <div class='kpi-card kpi-red'>
#             <div class='kpi-label'>Loss if SL Hit</div>
#             <div class='kpi-value'>${calc.loss:,.2f}</div>
#             <div class='kpi-sub'>-{(calc.loss/account_balance*100):.2f}% drawdown</div>
#         </div>
#     </div>
#     """)

#     # ── RRR + Risk-o-Meter ────────────────────────────────────────
#     col_rrr, col_bar = st.columns([1, 2])

#     with col_rrr:
#         rrr_color = "#69F0AE" if calc.rrr >= 2 else ("#FFD54F" if calc.rrr >= 1 else "#FF8A80")
#         html(f"""
#         <div style='padding:1rem 0;'>
#             <div class='section-title'>Risk / Reward</div>
#             <div style='font-family:Space Mono,monospace; font-size:2.4rem; font-weight:700;
#                         color:{rrr_color}; line-height:1;'>
#                 1 : {calc.rrr:.2f}
#             </div>
#             <div style='color:#566A80; font-size:0.75rem; margin-top:0.4rem;'>
#                 {"✅ Excellent RRR" if calc.rrr >= 2 else ("⚠️ Acceptable RRR" if calc.rrr >= 1 else "❌ Negative RRR")}
#             </div>
#         </div>
#         """)

#     with col_bar:
#         bar_class = "risk-safe" if risk_percent_sidebar <= 2 else ("risk-moderate" if risk_percent_sidebar <= 4 else "risk-danger")
#         bar_label = "🟢 Safe Zone" if risk_percent_sidebar <= 2 else ("🟡 Caution Zone" if risk_percent_sidebar <= 4 else "🔴 Danger Zone")
#         html(f"""
#         <div style='padding:1rem 0;'>
#             <div class='section-title'>Risk-o-Meter</div>
#             <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
#                 <span style='font-size:0.78rem; color:#8899AA;'>{bar_label}</span>
#                 <span style='font-family:Space Mono,monospace; font-size:0.9rem; color:#D4AF37; font-weight:700;'>{risk_percent_sidebar}%</span>
#             </div>
#             <div class='risk-bar-wrap'>
#                 <div class='risk-bar-fill {bar_class}' style='width:{min(risk_percent_sidebar*10, 100)}%;'></div>
#             </div>
#             <div style='display:flex; justify-content:space-between; font-size:0.6rem; color:#566A80; margin-top:0.25rem;'>
#                 <span>0%</span><span>2% Safe</span><span>5% Risky</span><span>10%</span>
#             </div>
#         </div>
#         """)

#     # ── Trade Summary + Lot Suggestions ──────────────────────────
#     col_summ, col_lots = st.columns([1, 1])

#     with col_summ:
#         html("<div class='section-title'>Trade Summary</div>")
#         html(f"""
#         <div class='summary-panel'>
#             <h3>📋 Position Overview</h3>
#             <div class='summary-row'>
#                 <span class='sr-label'>Account Balance</span>
#                 <span class='sr-val' style='color:#E8EAF0;'>${account_balance:,.2f}</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>You are risking</span>
#                 <span class='sr-val' style='color:#FFD54F;'>${calc.risk_amount:,.2f} ({risk_percent_sidebar}%)</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Position Size</span>
#                 <span class='sr-val' style='color:#82B1FF;'>{calc.lot_size:.3f} lots</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Stop Loss</span>
#                 <span class='sr-val' style='color:#FF8A80;'>{sl_pips_sidebar} pips → -${calc.loss:,.2f}</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Take Profit</span>
#                 <span class='sr-val' style='color:#69F0AE;'>{tp_pips_sidebar} pips → +${calc.profit:,.2f}</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Risk / Reward</span>
#                 <span class='sr-val' style='color:#D4AF37;'>1 : {calc.rrr:.2f}</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Account after Win</span>
#                 <span class='sr-val' style='color:#69F0AE;'>${calc.account_after_win:,.2f}</span>
#             </div>
#             <div class='summary-row'>
#                 <span class='sr-label'>Account after Loss</span>
#                 <span class='sr-val' style='color:#FF8A80;'>${calc.account_after_loss:,.2f}</span>
#             </div>
#         </div>
#         """)

#     with col_lots:
#         html("<div class='section-title'>Lot Size Suggestions</div>")
#         l1 = calc.lot_for_risk(1)
#         l2 = calc.lot_for_risk(2)
#         l5 = calc.lot_for_risk(5)
#         html(f"""
#         <div class='lot-row'>
#             <div class='lot-card lc-conservative'>
#                 <div class='lc-label'>Conservative</div>
#                 <div class='lc-value'>{l1:.3f}</div>
#                 <div class='lc-risk'>1% Risk · ${account_balance*0.01:,.0f}</div>
#             </div>
#             <div class='lot-card lc-moderate'>
#                 <div class='lc-label'>Moderate</div>
#                 <div class='lc-value'>{l2:.3f}</div>
#                 <div class='lc-risk'>2% Risk · ${account_balance*0.02:,.0f}</div>
#             </div>
#             <div class='lot-card lc-aggressive'>
#                 <div class='lc-label'>Aggressive</div>
#                 <div class='lc-value'>{l5:.3f}</div>
#                 <div class='lc-risk'>5% Risk · ${account_balance*0.05:,.0f}</div>
#             </div>
#         </div>
#         """)

#         html("<div class='section-title'>Formula Reference</div>")
#         html("""
#         <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
#                     border-radius:12px; padding:1rem 1.2rem; font-family:Space Mono,monospace;
#                     font-size:0.75rem; line-height:2; color:#8899AA;'>
#             <span style='color:#D4AF37;'>Risk $</span>     = Balance × Risk% ÷ 100<br>
#             <span style='color:#82B1FF;'>Lot Size</span>   = Risk$ ÷ (SL pips × $1)<br>
#             <span style='color:#69F0AE;'>Profit</span>     = TP pips × Lot × $1<br>
#             <span style='color:#FF8A80;'>Loss</span>       = SL pips × Lot × $1<br>
#             <span style='color:#FFD54F;'>RRR</span>        = TP pips ÷ SL pips
#         </div>
#         """)

#     # ── Drawdown Table ────────────────────────────────────────────
#     html("<div class='section-title'>Consecutive Loss Drawdown Analysis</div>")

#     dd_df = calc.drawdown_table(10)

#     def color_row(row):
#         dd = row["Drawdown %"]
#         if dd < 10:
#             color = "#69F0AE"
#         elif dd < 25:
#             color = "#FFD54F"
#         else:
#             color = "#FF8A80"
#         return [f"color: {color}"] * len(row)

#     styled = (
#         dd_df.style
#         .apply(color_row, axis=1)
#         .format({
#             "Account Balance ($)": "${:,.2f}",
#             "Total Drawdown ($)":  "${:,.2f}",
#             "Drawdown %":         "{:.2f}%",
#         })
#         .set_properties(**{
#             "background-color": "rgba(13,31,60,0.6)",
#             "border":           "1px solid rgba(212,175,55,0.1)",
#             "font-family":      "Space Mono, monospace",
#             "font-size":        "0.82rem",
#             "text-align":       "center",
#         })
#         .set_table_styles([
#             {"selector": "th", "props": [
#                 ("background-color", "rgba(212,175,55,0.12)"),
#                 ("color", "#D4AF37"),
#                 ("font-family", "Poppins, sans-serif"),
#                 ("font-size", "0.68rem"),
#                 ("letter-spacing", "0.1em"),
#                 ("text-transform", "uppercase"),
#                 ("border", "1px solid rgba(212,175,55,0.2)"),
#             ]},
#             {"selector": "tr:hover td", "props": [
#                 ("background-color", "rgba(212,175,55,0.05)"),
#             ]},
#         ])
#     )
#     st.dataframe(styled, use_container_width=True, hide_index=True)

#     html("""
#     <div style='text-align:center; padding:2.5rem 0 1rem 0; color:#2A3A4A;
#                 font-size:0.7rem; letter-spacing:0.12em; text-transform:uppercase;'>
#         XAUUSD Risk Management Pro &nbsp;·&nbsp; For Educational Purposes Only &nbsp;·&nbsp; Not Financial Advice
#     </div>
#     """)



# import streamlit as st
# import pandas as pd
# import numpy as np

# # ─────────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="XAUUSD Risk Management Pro",
#     page_icon="🥇",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─────────────────────────────────────────────
# # CUSTOM CSS — Deep Navy Fintech Premium Theme
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Poppins:wght@400;500;600;700;800&display=swap');

# /* ── Global Reset ── */
# *, *::before, *::after { box-sizing: border-box; }

# html, body, [class*="css"] {
#     font-family: 'Poppins', sans-serif;
#     background-color: #060D1F;
#     color: #E8EAF0;
# }

# /* ── App Background ── */
# .stApp {
#     background: radial-gradient(ellipse at 20% 0%, #0D1F3C 0%, #060D1F 50%, #060D1F 100%);
#     background-attachment: fixed;
# }

# /* ── Hide Streamlit Branding ── */
# #MainMenu, footer, header { visibility: hidden; }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: linear-gradient(180deg, #0A1628 0%, #060D1F 100%);
#     border-right: 1px solid rgba(212, 175, 55, 0.15);
# }
# [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

# /* ── Sidebar Labels ── */
# [data-testid="stSidebar"] label {
#     color: #B8C4D4 !important;
#     font-size: 0.78rem !important;
#     font-weight: 600 !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
# }

# /* ── Number Inputs & Sliders ── */
# [data-testid="stNumberInput"] input,
# [data-testid="stTextInput"] input {
#     background: rgba(212, 175, 55, 0.05) !important;
#     border: 1px solid rgba(212, 175, 55, 0.2) !important;
#     border-radius: 8px !important;
#     color: #E8EAF0 !important;
#     font-family: 'Space Mono', monospace !important;
# }
# [data-testid="stNumberInput"] input:focus,
# [data-testid="stTextInput"] input:focus {
#     border-color: rgba(212, 175, 55, 0.6) !important;
#     box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.12) !important;
# }

# /* Slider thumb color */
# [data-testid="stSlider"] [class*="thumb"] {
#     background: #D4AF37 !important;
# }
# [data-testid="stSlider"] [class*="track"] {
#     background: rgba(212, 175, 55, 0.3) !important;
# }

# /* ── Main Metric Cards ── */
# .kpi-grid {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 1rem;
#     margin-bottom: 2rem;
# }
# .kpi-card {
#     position: relative;
#     overflow: hidden;
#     border-radius: 16px;
#     padding: 1.5rem 1.2rem;
#     border: 1px solid rgba(255,255,255,0.06);
#     backdrop-filter: blur(12px);
# }
# .kpi-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 3px;
#     border-radius: 16px 16px 0 0;
# }
# .kpi-gold   { background: linear-gradient(135deg, rgba(212,175,55,0.12), rgba(212,175,55,0.04)); }
# .kpi-gold::before { background: linear-gradient(90deg, #D4AF37, #FFE082); }

# .kpi-blue   { background: linear-gradient(135deg, rgba(41,98,255,0.15), rgba(41,98,255,0.04)); }
# .kpi-blue::before { background: linear-gradient(90deg, #2962FF, #82B1FF); }

# .kpi-green  { background: linear-gradient(135deg, rgba(0,200,83,0.15), rgba(0,200,83,0.04)); }
# .kpi-green::before { background: linear-gradient(90deg, #00C853, #69F0AE); }

# .kpi-red    { background: linear-gradient(135deg, rgba(255,23,68,0.15), rgba(255,23,68,0.04)); }
# .kpi-red::before { background: linear-gradient(90deg, #FF1744, #FF8A80); }

# .kpi-label {
#     font-size: 0.68rem;
#     font-weight: 700;
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     color: #8899AA;
#     margin-bottom: 0.5rem;
# }
# .kpi-value {
#     font-family: 'Space Mono', monospace;
#     font-size: 1.9rem;
#     font-weight: 700;
#     line-height: 1;
#     margin-bottom: 0.3rem;
# }
# .kpi-gold .kpi-value   { color: #FFD54F; }
# .kpi-blue .kpi-value   { color: #82B1FF; }
# .kpi-green .kpi-value  { color: #69F0AE; }
# .kpi-red .kpi-value    { color: #FF8A80; }
# .kpi-sub {
#     font-size: 0.72rem;
#     color: #566A80;
#     font-family: 'Space Mono', monospace;
# }

# /* ── Section Title ── */
# .section-title {
#     font-family: 'Poppins', sans-serif;
#     font-size: 0.72rem;
#     font-weight: 700;
#     letter-spacing: 0.16em;
#     text-transform: uppercase;
#     color: #D4AF37;
#     border-left: 3px solid #D4AF37;
#     padding-left: 0.75rem;
#     margin: 2rem 0 1rem 0;
# }

# /* ── RRR Badge ── */
# .rrr-badge {
#     display: inline-block;
#     background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.05));
#     border: 1px solid rgba(212,175,55,0.3);
#     border-radius: 50px;
#     padding: 0.5rem 1.5rem;
#     font-family: 'Space Mono', monospace;
#     font-size: 1.1rem;
#     color: #D4AF37;
#     font-weight: 700;
#     letter-spacing: 0.05em;
# }

# /* ── Lot Suggestion Cards ── */
# .lot-row {
#     display: grid;
#     grid-template-columns: repeat(3, 1fr);
#     gap: 1rem;
#     margin-bottom: 1.5rem;
# }
# .lot-card {
#     background: rgba(255,255,255,0.03);
#     border-radius: 12px;
#     border: 1px solid rgba(255,255,255,0.07);
#     padding: 1.1rem 1rem;
#     text-align: center;
#     transition: border-color 0.2s;
# }
# .lot-card:hover { border-color: rgba(212,175,55,0.35); }
# .lot-card .lc-label {
#     font-size: 0.65rem;
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     font-weight: 700;
#     margin-bottom: 0.4rem;
# }
# .lot-card .lc-value {
#     font-family: 'Space Mono', monospace;
#     font-size: 1.35rem;
#     font-weight: 700;
#     line-height: 1;
# }
# .lot-card .lc-risk {
#     font-size: 0.68rem;
#     color: #566A80;
#     margin-top: 0.3rem;
#     font-family: 'Space Mono', monospace;
# }
# .lc-conservative .lc-label { color: #69F0AE; }
# .lc-conservative .lc-value { color: #69F0AE; }
# .lc-moderate     .lc-label { color: #FFD54F; }
# .lc-moderate     .lc-value { color: #FFD54F; }
# .lc-aggressive   .lc-label { color: #FF8A80; }
# .lc-aggressive   .lc-value { color: #FF8A80; }

# /* ── Trade Summary Panel ── */
# .summary-panel {
#     background: linear-gradient(135deg, rgba(212,175,55,0.08), rgba(6,13,31,0.95));
#     border: 1px solid rgba(212,175,55,0.2);
#     border-radius: 16px;
#     padding: 1.6rem 1.8rem;
#     margin-bottom: 1.5rem;
# }
# .summary-panel h3 {
#     font-family: 'Poppins', sans-serif;
#     font-size: 0.78rem;
#     letter-spacing: 0.14em;
#     text-transform: uppercase;
#     color: #D4AF37;
#     margin: 0 0 1rem 0;
# }
# .summary-row {
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#     padding: 0.55rem 0;
#     border-bottom: 1px solid rgba(255,255,255,0.05);
#     font-size: 0.88rem;
# }
# .summary-row:last-child { border-bottom: none; }
# .summary-row .sr-label { color: #8899AA; }
# .summary-row .sr-val   { font-family: 'Space Mono', monospace; font-weight: 700; }

# /* ── Risk-o-Meter Bar ── */
# .risk-bar-wrap {
#     background: rgba(255,255,255,0.04);
#     border-radius: 8px;
#     height: 10px;
#     overflow: hidden;
#     margin: 0.6rem 0 0.3rem 0;
# }
# .risk-bar-fill {
#     height: 100%;
#     border-radius: 8px;
#     transition: width 0.4s ease;
# }
# .risk-safe     { background: linear-gradient(90deg, #00C853, #69F0AE); }
# .risk-moderate { background: linear-gradient(90deg, #FFD54F, #FFA000); }
# .risk-danger   { background: linear-gradient(90deg, #FF6D00, #FF1744); }

# /* ── Drawdown Table ── */
# .dd-table {
#     width: 100%;
#     border-collapse: collapse;
#     font-size: 0.82rem;
#     font-family: 'Space Mono', monospace;
# }
# .dd-table th {
#     background: rgba(212,175,55,0.08);
#     color: #D4AF37;
#     font-size: 0.65rem;
#     letter-spacing: 0.1em;
#     text-transform: uppercase;
#     padding: 0.6rem 0.8rem;
#     text-align: left;
#     border-bottom: 1px solid rgba(212,175,55,0.2);
# }
# .dd-table td {
#     padding: 0.55rem 0.8rem;
#     border-bottom: 1px solid rgba(255,255,255,0.04);
#     color: #C0CDD8;
# }
# .dd-table tr:hover td { background: rgba(212,175,55,0.04); }
# .dd-table .loss-val { color: #FF8A80; }
# .dd-table .safe-val { color: #69F0AE; }

# /* ── Warning/Info Boxes ── */
# .warn-box {
#     background: rgba(255,167,38,0.08);
#     border: 1px solid rgba(255,167,38,0.25);
#     border-radius: 10px;
#     padding: 0.8rem 1rem;
#     font-size: 0.82rem;
#     color: #FFB74D;
#     margin-bottom: 0.8rem;
# }
# .info-box {
#     background: rgba(41,98,255,0.08);
#     border: 1px solid rgba(41,98,255,0.25);
#     border-radius: 10px;
#     padding: 0.8rem 1rem;
#     font-size: 0.82rem;
#     color: #82B1FF;
#     margin-bottom: 0.8rem;
# }

# /* ── Plotly override ── */
# .js-plotly-plot .plotly, .js-plotly-plot .plotly div {
#     background: transparent !important;
# }

# /* ── Sidebar gold header ── */
# .sidebar-brand {
#     text-align: center;
#     padding: 0 0 1.5rem 0;
#     border-bottom: 1px solid rgba(212,175,55,0.15);
#     margin-bottom: 1.5rem;
# }
# .sidebar-brand span {
#     font-family: 'Poppins', sans-serif;
#     font-weight: 800;
#     font-size: 1.1rem;
#     background: linear-gradient(90deg, #D4AF37, #FFE082);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     letter-spacing: 0.04em;
# }
# .sidebar-brand small {
#     display: block;
#     font-size: 0.62rem;
#     color: #566A80;
#     letter-spacing: 0.18em;
#     text-transform: uppercase;
#     margin-top: 0.15rem;
# }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # DOMAIN MODEL
# # ─────────────────────────────────────────────
# class XAUUSDCalculator:
#     """Core domain model for XAUUSD risk calculations."""

#     PIP_VALUE_PER_LOT = 1.0  # $1 per pip per standard lot for XAUUSD

#     def __init__(self, account_balance: float, risk_percent: float,
#                  sl_pips: float, tp_pips: float):
#         self.account_balance = account_balance
#         self.risk_percent    = risk_percent
#         self.sl_pips         = sl_pips
#         self.tp_pips         = tp_pips

#     @property
#     def risk_amount(self) -> float:
#         return (self.account_balance * self.risk_percent) / 100

#     @property
#     def lot_size(self) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return self.risk_amount / (self.sl_pips * self.PIP_VALUE_PER_LOT)

#     @property
#     def profit(self) -> float:
#         return self.tp_pips * self.lot_size * self.PIP_VALUE_PER_LOT

#     @property
#     def loss(self) -> float:
#         return self.sl_pips * self.lot_size * self.PIP_VALUE_PER_LOT

#     @property
#     def rrr(self) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return self.tp_pips / self.sl_pips

#     @property
#     def account_after_win(self) -> float:
#         return self.account_balance + self.profit

#     @property
#     def account_after_loss(self) -> float:
#         return self.account_balance - self.loss

#     def lot_for_risk(self, pct: float) -> float:
#         if self.sl_pips <= 0:
#             return 0.0
#         return (self.account_balance * pct / 100) / (self.sl_pips * self.PIP_VALUE_PER_LOT)

#     def equity_simulation(self, n_trades: int, win_rate: float = 0.5) -> list:
#         equity = self.account_balance
#         curve  = [equity]
#         for _ in range(n_trades):
#             if np.random.rand() < win_rate:
#                 equity += self.profit
#             else:
#                 equity -= self.loss
#             curve.append(equity)
#         return curve

#     def drawdown_table(self, consecutive_losses: int = 10) -> pd.DataFrame:
#         rows = []
#         equity = self.account_balance
#         for i in range(1, consecutive_losses + 1):
#             equity -= self.loss
#             dd_pct = ((self.account_balance - equity) / self.account_balance) * 100
#             rows.append({
#                 "Consecutive Losses": i,
#                 "Account Balance ($)": round(equity, 2),
#                 "Total Drawdown ($)": round(self.loss * i, 2),
#                 "Drawdown %": round(dd_pct, 2),
#             })
#         return pd.DataFrame(rows)


# # ─────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────
# st.sidebar.markdown("""
# <div class='sidebar-brand'>
#     <span>⚡ XAUUSD RISK PRO</span>
#     <small>Professional Risk Engine</small>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.markdown("### Trade Parameters")

# account_balance = st.sidebar.number_input(
#     "Account Balance ($)",
#     min_value=100.0,
#     max_value=10_000_000.0,
#     value=10_000.0,
#     step=500.0,
#     format="%.2f"
# )

# risk_percent = st.sidebar.number_input(
#     "Risk % per Trade",
#     min_value=0.1,
#     max_value=10.0,
#     value=2.0,
#     step=0.1,
#     format="%.1f"
# )

# sl_pips = st.sidebar.number_input(
#     "Stop Loss (pips)",
#     min_value=1,
#     max_value=500,
#     value=50,
#     step=1
# )

# tp_pips = st.sidebar.number_input(
#     "Take Profit (pips)",
#     min_value=1,
#     max_value=5000,
#     value=100,
#     step=1
# )

# # ─────────────────────────────────────────────
# # VALIDATION
# # ─────────────────────────────────────────────
# calc = XAUUSDCalculator(account_balance, risk_percent, sl_pips, tp_pips)

# if sl_pips <= 0:
#     st.sidebar.error("❌ Stop Loss must be > 0")
# if tp_pips <= sl_pips:
#     st.sidebar.warning("⚠️ TP < SL — negative risk-reward detected")
# if risk_percent >= 5:
#     st.sidebar.warning("⚠️ Risk ≥ 5% — high-risk territory")


# # ─────────────────────────────────────────────
# # HEADER
# # ─────────────────────────────────────────────
# st.markdown("""
# <h1 style='
#     font-family: Poppins, sans-serif;
#     font-weight: 800;
#     font-size: 1.7rem;
#     background: linear-gradient(90deg, #D4AF37 0%, #FFE082 50%, #D4AF37 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     margin-bottom: 0;
#     letter-spacing: -0.01em;
# '>XAUUSD Risk Management Pro</h1>
# <p style='color:#566A80; font-size:0.82rem; letter-spacing:0.1em;
#     text-transform:uppercase; margin-top:0.3rem; margin-bottom:2rem;'>
#     Precision Risk Engine &nbsp;·&nbsp; Gold Trading &nbsp;·&nbsp; Professional Grade
# </p>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # KPI CARDS
# # ─────────────────────────────────────────────
# st.markdown(f"""
# <div class='kpi-grid'>
#     <div class='kpi-card kpi-blue'>
#         <div class='kpi-label'>Lot Size</div>
#         <div class='kpi-value'>{calc.lot_size:.3f}</div>
#         <div class='kpi-sub'>Standard Lots</div>
#     </div>
#     <div class='kpi-card kpi-gold'>
#         <div class='kpi-label'>Risk Amount</div>
#         <div class='kpi-value'>${calc.risk_amount:,.2f}</div>
#         <div class='kpi-sub'>{risk_percent}% of account</div>
#     </div>
#     <div class='kpi-card kpi-green'>
#         <div class='kpi-label'>Profit if TP Hit</div>
#         <div class='kpi-value'>${calc.profit:,.2f}</div>
#         <div class='kpi-sub'>+{(calc.profit/account_balance*100):.2f}% return</div>
#     </div>
#     <div class='kpi-card kpi-red'>
#         <div class='kpi-label'>Loss if SL Hit</div>
#         <div class='kpi-value'>${calc.loss:,.2f}</div>
#         <div class='kpi-sub'>-{(calc.loss/account_balance*100):.2f}% drawdown</div>
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # RRR + RISK BAR
# # ─────────────────────────────────────────────
# col_rrr, col_riskbar = st.columns([1, 2])

# with col_rrr:
#     rrr_color = "#69F0AE" if calc.rrr >= 2 else ("#FFD54F" if calc.rrr >= 1 else "#FF8A80")
#     st.markdown(f"""
#     <div style='padding:1rem 0;'>
#         <div class='section-title'>Risk / Reward</div>
#         <div style='font-family:Space Mono,monospace; font-size:2.4rem;
#                     font-weight:700; color:{rrr_color}; line-height:1;'>
#             1 : {calc.rrr:.2f}
#         </div>
#         <div style='color:#566A80; font-size:0.75rem; margin-top:0.4rem;'>
#             {"✅ Excellent RRR" if calc.rrr >= 2 else ("⚠️ Acceptable RRR" if calc.rrr >= 1 else "❌ Negative RRR")}
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with col_riskbar:
#     bar_class = "risk-safe" if risk_percent <= 2 else ("risk-moderate" if risk_percent <= 4 else "risk-danger")
#     bar_label = "🟢 Safe Zone" if risk_percent <= 2 else ("🟡 Caution Zone" if risk_percent <= 4 else "🔴 Danger Zone")
#     st.markdown(f"""
#     <div style='padding:1rem 0;'>
#         <div class='section-title'>Risk-o-Meter</div>
#         <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;'>
#             <span style='font-size:0.78rem; color:#8899AA;'>{bar_label}</span>
#             <span style='font-family:Space Mono,monospace; font-size:0.9rem; color:#D4AF37; font-weight:700;'>{risk_percent}%</span>
#         </div>
#         <div class='risk-bar-wrap'>
#             <div class='risk-bar-fill {bar_class}' style='width:{min(risk_percent*10, 100)}%;'></div>
#         </div>
#         <div style='display:flex; justify-content:space-between; font-size:0.6rem; color:#566A80; margin-top:0.25rem;'>
#             <span>0%</span><span>2% Safe</span><span>5% Risky</span><span>10%</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # TRADE SUMMARY + LOT SUGGESTIONS
# # ─────────────────────────────────────────────
# col_summ, col_lots = st.columns([1, 1])

# with col_summ:
#     st.markdown("<div class='section-title'>Trade Summary</div>", unsafe_allow_html=True)
#     st.markdown(f"""
#     <div class='summary-panel'>
#         <h3>📋 Position Overview</h3>
#         <div class='summary-row'>
#             <span class='sr-label'>Account Balance</span>
#             <span class='sr-val' style='color:#E8EAF0;'>${account_balance:,.2f}</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>You are risking</span>
#             <span class='sr-val' style='color:#FFD54F;'>${calc.risk_amount:,.2f} ({risk_percent}%)</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Position Size</span>
#             <span class='sr-val' style='color:#82B1FF;'>{calc.lot_size:.3f} lots</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Stop Loss</span>
#             <span class='sr-val' style='color:#FF8A80;'>{sl_pips} pips → -${calc.loss:,.2f}</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Take Profit</span>
#             <span class='sr-val' style='color:#69F0AE;'>{tp_pips} pips → +${calc.profit:,.2f}</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Risk / Reward</span>
#             <span class='sr-val' style='color:#D4AF37;'>1 : {calc.rrr:.2f}</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Account after Win</span>
#             <span class='sr-val' style='color:#69F0AE;'>${calc.account_after_win:,.2f}</span>
#         </div>
#         <div class='summary-row'>
#             <span class='sr-label'>Account after Loss</span>
#             <span class='sr-val' style='color:#FF8A80;'>${calc.account_after_loss:,.2f}</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# with col_lots:
#     st.markdown("<div class='section-title'>Lot Size Suggestions</div>", unsafe_allow_html=True)
#     l1 = calc.lot_for_risk(1)
#     l2 = calc.lot_for_risk(2)
#     l5 = calc.lot_for_risk(5)
#     st.markdown(f"""
#     <div class='lot-row'>
#         <div class='lot-card lc-conservative'>
#             <div class='lc-label'>Conservative</div>
#             <div class='lc-value'>{l1:.3f}</div>
#             <div class='lc-risk'>1% Risk · ${account_balance*0.01:,.0f}</div>
#         </div>
#         <div class='lot-card lc-moderate'>
#             <div class='lc-label'>Moderate</div>
#             <div class='lc-value'>{l2:.3f}</div>
#             <div class='lc-risk'>2% Risk · ${account_balance*0.02:,.0f}</div>
#         </div>
#         <div class='lot-card lc-aggressive'>
#             <div class='lc-label'>Aggressive</div>
#             <div class='lc-value'>{l5:.3f}</div>
#             <div class='lc-risk'>5% Risk · ${account_balance*0.05:,.0f}</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Formula Reference
#     st.markdown("<div class='section-title'>Formula Reference</div>", unsafe_allow_html=True)
#     st.markdown("""
#     <div style='background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.07);
#                 border-radius:12px; padding:1rem 1.2rem; font-family:Space Mono,monospace;
#                 font-size:0.75rem; line-height:2; color:#8899AA;'>
#         <span style='color:#D4AF37;'>Risk $</span>    = Balance × Risk% / 100<br>
#         <span style='color:#82B1FF;'>Lot Size</span>  = Risk$ / (SL pips × $1)<br>
#         <span style='color:#69F0AE;'>Profit</span>    = TP pips × Lot × $1<br>
#         <span style='color:#FF8A80;'>Loss</span>      = SL pips × Lot × $1<br>
#         <span style='color:#FFD54F;'>RRR</span>       = TP pips / SL pips
#     </div>
#     """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # FOOTER
# # ─────────────────────────────────────────────
# st.markdown("""
# <div style='text-align:center; padding:2.5rem 0 1rem 0; color:#2A3A4A;
#             font-size:0.7rem; letter-spacing:0.12em; text-transform:uppercase;'>
#     XAUUSD Risk Management Pro &nbsp;·&nbsp; For Educational Purposes Only &nbsp;·&nbsp;
#     Not Financial Advice
# </div>
# """, unsafe_allow_html=True)
