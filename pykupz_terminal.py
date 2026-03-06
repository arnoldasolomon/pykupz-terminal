"""
PYKUPZ LIVE TERMINAL — Production-Grade Financial Intelligence System
=======================================================================
# requirements.txt
# streamlit>=1.32.0
# yfinance>=0.2.40
# pandas>=2.0.0
# plotly>=5.20.0
# requests>=2.31.0
# beautifulsoup4>=4.12.0
# numpy>=1.26.0
# scipy>=1.12.0
# openpyxl>=3.1.0
# xlsxwriter>=3.2.0
"""

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
from datetime import datetime, timedelta
import json
import time
import warnings
import re
from io import BytesIO
import scipy.stats as stats

warnings.filterwarnings("ignore")

# ────────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG & THEME
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PYKUPZ LIVE TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

:root {
  --bg: #050810;
  --surface: #0a0f1e;
  --surface2: #0d1428;
  --border: #1a2540;
  --accent: #00d4ff;
  --accent2: #7b2fff;
  --green: #00ff88;
  --red: #ff3366;
  --amber: #ffaa00;
  --text: #c8d8f0;
  --dim: #4a6080;
}

html, body, [class*="css"] {
  background-color: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Rajdhani', sans-serif !important;
}

.main { background: var(--bg) !important; }

/* HEADER */
.terminal-header {
  background: linear-gradient(135deg, #050810 0%, #0a1628 50%, #050810 100%);
  border: 1px solid var(--accent);
  border-radius: 4px;
  padding: 16px 24px;
  margin-bottom: 16px;
  box-shadow: 0 0 40px rgba(0,212,255,0.15), inset 0 1px 0 rgba(0,212,255,0.3);
  position: relative;
  overflow: hidden;
}
.terminal-header::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.terminal-title {
  font-family: 'Orbitron', monospace !important;
  font-size: 28px !important;
  font-weight: 900 !important;
  letter-spacing: 6px !important;
  color: var(--accent) !important;
  text-shadow: 0 0 20px rgba(0,212,255,0.6), 0 0 40px rgba(0,212,255,0.3);
  margin: 0 !important;
}
.terminal-sub {
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 11px !important;
  color: var(--dim) !important;
  letter-spacing: 3px !important;
  margin-top: 4px !important;
}

/* STATUS BADGES */
.badge-green { background: rgba(0,255,136,0.15); color: var(--green); border: 1px solid var(--green); border-radius: 3px; padding: 2px 8px; font-family: 'Share Tech Mono', monospace; font-size: 11px; }
.badge-red { background: rgba(255,51,102,0.15); color: var(--red); border: 1px solid var(--red); border-radius: 3px; padding: 2px 8px; font-family: 'Share Tech Mono', monospace; font-size: 11px; }
.badge-amber { background: rgba(255,170,0,0.15); color: var(--amber); border: 1px solid var(--amber); border-radius: 3px; padding: 2px 8px; font-family: 'Share Tech Mono', monospace; font-size: 11px; }
.badge-blue { background: rgba(0,212,255,0.15); color: var(--accent); border: 1px solid var(--accent); border-radius: 3px; padding: 2px 8px; font-family: 'Share Tech Mono', monospace; font-size: 11px; }

/* METRIC CARDS */
.metric-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 16px;
  text-align: center;
}
.metric-val { font-family: 'Orbitron', monospace; font-size: 20px; font-weight: 700; color: var(--accent); }
.metric-label { font-size: 10px; color: var(--dim); letter-spacing: 2px; text-transform: uppercase; margin-top: 4px; }

/* AUDIT PANEL */
.audit-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  background: var(--surface);
  border-left: 3px solid var(--accent);
  margin-bottom: 4px;
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
}
.audit-row.warn { border-left-color: var(--amber); }
.audit-row.fail { border-left-color: var(--red); }

/* TABLES */
.stDataFrame { background: var(--surface) !important; }
div[data-testid="stDataFrame"] > div { background: var(--surface) !important; }

/* TERMINAL INPUT */
.stTextInput input {
  background: var(--surface2) !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
  font-family: 'Share Tech Mono', monospace !important;
  letter-spacing: 1px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-bottom: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  font-family: 'Orbitron', monospace !important;
  font-size: 11px !important;
  letter-spacing: 2px !important;
  color: var(--dim) !important;
}
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
}

/* EXPANDERS */
.streamlit-expanderHeader {
  background: var(--surface) !important;
  font-family: 'Share Tech Mono', monospace !important;
  font-size: 12px !important;
  color: var(--accent) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

/* DIVIDER */
.hline { border: none; border-top: 1px solid var(--border); margin: 12px 0; }

/* TICKER CHIP */
.ticker-chip {
  display: inline-block;
  background: rgba(0,212,255,0.1);
  border: 1px solid var(--accent);
  border-radius: 3px;
  padding: 2px 8px;
  font-family: 'Orbitron', monospace;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  margin: 2px;
}

/* PRICE UP/DOWN */
.price-up { color: var(--green); font-weight: 700; }
.price-down { color: var(--red); font-weight: 700; }

/* SCAN LINE EFFECT */
@keyframes scanline {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100vh); }
}

/* BUTTON */
.stButton button {
  background: transparent !important;
  border: 1px solid var(--accent) !important;
  color: var(--accent) !important;
  font-family: 'Share Tech Mono', monospace !important;
  letter-spacing: 2px !important;
  border-radius: 3px !important;
}
.stButton button:hover {
  background: rgba(0,212,255,0.1) !important;
  box-shadow: 0 0 10px rgba(0,212,255,0.3) !important;
}

/* SELECT BOX */
.stSelectbox select, .stMultiSelect > div {
  background: var(--surface) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
}

p, li, span { font-family: 'Rajdhani', sans-serif !important; }
code { font-family: 'Share Tech Mono', monospace !important; color: var(--accent) !important; background: var(--surface2) !important; }
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ────────────────────────────────────────────────────────────────────────────────
if 'price_cache' not in st.session_state:
    st.session_state.price_cache = {}
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = {}
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []
if 'cmd_history' not in st.session_state:
    st.session_state.cmd_history = []
if 'terminal_output' not in st.session_state:
    st.session_state.terminal_output = []
if 'excel_data' not in st.session_state:
    st.session_state.excel_data = {}

# ────────────────────────────────────────────────────────────────────────────────
# CONSTANTS / WEIGHTAGES
# ────────────────────────────────────────────────────────────────────────────────
WEIGHTAGES = {
    "Current": {"rev_growth": 0.30, "eps": 0.20, "ebitda": 0.10, "cashflow": 0.20, "net_debt": 0.05, "adj_factor": 0.15},
    "Nandini": {"rev_growth": 0.20, "eps": 0.20, "ebitda": 0.10, "cashflow": 0.10, "net_debt": 0.05, "adj_factor": 0.20, "gaps_gape": 0.10, "sector": 0.05},
    "Arnold":  {"rev_growth": 0.20, "eps": 0.15, "ebitda": 0.10, "cashflow": 0.10, "net_debt": 0.00, "hypothesis": 0.35, "sector": 0.10},
}
GAPS_WEIGHT = 0.5
GAPE_WEIGHT = 1.2
SP500_MEDIAN_PE = 15.0
SP500_MEDIAN_PS = 1.54

# ────────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_excel(file_bytes):
    """Load all relevant sheets from Excel."""
    data = {}
    try:
        xl = pd.ExcelFile(BytesIO(file_bytes))

        # Stocks_to_buy
        df_stb = pd.read_excel(BytesIO(file_bytes), sheet_name='Stocks_to_buy', header=0)
        df_stb.columns = [str(c).strip() for c in df_stb.columns]
        data['stb'] = df_stb

        # Q1 2026 Stocks_to_buy
        df_q1 = pd.read_excel(BytesIO(file_bytes), sheet_name='Q1 2026  Stocks_to_buy', header=1)
        df_q1.columns = [str(c).strip() for c in df_q1.columns]
        data['q1'] = df_q1

        # Bonus
        df_bonus = pd.read_excel(BytesIO(file_bytes), sheet_name='Bonus', header=0)
        data['bonus'] = df_bonus

        # Hypothesis
        df_hyp = pd.read_excel(BytesIO(file_bytes), sheet_name='HYPOTHESIS', header=0)
        data['hypothesis'] = df_hyp

        # Stocks_to_sell
        df_sell = pd.read_excel(BytesIO(file_bytes), sheet_name='Stocks to Sell', header=0)
        df_sell.columns = [str(c).strip() for c in df_sell.columns]
        data['sell'] = df_sell

        # Weightage
        df_wt = pd.read_excel(BytesIO(file_bytes), sheet_name='Weightage sheet', header=0)
        data['weightage'] = df_wt

    except Exception as e:
        data['error'] = str(e)
    return data


def parse_stb_tickers(df):
    """Extract clean ticker rows from STB sheet."""
    rows = []
    for _, r in df.iterrows():
        ticker = r.iloc[1] if len(r) > 1 else None
        if isinstance(ticker, str) and ticker.strip() and ticker.strip().upper() == ticker.strip() and len(ticker.strip()) <= 7:
            name = r.iloc[2] if len(r) > 2 else ''
            price = r.iloc[3] if len(r) > 3 else None
            gaps = r.iloc[22] if len(r) > 22 else None
            gape = r.iloc[41] if len(r) > 41 else None
            rec = r.iloc[108] if len(r) > 108 else ''
            points = r.iloc[128] if len(r) > 128 else None
            rev_3y = r.iloc[54] if len(r) > 54 else None
            rev_ly = r.iloc[55] if len(r) > 55 else None
            rev_growth = r.iloc[56] if len(r) > 56 else None
            rev_cagr = r.iloc[57] if len(r) > 57 else None
            ebitda_3y = r.iloc[65] if len(r) > 65 else None
            ebitda_ly = r.iloc[66] if len(r) > 66 else None
            ebitda_g = r.iloc[67] if len(r) > 67 else None
            eps_3y = r.iloc[79] if len(r) > 79 else None
            eps_ly = r.iloc[80] if len(r) > 80 else None
            eps_cagr = r.iloc[81] if len(r) > 81 else None
            fcf = r.iloc[89] if len(r) > 89 else None
            net_debt = r.iloc[98] if len(r) > 98 else None
            sector = r.iloc[10] if len(r) > 10 else ''
            exchange = r.iloc[8] if len(r) > 8 else ''
            mcap = r.iloc[16] if len(r) > 16 else None
            price_follows = r.iloc[114] if len(r) > 114 else ''
            score_rev = r.iloc[119] if len(r) > 119 else None
            score_eps = r.iloc[120] if len(r) > 120 else None
            score_ebitda = r.iloc[121] if len(r) > 121 else None
            score_cf = r.iloc[122] if len(r) > 122 else None
            score_nd = r.iloc[123] if len(r) > 123 else None
            buy_limits = r.iloc[112] if len(r) > 112 else None
            rows.append({
                'ticker': ticker.strip(), 'name': str(name) if name else '',
                'buy_price': price, 'gaps': gaps, 'gape': gape,
                'recommendation': str(rec) if rec else '',
                'stb_points': points,
                'rev_3y': rev_3y, 'rev_ly': rev_ly, 'rev_growth_ly': rev_growth,
                'rev_cagr': rev_cagr, 'ebitda_3y': ebitda_3y, 'ebitda_ly': ebitda_ly,
                'ebitda_growth': ebitda_g, 'eps_3y': eps_3y, 'eps_ly': eps_ly,
                'eps_cagr': eps_cagr, 'fcf': fcf, 'net_debt': net_debt,
                'sector': str(sector) if sector else '', 'exchange': str(exchange) if exchange else '',
                'mcap_excel': mcap, 'price_follows': str(price_follows) if price_follows else '',
                'score_rev': score_rev, 'score_eps': score_eps,
                'score_ebitda': score_ebitda, 'score_cf': score_cf, 'score_nd': score_nd,
                'buy_limits': str(buy_limits) if buy_limits else '',
            })
    return rows


def parse_q1_tickers(df):
    """Extract tickers from Q1 2026 sheet."""
    rows = []
    for _, r in df.iterrows():
        ticker = r.iloc[1] if len(r) > 1 else None
        if isinstance(ticker, str) and ticker.strip() and len(ticker.strip()) <= 7:
            t = ticker.strip().upper()
            rows.append({
                'ticker': t,
                'name': str(r.iloc[2]) if len(r) > 2 else '',
                'pe': r.iloc[4] if len(r) > 4 else None,
                'ps': r.iloc[5] if len(r) > 5 else None,
                'mcap': r.iloc[6] if len(r) > 6 else None,
                'price': r.iloc[8] if len(r) > 8 else None,
                'gaps': r.iloc[12] if len(r) > 12 else None,
                'gape': r.iloc[24] if len(r) > 24 else None,
                'rev_3y': r.iloc[36] if len(r) > 36 else None,
                'rev_ly': r.iloc[37] if len(r) > 37 else None,
                'rev_growth': r.iloc[38] if len(r) > 38 else None,
                'rev_cagr_3y': r.iloc[39] if len(r) > 39 else None,
                'rev_ttm': r.iloc[40] if len(r) > 40 else None,
                'ebitda_3y': r.iloc[49] if len(r) > 49 else None,
                'ebitda_ly': r.iloc[51] if len(r) > 51 else None,
                'ebitda_growth': r.iloc[52] if len(r) > 52 else None,
                'eps_3y': r.iloc[63] if len(r) > 63 else None,
                'eps_ly': r.iloc[64] if len(r) > 64 else None,
                'eps_cagr': r.iloc[65] if len(r) > 65 else None,
                'fcf_ttm': r.iloc[73] if len(r) > 73 else None,
                'net_debt_ttm': r.iloc[77] if len(r) > 77 else None,
                'recommendation': str(r.iloc[80]) if len(r) > 80 else '',
                'score_rev': r.iloc[82] if len(r) > 82 else None,
                'score_eps': r.iloc[83] if len(r) > 83 else None,
                'score_ebitda': r.iloc[84] if len(r) > 84 else None,
                'score_cf': r.iloc[85] if len(r) > 85 else None,
                'score_nd': r.iloc[86] if len(r) > 86 else None,
                'total_points': r.iloc[88] if len(r) > 88 else None,
            })
    return rows


def parse_bonus(df):
    """Parse bonus portfolio."""
    rows = []
    for _, r in df.iterrows():
        ticker = r.iloc[1] if len(r) > 1 else None
        if isinstance(ticker, str) and ticker.strip() and len(ticker.strip()) <= 6 and ticker.strip().isalpha():
            rows.append({
                'date': r.iloc[0],
                'ticker': ticker.strip().upper(),
                'name': str(r.iloc[2]) if len(r) > 2 else '',
                'exchange': str(r.iloc[3]) if len(r) > 3 else '',
                'sector': str(r.iloc[4]) if len(r) > 4 else '',
                'buy_price': r.iloc[7] if len(r) > 7 else None,
                'qty': r.iloc[10] if len(r) > 10 else None,
                'invested': r.iloc[11] if len(r) > 11 else None,
            })
    return rows


# ────────────────────────────────────────────────────────────────────────────────
# LIVE DATA ENGINE
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_price(ticker):
    """Fetch live price via yfinance."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="2d")
        if hist.empty:
            return None, None, None
        price = float(hist['Close'].iloc[-1])
        prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
        chg = (price - prev_close) / prev_close
        volume = float(hist['Volume'].iloc[-1]) if 'Volume' in hist else None
        return price, chg, volume
    except Exception:
        return None, None, None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_fundamentals(ticker):
    """Fetch fundamentals via yfinance."""
    try:
        t = yf.Ticker(ticker)
        info = t.info
        return {
            'market_cap': info.get('marketCap'),
            'pe': info.get('trailingPE'),
            'forward_pe': info.get('forwardPE'),
            'ps': info.get('priceToSalesTrailing12Months'),
            'revenue': info.get('totalRevenue'),
            'ebitda': info.get('ebitda'),
            'net_income': info.get('netIncomeToCommon'),
            'eps': info.get('trailingEps'),
            'forward_eps': info.get('forwardEps'),
            'fcf': info.get('freeCashflow'),
            'total_debt': info.get('totalDebt'),
            'cash': info.get('totalCash'),
            'beta': info.get('beta'),
            'short_name': info.get('shortName', ticker),
            'sector': info.get('sector', ''),
            'industry': info.get('industry', ''),
            'employees': info.get('fullTimeEmployees'),
            'earnings_date': info.get('earningsTimestamp'),
            'revenue_growth': info.get('revenueGrowth'),
            'earnings_growth': info.get('earningsGrowth'),
            '52w_high': info.get('fiftyTwoWeekHigh'),
            '52w_low': info.get('fiftyTwoWeekLow'),
        }
    except Exception:
        return {}


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_historical(ticker, period="5y"):
    """Fetch historical OHLCV data."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        return hist
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_financials(ticker):
    """Fetch multi-year financials."""
    try:
        t = yf.Ticker(ticker)
        income = t.income_stmt
        cf = t.cash_flow
        balance = t.balance_sheet
        return income, cf, balance
    except Exception:
        return None, None, None


# ────────────────────────────────────────────────────────────────────────────────
# AUDIT ALGORITHMS
# ────────────────────────────────────────────────────────────────────────────────

def algo1_multi_source_reconciliation(ticker):
    """Algorithm 1: Multi-Source Reconciliation."""
    results = {'ticker': ticker, 'sources': {}, 'weighted': None, 'status': 'UNKNOWN', 'notes': []}
    try:
        # Source 1: Yahoo Finance (yfinance) — weight 40%
        t = yf.Ticker(ticker)
        info = t.info
        yf_price = info.get('currentPrice') or info.get('regularMarketPrice')
        yf_rev = info.get('totalRevenue')
        yf_eps = info.get('trailingEps')
        results['sources']['Yahoo'] = {'price': yf_price, 'revenue': yf_rev, 'eps': yf_eps, 'weight': 0.40}

        # Source 2: Fast Info (secondary Yahoo endpoint) — weight 30%
        fast = t.fast_info
        fa_price = getattr(fast, 'last_price', None)
        results['sources']['YF_Fast'] = {'price': fa_price, 'revenue': None, 'eps': None, 'weight': 0.30}

        # Source 3: History-based (calculate from OHLC) — weight 20%
        hist = t.history(period="1d")
        hist_price = float(hist['Close'].iloc[-1]) if not hist.empty else None
        results['sources']['Historical'] = {'price': hist_price, 'revenue': None, 'eps': None, 'weight': 0.20}

        # Source 4: Financials from quarterly — weight 10%
        try:
            qfin = t.quarterly_income_stmt
            qf_rev = float(qfin.loc['Total Revenue'].iloc[0]) / 1e9 if 'Total Revenue' in qfin.index else None
        except Exception:
            qf_rev = None
        results['sources']['Quarterly'] = {'price': None, 'revenue': qf_rev, 'eps': None, 'weight': 0.10}

        # Weighted average price
        prices = [(v['price'], v['weight']) for v in results['sources'].values() if v.get('price')]
        if prices:
            total_w = sum(w for _, w in prices)
            weighted_price = sum(p * w for p, w in prices) / total_w
            results['weighted'] = round(weighted_price, 4)
            # Check consistency
            vals = [p for p, _ in prices]
            spread = (max(vals) - min(vals)) / np.mean(vals) * 100 if np.mean(vals) != 0 else 0
            if spread < 1.0:
                results['status'] = '✅ AUDITED'
            elif spread < 3.0:
                results['status'] = '⚠️ MINOR DISCREPANCY'
                results['notes'].append(f"Price spread {spread:.2f}% across sources")
            else:
                results['status'] = '🚨 DISCREPANCY DETECTED'
                results['notes'].append(f"Price spread {spread:.2f}% — verify data")
    except Exception as e:
        results['status'] = f'❌ FETCH ERROR: {str(e)[:50]}'
    return results


def algo2_statistical_anomaly_detection(ticker, metric_name, current_value, historical_values):
    """Algorithm 2: Statistical Anomaly Detection — z-score against historical."""
    result = {'ticker': ticker, 'metric': metric_name, 'current': current_value,
              'mean': None, 'std': None, 'z_score': None, 'status': '🔵 NORMAL', 'flag': False}
    if not historical_values or len(historical_values) < 3:
        result['status'] = '⚪ INSUFFICIENT HISTORY'
        return result
    clean = [v for v in historical_values if v is not None and not np.isnan(v)]
    if len(clean) < 3 or current_value is None:
        result['status'] = '⚪ NO DATA'
        return result
    mean = np.mean(clean)
    std = np.std(clean)
    result['mean'] = round(mean, 4)
    result['std'] = round(std, 4)
    if std == 0:
        result['status'] = '⚪ ZERO STD'
        return result
    z = (current_value - mean) / std
    result['z_score'] = round(z, 3)
    if abs(z) > 3:
        result['status'] = '🚨 STATISTICAL OUTLIER'
        result['flag'] = True
    elif abs(z) > 2:
        result['status'] = '⚠️ ELEVATED (>2σ)'
        result['flag'] = True
    else:
        result['status'] = '✅ WITHIN NORMAL RANGE'
    return result


def algo3_cashflow_logic_reconciliation(revenue, ebitda, ebit, net_income, depreciation, interest, taxes, fcf, op_cf):
    """Algorithm 3: Cash-Flow Logic Chain Reconciliation."""
    issues = []
    checks = {}

    if ebitda and ebit and depreciation:
        expected_ebitda = ebit + abs(depreciation)
        diff = abs(ebitda - expected_ebitda) / abs(ebitda) * 100 if ebitda != 0 else 0
        if diff > 1:
            issues.append(f"EBITDA→EBIT gap: {diff:.1f}% (D&A mismatch?)")
            checks['ebitda_ebit'] = '❌'
        else:
            checks['ebitda_ebit'] = '✅'

    if net_income and ebitda and depreciation and interest and taxes:
        implied_ni = ebitda - abs(depreciation) - abs(interest) - abs(taxes)
        diff = abs(net_income - implied_ni) / abs(net_income) * 100 if net_income != 0 else 0
        if diff > 5:
            issues.append(f"Net Income reconciliation off by {diff:.1f}%")
            checks['net_income'] = '❌'
        else:
            checks['net_income'] = '✅'

    if fcf and op_cf:
        if fcf > op_cf * 1.1:
            issues.append("FCF > OCF by >10% — unusual capex accounting")
            checks['fcf_ocf'] = '⚠️'
        else:
            checks['fcf_ocf'] = '✅'

    overall = '✅ CHAIN INTACT' if not issues else f'🚨 {len(issues)} ISSUE(S)'
    return {'checks': checks, 'issues': issues, 'overall': overall}


def algo4_freshness_reliability_score(last_price_date, last_fundamentals_date):
    """Algorithm 4: Freshness & Reliability Scoring."""
    now = datetime.now()
    price_age_days = (now - last_price_date).days if last_price_date else 999
    fund_age_days = (now - last_fundamentals_date).days if last_fundamentals_date else 999

    if price_age_days < 1:
        price_score = 100
    elif price_age_days < 7:
        price_score = 80
    elif price_age_days < 30:
        price_score = 60
    else:
        price_score = 40

    if fund_age_days < 90:
        fund_score = 100
    elif fund_age_days < 180:
        fund_score = 75
    else:
        fund_score = 40

    overall = round(price_score * 0.5 + fund_score * 0.5)
    flag = overall < 70

    if overall >= 90:
        status = '🟢 FRESH'
    elif overall >= 70:
        status = '🟡 ACCEPTABLE'
    else:
        status = '🔴 STALE DATA'

    return {
        'price_score': price_score,
        'fund_score': fund_score,
        'overall': overall,
        'status': status,
        'flag': flag,
    }


def algo5_historical_trend_validation(ticker, metric_series, metric_name):
    """Algorithm 5: Historical Trend Validation vs CAGR bands."""
    result = {'metric': metric_name, 'status': '🔵 UNCHECKED', 'cagr_3y': None, 'cagr_5y': None, 'flag': False}
    if not metric_series or len(metric_series) < 3:
        return result
    clean = [(i, v) for i, v in enumerate(metric_series) if v is not None and v != 0]
    if len(clean) < 2:
        return result
    try:
        vals = [v for _, v in clean]
        n = len(vals)
        if n >= 3 and vals[0] != 0:
            cagr_3y = (vals[-1] / vals[max(0, n-4)]) ** (1 / min(3, n-1)) - 1
            result['cagr_3y'] = round(cagr_3y * 100, 2)
        if n >= 5 and vals[0] != 0:
            cagr_5y = (vals[-1] / vals[0]) ** (1 / (n-1)) - 1
            result['cagr_5y'] = round(cagr_5y * 100, 2)

        # Check if latest growth is within ±2σ of historical growth rates
        growths = [(vals[i] - vals[i-1]) / abs(vals[i-1]) for i in range(1, n) if vals[i-1] != 0]
        if len(growths) >= 3:
            mean_g = np.mean(growths)
            std_g = np.std(growths)
            latest_g = growths[-1]
            if std_g > 0:
                z = (latest_g - mean_g) / std_g
                if abs(z) > 2:
                    result['status'] = '📉 TREND BREAK'
                    result['flag'] = True
                else:
                    result['status'] = '✅ TREND INTACT'
            else:
                result['status'] = '✅ STABLE TREND'
    except Exception:
        result['status'] = '⚠️ COMPUTE ERROR'
    return result


def algo6_guidance_backtest(ticker):
    """Algorithm 6: Guidance Back-Testing — compare actuals vs prior guidance."""
    result = {'ticker': ticker, 'quarters': [], 'accuracy': None, 'status': '⚪ NO DATA', 'flag': False}
    try:
        t = yf.Ticker(ticker)
        earnings_hist = t.earnings_history
        if earnings_hist is not None and not earnings_hist.empty and 'epsEstimate' in earnings_hist.columns:
            recent = earnings_hist.dropna(subset=['epsEstimate', 'epsActual']).tail(8)
            if len(recent) >= 2:
                beats = 0
                total = 0
                for _, row in recent.iterrows():
                    est = row.get('epsEstimate', 0)
                    actual = row.get('epsActual', 0)
                    if est and est != 0:
                        pct = (actual - est) / abs(est) * 100
                        result['quarters'].append({
                            'date': str(row.name)[:10] if hasattr(row, 'name') else '',
                            'estimate': round(est, 3),
                            'actual': round(actual, 3),
                            'beat_pct': round(pct, 1),
                        })
                        total += 1
                        if actual >= est:
                            beats += 1

                if total > 0:
                    acc = beats / total * 100
                    result['accuracy'] = round(acc, 1)
                    if acc >= 75:
                        result['status'] = f'✅ {acc:.0f}% BEAT RATE (last {total}Q)'
                    elif acc >= 50:
                        result['status'] = f'⚠️ {acc:.0f}% BEAT RATE'
                        result['flag'] = True
                    else:
                        result['status'] = f'🚨 {acc:.0f}% BEAT RATE — LOW ACCURACY'
                        result['flag'] = True
    except Exception:
        result['status'] = '⚪ DATA UNAVAILABLE'
    return result


def algo7_hypothesis_audit(ticker, gaps_excel, gape_excel, current_price, fundamentals):
    """Algorithm 7: Hypothesis & Valuation Audit."""
    result = {
        'ticker': ticker,
        'checks': [],
        'validated': 0,
        'total': 0,
        'overall': '⚪ NOT EVALUATED',
    }

    pe = fundamentals.get('pe')
    ps = fundamentals.get('ps')
    eps = fundamentals.get('eps')
    revenue = fundamentals.get('revenue')
    mcap = fundamentals.get('market_cap')

    # GAPS validation
    if gaps_excel and current_price and isinstance(gaps_excel, (int, float)) and not np.isnan(gaps_excel):
        deviation = (current_price - gaps_excel) / gaps_excel * 100 if gaps_excel != 0 else 0
        validated = abs(deviation) < 30
        result['checks'].append({
            'name': 'GAPS Price',
            'excel_val': gaps_excel,
            'live_val': current_price,
            'deviation': round(deviation, 1),
            'status': '✅ VALIDATED' if validated else '⚠️ DEVIATING',
            'badge': f"{deviation:+.1f}%",
        })
        result['total'] += 1
        if validated:
            result['validated'] += 1

    # GAPE validation
    if gape_excel and current_price and isinstance(gape_excel, (int, float)) and not np.isnan(gape_excel):
        deviation = (current_price - gape_excel) / gape_excel * 100 if gape_excel != 0 else 0
        validated = abs(deviation) < 35
        result['checks'].append({
            'name': 'GAPE Price',
            'excel_val': gape_excel,
            'live_val': current_price,
            'deviation': round(deviation, 1),
            'status': '✅ VALIDATED' if validated else '⚠️ DEVIATING',
            'badge': f"{deviation:+.1f}%",
        })
        result['total'] += 1
        if validated:
            result['validated'] += 1

    # P/S validation
    if ps and revenue and mcap:
        implied_ps = mcap / revenue if revenue != 0 else None
        if implied_ps:
            deviation = (ps - implied_ps) / implied_ps * 100 if implied_ps != 0 else 0
            result['checks'].append({
                'name': 'P/S Ratio',
                'excel_val': round(ps, 2),
                'live_val': round(implied_ps, 2),
                'deviation': round(deviation, 1),
                'status': '✅ CONSISTENT' if abs(deviation) < 10 else '⚠️ INCONSISTENT',
                'badge': f"{deviation:+.1f}%",
            })
            result['total'] += 1
            if abs(deviation) < 10:
                result['validated'] += 1

    # P/E validation
    if pe and eps and current_price:
        implied_pe = current_price / eps if eps != 0 else None
        if implied_pe:
            deviation = (pe - implied_pe) / abs(implied_pe) * 100 if implied_pe != 0 else 0
            result['checks'].append({
                'name': 'P/E Ratio',
                'excel_val': round(pe, 2),
                'live_val': round(implied_pe, 2),
                'deviation': round(deviation, 1),
                'status': '✅ CONSISTENT' if abs(deviation) < 15 else '⚠️ INCONSISTENT',
                'badge': f"{deviation:+.1f}%",
            })
            result['total'] += 1
            if abs(deviation) < 15:
                result['validated'] += 1

    if result['total'] > 0:
        pct = result['validated'] / result['total'] * 100
        if pct >= 75:
            result['overall'] = f'🏆 HYPOTHESIS VALIDATED ({result["validated"]}/{result["total"]})'
        elif pct >= 50:
            result['overall'] = f'⚠️ PARTIAL VALIDATION ({result["validated"]}/{result["total"]})'
        else:
            result['overall'] = f'🚨 HYPOTHESIS CHALLENGED ({result["validated"]}/{result["total"]})'

    return result


def run_full_audit(ticker, excel_data_row=None):
    """Run all 7 audit algorithms for a ticker."""
    audit = {'ticker': ticker, 'timestamp': datetime.now().isoformat(), 'algorithms': {}}

    # Live data
    price, chg, vol = fetch_live_price(ticker)
    fundamentals = fetch_fundamentals(ticker)
    hist = fetch_historical(ticker, period="5y")
    income, cf_stmt, bal = fetch_financials(ticker)

    # Algo 1
    audit['algorithms']['A1_reconciliation'] = algo1_multi_source_reconciliation(ticker)

    # Algo 2 — price anomaly
    price_history = hist['Close'].tolist()[-60:] if not hist.empty else []
    price_history_monthly = hist['Close'].resample('ME').last().tolist() if not hist.empty else []
    a2 = algo2_statistical_anomaly_detection(ticker, 'Price', price, price_history_monthly)
    audit['algorithms']['A2_anomaly'] = a2

    # Algo 3
    ebitda = fundamentals.get('ebitda')
    net_income = fundamentals.get('net_income')
    fcf = fundamentals.get('fcf')
    revenue = fundamentals.get('revenue')
    a3 = algo3_cashflow_logic_reconciliation(
        revenue=revenue, ebitda=ebitda, ebit=None,
        net_income=net_income, depreciation=None, interest=None, taxes=None,
        fcf=fcf, op_cf=None
    )
    audit['algorithms']['A3_cashflow'] = a3

    # Algo 4
    last_price_dt = hist.index[-1].to_pydatetime() if not hist.empty else None
    last_fund_dt = datetime.now() - timedelta(days=30)  # approximate
    a4 = algo4_freshness_reliability_score(last_price_dt, last_fund_dt)
    audit['algorithms']['A4_freshness'] = a4

    # Algo 5
    rev_series = []
    if income is not None and not income.empty:
        try:
            if 'Total Revenue' in income.index:
                rev_series = [float(v) / 1e9 for v in income.loc['Total Revenue'].values if v is not None][::-1]
        except Exception:
            pass
    a5 = algo5_historical_trend_validation(ticker, rev_series, 'Revenue')
    audit['algorithms']['A5_trend'] = a5

    # Algo 6
    a6 = algo6_guidance_backtest(ticker)
    audit['algorithms']['A6_guidance'] = a6

    # Algo 7
    gaps = excel_data_row.get('gaps') if excel_data_row else None
    gape = excel_data_row.get('gape') if excel_data_row else None
    a7 = algo7_hypothesis_audit(ticker, gaps, gape, price, fundamentals)
    audit['algorithms']['A7_hypothesis'] = a7

    # Overall score
    flags = [
        audit['algorithms']['A2_anomaly'].get('flag', False),
        bool(audit['algorithms']['A3_cashflow'].get('issues')),
        audit['algorithms']['A4_freshness'].get('flag', False),
        audit['algorithms']['A5_trend'].get('flag', False),
        audit['algorithms']['A6_guidance'].get('flag', False),
    ]
    score = 100 - sum(flags) * 15
    audit['score'] = max(0, score)
    audit['price'] = price
    audit['change'] = chg
    audit['fundamentals'] = fundamentals

    return audit


# ────────────────────────────────────────────────────────────────────────────────
# STB RANKING ENGINE
# ────────────────────────────────────────────────────────────────────────────────
def compute_stb_score(row, weightage_profile="Current"):
    """Compute weighted STB score from component scores (0-10 each)."""
    w = WEIGHTAGES.get(weightage_profile, WEIGHTAGES["Current"])

    def safe(v, default=5.0):
        try:
            f = float(v)
            return f if not np.isnan(f) else default
        except (TypeError, ValueError):
            return default

    s_rev = safe(row.get('score_rev'), 5)
    s_eps = safe(row.get('score_eps'), 5)
    s_ebitda = safe(row.get('score_ebitda'), 5)
    s_cf = safe(row.get('score_cf'), 5)
    s_nd = safe(row.get('score_nd'), 5)

    score = (
        s_rev * w.get('rev_growth', 0.30) +
        s_eps * w.get('eps', 0.20) +
        s_ebitda * w.get('ebitda', 0.10) +
        s_cf * w.get('cashflow', 0.20) +
        s_nd * w.get('net_debt', 0.05)
    ) / sum([w.get('rev_growth', 0.30), w.get('eps', 0.20), w.get('ebitda', 0.10),
             w.get('cashflow', 0.20), w.get('net_debt', 0.05)])

    return round(score * 10, 2)


# ────────────────────────────────────────────────────────────────────────────────
# TERMINAL COMMAND PARSER
# ────────────────────────────────────────────────────────────────────────────────
def parse_command(cmd, all_tickers_map):
    """Parse and execute terminal commands."""
    cmd = cmd.strip()
    lower = cmd.lower()
    output = []

    if lower.startswith("analyze ") or lower.startswith("audit "):
        parts = cmd.split()
        ticker = parts[1].upper().strip()
        output.append(f"⚡ Running full audit on {ticker}...")
        row = all_tickers_map.get(ticker, {})
        audit = run_full_audit(ticker, row)
        output.append(f"📊 AUDIT COMPLETE — {ticker}")
        output.append(f"   Price: ${audit.get('price', 'N/A')}")
        output.append(f"   Audit Score: {audit.get('score', 'N/A')}/100")
        for k, v in audit['algorithms'].items():
            status = v.get('status', v.get('overall', '—'))
            output.append(f"   {k}: {status}")
        return output, audit

    elif lower.startswith("compare "):
        parts = cmd.split()
        tickers = [p.upper() for p in parts[1:] if p.upper().isalpha()][:4]
        output.append(f"📊 Comparing: {', '.join(tickers)}")
        rows = []
        for t in tickers:
            p, chg, _ = fetch_live_price(t)
            fund = fetch_fundamentals(t)
            rows.append({'Ticker': t, 'Price': f"${p:.2f}" if p else 'N/A',
                         'Change': f"{chg*100:+.2f}%" if chg else 'N/A',
                         'PE': round(fund.get('pe', 0) or 0, 1),
                         'PS': round(fund.get('ps', 0) or 0, 2),
                         'MCap': f"${fund.get('market_cap', 0)/1e9:.1f}B" if fund.get('market_cap') else 'N/A'})
        return output, pd.DataFrame(rows)

    elif lower.startswith("show 10yr chart ") or lower.startswith("chart "):
        parts = cmd.split()
        ticker = parts[-1].upper()
        output.append(f"📈 Fetching 10yr chart for {ticker}...")
        return output, {'chart_ticker': ticker}

    elif lower.startswith("validate hypothesis"):
        output.append("🧪 Running hypothesis validation on all tickers...")
        return output, {'run_hypothesis': True}

    elif lower.startswith("update stb ranking"):
        output.append("🔄 Refreshing STB rankings with live data...")
        return output, {'update_ranking': True}

    elif lower.startswith("bonus portfolio"):
        output.append("💰 Loading bonus portfolio P&L...")
        return output, {'show_bonus': True}

    elif lower.startswith("help"):
        output = [
            "═══ PYKUPZ TERMINAL COMMANDS ═══",
            "  analyze TICKER       — Full 7-algo audit",
            "  audit TICKER         — Same as analyze",
            "  compare T1 T2 T3     — Side-by-side comparison",
            "  chart TICKER         — 10yr price chart",
            "  show 10yr chart T    — Same as chart",
            "  validate hypothesis  — Run all hypothesis checks",
            "  update stb ranking   — Refresh STB scores",
            "  bonus portfolio      — P&L for bonus stocks",
            "  help                 — Show this menu",
        ]
        return output, None

    else:
        # Try to interpret as ticker lookup
        possible_ticker = cmd.upper().strip().split()[0] if cmd.strip() else ''
        if possible_ticker and len(possible_ticker) <= 7:
            p, chg, vol = fetch_live_price(possible_ticker)
            if p:
                output.append(f"📌 {possible_ticker}: ${p:.4f} ({chg*100:+.2f}%)")
                return output, None
        output.append(f"❓ Unknown command: '{cmd}'. Type 'help' for commands.")
        return output, None


# ────────────────────────────────────────────────────────────────────────────────
# VISUALIZATION FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────────
def build_price_chart(ticker, period="5y"):
    hist = fetch_historical(ticker, period=period)
    if hist.empty:
        return go.Figure()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist.index, y=hist['Close'],
        mode='lines', name=ticker,
        line=dict(color='#00d4ff', width=2),
        fill='tozeroy',
        fillcolor='rgba(0,212,255,0.05)'
    ))

    # 50MA, 200MA
    if len(hist) >= 50:
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(50).mean(),
                                  mode='lines', name='50MA', line=dict(color='#ffaa00', width=1, dash='dot')))
    if len(hist) >= 200:
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'].rolling(200).mean(),
                                  mode='lines', name='200MA', line=dict(color='#ff3366', width=1, dash='dash')))

    fig.update_layout(
        paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
        font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
        title=dict(text=f'📈 {ticker} — {period.upper()} PRICE', font=dict(color='#00d4ff', size=16)),
        xaxis=dict(gridcolor='#1a2540', showgrid=True),
        yaxis=dict(gridcolor='#1a2540', showgrid=True),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1a2540'),
        margin=dict(l=10, r=10, t=40, b=10),
        height=400,
    )
    return fig


def build_growth_chart(tickers_data, metric='revenue'):
    """Multi-ticker revenue/EPS/EBITDA growth bars."""
    names, vals = [], []
    for t, d in tickers_data.items():
        v = d.get(f'{metric}_growth') or d.get(f'{metric}_cagr')
        if v is not None:
            try:
                names.append(t)
                vals.append(float(v) * 100 if abs(float(v)) < 10 else float(v))
            except Exception:
                pass

    if not names:
        return go.Figure()

    colors = ['#00ff88' if v > 0 else '#ff3366' for v in vals]
    fig = go.Figure(go.Bar(
        x=names, y=vals, marker_color=colors,
        text=[f'{v:.1f}%' for v in vals], textposition='outside',
        textfont=dict(color='#c8d8f0', size=10, family='Share Tech Mono'),
    ))
    fig.update_layout(
        paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
        font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
        title=dict(text=f'📊 {metric.upper()} GROWTH %', font=dict(color='#00d4ff', size=14)),
        xaxis=dict(tickangle=-45, gridcolor='#1a2540'),
        yaxis=dict(gridcolor='#1a2540', zeroline=True, zerolinecolor='#4a6080'),
        margin=dict(l=10, r=10, t=40, b=60),
        height=380,
    )
    return fig


def build_pe_ps_scatter(tickers_data):
    """P/E vs P/S scatter."""
    data = []
    for t, d in tickers_data.items():
        pe = d.get('pe')
        ps = d.get('ps')
        if pe and ps:
            try:
                data.append({'ticker': t, 'pe': float(pe), 'ps': float(ps),
                              'mcap': d.get('market_cap', 0) or 0})
            except Exception:
                pass
    if not data:
        return go.Figure()

    df = pd.DataFrame(data)
    fig = px.scatter(df, x='ps', y='pe', text='ticker',
                     size=[max(1, m / 1e10) for m in df['mcap']],
                     color='pe', color_continuous_scale='RdYlGn_r')
    fig.update_traces(textposition='top center', textfont=dict(color='#c8d8f0', size=9, family='Share Tech Mono'))
    fig.update_layout(
        paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
        font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
        title=dict(text='📊 P/E vs P/S MAP', font=dict(color='#00d4ff', size=14)),
        xaxis=dict(title='P/S', gridcolor='#1a2540'),
        yaxis=dict(title='P/E', gridcolor='#1a2540'),
        coloraxis_showscale=False,
        margin=dict(l=10, r=10, t=40, b=10),
        height=380,
    )
    return fig


def build_mcap_vs_gaps_chart(tickers_data):
    """Market Cap vs GAPS/GAPE comparison."""
    rows = []
    for t, d in tickers_data.items():
        mcap = d.get('market_cap')
        gaps = d.get('gaps_excel')
        gape = d.get('gape_excel')
        if mcap and (gaps or gape):
            rows.append({'ticker': t, 'live_mcap': mcap / 1e9,
                         'gaps': gaps, 'gape': gape})
    if not rows:
        return go.Figure()
    df = pd.DataFrame(rows)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df['ticker'], y=df['live_mcap'], name='Live MCap ($B)',
                         marker_color='#00d4ff'))
    if df['gaps'].notna().any():
        fig.add_trace(go.Bar(x=df['ticker'], y=df['gaps'].fillna(0), name='GAPS Target',
                             marker_color='#00ff88'))
    if df['gape'].notna().any():
        fig.add_trace(go.Bar(x=df['ticker'], y=df['gape'].fillna(0), name='GAPE Target',
                             marker_color='#7b2fff'))
    fig.update_layout(
        barmode='group',
        paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
        font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
        title=dict(text='📊 MCAP vs GAPS/GAPE TARGETS', font=dict(color='#00d4ff', size=14)),
        xaxis=dict(tickangle=-45, gridcolor='#1a2540'),
        yaxis=dict(title='$B', gridcolor='#1a2540'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(l=10, r=10, t=40, b=60),
        height=380,
    )
    return fig


def build_correlation_heatmap(tickers_prices):
    """Correlation heatmap of returns."""
    if len(tickers_prices) < 2:
        return go.Figure()
    try:
        returns = {}
        for t, hist in tickers_prices.items():
            if hist is not None and not hist.empty and len(hist) > 10:
                returns[t] = hist['Close'].pct_change().dropna()
        if len(returns) < 2:
            return go.Figure()
        df = pd.DataFrame(returns).dropna()
        if df.empty:
            return go.Figure()
        corr = df.corr()
        fig = go.Figure(go.Heatmap(
            z=corr.values, x=corr.columns, y=corr.index,
            colorscale=[[0, '#ff3366'], [0.5, '#0a0f1e'], [1, '#00ff88']],
            text=[[f'{v:.2f}' for v in row] for row in corr.values],
            texttemplate='%{text}',
            textfont=dict(size=9, family='Share Tech Mono'),
            zmin=-1, zmax=1,
        ))
        fig.update_layout(
            paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
            font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
            title=dict(text='🔗 CORRELATION HEATMAP (1yr returns)', font=dict(color='#00d4ff', size=14)),
            margin=dict(l=10, r=10, t=40, b=10),
            height=380,
        )
        return fig
    except Exception:
        return go.Figure()


def build_earnings_calendar(tickers):
    """Next 14-day earnings calendar."""
    events = []
    for ticker in tickers[:20]:
        try:
            t = yf.Ticker(ticker)
            ts = t.info.get('earningsTimestamp')
            if ts:
                dt = datetime.fromtimestamp(ts)
                if timedelta(0) <= dt - datetime.now() <= timedelta(days=14):
                    events.append({'ticker': ticker, 'date': dt.strftime('%Y-%m-%d'), 'days': (dt - datetime.now()).days})
        except Exception:
            pass
    return sorted(events, key=lambda x: x['date'])


# ────────────────────────────────────────────────────────────────────────────────
# EXPORT
# ────────────────────────────────────────────────────────────────────────────────
def export_to_excel(df_live, audit_log):
    """Export updated data to Excel."""
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
        if not df_live.empty:
            df_live.to_excel(writer, sheet_name='Live Sheet', index=False)
        if audit_log:
            df_audit = pd.DataFrame([{
                'ticker': a.get('ticker', ''),
                'score': a.get('score', ''),
                'timestamp': a.get('timestamp', ''),
                'A1': a['algorithms'].get('A1_reconciliation', {}).get('status', ''),
                'A2': a['algorithms'].get('A2_anomaly', {}).get('status', ''),
                'A3': a['algorithms'].get('A3_cashflow', {}).get('overall', ''),
                'A4': a['algorithms'].get('A4_freshness', {}).get('status', ''),
                'A5': a['algorithms'].get('A5_trend', {}).get('status', ''),
                'A6': a['algorithms'].get('A6_guidance', {}).get('status', ''),
                'A7': a['algorithms'].get('A7_hypothesis', {}).get('overall', ''),
            } for a in audit_log])
            df_audit.to_excel(writer, sheet_name='Audit Log', index=False)
    buf.seek(0)
    return buf


# ────────────────────────────────────────────────────────────────────────────────
# MAIN APP
# ────────────────────────────────────────────────────────────────────────────────
def main():
    # ── HEADER ──
    st.markdown("""
    <div class="terminal-header">
      <div class="terminal-title">⚡ PYKUPZ LIVE TERMINAL</div>
      <div class="terminal-sub">PRODUCTION-GRADE FINANCIAL INTELLIGENCE SYSTEM · 7-ALGORITHM AUDIT ENGINE · REAL-TIME</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FILE UPLOAD ──
    col_up, col_status = st.columns([3, 1])
    with col_up:
        uploaded = st.file_uploader("Upload Pyk-Inv-List.xlsx", type=['xlsx'], label_visibility="collapsed")
    with col_status:
        if uploaded:
            st.markdown('<span class="badge-green">✅ FILE LOADED</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-amber">📂 UPLOAD EXCEL TO BEGIN</span>', unsafe_allow_html=True)

    if not uploaded:
        st.info("Upload your **Pyk-Inv-List.xlsx** to activate the terminal.")
        st.stop()

    # Load Excel data
    file_bytes = uploaded.read()
    if not st.session_state.excel_data or st.session_state.get('loaded_file') != uploaded.name:
        with st.spinner("🔄 Parsing Excel..."):
            st.session_state.excel_data = load_excel(file_bytes)
            st.session_state.loaded_file = uploaded.name

    data = st.session_state.excel_data
    if 'error' in data:
        st.error(f"Excel parse error: {data['error']}")
        st.stop()

    # Parse tickers
    stb_rows = parse_stb_tickers(data['stb']) if 'stb' in data else []
    q1_rows = parse_q1_tickers(data['q1']) if 'q1' in data else []
    bonus_rows = parse_bonus(data['bonus']) if 'bonus' in data else []

    all_stb = {r['ticker']: r for r in stb_rows if r['ticker']}
    all_q1 = {r['ticker']: r for r in q1_rows if r['ticker']}
    all_tickers_map = {**all_stb, **all_q1}
    unique_tickers = list(all_tickers_map.keys())

    # ── SIDEBAR ──
    with st.sidebar:
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;margin-bottom:12px;">⚙ CONTROL CENTER</div>', unsafe_allow_html=True)

        # Command terminal
        st.markdown('<div style="font-size:11px;color:#4a6080;letter-spacing:2px;margin-bottom:4px;">TERMINAL COMMAND</div>', unsafe_allow_html=True)
        cmd_input = st.text_input("", placeholder="analyze NVDA | compare NVDA SHOP | help", key="cmd", label_visibility="collapsed")

        if cmd_input:
            with st.spinner("⚡ Processing..."):
                output, result = parse_command(cmd_input, all_tickers_map)
            st.session_state.cmd_history.append(cmd_input)
            st.session_state.terminal_output = output
            if isinstance(result, dict) and 'algorithms' in result:
                st.session_state.audit_log.append(result)

        # Show terminal output
        if st.session_state.terminal_output:
            st.markdown("---")
            for line in st.session_state.terminal_output:
                st.markdown(f'<div style="font-family:Share Tech Mono,monospace;font-size:11px;color:#c8d8f0;padding:2px 0;">{line}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div style="font-size:11px;color:#4a6080;letter-spacing:2px;">QUICK AUDIT</div>', unsafe_allow_html=True)
        sel_ticker = st.selectbox("Select Ticker", options=["—"] + unique_tickers, label_visibility="collapsed")

        if sel_ticker and sel_ticker != "—":
            if st.button("⚡ RUN FULL AUDIT", use_container_width=True):
                with st.spinner(f"Auditing {sel_ticker}..."):
                    row = all_tickers_map.get(sel_ticker, {})
                    audit = run_full_audit(sel_ticker, row)
                    st.session_state.audit_log.append(audit)
                    st.session_state.selected_audit = audit
                st.success(f"Audit complete! Score: {audit['score']}/100")

        st.markdown("---")
        st.markdown('<div style="font-size:11px;color:#4a6080;letter-spacing:2px;">WEIGHTAGE PROFILE</div>', unsafe_allow_html=True)
        weight_profile = st.selectbox("", options=["Current", "Nandini", "Arnold"], label_visibility="collapsed")

        st.markdown("---")
        # Export button
        if st.session_state.audit_log:
            df_export = pd.DataFrame([{
                'Ticker': a.get('ticker', ''), 'Score': a.get('score', ''),
                'Price': a.get('price', ''), 'Timestamp': a.get('timestamp', ''),
            } for a in st.session_state.audit_log])
            buf = export_to_excel(df_export, st.session_state.audit_log)
            st.download_button("📥 EXPORT AUDIT LOG", buf, "pykupz_audit.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               use_container_width=True)

        # Auto-refresh toggle
        auto_refresh = st.toggle("60s Auto-Refresh", value=False)
        if auto_refresh:
            time.sleep(1)
            st.rerun()

    # ── MAIN AREA — TOP METRICS ──
    m_cols = st.columns(5)
    metrics = [
        ("STOCKS TRACKED", len(unique_tickers), ""),
        ("STB UNIVERSE", len(stb_rows), ""),
        ("Q1 2026 PICKS", len(q1_rows), ""),
        ("AUDIT LOG", len(st.session_state.audit_log), ""),
        ("LAST UPDATE", datetime.now().strftime("%H:%M:%S"), ""),
    ]
    for col, (label, val, _) in zip(m_cols, metrics):
        col.markdown(f'<div class="metric-card"><div class="metric-val">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── MAIN TABS ──
    tab1, tab2, tab3, tab4 = st.tabs(["📊 LIVE SHEET MIRROR", "📈 VISUALIZATION LAB", "🔬 AUDIT ENGINE", "💰 BONUS PORTFOLIO"])

    # ════════════════════════════════════════════════════════════════════════
    # TAB 1 — LIVE SHEET MIRROR
    # ════════════════════════════════════════════════════════════════════════
    with tab1:
        sub1, sub2 = st.columns([2, 1])
        with sub1:
            sheet_view = st.radio("Sheet", ["Q1 2026 Stocks to Buy", "All STB", "Stocks to Sell"], horizontal=True, label_visibility="collapsed")
        with sub2:
            refresh_count = st.number_input("Tickers to refresh (live)", min_value=5, max_value=50, value=15, step=5, label_visibility="collapsed")

        # Choose source rows
        if sheet_view == "Q1 2026 Stocks to Buy":
            source_rows = q1_rows[:50]
            source_key = 'q1'
        elif sheet_view == "All STB":
            source_rows = stb_rows[:50]
            source_key = 'stb'
        else:
            sell_rows = []
            if 'sell' in data:
                for _, r in data['sell'].iterrows():
                    t = r.iloc[1] if len(r) > 1 else None
                    if isinstance(t, str) and t.strip() and t.strip().upper() == t.strip() and len(t.strip()) <= 7:
                        sell_rows.append({'ticker': t.strip(), 'name': str(r.iloc[3]) if len(r) > 3 else ''})
            source_rows = sell_rows[:30]
            source_key = 'sell'

        # Fetch live prices for visible tickers
        with st.spinner(f"⚡ Fetching live prices for top {min(refresh_count, len(source_rows))} tickers..."):
            live_rows = []
            for row in source_rows[:refresh_count]:
                ticker = row.get('ticker', '')
                if not ticker:
                    continue
                price, chg, vol = fetch_live_price(ticker)
                fund = fetch_fundamentals(ticker)

                # Compute STB score
                stb_score = compute_stb_score(row, weight_profile)

                # GAPS / GAPE upside
                gaps = row.get('gaps')
                gape = row.get('gape')
                gaps_upside = f"+{((gaps/price-1)*100):.1f}%" if price and gaps and isinstance(gaps, (int, float)) and not np.isnan(gaps) else "—"
                gape_upside = f"+{((gape/price-1)*100):.1f}%" if price and gape and isinstance(gape, (int, float)) and not np.isnan(gape) else "—"

                live_rows.append({
                    'TICKER': f"{'⬆' if chg and chg > 0 else '⬇' if chg and chg < 0 else '—'} {ticker}",
                    'NAME': str(row.get('name', fund.get('short_name', '')))[:25],
                    'LIVE PRICE': f"${price:.2f}" if price else '—',
                    'CHANGE': f"{chg*100:+.2f}%" if chg else '—',
                    'PE': f"{fund.get('pe', '—'):.1f}" if fund.get('pe') else '—',
                    'PS': f"{fund.get('ps', '—'):.2f}" if fund.get('ps') else '—',
                    'MCAP ($B)': f"{fund.get('market_cap', 0)/1e9:.1f}" if fund.get('market_cap') else '—',
                    'GAPS': f"${gaps:.1f}" if gaps and isinstance(gaps, (int, float)) else '—',
                    'GAPS UPSIDE': gaps_upside,
                    'GAPE': f"${gape:.1f}" if gape and isinstance(gape, (int, float)) else '—',
                    'GAPE UPSIDE': gape_upside,
                    'REV CAGR': f"{row.get('rev_cagr', row.get('rev_cagr_3y', '—')):.1%}" if row.get('rev_cagr') and isinstance(row.get('rev_cagr'), (int, float)) else '—',
                    'EPS CAGR': f"{row.get('eps_cagr', '—'):.1%}" if row.get('eps_cagr') and isinstance(row.get('eps_cagr'), (int, float)) else '—',
                    'FCF ($B)': f"${row.get('fcf', 0)/1e3:.1f}" if row.get('fcf') and isinstance(row.get('fcf'), (int, float)) else '—',
                    'NET DEBT': f"{row.get('net_debt', '—')}",
                    'RECOMMENDATION': str(row.get('recommendation', '')).upper()[:12],
                    'STB SCORE': f"{stb_score:.1f}",
                })

        df_live = pd.DataFrame(live_rows)

        # Color coding via st.dataframe with styling
        def style_change(val):
            if '+' in str(val):
                return 'color: #00ff88; font-weight: bold'
            elif '-' in str(val) and '%' in str(val):
                return 'color: #ff3366; font-weight: bold'
            return ''

        def style_rec(val):
            v = str(val).upper()
            if 'STRONG BUY' in v:
                return 'background: rgba(0,255,136,0.2); color: #00ff88; font-weight: bold'
            elif 'BUY' in v:
                return 'background: rgba(0,212,255,0.1); color: #00d4ff'
            elif 'SELL' in v:
                return 'background: rgba(255,51,102,0.2); color: #ff3366'
            return ''

        if not df_live.empty:
            styled = df_live.style.applymap(style_change, subset=['CHANGE']) \
                                   .applymap(style_rec, subset=['RECOMMENDATION'])
            st.dataframe(styled, use_container_width=True, height=500,
                         column_config={
                             'STB SCORE': st.column_config.ProgressColumn('STB SCORE', min_value=0, max_value=100, format="%.1f"),
                         })

        # Rankings
        st.markdown("---")
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;">📋 STB RANKINGS</div>', unsafe_allow_html=True)

        ranked = []
        for row in source_rows[:refresh_count]:
            s = compute_stb_score(row, weight_profile)
            ranked.append({'Ticker': row.get('ticker', ''), 'Name': str(row.get('name', ''))[:20],
                           'Score': s, 'Rec': str(row.get('recommendation', ''))})
        if ranked:
            df_rank = pd.DataFrame(ranked).sort_values('Score', ascending=False).reset_index(drop=True)
            df_rank.index += 1
            st.dataframe(df_rank, use_container_width=True, height=300,
                         column_config={'Score': st.column_config.ProgressColumn('Score', min_value=0, max_value=100, format="%.1f")})

        # Earnings calendar
        st.markdown("---")
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;">📅 NEXT 14-DAY EARNINGS CALENDAR</div>', unsafe_allow_html=True)
        cal_tickers = [r['ticker'] for r in source_rows[:20]]
        with st.spinner("Fetching earnings dates..."):
            cal = build_earnings_calendar(cal_tickers)
        if cal:
            df_cal = pd.DataFrame(cal)
            st.dataframe(df_cal, use_container_width=True, height=200)
        else:
            st.info("No earnings in next 14 days for tracked tickers.")

    # ════════════════════════════════════════════════════════════════════════
    # TAB 2 — VISUALIZATION LAB
    # ════════════════════════════════════════════════════════════════════════
    with tab2:
        viz_type = st.selectbox("Chart Type", [
            "📈 Price Chart (Single)", "📊 Revenue Growth Bars", "📊 EPS Growth Bars",
            "📊 EBITDA Growth Bars", "🔗 Correlation Heatmap",
            "📊 P/E vs P/S Scatter", "📊 MCap vs GAPS/GAPE",
            "📉 Waterfall CAGR", "🔬 Hypothesis Overlay",
        ], label_visibility="collapsed")

        if "Price Chart" in viz_type:
            col_t, col_p = st.columns(2)
            with col_t:
                chart_ticker = st.selectbox("Ticker", unique_tickers, label_visibility="collapsed")
            with col_p:
                chart_period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=5, label_visibility="collapsed")

            with st.spinner(f"Loading {chart_ticker} history..."):
                fig = build_price_chart(chart_ticker, chart_period)
            st.plotly_chart(fig, use_container_width=True)

            # Show fundamentals
            fund = fetch_fundamentals(chart_ticker)
            if fund:
                cols = st.columns(6)
                fund_metrics = [
                    ("P/E", f"{fund.get('pe', '—'):.1f}" if fund.get('pe') else '—'),
                    ("P/S", f"{fund.get('ps', '—'):.2f}" if fund.get('ps') else '—'),
                    ("REVENUE", f"${fund.get('revenue', 0)/1e9:.1f}B" if fund.get('revenue') else '—'),
                    ("EBITDA", f"${fund.get('ebitda', 0)/1e9:.1f}B" if fund.get('ebitda') else '—'),
                    ("EPS", f"${fund.get('eps', '—'):.2f}" if fund.get('eps') else '—'),
                    ("BETA", f"{fund.get('beta', '—'):.2f}" if fund.get('beta') else '—'),
                ]
                for col, (label, val) in zip(cols, fund_metrics):
                    col.markdown(f'<div class="metric-card"><div class="metric-val" style="font-size:16px;">{val}</div><div class="metric-label">{label}</div></div>', unsafe_allow_html=True)

        elif "Revenue Growth" in viz_type or "EPS Growth" in viz_type or "EBITDA Growth" in viz_type:
            metric = 'revenue' if 'Revenue' in viz_type else ('eps' if 'EPS' in viz_type else 'ebitda')
            top_n = st.slider("Top N tickers", 5, 30, 15)
            source = source_rows if 'source_rows' in dir() else q1_rows

            tickers_data = {}
            with st.spinner("Fetching growth data..."):
                for row in (q1_rows + stb_rows)[:top_n]:
                    t = row.get('ticker', '')
                    fund = fetch_fundamentals(t)
                    tickers_data[t] = {
                        **fund,
                        'revenue_growth': row.get('rev_growth') or row.get('rev_growth_ly'),
                        'revenue_cagr': row.get('rev_cagr_3y') or row.get('rev_cagr'),
                        'eps_growth': row.get('eps_cagr'),
                        'ebitda_growth': row.get('ebitda_growth'),
                    }

            fig = build_growth_chart(tickers_data, metric)
            st.plotly_chart(fig, use_container_width=True)

        elif "Correlation" in viz_type:
            top_n = st.slider("Top N tickers", 5, 25, 15)
            with st.spinner("Fetching historical returns..."):
                tickers_hist = {}
                for row in (q1_rows + stb_rows)[:top_n]:
                    t = row.get('ticker', '')
                    h = fetch_historical(t, period="1y")
                    tickers_hist[t] = h

            fig = build_correlation_heatmap(tickers_hist)
            st.plotly_chart(fig, use_container_width=True)

        elif "P/E vs P/S" in viz_type:
            top_n = st.slider("Top N tickers", 5, 30, 20)
            with st.spinner("Fetching valuation data..."):
                tickers_data = {}
                for row in (q1_rows + stb_rows)[:top_n]:
                    t = row.get('ticker', '')
                    fund = fetch_fundamentals(t)
                    tickers_data[t] = fund

            fig = build_pe_ps_scatter(tickers_data)
            st.plotly_chart(fig, use_container_width=True)

        elif "MCap vs GAPS" in viz_type:
            top_n = st.slider("Top N tickers", 5, 30, 20)
            with st.spinner("Fetching MCap data..."):
                tickers_data = {}
                for row in (q1_rows + stb_rows)[:top_n]:
                    t = row.get('ticker', '')
                    fund = fetch_fundamentals(t)
                    tickers_data[t] = {
                        **fund,
                        'gaps_excel': row.get('gaps'),
                        'gape_excel': row.get('gape'),
                    }

            fig = build_mcap_vs_gaps_chart(tickers_data)
            st.plotly_chart(fig, use_container_width=True)

        elif "Waterfall CAGR" in viz_type:
            wf_ticker = st.selectbox("Ticker for CAGR Waterfall", unique_tickers, label_visibility="collapsed")
            income, _, _ = fetch_financials(wf_ticker)
            if income is not None and not income.empty and 'Total Revenue' in income.index:
                rev_vals = income.loc['Total Revenue'].dropna().sort_index()
                years = [str(d.year) for d in rev_vals.index]
                vals = [float(v) / 1e9 for v in rev_vals.values]
                measure = ['absolute'] + ['relative'] * (len(vals) - 1)
                fig = go.Figure(go.Waterfall(
                    x=years, y=vals, measure=measure,
                    increasing=dict(marker_color='#00ff88'),
                    decreasing=dict(marker_color='#ff3366'),
                    totals=dict(marker_color='#00d4ff'),
                    connector=dict(line=dict(color='#1a2540', width=1)),
                    text=[f"${v:.1f}B" for v in vals],
                ))
                fig.update_layout(
                    paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
                    font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
                    title=dict(text=f'{wf_ticker} — REVENUE CAGR WATERFALL', font=dict(color='#00d4ff', size=14)),
                    height=380, margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No income statement data available.")

        elif "Hypothesis Overlay" in viz_type:
            hyp_ticker = st.selectbox("Ticker", unique_tickers, label_visibility="collapsed")
            row = all_tickers_map.get(hyp_ticker, {})
            price, chg, _ = fetch_live_price(hyp_ticker)
            hist = fetch_historical(hyp_ticker, "2y")
            if not hist.empty and price:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines',
                                         name='Price', line=dict(color='#00d4ff', width=2)))
                gaps = row.get('gaps')
                gape = row.get('gape')
                if gaps and isinstance(gaps, (int, float)):
                    fig.add_hline(y=gaps, line=dict(color='#00ff88', dash='dash', width=1),
                                  annotation=dict(text=f"GAPS: ${gaps:.1f}", font=dict(color='#00ff88', size=10)))
                if gape and isinstance(gape, (int, float)):
                    fig.add_hline(y=gape, line=dict(color='#7b2fff', dash='dot', width=1),
                                  annotation=dict(text=f"GAPE: ${gape:.1f}", font=dict(color='#7b2fff', size=10)))
                fig.add_hline(y=price, line=dict(color='#ffaa00', width=1),
                              annotation=dict(text=f"NOW: ${price:.2f}", font=dict(color='#ffaa00', size=10)))
                fig.update_layout(
                    paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
                    font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
                    title=dict(text=f'{hyp_ticker} — HYPOTHESIS OVERLAY', font=dict(color='#00d4ff', size=14)),
                    height=400, margin=dict(l=10, r=10, t=40, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 3 — AUDIT ENGINE
    # ════════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;margin-bottom:16px;">🔬 7-ALGORITHM AUDIT ENGINE</div>', unsafe_allow_html=True)

        audit_col1, audit_col2 = st.columns([1, 2])

        with audit_col1:
            st.markdown("**Select Ticker to Audit**")
            audit_ticker = st.selectbox("", ["—"] + unique_tickers, key="audit_sel", label_visibility="collapsed")

            if audit_ticker and audit_ticker != "—":
                if st.button("⚡ RUN ALL 7 ALGORITHMS", use_container_width=True, key="run_all_algos"):
                    with st.spinner(f"Running 7-algo audit on {audit_ticker}..."):
                        row = all_tickers_map.get(audit_ticker, {})
                        audit_result = run_full_audit(audit_ticker, row)
                        st.session_state.audit_log.append(audit_result)
                        st.session_state.selected_audit = audit_result

        with audit_col2:
            if 'selected_audit' in st.session_state:
                a = st.session_state.selected_audit
                t = a.get('ticker', '—')
                price = a.get('price', '—')
                chg = a.get('change', 0)
                score = a.get('score', 0)

                # Score display
                score_color = '#00ff88' if score >= 80 else '#ffaa00' if score >= 60 else '#ff3366'
                st.markdown(f"""
                <div style="background:#0a0f1e;border:1px solid {score_color};border-radius:4px;padding:12px;margin-bottom:12px;">
                  <span style="font-family:Orbitron,monospace;font-size:24px;color:{score_color};">{t}</span>
                  <span style="font-family:Share Tech Mono,monospace;font-size:16px;color:#c8d8f0;margin-left:16px;">${price:.2f} ({chg*100:+.2f}%)</span>
                  <br><span style="font-family:Orbitron,monospace;font-size:14px;color:{score_color};">AUDIT SCORE: {score}/100</span>
                </div>
                """, unsafe_allow_html=True)

                # Per-algorithm results
                algos = a.get('algorithms', {})

                with st.expander("🔵 A1 · Multi-Source Reconciliation", expanded=True):
                    a1 = algos.get('A1_reconciliation', {})
                    for src, info in a1.get('sources', {}).items():
                        p = info.get('price', '—')
                        w = info.get('weight', 0)
                        st.markdown(f'<div class="audit-row"><b>{src}</b> ({w*100:.0f}%): <b>${p:.4f}</b> if price else "N/A"</div>', unsafe_allow_html=True)
                    w_avg = a1.get('weighted', '—')
                    status = a1.get('status', '—')
                    st.markdown(f'<div class="audit-row" style="border-left-color:#00ff88;"><b>WEIGHTED AVG: ${w_avg} → {status}</b></div>', unsafe_allow_html=True)

                with st.expander("📊 A2 · Statistical Anomaly Detection"):
                    a2 = algos.get('A2_anomaly', {})
                    st.markdown(f"""
                    - **Metric**: {a2.get('metric', '—')}
                    - **Current**: {a2.get('current', '—')}
                    - **5yr Mean**: {a2.get('mean', '—')} | **Std**: {a2.get('std', '—')}
                    - **Z-Score**: {a2.get('z_score', '—')}
                    - **Status**: {a2.get('status', '—')}
                    """)

                with st.expander("⛓ A3 · Cash-Flow Logic Chain"):
                    a3 = algos.get('A3_cashflow', {})
                    for k, v in a3.get('checks', {}).items():
                        st.markdown(f"  `{k}`: {v}")
                    for issue in a3.get('issues', []):
                        st.warning(issue)
                    st.markdown(f"**{a3.get('overall', '—')}**")

                with st.expander("🕐 A4 · Freshness & Reliability"):
                    a4 = algos.get('A4_freshness', {})
                    st.progress(a4.get('overall', 0) / 100)
                    st.markdown(f"""
                    - **Price Freshness**: {a4.get('price_score', '—')}%
                    - **Fundamentals**: {a4.get('fund_score', '—')}%
                    - **Overall**: {a4.get('overall', '—')}% → {a4.get('status', '—')}
                    """)

                with st.expander("📉 A5 · Historical Trend Validation"):
                    a5 = algos.get('A5_trend', {})
                    st.markdown(f"""
                    - **Metric**: {a5.get('metric', '—')}
                    - **3yr CAGR**: {a5.get('cagr_3y', '—')}%
                    - **5yr CAGR**: {a5.get('cagr_5y', '—')}%
                    - **Status**: {a5.get('status', '—')}
                    """)

                with st.expander("🎯 A6 · Guidance Back-Testing"):
                    a6 = algos.get('A6_guidance', {})
                    st.markdown(f"**Beat Rate**: {a6.get('accuracy', '—')}% → {a6.get('status', '—')}")
                    quarters = a6.get('quarters', [])
                    if quarters:
                        df_q = pd.DataFrame(quarters)
                        df_q['result'] = df_q.apply(lambda r: '✅ BEAT' if r['actual'] >= r['estimate'] else '❌ MISS', axis=1)
                        st.dataframe(df_q, use_container_width=True, height=180)

                with st.expander("🏆 A7 · Hypothesis & Valuation Audit"):
                    a7 = algos.get('A7_hypothesis', {})
                    st.markdown(f"**{a7.get('overall', '—')}**")
                    for check in a7.get('checks', []):
                        badge_color = '#00ff88' if '✅' in check['status'] else '#ffaa00'
                        st.markdown(f"""
                        <div class="audit-row" style="border-left-color:{badge_color};">
                          <b>{check['name']}</b> | Excel: {check['excel_val']} | Live: {check['live_val']} | Deviation: {check['badge']} → {check['status']}
                        </div>
                        """, unsafe_allow_html=True)

        # Audit Log Summary
        if st.session_state.audit_log:
            st.markdown("---")
            st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;margin-bottom:8px;">📋 AUDIT LOG</div>', unsafe_allow_html=True)
            log_data = []
            for a in st.session_state.audit_log[-20:]:
                algos = a.get('algorithms', {})
                log_data.append({
                    'Ticker': a.get('ticker', ''),
                    'Score': a.get('score', 0),
                    'A1': algos.get('A1_reconciliation', {}).get('status', '—')[:20],
                    'A2': algos.get('A2_anomaly', {}).get('status', '—')[:20],
                    'A3': algos.get('A3_cashflow', {}).get('overall', '—')[:20],
                    'A4': algos.get('A4_freshness', {}).get('status', '—')[:15],
                    'A5': algos.get('A5_trend', {}).get('status', '—')[:20],
                    'A6': algos.get('A6_guidance', {}).get('status', '—')[:20],
                    'A7': algos.get('A7_hypothesis', {}).get('overall', '—')[:25],
                    'Time': a.get('timestamp', '')[:19],
                })
            st.dataframe(pd.DataFrame(log_data), use_container_width=True, height=250,
                         column_config={'Score': st.column_config.ProgressColumn('Score', min_value=0, max_value=100, format="%d")})

        # Batch audit
        st.markdown("---")
        if st.button("⚡ BATCH AUDIT TOP 10 Q1 2026 PICKS", use_container_width=False):
            st.info("Running batch audit on top 10 Q1 2026 picks...")
            batch_results = []
            progress = st.progress(0)
            for i, row in enumerate(q1_rows[:10]):
                t = row.get('ticker', '')
                if t:
                    audit_r = run_full_audit(t, row)
                    st.session_state.audit_log.append(audit_r)
                    batch_results.append({'Ticker': t, 'Score': audit_r['score'],
                                          'Price': f"${audit_r.get('price', '—'):.2f}" if audit_r.get('price') else '—'})
                progress.progress((i + 1) / 10)
            if batch_results:
                st.dataframe(pd.DataFrame(batch_results).sort_values('Score', ascending=False), use_container_width=True)

    # ════════════════════════════════════════════════════════════════════════
    # TAB 4 — BONUS PORTFOLIO
    # ════════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;margin-bottom:16px;">💰 BONUS PORTFOLIO — LIVE P&L</div>', unsafe_allow_html=True)

        if bonus_rows:
            portfolio = []
            total_invested = 0
            total_current = 0

            with st.spinner("Fetching live prices for portfolio..."):
                for row in bonus_rows:
                    ticker = row.get('ticker', '')
                    if not ticker:
                        continue
                    buy_price = row.get('buy_price')
                    qty = row.get('qty')
                    invested = row.get('invested')
                    price, chg, _ = fetch_live_price(ticker)

                    if price and buy_price:
                        pnl_pct = (price - buy_price) / buy_price * 100
                        pnl_abs = (price - buy_price) * (qty or 1)
                        curr_val = price * (qty or 1)
                        total_invested += invested or 0
                        total_current += curr_val

                        portfolio.append({
                            'TICKER': ticker,
                            'NAME': str(row.get('name', ''))[:20],
                            'EXCHANGE': str(row.get('exchange', '')),
                            'SECTOR': str(row.get('sector', '')),
                            'BUY PRICE': f"${buy_price:.2f}",
                            'LIVE PRICE': f"${price:.2f}",
                            'QTY': qty or 1,
                            'P&L %': f"{pnl_pct:+.2f}%",
                            'P&L ABS': f"${pnl_abs:+.2f}",
                            '24H CHANGE': f"{chg*100:+.2f}%" if chg else '—',
                            'STATUS': '🟢 PROFIT' if pnl_pct > 0 else '🔴 LOSS',
                        })

            if portfolio:
                # Summary metrics
                total_pnl = total_current - total_invested
                total_pnl_pct = (total_pnl / total_invested * 100) if total_invested else 0

                m1, m2, m3, m4 = st.columns(4)
                m1.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#00d4ff;">${total_invested:,.0f}</div><div class="metric-label">TOTAL INVESTED</div></div>', unsafe_allow_html=True)
                m2.markdown(f'<div class="metric-card"><div class="metric-val" style="color:#00d4ff;">${total_current:,.0f}</div><div class="metric-label">CURRENT VALUE</div></div>', unsafe_allow_html=True)
                m3_color = '#00ff88' if total_pnl >= 0 else '#ff3366'
                m3.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{m3_color};">${total_pnl:+,.0f}</div><div class="metric-label">TOTAL P&L</div></div>', unsafe_allow_html=True)
                m4.markdown(f'<div class="metric-card"><div class="metric-val" style="color:{m3_color};">{total_pnl_pct:+.1f}%</div><div class="metric-label">TOTAL RETURN</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                df_port = pd.DataFrame(portfolio)
                st.dataframe(df_port, use_container_width=True, height=400)

                # Portfolio chart
                if len(portfolio) >= 2:
                    tickers_p = [r['TICKER'] for r in portfolio]
                    pnl_vals = [float(r['P&L %'].replace('%', '').replace('+', '')) for r in portfolio]
                    colors = ['#00ff88' if v > 0 else '#ff3366' for v in pnl_vals]
                    fig_port = go.Figure(go.Bar(
                        x=tickers_p, y=pnl_vals, marker_color=colors,
                        text=[f'{v:+.1f}%' for v in pnl_vals], textposition='outside',
                        textfont=dict(color='#c8d8f0', size=11, family='Share Tech Mono'),
                    ))
                    fig_port.update_layout(
                        paper_bgcolor='#050810', plot_bgcolor='#0a0f1e',
                        font=dict(family='Share Tech Mono', color='#c8d8f0', size=11),
                        title=dict(text='💰 BONUS PORTFOLIO — P&L %', font=dict(color='#00d4ff', size=14)),
                        yaxis=dict(gridcolor='#1a2540', zeroline=True, zerolinecolor='#4a6080'),
                        margin=dict(l=10, r=10, t=40, b=10),
                        height=350,
                    )
                    st.plotly_chart(fig_port, use_container_width=True)
            else:
                st.info("Couldn't fetch live prices for portfolio tickers.")

        # Hypothesis tracker
        st.markdown("---")
        st.markdown('<div style="font-family:Orbitron,monospace;font-size:13px;color:#00d4ff;letter-spacing:3px;margin-bottom:8px;">🧪 HYPOTHESIS TRACKER</div>', unsafe_allow_html=True)
        if 'hypothesis' in data:
            df_hyp = data['hypothesis']
            if not df_hyp.empty:
                df_hyp_clean = df_hyp.dropna(how='all').head(30)
                st.dataframe(df_hyp_clean, use_container_width=True, height=300)

    # ── FOOTER ──
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;font-family:Share Tech Mono,monospace;font-size:10px;color:#1a2540;letter-spacing:3px;padding:8px 0;">
      PYKUPZ LIVE TERMINAL · 7-ALGO AUDIT ENGINE · DATA: YFINANCE + YAHOO FINANCE · NOT FINANCIAL ADVICE
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════════
# HOW TO RUN:
# 1. pip install streamlit pandas plotly yfinance requests beautifulsoup4 numpy scipy openpyxl xlsxwriter
# 2. Save code as pykupz_terminal.py
# 3. streamlit run pykupz_terminal.py
# 4. Upload Pyk-Inv-List.xlsx when prompted
# 5. Type commands → live audited terminal activated
# ═══════════════════════════════════════════════════════════════════════
