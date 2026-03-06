"""
╔══════════════════════════════════════════════════════════════════════════════╗
║         PYKUPZ LIVE TERMINAL  —  HEDGE FUND EDITION  v4                    ║
║  Fully Automated · No Excel · 7 Audit Algorithms · Overlay Financial Charts ║
║  FIX: All StreamlitDuplicateElementId errors resolved with unique key=      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PYKUPZ ANALYTICS TERMINAL",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# AUTO-REFRESH  60 s
# ─────────────────────────────────────────────────────────────────────────────
refresh_count = st_autorefresh(interval=60000, key="ar_main")

# ─────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS / THEME
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');
:root{
  --bg:#03070f;--sf:#070d1a;--s2:#0b1220;--s3:#0f1830;
  --bd:#162040;--ac:#00e5ff;--gn:#00ff9d;--rd:#ff2d55;
  --am:#ffb800;--pu:#9d4edd;--tx:#b8cce0;--dm:#3a5070;--wh:#e8f2ff;
}
*,html,body{box-sizing:border-box;}
html,body,.main,[class*="css"],.block-container{
  background:var(--bg)!important;color:var(--tx)!important;
  font-family:'Inter',sans-serif!important;
}
.block-container{padding:.5rem 1.5rem 2rem!important;max-width:100%!important;}
.hf-hdr{display:flex;align-items:center;justify-content:space-between;
  background:linear-gradient(90deg,#03070f,#0a1628,#03070f);
  border-bottom:1px solid var(--ac);padding:10px 0;margin-bottom:4px;
  box-shadow:0 1px 30px rgba(0,229,255,.08);}
.hf-logo{font-family:'Bebas Neue',monospace;font-size:32px;letter-spacing:8px;
  color:var(--ac);text-shadow:0 0 20px rgba(0,229,255,.5);}
.hf-sub{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--dm);
  letter-spacing:3px;margin-top:2px;}
.hf-clock{font-family:'IBM Plex Mono',monospace;font-size:22px;color:var(--gn);
  text-shadow:0 0 10px rgba(0,255,157,.4);}
.hf-stat{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--dm);
  letter-spacing:2px;margin-top:3px;text-align:right;}
.tape{background:var(--sf);border-top:1px solid var(--bd);border-bottom:1px solid var(--bd);
  padding:6px 0;overflow:hidden;white-space:nowrap;margin:4px 0 10px;}
.tape-inner{display:inline-block;animation:tape 90s linear infinite;
  font-family:'IBM Plex Mono',monospace;font-size:12px;}
@keyframes tape{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.up{color:var(--gn)}.down{color:var(--rd)}.flat{color:var(--dm)}
.tu{color:var(--gn);margin:0 18px}.td{color:var(--rd);margin:0 18px}.tf{color:var(--dm);margin:0 18px}
.idx{display:flex;gap:10px;flex-wrap:wrap;background:var(--sf);
  border:1px solid var(--bd);border-radius:6px;padding:8px 14px;margin-bottom:8px;}
.idx-i{font-family:'IBM Plex Mono',monospace;font-size:12px;min-width:130px;}
.idx-n{color:var(--dm);font-size:10px;letter-spacing:1px;}
.card{background:var(--sf);border:1px solid var(--bd);border-radius:6px;
  padding:12px 16px;position:relative;overflow:hidden;}
.card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--ac);}
.card.gn::after{background:var(--gn)}.card.rd::after{background:var(--rd)}
.card.am::after{background:var(--am)}.card.pu::after{background:var(--pu)}
.cv{font-family:'IBM Plex Mono',monospace;font-size:21px;font-weight:600;
  color:var(--wh);margin-bottom:2px;}
.cl{font-size:9px;color:var(--dm);letter-spacing:2px;text-transform:uppercase;}
.cc{font-family:'IBM Plex Mono',monospace;font-size:11px;margin-top:3px;}
.sh{font-family:'Bebas Neue',monospace;font-size:17px;letter-spacing:4px;
  color:var(--ac);border-bottom:1px solid var(--bd);padding-bottom:5px;margin:14px 0 8px;}
.ab{background:var(--s2);border:1px solid var(--bd);border-radius:6px;
  padding:10px 14px;margin-bottom:6px;font-family:'IBM Plex Mono',monospace;font-size:11px;}
.ar{display:flex;align-items:center;justify-content:space-between;
  padding:4px 0;border-bottom:1px solid var(--bd);
  font-family:'IBM Plex Mono',monospace;font-size:11px;}
.ar:last-child{border-bottom:none;}
.an{color:var(--dm);width:240px;flex-shrink:0;}
.stTabs [data-baseweb="tab-list"]{background:var(--s2)!important;border-bottom:1px solid var(--bd)!important;gap:1px;}
.stTabs [data-baseweb="tab"]{font-family:'IBM Plex Mono',monospace!important;font-size:10px!important;
  letter-spacing:2px!important;color:var(--dm)!important;padding:8px 14px!important;}
.stTabs [aria-selected="true"]{color:var(--ac)!important;border-bottom:2px solid var(--ac)!important;}
.stDataFrame>div{background:var(--sf)!important;border-radius:6px;}
div[data-testid="stDataFrame"]{background:var(--sf)!important;}
.stSelectbox>div>div,.stTextInput input,.stMultiSelect>div{
  background:var(--s2)!important;border-color:var(--bd)!important;
  color:var(--wh)!important;font-family:'IBM Plex Mono',monospace!important;}
.stTextInput input{color:var(--ac)!important;}
.stTextInput input::placeholder{color:var(--dm)!important;}
.stButton button{background:transparent!important;border:1px solid var(--ac)!important;
  color:var(--ac)!important;font-family:'IBM Plex Mono',monospace!important;
  font-size:11px!important;letter-spacing:2px!important;border-radius:4px!important;}
.stButton button:hover{background:rgba(0,229,255,.08)!important;}
section[data-testid="stSidebar"]{background:var(--sf)!important;border-right:1px solid var(--bd)!important;}
.streamlit-expanderHeader{background:var(--s2)!important;color:var(--ac)!important;
  font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;}
details{border:1px solid var(--bd)!important;border-radius:6px!important;}
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--ac);border-radius:2px}
p,span,li{font-family:'Inter',sans-serif!important;}
code{background:var(--s3)!important;color:var(--ac)!important;font-family:'IBM Plex Mono',monospace!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# UNIVERSE
# ─────────────────────────────────────────────────────────────────────────────
# ── Core high-conviction picks ──
Q1_2026 = [
    "NVDA","ANET","PLTR","HUBS","HIMS","LLY","PMRTY","CRWD","DKNG","APP",
    "AFRM","ONON","SHOP","NU","NFLX","AVGO","SPOT","META","MU","FTNT",
    "SOFI","ALAB","AMD","RDDT","TTD","AMZN","ROKU","MELI","PANW","XYZ",
]

# ── Extended STB universe ──
STB_ALL = [
    "NVDA","ANET","DT","MELI","SHOP","TSM","GOOG","AMZN","ISRG","MSFT",
    "SPOT","PLTR","CRWD","NFLX","CRM","AMD","ASML","META","IBKR","AXP",
    "FTNT","NVO","HUBS","DUOL","NET","DOCS","HIMS","APP","LLY","DKNG",
    "NU","AVGO","ONON","SOFI","TTD","PANW","JD","VEEV","IREN","BKNG",
    "UBER","HOOD","BABA","ARGX","ELF","RYCEY","ETSY","UPWK","BRK-B",
    "CRWV","COIN","BYDDY","UPST","WPLCF","KNSL","MGNI","AAPL","PDD",
    "BIDU","TCEHY","MAR","ON","DOCU","TSLA","ENPH","PERI","TCOM","FUBO",
    "GCT","LC","NBIS","AFRM","RDDT","ROKU","ALAB","SOFI","XYZ","ANET",
]

# ── Deduplicated master universe ──
MASTER_UNIVERSE = sorted(set(Q1_2026 + STB_ALL))

# ── Ticker metadata (name + sector) ──
TICKER_META = {
    "NVDA":"Nvidia · Semiconductors","ANET":"Arista Networks · Networking",
    "PLTR":"Palantir · AI/Data","HUBS":"HubSpot · SaaS CRM",
    "HIMS":"Hims & Hers · Health","LLY":"Eli Lilly · Pharma",
    "PMRTY":"Prysmian · Infrastructure","CRWD":"CrowdStrike · Cybersecurity",
    "DKNG":"DraftKings · Gaming","APP":"AppLovin · AdTech",
    "AFRM":"Affirm · FinTech","ONON":"On Running · Footwear",
    "SHOP":"Shopify · E-Commerce","NU":"Nu Holdings · FinTech",
    "NFLX":"Netflix · Streaming","AVGO":"Broadcom · Semiconductors",
    "SPOT":"Spotify · Streaming","META":"Meta · Social Media",
    "MU":"Micron · Memory","FTNT":"Fortinet · Cybersecurity",
    "SOFI":"SoFi · FinTech","ALAB":"Astera Labs · AI Networking",
    "AMD":"AMD · Semiconductors","RDDT":"Reddit · Social Media",
    "TTD":"Trade Desk · AdTech","AMZN":"Amazon · Cloud/Retail",
    "ROKU":"Roku · Streaming","MELI":"MercadoLibre · LatAm E-Com",
    "PANW":"Palo Alto · Cybersecurity","XYZ":"Block Inc · FinTech",
    "TSM":"TSMC · Foundry","GOOG":"Alphabet · Search/Cloud",
    "MSFT":"Microsoft · Cloud/AI","JD":"JD.com · China E-Com",
    "VEEV":"Veeva · Life Sciences SaaS","ASML":"ASML · Lithography",
    "IREN":"Iris Energy · BTC Mining","BKNG":"Booking Holdings · Travel",
    "UBER":"Uber · Mobility","HOOD":"Robinhood · FinTech",
    "BABA":"Alibaba · China Tech","ARGX":"argenx · Biotech",
    "NET":"Cloudflare · Networking","DUOL":"Duolingo · EdTech",
    "ELF":"e.l.f. Beauty · Consumer","AXP":"Amex · Financials",
    "ISRG":"Intuitive Surgical · MedTech","DOCS":"Doximity · Health SaaS",
    "RYCEY":"Rolls-Royce · Aerospace","ETSY":"Etsy · Marketplace",
    "UPWK":"Upwork · Future of Work","BRK-B":"Berkshire · Conglomerate",
    "CRWV":"CoreWeave · AI Cloud","COIN":"Coinbase · Crypto",
    "IBKR":"IBKR · Brokerage","BYDDY":"BYD · EV/Batteries",
    "UPST":"Upstart · AI Lending","CRM":"Salesforce · CRM",
    "NVO":"Novo Nordisk · Pharma","WPLCF":"Wise PLC · FinTech",
    "KNSL":"Kinsale Capital · Insurance","ETOR":"eToro · FinTech",
    "MGNI":"Magnite · AdTech","AAPL":"Apple · Consumer Tech",
    "PDD":"Pinduoduo · China E-Com","BIDU":"Baidu · China Search/AI",
    "TCEHY":"Tencent · China Tech","MAR":"Marriott · Hospitality",
    "ON":"onsemi · Power Semis","DOCU":"DocuSign · eSign SaaS",
    "TSLA":"Tesla · EV/AI","ENPH":"Enphase · Solar",
    "PERI":"Perion Network · AdTech","TCOM":"Trip.com · Travel",
    "FUBO":"FuboTV · Streaming","GCT":"GigaCloud · B2B E-Com",
    "LC":"LendingClub · FinTech","NBIS":"Nebius · AI Cloud",
    "DT":"Dynatrace · Observability","SOFI":"SoFi · FinTech",
}

BONUS = [
    {"ticker":"CRWD",  "name":"Crowdstrike",  "buy":150.90, "qty":0.404},
    {"ticker":"WPLCF", "name":"Wise PLC",      "buy":9.90,   "qty":6.16},
    {"ticker":"SHOP",  "name":"Shopify",        "buy":82.68,  "qty":0.737},
    {"ticker":"XYZ",   "name":"Block Inc",      "buy":98.92,  "qty":1.203},
    {"ticker":"HIMS",  "name":"Hims & Hers",    "buy":18.50,  "qty":5.40},
    {"ticker":"NVO",   "name":"Novo Nordisk",   "buy":95.00,  "qty":1.05},
    {"ticker":"FTNT",  "name":"Fortinet",       "buy":65.00,  "qty":1.54},
    {"ticker":"NU",    "name":"Nu Holdings",    "buy":12.00,  "qty":8.33},
]

INDICES = {
    "S&P 500":"^GSPC","NASDAQ":"^IXIC","DOW":"^DJI","VIX":"^VIX",
    "10Y YIELD":"^TNX","GOLD":"GC=F","OIL":"CL=F","BTC":"BTC-USD",
}
SECTORS = {
    "Technology":"XLK","Healthcare":"XLV","Financials":"XLF",
    "Consumer":"XLY","Energy":"XLE","Industrials":"XLI","Utilities":"XLU",
}

# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for k, v in {
    "audit_cache":{}, "audit_log":[], "startup_done":False, "last_run":None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────────────────
# DATA FETCHERS  (cached)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def get_price(ticker):
    try:
        h = yf.Ticker(ticker).history(period="5d")
        if h.empty or len(h) < 2:
            return None, None, None
        p    = float(h["Close"].iloc[-1])
        prev = float(h["Close"].iloc[-2])
        vol  = float(h["Volume"].iloc[-1]) if "Volume" in h else 0
        return p, (p - prev) / prev, vol
    except Exception:
        return None, None, None

@st.cache_data(ttl=3600, show_spinner=False)
def get_info(ticker):
    try:
        return yf.Ticker(ticker).info
    except Exception:
        return {}

@st.cache_data(ttl=3600, show_spinner=False)
def get_hist(ticker, period="5y"):
    try:
        return yf.Ticker(ticker).history(period=period)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_all_financials(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.income_stmt, t.cash_flow, t.balance_sheet, t.history(period="max")
    except Exception:
        return None, None, None, pd.DataFrame()

@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_hist(ticker):
    try:
        return yf.Ticker(ticker).earnings_history
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_mcap(v):
    if not v: return "—"
    if v >= 1e12: return f"${v/1e12:.2f}T"
    if v >= 1e9:  return f"${v/1e9:.1f}B"
    if v >= 1e6:  return f"${v/1e6:.0f}M"
    return f"${v:.0f}"

def fmt_pct(v, mult=True):
    if v is None: return "—"
    try:
        f = float(v) * (100 if mult else 1)
        return f"{f:+.2f}%"
    except Exception:
        return "—"

def safe_row(df, *keys):
    if df is None or df.empty: return None
    for k in keys:
        if k in df.index:
            r = df.loc[k].dropna()
            return r if not r.empty else None
    return None

def base_layout(title_text, height=420):
    return dict(
        paper_bgcolor="#03070f",
        plot_bgcolor="#070d1a",
        font=dict(family="IBM Plex Mono", color="#b8cce0", size=11),
        title=dict(text=title_text, font=dict(color="#00e5ff", size=14)),
        height=height,
        margin=dict(l=8, r=8, t=48, b=8),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#162040",
                    orientation="h", y=1.10, x=0),
    )

# ─────────────────────────────────────────────────────────────────────────────
# RANKING ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def rank_score(info):
    score = 0.0
    try:
        rg  = (info.get("revenueGrowth")  or 0) * 100
        eg  = (info.get("earningsGrowth") or 0) * 100
        pe  =  info.get("trailingPE")      or 0
        ps  =  info.get("priceToSalesTrailing12Months") or 0
        fcf =  info.get("freeCashflow")    or 0
        td  =  info.get("totalDebt")       or 0
        tc  =  info.get("totalCash")       or 0
        rev =  info.get("totalRevenue")    or 1
        nd  = (td - tc) / rev if rev else 0
        score += min(max(rg + 50, 0), 150) / 150 * 30
        score += min(max(eg + 50, 0), 150) / 150 * 20
        score += 20 if fcf > 0 else 10 if fcf == 0 else 0
        if nd < 0:   score += 10
        elif nd < 1: score += 7
        elif nd < 3: score += 3
        if 0 < pe < 80:  score += 10
        if 0 < ps < 20:  score += 10
    except Exception:
        pass
    return round(min(score, 100), 1)

def signal(score, chg):
    if score >= 75 and (chg or 0) > -0.03: return "🟢 STRONG BUY"
    elif score >= 60: return "🟡 BUY"
    elif score >= 45: return "🟠 HOLD"
    else:             return "🔴 WATCH"

# ─────────────────────────────────────────────────────────────────────────────
# 7 AUDIT ALGORITHMS
# ─────────────────────────────────────────────────────────────────────────────
def algo1(ticker, price):
    try:
        t     = yf.Ticker(ticker)
        info  = t.info
        srcs  = {
            "Yahoo Info": (info.get("currentPrice") or info.get("regularMarketPrice"), 0.40),
            "Fast Info":  (getattr(t.fast_info, "last_price", None), 0.30),
            "Historical": (None, 0.20),
            "Prev Close": (info.get("previousClose"), 0.10),
        }
        h = t.history(period="2d")
        if not h.empty:
            srcs["Historical"] = (float(h["Close"].iloc[-1]), 0.20)
        prices = [(v, w) for v, w in srcs.values() if v is not None]
        if not prices:
            return {"status":"⚪ NO DATA","weighted":price}
        tw  = sum(w for _, w in prices)
        wav = sum(p * w for p, w in prices) / tw
        vals   = [p for p, _ in prices]
        spread = (max(vals) - min(vals)) / np.mean(vals) * 100 if np.mean(vals) else 0
        s = "✅ AUDITED" if spread < 0.5 else "⚠️ MINOR DISCREPANCY" if spread < 2 else "🚨 DISCREPANCY"
        return {"status":s, "weighted":round(wav,4), "spread":round(spread,3)}
    except Exception:
        return {"status":"❌ ERROR","weighted":price}

def algo2(ticker, price):
    try:
        h = get_hist(ticker, "5y")
        if h.empty or len(h) < 30:
            return {"status":"⚪ INSUFFICIENT DATA","z":None,"flag":False}
        monthly = h["Close"].resample("ME").last().dropna()
        if len(monthly) < 12:
            return {"status":"⚪ INSUFFICIENT DATA","z":None,"flag":False}
        mu, sig = float(monthly.mean()), float(monthly.std())
        if sig == 0:
            return {"status":"⚪ ZERO STD","z":0,"flag":False}
        z = (price - mu) / sig
        if   abs(z) > 3: return {"status":f"🚨 OUTLIER >3σ (z={z:.1f})","z":round(z,2),"flag":True}
        elif abs(z) > 2: return {"status":f"⚠️ ELEVATED >2σ (z={z:.1f})","z":round(z,2),"flag":True}
        else:            return {"status":f"✅ NORMAL (z={z:.1f})","z":round(z,2),"flag":False}
    except Exception:
        return {"status":"⚪ ERROR","z":None,"flag":False}

def algo3(ticker):
    try:
        tk  = yf.Ticker(ticker)
        inc = tk.income_stmt
        cf  = None
        try: cf = tk.cash_flow
        except Exception: pass
        if inc is None or inc.empty:
            return {"status":"⚪ NO DATA","issues":[],"checks":{}}
        def v(*keys):
            for k in keys:
                if k in inc.index:
                    val = inc.loc[k].iloc[0]
                    return float(val) if pd.notna(val) else None
            return None
        def vcf(*keys):
            if cf is None or cf.empty: return None
            for k in keys:
                if k in cf.index:
                    val = cf.loc[k].iloc[0]
                    return float(val) if pd.notna(val) else None
            return None
        ebitda = v("EBITDA","Normalized EBITDA")
        ebit   = v("EBIT","Operating Income")
        ni     = v("Net Income","Net Income Common Stockholders")
        da     = v("Reconciled Depreciation","Depreciation And Amortization")
        fcf    = vcf("Free Cash Flow")
        opcf   = vcf("Operating Cash Flow")
        issues, checks = [], {}
        if ebitda and ebit and da:
            d = abs(ebitda - (ebit + abs(da))) / abs(ebitda) * 100
            checks["EBITDA→EBIT"] = "✅" if d < 5 else "⚠️"
            if d >= 5: issues.append(f"EBITDA gap {d:.1f}%")
        if fcf and opcf:
            checks["FCF≤OCF"] = "✅" if fcf <= opcf * 1.05 else "⚠️"
            if fcf > opcf * 1.05: issues.append("FCF > OCF unusual")
        if ni and ebitda:
            checks["NI<EBITDA"] = "✅" if ni < ebitda else "⚠️"
        return {"status":"✅ CHAIN INTACT" if not issues else f"🚨 {len(issues)} ISSUE(S)",
                "issues":issues,"checks":checks}
    except Exception:
        return {"status":"⚪ ERROR","issues":[],"checks":{}}

def algo4(ticker):
    try:
        h = get_hist(ticker,"5d")
        if h.empty:
            return {"status":"🔴 NO DATA","score":0,"flag":True}
        last = h.index[-1]
        if hasattr(last,"to_pydatetime"): last = last.to_pydatetime()
        try:    age = (datetime.now(last.tzinfo) - last).days
        except Exception: age = (datetime.now() - last.replace(tzinfo=None)).days
        if   age < 1:  s, lbl = 100, "🟢 REAL-TIME"
        elif age < 7:  s, lbl = 80,  "🟡 RECENT"
        elif age < 30: s, lbl = 60,  "🟠 MODERATE"
        else:          s, lbl = 30,  "🔴 STALE"
        return {"status":lbl,"score":s,"age":age,"flag":s<70}
    except Exception:
        return {"status":"⚪ ERROR","score":0,"flag":True}

def algo5(ticker):
    try:
        inc,_,_,_ = get_all_financials(ticker)
        if inc is None or inc.empty: return {"status":"⚪ NO DATA","cagr":None,"flag":False}
        rr = safe_row(inc,"Total Revenue","Revenue")
        if rr is None: return {"status":"⚪ NO REVENUE","cagr":None,"flag":False}
        vals = [float(v) for v in rr.sort_index().values[::-1]]
        if len(vals) < 3: return {"status":"⚪ NEED 3+ YEARS","cagr":None,"flag":False}
        cagr = (vals[-1]/vals[0])**(1/max(len(vals)-1,1)) - 1 if vals[0]!=0 else 0
        gs = [(vals[i]-vals[i-1])/abs(vals[i-1]) for i in range(1,len(vals)) if vals[i-1]!=0]
        if len(gs) >= 3:
            mg, sg = np.mean(gs), np.std(gs)
            z = (gs[-1]-mg)/sg if sg>0 else 0
            if abs(z) > 2:
                return {"status":f"📉 TREND BREAK (z={z:.1f})","cagr":round(cagr*100,1),"flag":True}
        return {"status":"✅ TREND INTACT","cagr":round(cagr*100,1),"flag":False}
    except Exception:
        return {"status":"⚪ ERROR","cagr":None,"flag":False}

def algo6(ticker):
    try:
        eh = get_earnings_hist(ticker)
        if eh is None or eh.empty: return {"status":"⚪ NO DATA","acc":None,"flag":False,"q":[]}
        ec = next((c for c in eh.columns if "estimate" in c.lower()),None)
        ac = next((c for c in eh.columns if "actual"   in c.lower()),None)
        if not ec or not ac: return {"status":"⚪ NO EPS COLS","acc":None,"flag":False,"q":[]}
        recent = eh[[ec,ac]].dropna().tail(8)
        beats  = int((recent[ac] >= recent[ec]).sum())
        total  = len(recent)
        if total == 0: return {"status":"⚪ NO QTRS","acc":None,"flag":False,"q":[]}
        acc  = beats/total*100
        flag = acc < 50
        s = f"✅ {acc:.0f}% BEAT RATE" if acc>=75 else f"⚠️ {acc:.0f}% BEAT" if acc>=50 else f"🚨 {acc:.0f}% — LOW"
        q = [{"date":str(i)[:10],"est":round(float(r[ec]),2),"act":round(float(r[ac]),2),
               "res":"✅" if r[ac]>=r[ec] else "❌"} for i,r in recent.iterrows()]
        return {"status":s,"acc":round(acc,1),"flag":flag,"q":q}
    except Exception:
        return {"status":"⚪ ERROR","acc":None,"flag":False,"q":[]}

def algo7(ticker, price, info):
    checks=[]; val=0; tot=0
    def chk(name, fair, live, tol=25):
        nonlocal val, tot
        tot += 1
        if fair and live and fair > 0:
            dev = (live-fair)/fair*100
            ok  = abs(dev) < tol
            if ok: val += 1
            return {"name":name,"fair":round(fair,2),"live":round(live,2),
                    "dev":round(dev,1),"status":"✅ VALIDATED" if ok else "⚠️ DEVIATING"}
        return None
    pe  = info.get("trailingPE")
    fpe = info.get("forwardPE")
    eps = info.get("trailingEps")
    rev = info.get("totalRevenue")
    mc  = info.get("marketCap")
    if pe  and eps and eps>0: c=chk("P/E Implied",pe*eps,price);  checks.append(c) if c else None
    if fpe and eps and eps>0: c=chk("Fwd P/E",fpe*eps,price);     checks.append(c) if c else None
    if rev and mc and rev>0:  c=chk("P/S vs 2.5x",2.5,mc/rev,100);checks.append(c) if c else None
    pct = val/tot*100 if tot>0 else 0
    return {
        "overall": f"🏆 VALIDATED ({val}/{tot})" if pct>=75 else f"⚠️ PARTIAL ({val}/{tot})" if pct>=50 else f"🚨 CHALLENGED ({val}/{tot})",
        "checks": checks, "score": pct
    }

def run_audit(ticker):
    price, chg, _ = get_price(ticker)
    info  = get_info(ticker)
    if not price: price = info.get("currentPrice") or 0.0
    a1=algo1(ticker,price); a2=algo2(ticker,price); a3=algo3(ticker)
    a4=algo4(ticker);       a5=algo5(ticker);       a6=algo6(ticker)
    a7=algo7(ticker,price,info)
    flags = [a2.get("flag",False), bool(a3.get("issues")),
             a4.get("flag",False), a5.get("flag",False), a6.get("flag",False)]
    return {
        "ticker":ticker,"price":price,"change":chg,"info":info,
        "score":max(0, 100 - sum(flags)*15),
        "ts":datetime.now().strftime("%H:%M:%S"),
        "A1":a1,"A2":a2,"A3":a3,"A4":a4,"A5":a5,"A6":a6,"A7":a7,
    }

def startup_audit():
    """Run on first load — uses a single placeholder to avoid ghost None slots."""
    placeholder = st.empty()
    with placeholder.container():
        prog = st.progress(0, text="⚡ Initialising — auditing top picks...")
        for i, t in enumerate(Q1_2026[:10]):
            try:
                res = run_audit(t)
                st.session_state.audit_cache[t] = res
                st.session_state.audit_log.append(res)
            except Exception:
                pass
            prog.progress((i+1)/10, text=f"⚡ Auditing {t}... ({i+1}/10)")
    placeholder.empty()          # wipes the entire container — no ghost slots
    st.session_state.startup_done = True
    st.session_state.last_run = datetime.now().strftime("%H:%M:%S")

# ─────────────────────────────────────────────────────────────────────────────
# ████████████  CHART BUILDERS  ████████████
# ─────────────────────────────────────────────────────────────────────────────

def fig_candlestick(ticker, period="1y"):
    h = get_hist(ticker, period)
    if h.empty: return go.Figure()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.75, 0.25], vertical_spacing=0.03)
    ma20 = h["Close"].rolling(20).mean()
    ma50 = h["Close"].rolling(50).mean()
    std  = h["Close"].rolling(20).std()
    bbu, bbl = ma20+2*std, ma20-2*std
    fig.add_trace(go.Candlestick(
        x=h.index, open=h["Open"], high=h["High"], low=h["Low"], close=h["Close"],
        name="OHLC", increasing_fillcolor="#00ff9d", decreasing_fillcolor="#ff2d55",
        increasing_line_color="#00ff9d", decreasing_line_color="#ff2d55"), row=1, col=1)
    fig.add_trace(go.Scatter(x=h.index,y=ma20,mode="lines",name="MA20",
                              line=dict(color="#ffb800",width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=ma50,mode="lines",name="MA50",
                              line=dict(color="#9d4edd",width=1,dash="dot")),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=bbu,mode="lines",name="BB+",
                              line=dict(color="#00e5ff",width=0.7,dash="dash")),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=bbl,mode="lines",name="BB-",
                              line=dict(color="#00e5ff",width=0.7,dash="dash"),
                              fill="tonexty",fillcolor="rgba(0,229,255,0.03)"),row=1,col=1)
    colors = ["#00ff9d" if c>=o else "#ff2d55" for c,o in zip(h["Close"],h["Open"])]
    fig.add_trace(go.Bar(x=h.index,y=h["Volume"],name="Vol",marker_color=colors,opacity=0.5),row=2,col=1)
    fig.update_layout(**base_layout(f"⚡ {ticker}  CANDLESTICK + BOLLINGER BANDS + VOLUME", 500))
    fig.update_xaxes(rangeslider_visible=False, gridcolor="#162040")
    fig.update_yaxes(gridcolor="#162040", zeroline=False)
    return fig


def _extract_annual_series(ticker):
    """Extract all annual financial series needed for overlay charts."""
    inc, cf, bal, hist = get_all_financials(ticker)
    info = get_info(ticker)

    def series(df, *keys, divisor=1e9):
        r = safe_row(df, *keys)
        if r is None: return {}, []
        s = r.sort_index()
        d = {str(k.year): float(v)/divisor for k,v in zip(s.index,s.values) if pd.notna(v)}
        return d, sorted(d.keys())

    rev_d,  rev_y  = series(inc, "Total Revenue","Revenue")
    ebi_d,  ebi_y  = series(inc, "EBITDA","Normalized EBITDA")
    ni_d,   ni_y   = series(inc, "Net Income","Net Income Common Stockholders")
    fcf_d,  fcf_y  = series(cf,  "Free Cash Flow")
    shares_d, _    = series(inc, "Diluted Average Shares","Basic Average Shares", divisor=1)

    all_years = sorted(set(rev_y + ebi_y + fcf_y))

    # EPS per year
    eps_d = {}
    for yr in all_years:
        ni_v = ni_d.get(yr); sh_v = shares_d.get(yr)
        if ni_v is not None and sh_v and sh_v > 0:
            eps_d[yr] = round(ni_v * 1e9 / sh_v, 3)

    # Revenue growth %
    rev_g = {}
    yr_list = sorted(rev_d.keys())
    for i in range(1, len(yr_list)):
        pv = rev_d.get(yr_list[i-1]); cv = rev_d.get(yr_list[i])
        if pv and pv != 0: rev_g[yr_list[i]] = round((cv-pv)/abs(pv)*100, 1)

    # EPS growth %
    eps_g = {}
    eps_yrs = sorted(eps_d.keys())
    for i in range(1, len(eps_yrs)):
        pv = eps_d.get(eps_yrs[i-1]); cv = eps_d.get(eps_yrs[i])
        if pv and pv != 0: eps_g[eps_yrs[i]] = round((cv-pv)/abs(pv)*100, 1)

    # Stock price at year-end + P/E + P/S
    price_yr = {}; pe_yr = {}; ps_yr = {}
    sh_out = info.get("sharesOutstanding", 0) or 0
    for yr in all_years:
        try:
            yh = hist[hist.index.year == int(yr)]
            if not yh.empty:
                yp = float(yh["Close"].iloc[-1])
                price_yr[yr] = yp
                ep = eps_d.get(yr)
                if ep and ep > 0: pe_yr[yr] = round(yp / ep, 1)
                rv = rev_d.get(yr)
                if rv and rv > 0 and sh_out > 0:
                    ps_yr[yr] = round(yp * sh_out / (rv*1e9), 2)
        except Exception:
            pass

    return {
        "all_years": all_years, "rev_d": rev_d, "ebi_d": ebi_d,
        "fcf_d": fcf_d, "ni_d": ni_d, "eps_d": eps_d,
        "rev_g": rev_g, "eps_g": eps_g, "price_yr": price_yr,
        "pe_yr": pe_yr, "ps_yr": ps_yr, "hist": hist,
    }


def fig_financial_lines(ticker):
    """4-panel: Revenue/EBITDA/FCF vs Price | P/E & P/S | EPS & EPS Growth | Rev Growth"""
    d = _extract_annual_series(ticker)
    all_years = d["all_years"]

    if not all_years:
        fig = go.Figure()
        fig.update_layout(**base_layout(f"{ticker} — No annual data", 200))
        return fig

    def ylist(dct, years): return [dct.get(y) for y in years]

    fig = make_subplots(
        rows=4, cols=1, shared_xaxes=True,
        subplot_titles=[
            f"{ticker} — Revenue · EBITDA · FCF ($B) + Stock Price",
            "Valuation Multiples — P/E  &  P/S  (year-end)",
            "EPS per Share ($)  +  EPS Growth %",
            "Revenue Growth %  YoY",
        ],
        vertical_spacing=0.07,
        row_heights=[0.35, 0.22, 0.22, 0.21],
        specs=[[{"secondary_y":True}],[{"secondary_y":False}],
               [{"secondary_y":True}],[{"secondary_y":False}]],
    )

    # Panel 1 — bars + price line
    if d["rev_d"]:
        fig.add_trace(go.Bar(x=all_years, y=ylist(d["rev_d"],all_years), name="Revenue $B",
                             marker_color="rgba(0,229,255,0.6)", offsetgroup=0), row=1, col=1, secondary_y=False)
    if d["ebi_d"]:
        fig.add_trace(go.Bar(x=all_years, y=ylist(d["ebi_d"],all_years), name="EBITDA $B",
                             marker_color="rgba(0,255,157,0.6)", offsetgroup=1), row=1, col=1, secondary_y=False)
    if d["fcf_d"]:
        fig.add_trace(go.Bar(x=all_years, y=ylist(d["fcf_d"],all_years), name="FCF $B",
                             marker_color="rgba(157,77,221,0.6)", offsetgroup=2), row=1, col=1, secondary_y=False)
    if d["price_yr"]:
        py = d["price_yr"]; ky = sorted(py.keys())
        fig.add_trace(go.Scatter(x=ky, y=[py[y] for y in ky], name="Stock Price $",
                                  mode="lines+markers",
                                  line=dict(color="#ffb800",width=2.5),
                                  marker=dict(size=7,color="#ffb800",symbol="diamond")),
                      row=1, col=1, secondary_y=True)

    # Panel 2 — P/E & P/S
    if d["pe_yr"]:
        ky = sorted(d["pe_yr"].keys())
        fig.add_trace(go.Scatter(x=ky, y=[d["pe_yr"][y] for y in ky], name="P/E",
                                  mode="lines+markers+text",
                                  text=[f"{v:.0f}" for v in [d["pe_yr"][y] for y in ky]],
                                  textposition="top center", textfont=dict(size=9,color="#00e5ff"),
                                  line=dict(color="#00e5ff",width=2), marker=dict(size=7)), row=2, col=1)
    if d["ps_yr"]:
        ky = sorted(d["ps_yr"].keys())
        fig.add_trace(go.Scatter(x=ky, y=[d["ps_yr"][y] for y in ky], name="P/S",
                                  mode="lines+markers+text",
                                  text=[f"{v:.1f}" for v in [d["ps_yr"][y] for y in ky]],
                                  textposition="bottom center", textfont=dict(size=9,color="#ff2d55"),
                                  line=dict(color="#ff2d55",width=2), marker=dict(size=7)), row=2, col=1)

    # Panel 3 — EPS bars + EPS growth line
    if d["eps_d"]:
        ec = ["#00ff9d" if (d["eps_d"].get(y,0) or 0)>=0 else "#ff2d55" for y in all_years]
        fig.add_trace(go.Bar(x=all_years, y=[d["eps_d"].get(y) for y in all_years],
                             name="EPS $", marker_color=ec, opacity=0.75),
                      row=3, col=1, secondary_y=False)
    if d["eps_g"]:
        ky = sorted(d["eps_g"].keys())
        fig.add_trace(go.Scatter(x=ky, y=[d["eps_g"][y] for y in ky], name="EPS Grw %",
                                  mode="lines+markers",
                                  line=dict(color="#ffb800",width=2,dash="dot"),
                                  marker=dict(size=6,color="#ffb800")),
                      row=3, col=1, secondary_y=True)

    # Panel 4 — Revenue growth bars
    if d["rev_g"]:
        ky = sorted(d["rev_g"].keys()); rv = [d["rev_g"][y] for y in ky]
        rc = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in rv]
        fig.add_trace(go.Bar(x=ky, y=rv, name="Rev Grw %", marker_color=rc,
                             text=[f"{v:.1f}%" for v in rv], textposition="outside",
                             textfont=dict(size=9,family="IBM Plex Mono",color="#b8cce0")), row=4, col=1)

    fig.update_layout(
        paper_bgcolor="#03070f", plot_bgcolor="#070d1a",
        font=dict(family="IBM Plex Mono", color="#b8cce0", size=10),
        height=950, margin=dict(l=8,r=8,t=60,b=8), barmode="group",
        legend=dict(orientation="h",y=1.04,bgcolor="rgba(0,0,0,0)",x=0),
    )
    fig.update_annotations(font=dict(color="#3a5070",size=10,family="IBM Plex Mono"))
    for r in range(1,5):
        # FIX: type='category' prevents Plotly treating year strings as floats (2,021.5 bug)
        fig.update_xaxes(gridcolor="#162040",showgrid=True,zeroline=False,
                         type="category", row=r, col=1)
        fig.update_yaxes(gridcolor="#162040",showgrid=True,zeroline=True,zerolinecolor="#3a5070",row=r,col=1)
    try:
        fig.update_yaxes(title_text="$B",       row=1, col=1, secondary_y=False)
        fig.update_yaxes(title_text="Price $",  row=1, col=1, secondary_y=True, gridcolor="rgba(0,0,0,0)")
        fig.update_yaxes(title_text="EPS $",    row=3, col=1, secondary_y=False)
        fig.update_yaxes(title_text="EPS Grw%", row=3, col=1, secondary_y=True, gridcolor="rgba(0,0,0,0)")
    except Exception:
        pass
    return fig


def fig_overlay_price_vs_metrics(ticker):
    """
    INSTITUTIONAL OVERLAY CHART
    Stock price (daily close — full history) as the PRIMARY continuous line,
    with annual P/E, P/S, Revenue Growth, and EPS Growth plotted as secondary
    markers/lines on shared time axis so investors can see exact correlation.
    """
    d = _extract_annual_series(ticker)
    hist = d["hist"]
    if hist.empty and not d["all_years"]:
        fig = go.Figure()
        fig.update_layout(**base_layout(f"{ticker} — No data", 200))
        return fig

    # Convert annual year-labels to datetime for alignment
    def yr_to_dt(yr_str):
        return pd.Timestamp(f"{yr_str}-12-31")

    fig = make_subplots(
        rows=5, cols=1, shared_xaxes=True,
        subplot_titles=[
            f"⚡ {ticker} — Daily Stock Price",
            "P/E Ratio  (year-end, overlaid on price axis below)",
            "P/S Ratio  (year-end)",
            "Revenue Growth %  YoY",
            "EPS Growth %  YoY",
        ],
        vertical_spacing=0.05,
        row_heights=[0.30, 0.175, 0.175, 0.175, 0.175],
        specs=[[{"secondary_y":False}],[{"secondary_y":False}],
               [{"secondary_y":False}],[{"secondary_y":False}],
               [{"secondary_y":False}]],
    )

    # ── Panel 1: Daily stock price (full continuous line) ──
    if not hist.empty:
        fig.add_trace(go.Scatter(
            x=hist.index, y=hist["Close"],
            name="Price $", mode="lines",
            line=dict(color="#ffb800", width=1.5),
            fill="tozeroy", fillcolor="rgba(255,184,0,0.05)"), row=1, col=1)
        # Annual year-end price markers
        if d["price_yr"]:
            ky = sorted(d["price_yr"].keys())
            xd = [yr_to_dt(y) for y in ky]; yv = [d["price_yr"][y] for y in ky]
            fig.add_trace(go.Scatter(
                x=xd, y=yv, name="Year-End Price",
                mode="markers+text",
                text=[f"${v:.0f}" for v in yv], textposition="top center",
                textfont=dict(size=8, color="#ffb800"),
                marker=dict(size=10, color="#ffb800", symbol="diamond",
                            line=dict(color="#03070f",width=1))), row=1, col=1)

    # ── Panel 2: P/E over time ──
    if d["pe_yr"]:
        ky = sorted(d["pe_yr"].keys())
        xd = [yr_to_dt(y) for y in ky]; yv = [d["pe_yr"][y] for y in ky]
        fig.add_trace(go.Scatter(
            x=xd, y=yv, name="P/E Ratio",
            mode="lines+markers+text",
            text=[f"{v:.0f}x" for v in yv], textposition="top center",
            textfont=dict(size=8, color="#00e5ff"),
            line=dict(color="#00e5ff", width=2),
            marker=dict(size=8, color="#00e5ff")), row=2, col=1)
        # Reference lines
        for ref, lbl in [(25,"25x"),(50,"50x"),(100,"100x")]:
            fig.add_hline(y=ref, line=dict(color="#162040",width=1,dash="dot"),
                          annotation_text=lbl,
                          annotation_font=dict(color="#3a5070",size=8), row=2, col=1)

    # ── Panel 3: P/S over time ──
    if d["ps_yr"]:
        ky = sorted(d["ps_yr"].keys())
        xd = [yr_to_dt(y) for y in ky]; yv = [d["ps_yr"][y] for y in ky]
        fig.add_trace(go.Scatter(
            x=xd, y=yv, name="P/S Ratio",
            mode="lines+markers+text",
            text=[f"{v:.1f}x" for v in yv], textposition="top center",
            textfont=dict(size=8, color="#ff2d55"),
            line=dict(color="#ff2d55", width=2),
            marker=dict(size=8, color="#ff2d55")), row=3, col=1)
        for ref, lbl in [(5,"5x"),(10,"10x"),(20,"20x"),(40,"40x")]:
            fig.add_hline(y=ref, line=dict(color="#162040",width=1,dash="dot"),
                          annotation_text=lbl,
                          annotation_font=dict(color="#3a5070",size=8), row=3, col=1)

    # ── Panel 4: Revenue Growth % bars ──
    if d["rev_g"]:
        ky = sorted(d["rev_g"].keys())
        xd = [yr_to_dt(y) for y in ky]; yv = [d["rev_g"][y] for y in ky]
        colors = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in yv]
        fig.add_trace(go.Bar(
            x=xd, y=yv, name="Rev Grw %", marker_color=colors,
            text=[f"{v:.1f}%" for v in yv], textposition="outside",
            textfont=dict(size=8, family="IBM Plex Mono", color="#b8cce0")), row=4, col=1)
        fig.add_hline(y=0, line=dict(color="#3a5070",width=1), row=4, col=1)

    # ── Panel 5: EPS Growth % bars ──
    if d["eps_g"]:
        ky = sorted(d["eps_g"].keys())
        xd = [yr_to_dt(y) for y in ky]; yv = [d["eps_g"][y] for y in ky]
        colors = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in yv]
        fig.add_trace(go.Bar(
            x=xd, y=yv, name="EPS Grw %", marker_color=colors,
            text=[f"{v:.1f}%" for v in yv], textposition="outside",
            textfont=dict(size=8, family="IBM Plex Mono", color="#b8cce0")), row=5, col=1)
        fig.add_hline(y=0, line=dict(color="#3a5070",width=1), row=5, col=1)

    fig.update_layout(
        paper_bgcolor="#03070f", plot_bgcolor="#070d1a",
        font=dict(family="IBM Plex Mono", color="#b8cce0", size=10),
        height=1100, margin=dict(l=8,r=8,t=60,b=8),
        legend=dict(orientation="h",y=1.03,bgcolor="rgba(0,0,0,0)",x=0),
        hovermode="x unified",
    )
    fig.update_annotations(font=dict(color="#3a5070",size=10,family="IBM Plex Mono"))
    for r in range(1,6):
        fig.update_xaxes(gridcolor="#162040",showgrid=True,zeroline=False,row=r,col=1)
        fig.update_yaxes(gridcolor="#162040",showgrid=True,zeroline=True,zerolinecolor="#3a5070",row=r,col=1)
    try:
        fig.update_yaxes(title_text="Price $",  row=1, col=1)
        fig.update_yaxes(title_text="P/E",      row=2, col=1)
        fig.update_yaxes(title_text="P/S",      row=3, col=1)
        fig.update_yaxes(title_text="Rev Grw%", row=4, col=1)
        fig.update_yaxes(title_text="EPS Grw%", row=5, col=1)
    except Exception:
        pass
    return fig


def fig_valuation_score_card(ticker):
    """Hedge-fund style multi-metric valuation score card chart."""
    info = get_info(ticker)
    p, chg, _ = get_price(ticker)

    metrics = {}
    pe  = info.get("trailingPE");        ps  = info.get("priceToSalesTrailing12Months")
    fpe = info.get("forwardPE");         pb  = info.get("priceToBook")
    rg  = info.get("revenueGrowth");     eg  = info.get("earningsGrowth")
    roe = info.get("returnOnEquity");    fcf = info.get("freeCashflow")
    rev = info.get("totalRevenue") or 1; mc  = info.get("marketCap") or 0
    # Score each metric 0-100
    def norm(val, lo, hi, invert=False):
        if val is None: return 50
        try:
            val = float(val); s = (val - lo) / (hi - lo) * 100
            s = max(0, min(100, s))
            return 100 - s if invert else s
        except Exception: return 50
    scores = {
        "Rev Growth":   norm((rg or 0)*100, -10, 60),
        "EPS Growth":   norm((eg or 0)*100, -20, 80),
        "FCF Positive": 90 if (fcf or 0)>0 else 20,
        "ROE":          norm((roe or 0)*100, -5, 35),
        "P/E Value":    norm(pe or 999, 120, 10, invert=True),
        "P/S Value":    norm(ps or 999, 60, 5,  invert=True),
        "Fwd P/E":      norm(fpe or 999, 80, 10, invert=True),
    }
    cats = list(scores.keys()); vals = list(scores.values())
    colors = ["#00ff9d" if v>=70 else "#ffb800" if v>=40 else "#ff2d55" for v in vals]

    fig = go.Figure(go.Bar(
        x=vals, y=cats, orientation="h",
        marker_color=colors,
        text=[f"{v:.0f}/100" for v in vals], textposition="outside",
        textfont=dict(size=10, family="IBM Plex Mono", color="#b8cce0"),
    ))
    fig.add_vline(x=70, line=dict(color="#00ff9d",width=1,dash="dash"))
    fig.add_vline(x=40, line=dict(color="#ffb800",width=1,dash="dash"))
    fig.update_layout(**base_layout(f"{ticker} — INSTITUTIONAL VALUATION SCORECARD", 380))
    fig.update_xaxes(gridcolor="#162040", range=[0, 130])
    fig.update_yaxes(gridcolor="#162040")
    return fig, scores


def fig_ranking(df):
    df = df.sort_values("Score", ascending=True).tail(25)
    colors = ["#00ff9d" if s>=70 else "#ffb800" if s>=50 else "#ff2d55" for s in df["Score"]]
    fig = go.Figure(go.Bar(
        x=df["Score"], y=df["Ticker"], orientation="h", marker_color=colors,
        text=[f"{s:.0f}" for s in df["Score"]], textposition="outside",
        textfont=dict(color="#b8cce0", size=10, family="IBM Plex Mono"),
    ))
    fig.update_layout(**base_layout("📊 LIVE STB RANKING SCORES", 520))
    fig.update_xaxes(gridcolor="#162040", range=[0, 115])
    fig.update_yaxes(gridcolor="#162040")
    return fig


def fig_sector(data):
    colors = ["#00ff9d" if v>0 else "#ff2d55" for v in data.values()]
    fig = go.Figure(go.Bar(
        x=list(data.keys()), y=list(data.values()), marker_color=colors,
        text=[f"{v:+.2f}%" for v in data.values()], textposition="outside",
        textfont=dict(color="#b8cce0", size=10, family="IBM Plex Mono"),
    ))
    fig.update_layout(**base_layout("🏭 SECTOR PERFORMANCE (ETF)", 300))
    fig.update_xaxes(gridcolor="#162040")
    fig.update_yaxes(gridcolor="#162040", zeroline=True, zerolinecolor="#3a5070")
    return fig


def fig_correlation(tickers):
    rets = {}
    for t in tickers:
        h = get_hist(t, "1y")
        if not h.empty and len(h) > 20:
            rets[t] = h["Close"].pct_change().dropna()
    if len(rets) < 3: return go.Figure()
    df   = pd.DataFrame(rets).dropna()
    corr = df.corr()
    fig  = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns, y=corr.index,
        colorscale=[[0,"#ff2d55"],[0.5,"#070d1a"],[1,"#00ff9d"]],
        text=[[f"{v:.2f}" for v in row] for row in corr.values],
        texttemplate="%{text}", textfont=dict(size=9, family="IBM Plex Mono"),
        zmin=-1, zmax=1,
    ))
    fig.update_layout(**base_layout("🔗 1Y RETURN CORRELATION MATRIX", 480))
    fig.update_xaxes(gridcolor="#162040"); fig.update_yaxes(gridcolor="#162040")
    return fig


def fig_pnl():
    pnls = []
    for r in BONUS:
        p, _, _ = get_price(r["ticker"])
        if p and r["buy"]:
            pnls.append((r["ticker"], (p - r["buy"]) / r["buy"] * 100))
        else:
            pnls.append((r["ticker"], 0.0))
    colors = ["#00ff9d" if v >= 0 else "#ff2d55" for _, v in pnls]
    fig = go.Figure(go.Bar(
        x=[t for t,_ in pnls], y=[v for _,v in pnls], marker_color=colors,
        text=[f"{v:+.1f}%" for _,v in pnls], textposition="outside",
        textfont=dict(color="#b8cce0", size=11, family="IBM Plex Mono"),
    ))
    fig.update_layout(**base_layout("💰 BONUS PORTFOLIO  P&L %", 320))
    fig.update_xaxes(gridcolor="#162040")
    fig.update_yaxes(gridcolor="#162040", zeroline=True, zerolinecolor="#3a5070")
    return fig


def fig_waterfall(ticker):
    inc,_,_,_ = get_all_financials(ticker)
    rr = safe_row(inc, "Total Revenue","Revenue")
    if rr is None: return go.Figure()
    s    = rr.sort_index()
    vals = [float(v)/1e9 for v in s.values]
    yrs  = [str(d.year) for d in s.index]
    fig  = go.Figure(go.Waterfall(
        x=yrs, y=vals,
        measure=["absolute"] + ["relative"]*(len(vals)-1),
        increasing=dict(marker_color="#00ff9d"),
        decreasing=dict(marker_color="#ff2d55"),
        totals=dict(marker_color="#00e5ff"),
        connector=dict(line=dict(color="#162040", width=1)),
        text=[f"${v:.1f}B" for v in vals],
        textfont=dict(family="IBM Plex Mono", size=10, color="#b8cce0"),
    ))
    fig.update_layout(**base_layout(f"{ticker}  REVENUE WATERFALL ($B)", 360))
    fig.update_xaxes(gridcolor="#162040", type="category")
    fig.update_yaxes(gridcolor="#162040", zeroline=True, zerolinecolor="#3a5070")
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# ████████████████████████  MAIN APP  ████████████████████████
# ─────────────────────────────────────────────────────────────────────────────
def main():
    if not st.session_state.startup_done:
        startup_audit()

    now = datetime.now()
    mkt = now.weekday() < 5 and 9 <= now.hour < 16
    mkt_html = '<span style="color:#00ff9d">● LIVE</span>' if mkt else '<span style="color:#3a5070">● CLOSED</span>'

    # ── HEADER ──
    st.markdown(f"""
    <div class="hf-hdr">
      <div>
        <div class="hf-logo">📊 PYKUPZ ANALYTICS TERMINAL</div>
        <div class="hf-sub">MARKET INTELLIGENCE · {len(MASTER_UNIVERSE)} TICKERS · 7-ALGO AUDIT · LIVE DATA · NOT FINANCIAL ADVICE</div>
      </div>
      <div style="text-align:right">
        <div class="hf-clock">{now.strftime("%H:%M:%S")}</div>
        <div class="hf-stat">
          {mkt_html} &nbsp;|&nbsp; {now.strftime("%a %d %b %Y")}
          &nbsp;|&nbsp; REFRESH #{refresh_count}
          &nbsp;|&nbsp; AUDITED: {len(st.session_state.audit_cache)} TICKERS
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── INDEX BAR ──
    idx_html = '<div class="idx">'
    for name, sym in INDICES.items():
        p, chg, _ = get_price(sym)
        if p:
            cls = "up" if (chg or 0)>0 else "down" if (chg or 0)<0 else "flat"
            arr = "▲" if (chg or 0)>0 else "▼"
            idx_html += (f'<div class="idx-i"><div class="idx-n">{name}</div>'
                         f'<span style="color:#e8f2ff">{p:,.2f}</span> '
                         f'<span class="{cls}">{arr}{abs((chg or 0)*100):.2f}%</span></div>')
    idx_html += "</div>"
    st.markdown(idx_html, unsafe_allow_html=True)

    # ── TICKER TAPE (show all tickers) ──
    tape = ""
    for t in MASTER_UNIVERSE:
        p, chg, _ = get_price(t)
        if p and chg is not None:
            cls = "tu" if chg>0 else "td" if chg<0 else "tf"
            arr = "▲" if chg>0 else "▼"
            tape += f'<span class="{cls}">{t} ${p:.2f} {arr}{abs(chg*100):.2f}%</span>'
    if tape:
        st.markdown(f'<div class="tape"><div class="tape-inner">{tape*2}</div></div>',
                    unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # TABS  — every widget has a unique key= to prevent DuplicateElementId
    # ══════════════════════════════════════════════════════════════
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏆  RANKINGS",
        "📈  FINANCIAL CHARTS",
        "🔬  AUDIT ENGINE",
        "💰  PORTFOLIO",
        "🌐  MARKET PULSE",
        "🧠  DEEP INSIGHTS",
        "⚙️  COMMAND CENTER",
    ])

    # ══════════ TAB 1 — LIVE RANKINGS ══════════
    with tab1:
        st.markdown('<div class="sh">🏆 LIVE STB RANKINGS — AUTO-COMPUTED EVERY 60s</div>', unsafe_allow_html=True)
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1: uni  = st.radio("Universe",["Q1 2026","STB Core","Master All"],
                                   horizontal=True,label_visibility="collapsed",key="rank_uni")
        with fc2: topn = st.slider("Top N",10,len(MASTER_UNIVERSE),30,label_visibility="collapsed",key="rank_topn")
        with fc3: srt  = st.selectbox("Sort",["Score","Change %","Market Cap","P/E","P/S"],
                                        label_visibility="collapsed",key="rank_sort")
        with fc4: sig_f = st.selectbox("Signal Filter",["All","STRONG BUY","BUY","HOLD","WATCH"],
                                        label_visibility="collapsed",key="rank_sig_filter")

        universe = Q1_2026 if uni=="Q1 2026" else STB_ALL if uni=="STB Core" else MASTER_UNIVERSE
        rows = []
        with st.spinner(f"⚡ Computing live scores for {len(universe[:topn])} tickers..."):
            for tk in universe[:topn]:
                p, chg, _ = get_price(tk)
                info = get_info(tk)
                sc   = rank_score(info)
                sig  = signal(sc, chg)
                au   = st.session_state.audit_cache.get(tk, {})
                rows.append({
                    "Ticker":    tk,
                    "Name":      TICKER_META.get(tk, tk).split("·")[0].strip(),
                    "Price":     f"${p:.2f}" if p else "—",
                    "Change %":  round((chg or 0)*100, 2),
                    "Score":     sc,
                    "Signal":    sig,
                    "P/E":       round(float(info["trailingPE"]), 1) if info.get("trailingPE") else float("nan"),
                    "P/S":       round(float(info["priceToSalesTrailing12Months"]), 2) if info.get("priceToSalesTrailing12Months") else float("nan"),
                    "Fwd P/E":   round(float(info["forwardPE"]), 1) if info.get("forwardPE") else float("nan"),
                    "Market Cap":fmt_mcap(info.get("marketCap")),
                    "Rev Grw":   fmt_pct(info.get("revenueGrowth")),
                    "EPS Grw":   fmt_pct(info.get("earningsGrowth")),
                    "Sector":    TICKER_META.get(tk,"").split("·")[-1].strip() if "·" in TICKER_META.get(tk,"") else "—",
                    "Audit":     int(au.get("score", 0)) if au and isinstance(au.get("score"), (int, float)) else float("nan"),
                })

        df = pd.DataFrame(rows)
        if sig_f != "All":
            sig_clean = sig_f
            df = df[df["Signal"].str.contains(sig_clean, na=False)]
        if srt=="Score":      df = df.sort_values("Score",ascending=False)
        elif srt=="Change %": df = df.sort_values("Change %",ascending=False)
        elif srt=="P/E":      df = df.sort_values("P/E",ascending=True, na_position="last")
        elif srt=="P/S":      df = df.sort_values("P/S",ascending=True, na_position="last")
        df = df.reset_index(drop=True); df.index += 1

        st.dataframe(df, use_container_width=True, height=580,
            column_config={
                "Score":    st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%.0f"),
                "Change %": st.column_config.NumberColumn("Chg %",format="%.2f%%"),
                "Audit":    st.column_config.NumberColumn("Audit",format="%d"),
                "P/E":      st.column_config.NumberColumn("P/E",format="%.1f"),
                "P/S":      st.column_config.NumberColumn("P/S",format="%.2f"),
                "Fwd P/E":  st.column_config.NumberColumn("Fwd P/E",format="%.1f"),
            })

        dfc = df[["Ticker","Score"]].copy()
        dfc["Score"] = pd.to_numeric(dfc["Score"],errors="coerce").fillna(0)
        st.plotly_chart(fig_ranking(dfc), use_container_width=True)

    # ══════════ TAB 2 — FINANCIAL CHARTS ══════════
    with tab2:
        st.markdown(
            '<div class="sh">📈 FINANCIAL CHARTS — PE · PS · REVENUE · EPS GROWTH vs STOCK PRICE</div>',
            unsafe_allow_html=True)

        all_t = MASTER_UNIVERSE
        c1, c2 = st.columns([2, 1])
        with c1:
            # KEY FIX: unique key= avoids StreamlitDuplicateElementId
            ct = st.selectbox("Select ticker", all_t,
                               label_visibility="collapsed", key="fin_ticker_sel")
        with c2:
            vmode = st.selectbox("Chart View", [
                "📊 Price vs PE · PS · Rev Grw · EPS Grw  (OVERLAY)",
                "💹 Full Financial Analysis (4-Panel)",
                "📈 Candlestick + Bollinger",
                "📉 Revenue Waterfall",
                "🏆 Valuation Score Card",
                "🔗 Correlation Matrix",
            ], label_visibility="collapsed", key="fin_view_sel")

        # Snapshot bar
        info = get_info(ct); p, chg, _ = get_price(ct)
        scols = st.columns(8)
        snaps = [
            ("PRICE",    f"${p:.2f}" if p else "—",      "gn" if (chg or 0)>0 else "rd"),
            ("24H CHG",  fmt_pct(chg,False),              "gn" if (chg or 0)>0 else "rd"),
            ("P/E",      f"{info.get('trailingPE',0):.1f}" if info.get('trailingPE') else "—",""),
            ("FWD P/E",  f"{info.get('forwardPE',0):.1f}" if info.get('forwardPE') else "—",""),
            ("P/S",      f"{info.get('priceToSalesTrailing12Months',0):.2f}" if info.get('priceToSalesTrailing12Months') else "—",""),
            ("MCAP",     fmt_mcap(info.get("marketCap")),""),
            ("REV GRW",  fmt_pct(info.get("revenueGrowth")), "gn" if (info.get("revenueGrowth") or 0)>0 else "rd"),
            ("EPS",      f"${info.get('trailingEps',0):.2f}" if info.get('trailingEps') else "—",""),
        ]
        for col, (lbl, val, card_cls) in zip(scols, snaps):
            col.markdown(
                f'<div class="card {card_cls}" style="padding:8px 10px;">'
                f'<div class="cv" style="font-size:14px;">{val}</div>'
                f'<div class="cl">{lbl}</div></div>',
                unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        if "OVERLAY" in vmode:
            st.markdown(
                '<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#3a5070;margin-bottom:8px;">'
                'Panel 1: Daily stock price (continuous line) + annual year-end price markers &nbsp;|&nbsp; '
                'Panel 2: P/E ratio per year &nbsp;|&nbsp; Panel 3: P/S ratio per year &nbsp;|&nbsp; '
                'Panel 4: Revenue Growth % YoY &nbsp;|&nbsp; Panel 5: EPS Growth % YoY — '
                'all on SHARED X-AXIS so you can see how price tracked each metric</div>',
                unsafe_allow_html=True)
            with st.spinner(f"⚡ Loading overlay chart for {ct}..."):
                st.plotly_chart(fig_overlay_price_vs_metrics(ct), use_container_width=True)

        elif "Full Financial" in vmode:
            st.markdown(
                '<div style="font-family:IBM Plex Mono,monospace;font-size:10px;color:#3a5070;margin-bottom:6px;">'
                'Panel 1: Revenue · EBITDA · FCF ($B) + Year-End Price &nbsp;|&nbsp; '
                'Panel 2: P/E & P/S &nbsp;|&nbsp; Panel 3: EPS + EPS Growth &nbsp;|&nbsp; Panel 4: Revenue Growth %</div>',
                unsafe_allow_html=True)
            with st.spinner(f"⚡ Loading financials for {ct}..."):
                st.plotly_chart(fig_financial_lines(ct), use_container_width=True)

            # Raw tables
            inc2, cf2, _, _ = get_all_financials(ct)
            if inc2 is not None and not inc2.empty:
                with st.expander("📋 Raw Annual Financials"):
                    want  = ["Total Revenue","Gross Profit","EBITDA","Operating Income",
                             "Net Income","Diluted EPS","Reconciled Depreciation"]
                    avail = [r for r in want if r in inc2.index]
                    if avail:
                        def fmt_cell(x):
                            if pd.isna(x): return "—"
                            try:
                                f = float(x)
                                if abs(f)>=1e9: return f"${f/1e9:.2f}B"
                                if abs(f)>=1e6: return f"${f/1e6:.1f}M"
                                return f"{f:.3f}"
                            except Exception: return str(x)
                        df_raw = inc2.loc[avail].copy().applymap(fmt_cell)
                        df_raw.columns = [str(c.year) if hasattr(c,"year") else str(c) for c in df_raw.columns]
                        st.dataframe(df_raw, use_container_width=True)
                with st.expander("💹 Cash Flow Statement"):
                    if cf2 is not None and not cf2.empty:
                        cf_want  = ["Operating Cash Flow","Free Cash Flow","Capital Expenditure",
                                    "Repurchase Of Capital Stock","Cash Dividends Paid"]
                        cf_avail = [r for r in cf_want if r in cf2.index]
                        if cf_avail:
                            df_cf = cf2.loc[cf_avail].applymap(
                                lambda x: f"${float(x)/1e9:.2f}B" if pd.notna(x) else "—")
                            df_cf.columns = [str(c.year) if hasattr(c,"year") else str(c) for c in df_cf.columns]
                            st.dataframe(df_cf, use_container_width=True)

        elif "Candlestick" in vmode:
            cp = st.select_slider("Period",["1mo","3mo","6mo","1y","2y","5y","max"],
                                   value="1y", label_visibility="collapsed", key="fin_period_sel")
            st.plotly_chart(fig_candlestick(ct, cp), use_container_width=True)

        elif "Waterfall" in vmode:
            st.plotly_chart(fig_waterfall(ct), use_container_width=True)

        elif "Score Card" in vmode:
            with st.spinner(f"⚡ Building scorecard for {ct}..."):
                fig_sc, scores = fig_valuation_score_card(ct)
            st.plotly_chart(fig_sc, use_container_width=True)
            overall = sum(scores.values()) / len(scores)
            col_v = "#00ff9d" if overall>=70 else "#ffb800" if overall>=45 else "#ff2d55"
            st.markdown(f"""
            <div class="ab" style="margin-top:8px;border-color:{col_v};">
              <div style="font-family:Bebas Neue,monospace;font-size:18px;color:{col_v};margin-bottom:6px;">
                INSTITUTIONAL VALUATION SCORE: {overall:.0f}/100</div>
              <div style="font-size:10px;color:#3a5070;font-family:IBM Plex Mono,monospace;">
              Scoring methodology: Rev Growth (30pt) · EPS Growth (20pt) · FCF (10pt) ·
              Net Debt (10pt) · P/E attractiveness (15pt) · P/S attractiveness (15pt)</div>
            </div>""", unsafe_allow_html=True)

        elif "Correlation" in vmode:
            sel = st.multiselect("Select tickers", all_t, default=Q1_2026[:14],
                                  label_visibility="collapsed", key="fin_corr_sel")
            if sel:
                with st.spinner("Computing correlations..."):
                    st.plotly_chart(fig_correlation(sel), use_container_width=True)

    # ══════════ TAB 3 — AUDIT ENGINE ══════════
    with tab3:
        st.markdown('<div class="sh">🔬 7-ALGORITHM AUDIT ENGINE — AUTO-RUN ON STARTUP</div>', unsafe_allow_html=True)
        al, ar = st.columns([1, 2])

        with al:
            # KEY FIX: unique key= — was clashing with tab2's "Ticker" selectbox
            audit_t = st.selectbox("Select ticker to audit",
                                    MASTER_UNIVERSE,
                                    label_visibility="collapsed", key="aud_ticker_sel")
            run_b   = st.button("⚡ RUN FULL AUDIT",      use_container_width=True, key="aud_run_btn")
            batch_b = st.button("🔄 BATCH AUDIT TOP 15",  use_container_width=True, key="aud_batch_btn")

            if batch_b:
                _ph = st.empty()
                with _ph.container():
                    prog = st.progress(0, text="Starting batch audit...")
                    for i, t in enumerate(MASTER_UNIVERSE[:20]):
                        try:
                            res = run_audit(t)
                            st.session_state.audit_cache[t] = res
                            st.session_state.audit_log.append(res)
                        except Exception:
                            pass
                        prog.progress((i+1)/20, text=f"Auditing {t}... ({i+1}/20)")
                    st.session_state.last_run = datetime.now().strftime("%H:%M:%S")
                _ph.empty()
                st.success("✅ Batch audit complete — 20 tickers")

            if run_b:
                with st.spinner(f"Running 7 algorithms on {audit_t}..."):
                    res = run_audit(audit_t)
                    st.session_state.audit_cache[audit_t] = res
                    st.session_state.audit_log.append(res)
                    st.session_state.last_run = datetime.now().strftime("%H:%M:%S")

            if audit_t in st.session_state.audit_cache:
                res   = st.session_state.audit_cache[audit_t]
                score = res.get("score", 0)
                pr    = res.get("price") or 0
                chg_a = res.get("change") or 0
                col   = "#00ff9d" if score>=80 else "#ffb800" if score>=60 else "#ff2d55"
                cclr  = "#00ff9d" if chg_a>=0 else "#ff2d55"
                st.markdown(f"""
                <div style="background:#0b1220;border:1px solid {col};border-radius:8px;padding:14px;margin-top:10px;">
                  <div style="font-family:Bebas Neue,monospace;font-size:26px;color:{col};">{audit_t}</div>
                  <div style="font-family:IBM Plex Mono,monospace;font-size:15px;color:#e8f2ff;">
                    ${pr:.2f} <span style="color:{cclr}">{chg_a*100:+.2f}%</span></div>
                  <div style="font-size:9px;color:#3a5070;letter-spacing:2px;margin-top:8px;">AUDIT SCORE</div>
                  <div style="font-family:Bebas Neue,monospace;font-size:48px;color:{col};line-height:1;">
                    {score}<span style="font-size:16px;color:#3a5070">/100</span></div>
                  <div style="font-size:9px;color:#3a5070;margin-top:2px;">Updated: {res.get('ts','—')}</div>
                </div>
                """, unsafe_allow_html=True)

        with ar:
            if audit_t in st.session_state.audit_cache:
                res = st.session_state.audit_cache[audit_t]
                algo_rows = [
                    ("A1 · Multi-Source Reconciliation",   res["A1"].get("status","—")),
                    ("A2 · Statistical Anomaly (z-score)", res["A2"].get("status","—")),
                    ("A3 · Cash-Flow Logic Chain",          res["A3"].get("status","—")),
                    ("A4 · Data Freshness Score",           f"{res['A4'].get('status','—')} ({res['A4'].get('score','—')}%)"),
                    ("A5 · Historical Trend Validation",    f"{res['A5'].get('status','—')} | CAGR={res['A5'].get('cagr','—')}%"),
                    ("A6 · Guidance Back-Test",              res["A6"].get("status","—")),
                    ("A7 · Hypothesis & Valuation Audit",   res["A7"].get("overall","—")),
                ]
                html = '<div class="ab">'
                for nm, st_txt in algo_rows:
                    ok   = "✅" in st_txt
                    warn = "⚠️" in st_txt or "📉" in st_txt
                    clr  = "#00ff9d" if ok else "#ffb800" if warn else "#ff2d55" if "🚨" in st_txt else "#3a5070"
                    html += (f'<div class="ar"><span class="an">{nm}</span>'
                             f'<span style="color:{clr}">{st_txt}</span></div>')
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

                q = res["A6"].get("q",[])
                if q:
                    with st.expander("📋 EPS Beat/Miss History"):
                        st.dataframe(pd.DataFrame(q), use_container_width=True, height=200)

                ch = res["A7"].get("checks",[])
                if ch:
                    with st.expander("🏆 Hypothesis Checks"):
                        for c in ch:
                            clr = "#00ff9d" if "✅" in c["status"] else "#ffb800"
                            st.markdown(
                                f'<div class="ar"><span class="an">{c["name"]}</span>'
                                f'<span>Fair: <b>${c["fair"]}</b> · Live: <b>${c["live"]}</b> · '
                                f'<b style="color:{clr}">{c["dev"]:+.1f}%</b> → {c["status"]}</span></div>',
                                unsafe_allow_html=True)

        if st.session_state.audit_log:
            st.markdown('<div class="sh" style="margin-top:14px;">📋 AUDIT LOG</div>', unsafe_allow_html=True)
            log_rows = []
            for a in reversed(st.session_state.audit_log[-30:]):
                log_rows.append({
                    "Time":a.get("ts",""),"Ticker":a.get("ticker",""),"Score":a.get("score",0),
                    "Price":f"${a.get('price',0):.2f}" if a.get("price") else "—",
                    "A1":a["A1"].get("status","")[:16],"A2":a["A2"].get("status","")[:16],
                    "A3":a["A3"].get("status","")[:16],"A4":a["A4"].get("status","")[:12],
                    "A5":a["A5"].get("status","")[:16],"A6":a["A6"].get("status","")[:18],
                })
            st.dataframe(pd.DataFrame(log_rows), use_container_width=True, height=260,
                column_config={"Score":st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%d")})

    # ══════════ TAB 4 — PORTFOLIO ══════════
    with tab4:
        st.markdown('<div class="sh">💰 BONUS PORTFOLIO — LIVE P&L</div>', unsafe_allow_html=True)
        rows=[]; total_inv=total_curr=0

        for r in BONUS:
            p, chg, _ = get_price(r["ticker"])
            if not p: p = r["buy"]
            pct  = (p - r["buy"]) / r["buy"] * 100 if r["buy"] else 0
            curr = p * r["qty"]; inv = r["buy"] * r["qty"]
            total_inv += inv; total_curr += curr
            rows.append({
                "Ticker":r["ticker"],"Name":r["name"],
                "Buy":f"${r['buy']:.2f}","Live":f"${p:.2f}","Qty":r["qty"],
                "P&L %":pct,"P&L $":curr-inv,"Value $":curr,
                "24H %":(chg or 0)*100,"Status":"🟢" if pct>0 else "🔴",
            })

        tp = total_curr - total_inv
        tp_pct = tp / total_inv * 100 if total_inv else 0
        pc1,pc2,pc3,pc4 = st.columns(4)
        pc1.markdown(f'<div class="card"><div class="cv">${total_inv:,.0f}</div><div class="cl">INVESTED</div></div>', unsafe_allow_html=True)
        pc2.markdown(f'<div class="card"><div class="cv">${total_curr:,.0f}</div><div class="cl">CURRENT VALUE</div></div>', unsafe_allow_html=True)
        pnl_cls = "gn" if tp >= 0 else "rd"
        pv_cls  = "up"  if tp >= 0 else "down"
        pc3.markdown(f'<div class="card {pnl_cls}"><div class="cv {pv_cls}">${tp:+,.0f}</div><div class="cl">TOTAL P&L $</div></div>', unsafe_allow_html=True)
        pc4.markdown(f'<div class="card {pnl_cls}"><div class="cv {pv_cls}">{tp_pct:+.1f}%</div><div class="cl">TOTAL RETURN</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=340,
            column_config={
                "P&L %":  st.column_config.NumberColumn("P&L %",  format="%.2f%%"),
                "P&L $":  st.column_config.NumberColumn("P&L $",  format="$%.2f"),
                "Value $":st.column_config.NumberColumn("Value $", format="$%.2f"),
                "24H %":  st.column_config.NumberColumn("24H %",  format="%.2f%%"),
            })
        st.plotly_chart(fig_pnl(), use_container_width=True)

    # ══════════ TAB 5 — MARKET PULSE ══════════
    with tab5:
        st.markdown('<div class="sh">🌐 MARKET PULSE — SECTORS · INDICES · EARNINGS</div>', unsafe_allow_html=True)

        sec_data = {}
        with st.spinner("Fetching sector ETFs..."):
            for name, sym in SECTORS.items():
                _, chg, _ = get_price(sym)
                if chg is not None: sec_data[name] = chg * 100
        if sec_data:
            st.plotly_chart(fig_sector(sec_data), use_container_width=True)

        st.markdown('<div class="sh" style="margin-top:4px;">📊 GLOBAL INDICES</div>', unsafe_allow_html=True)
        icols = st.columns(4)
        for i, (name, sym) in enumerate(INDICES.items()):
            p, chg, _ = get_price(sym)
            if p:
                cls = "gn" if (chg or 0)>0 else "rd" if (chg or 0)<0 else ""
                cc  = "up" if (chg or 0)>0 else "down"
                icols[i%4].markdown(
                    f'<div class="card {cls}" style="margin-bottom:7px;">'
                    f'<div class="cv" style="font-size:16px;">{p:,.2f}</div>'
                    f'<div class="cl">{name}</div>'
                    f'<div class="cc {cc}">{fmt_pct(chg,False)}</div></div>',
                    unsafe_allow_html=True)

        st.markdown('<div class="sh" style="margin-top:8px;">📅 UPCOMING EARNINGS (30 DAYS)</div>', unsafe_allow_html=True)
        earns = []
        with st.spinner("Scanning earnings dates across full universe..."):
            for t in MASTER_UNIVERSE[:50]:
                try:
                    info2 = get_info(t)
                    ts    = info2.get("earningsTimestamp")
                    if ts:
                        dt   = datetime.fromtimestamp(ts)
                        diff = (dt - datetime.now()).days
                        if 0 <= diff <= 30:
                            earns.append({"Ticker":t,"Date":dt.strftime("%Y-%m-%d"),
                                          "Days Away":diff,
                                          "Company":info2.get("shortName",""),
                                          "Sector": TICKER_META.get(t,"").split("·")[-1].strip()})
                except Exception:
                    pass
        if earns:
            st.dataframe(pd.DataFrame(earns).sort_values("Days Away"), use_container_width=True, height=300)
        else:
            st.info("No earnings within 30 days for tracked tickers.")

    # ══════════ TAB 6 — DEEP INSIGHTS ══════════
    with tab6:
        st.markdown('<div class="sh">🧠 DEEP INSIGHTS — COMPARATIVE ANALYSIS & INTELLIGENCE</div>', unsafe_allow_html=True)

        ins1, ins2 = st.columns([1, 1])

        with ins1:
            st.markdown("**📊 SIDE-BY-SIDE TICKER COMPARISON**")
            cmp_tickers = st.multiselect(
                "Compare up to 6 tickers",
                MASTER_UNIVERSE,
                default=["NVDA","META","AMZN","MSFT","GOOG","AAPL"],
                max_selections=6,
                key="ins_compare_sel",
                label_visibility="collapsed",
            )
            if cmp_tickers:
                cmp_rows = []
                for tk in cmp_tickers:
                    p, chg, _ = get_price(tk)
                    info = get_info(tk)
                    cmp_rows.append({
                        "Ticker":    tk,
                        "Price":     f"${p:.2f}" if p else "—",
                        "Chg %":     round((chg or 0)*100, 2),
                        "Score":     rank_score(info),
                        "MCap":      fmt_mcap(info.get("marketCap")),
                        "P/E":       round(float(info["trailingPE"]),1) if info.get("trailingPE") else float("nan"),
                        "Fwd P/E":   round(float(info["forwardPE"]),1) if info.get("forwardPE") else float("nan"),
                        "P/S":       round(float(info["priceToSalesTrailing12Months"]),2) if info.get("priceToSalesTrailing12Months") else float("nan"),
                        "P/B":       round(float(info["priceToBook"]),2) if info.get("priceToBook") else float("nan"),
                        "Rev Grw":   fmt_pct(info.get("revenueGrowth")),
                        "EPS Grw":   fmt_pct(info.get("earningsGrowth")),
                        "Gross Mgn": fmt_pct(info.get("grossMargins")),
                        "Op Mgn":    fmt_pct(info.get("operatingMargins")),
                        "Net Mgn":   fmt_pct(info.get("profitMargins")),
                        "ROE":       fmt_pct(info.get("returnOnEquity")),
                        "Debt/Eq":   round(float(info["debtToEquity"])/100,2) if info.get("debtToEquity") else float("nan"),
                        "FCF $B":    round(float(info["freeCashflow"])/1e9,1) if info.get("freeCashflow") else float("nan"),
                        "52W High":  f"${info.get('fiftyTwoWeekHigh',0):.2f}" if info.get("fiftyTwoWeekHigh") else "—",
                        "52W Low":   f"${info.get('fiftyTwoWeekLow',0):.2f}" if info.get("fiftyTwoWeekLow") else "—",
                        "Beta":      round(float(info["beta"]),2) if info.get("beta") else float("nan"),
                        "Signal":    signal(rank_score(info), chg),
                    })
                df_cmp = pd.DataFrame(cmp_rows).set_index("Ticker")
                st.dataframe(df_cmp.T, use_container_width=True, height=640)

                # Radar-style bar comparison on key metrics
                if len(cmp_tickers) >= 2:
                    fig_cmp = go.Figure()
                    metrics_to_plot = ["Score","P/E","P/S","Gross Mgn","Rev Grw","EPS Grw"]
                    colors_list = ["#00e5ff","#00ff9d","#ffb800","#ff2d55","#9d4edd","#ffffff"]
                    for tk, clr in zip(cmp_tickers, colors_list):
                        row = next((r for r in cmp_rows if r["Ticker"]==tk), {})
                        def safe_float(v):
                            try:
                                if isinstance(v, str):
                                    return float(v.replace("%","").replace("$","").replace(",","").replace("—","0"))
                                return float(v) if v == v else 0  # nan check
                            except:
                                return 0
                        vals_plot = [safe_float(row.get(m, 0)) for m in metrics_to_plot]
                        fig_cmp.add_trace(go.Bar(
                            name=tk, x=metrics_to_plot, y=vals_plot,
                            marker_color=clr, opacity=0.8,
                            text=[f"{v:.1f}" for v in vals_plot], textposition="outside",
                        ))
                    fig_cmp.update_layout(
                        paper_bgcolor="#03070f", plot_bgcolor="#070d1a",
                        font=dict(family="IBM Plex Mono", color="#b8cce0", size=10),
                        title=dict(text="COMPARATIVE KEY METRICS", font=dict(color="#00e5ff",size=13)),
                        height=380, barmode="group",
                        legend=dict(orientation="h", y=1.12, bgcolor="rgba(0,0,0,0)"),
                        margin=dict(l=8,r=8,t=60,b=8),
                    )
                    fig_cmp.update_xaxes(gridcolor="#162040")
                    fig_cmp.update_yaxes(gridcolor="#162040", zeroline=True, zerolinecolor="#3a5070")
                    st.plotly_chart(fig_cmp, use_container_width=True)

        with ins2:
            st.markdown("**⚡ SINGLE-TICKER DEEP DIVE**")
            dive_t = st.selectbox("Select ticker for deep dive", MASTER_UNIVERSE,
                                   key="ins_dive_sel", label_visibility="collapsed")
            if dive_t:
                with st.spinner(f"Loading deep data for {dive_t}..."):
                    p, chg, _ = get_price(dive_t)
                    info      = get_info(dive_t)
                    sc        = rank_score(info)
                    sig_v     = signal(sc, chg)
                    inc, cf, bal, hist = get_all_financials(dive_t)

                score_color = "#00ff9d" if sc>=70 else "#ffb800" if sc>=45 else "#ff2d55"

                st.markdown(f"""
                <div style="background:#0b1220;border:1px solid {score_color};border-radius:8px;padding:16px;margin-bottom:10px;">
                  <div style="font-family:Bebas Neue,monospace;font-size:28px;color:{score_color};">{dive_t}</div>
                  <div style="font-size:11px;color:#3a5070;font-family:IBM Plex Mono;">{TICKER_META.get(dive_t,"")}</div>
                  <div style="font-family:IBM Plex Mono;font-size:18px;color:#e8f2ff;margin-top:6px;">
                    ${p:.2f} <span style="color:{'#00ff9d' if (chg or 0)>=0 else '#ff2d55'}">{fmt_pct(chg,False)}</span>
                    &nbsp;&nbsp; SCORE: <span style="color:{score_color}">{sc:.0f}/100</span>
                    &nbsp;&nbsp; {sig_v}</div>
                </div>
                """, unsafe_allow_html=True)

                # Key metrics grid
                metrics_grid = [
                    ("Market Cap",    fmt_mcap(info.get("marketCap"))),
                    ("Enterprise Val",fmt_mcap(info.get("enterpriseValue"))),
                    ("Revenue TTM",   fmt_mcap(info.get("totalRevenue"))),
                    ("Gross Margin",  fmt_pct(info.get("grossMargins"))),
                    ("Op Margin",     fmt_pct(info.get("operatingMargins"))),
                    ("Net Margin",    fmt_pct(info.get("profitMargins"))),
                    ("ROE",           fmt_pct(info.get("returnOnEquity"))),
                    ("ROA",           fmt_pct(info.get("returnOnAssets"))),
                    ("FCF",           fmt_mcap(info.get("freeCashflow"))),
                    ("Total Debt",    fmt_mcap(info.get("totalDebt"))),
                    ("Cash",          fmt_mcap(info.get("totalCash"))),
                    ("Employees",     f"{info.get('fullTimeEmployees',0):,}" if info.get("fullTimeEmployees") else "—"),
                    ("52W High",      f"${info.get('fiftyTwoWeekHigh',0):.2f}" if info.get("fiftyTwoWeekHigh") else "—"),
                    ("52W Low",       f"${info.get('fiftyTwoWeekLow',0):.2f}" if info.get("fiftyTwoWeekLow") else "—"),
                    ("Beta",          f"{info.get('beta',0):.2f}" if info.get("beta") else "—"),
                    ("Div Yield",     fmt_pct(info.get("dividendYield"))),
                ]
                grid_html = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-bottom:10px;">'
                for lbl, val in metrics_grid:
                    grid_html += (f'<div class="ab" style="padding:6px 10px;">'
                                  f'<div class="cl">{lbl}</div>'
                                  f'<div style="font-family:IBM Plex Mono,monospace;font-size:13px;color:#e8f2ff;">{val}</div></div>')
                grid_html += '</div>'
                st.markdown(grid_html, unsafe_allow_html=True)

                # Analyst targets
                target = info.get("targetMeanPrice")
                if target and p:
                    upside = (target - p) / p * 100
                    t_clr = "#00ff9d" if upside > 0 else "#ff2d55"
                    st.markdown(f"""
                    <div class="ab" style="margin-bottom:8px;">
                      <div class="cl">ANALYST CONSENSUS TARGET</div>
                      <div style="font-family:IBM Plex Mono;font-size:16px;color:#e8f2ff;">
                        ${target:.2f} &nbsp;
                        <span style="color:{t_clr}">{upside:+.1f}% {'UPSIDE' if upside>0 else 'DOWNSIDE'}</span>
                      </div>
                      <div style="font-size:10px;color:#3a5070;margin-top:2px;">
                        Low: ${info.get('targetLowPrice',0):.2f} &nbsp;|&nbsp;
                        High: ${info.get('targetHighPrice',0):.2f} &nbsp;|&nbsp;
                        Rec: {info.get('recommendationKey','—').upper()}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                # Business summary
                summary = info.get("longBusinessSummary","")
                if summary:
                    with st.expander("📋 Business Overview"):
                        st.markdown(f'<div style="font-size:11px;color:#b8cce0;line-height:1.6;">{summary[:900]}{"..." if len(summary)>900 else ""}</div>',
                                    unsafe_allow_html=True)

    # ══════════ TAB 7 — COMMAND CENTER ══════════
    with tab7:
        st.markdown('<div class="sh">⚙️ COMMAND CENTER</div>', unsafe_allow_html=True)
        cc1, cc2 = st.columns([2, 3])

        with cc1:
            st.markdown("**⚡ INSTANT TICKER LOOKUP**")
            # KEY FIX: unique key= avoids clash with any other text_input
            lookup = st.text_input("Ticker lookup", placeholder="Any ticker: NVDA, TSLA, MSFT...",
                                    label_visibility="collapsed", key="cmd_lookup_input")
            if lookup:
                tk = lookup.strip().upper()
                p, chg, _ = get_price(tk)
                info = get_info(tk)
                if p:
                    cclr = "#00ff9d" if (chg or 0)>0 else "#ff2d55"
                    st.markdown(f"""
                    <div class="ab" style="margin-top:8px;">
                      <div style="font-family:Bebas Neue,monospace;font-size:26px;color:#00e5ff;">{tk}</div>
                      <div style="font-family:IBM Plex Mono,monospace;font-size:15px;color:#e8f2ff;">
                        ${p:.4f} <span style="color:{cclr}">{fmt_pct(chg,False)}</span></div>
                      <div style="font-size:11px;color:#3a5070;margin-top:6px;">
                        P/E: {info.get('trailingPE','—')} &nbsp;|&nbsp;
                        P/S: {info.get('priceToSalesTrailing12Months','—')} &nbsp;|&nbsp;
                        MCap: {fmt_mcap(info.get('marketCap'))}</div>
                      <div style="font-size:11px;color:#3a5070;">
                        Rev Growth: {fmt_pct(info.get('revenueGrowth'))} &nbsp;|&nbsp;
                        EPS: ${info.get('trailingEps','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"⚡ AUDIT {tk}", key=f"cmd_audit_{tk}"):
                        with st.spinner(f"Auditing {tk}..."):
                            res = run_audit(tk)
                            st.session_state.audit_cache[tk] = res
                            st.session_state.audit_log.append(res)
                        st.success(f"Score: {res['score']}/100")
                else:
                    st.warning(f"No data for {tk}")

            st.markdown("---")
            st.markdown("**📋 UNIVERSES**")
            vu = st.radio("Universe view",["Q1 2026","STB Core","Master All","Bonus"],
                           horizontal=True, label_visibility="collapsed", key="cmd_uni_radio")
            if vu=="Q1 2026":
                for t in Q1_2026:
                    meta = TICKER_META.get(t,"")
                    st.markdown(f"**{t}** — {meta}" if meta else f"**{t}**")
            elif vu=="STB Core":
                for t in STB_ALL:
                    meta = TICKER_META.get(t,"")
                    st.markdown(f"**{t}** — {meta}" if meta else f"**{t}**")
            elif vu=="Master All":
                cols = st.columns(3)
                for i, t in enumerate(MASTER_UNIVERSE):
                    meta = TICKER_META.get(t,"")
                    cols[i%3].markdown(f"**{t}** {meta.split('·')[-1].strip() if '·' in meta else ''}")
            else:
                for r in BONUS:
                    st.markdown(f"**{r['ticker']}** — {r['name']} @ ${r['buy']}")

        with cc2:
            st.markdown("**📥 EXPORT & STATS**")
            if st.session_state.audit_log:
                export_rows = [{
                    "Ticker":a.get("ticker",""),"Score":a.get("score",""),
                    "Price":a.get("price",""),"Time":a.get("ts",""),
                    "A1":a["A1"].get("status",""),"A2":a["A2"].get("status",""),
                    "A3":a["A3"].get("status",""),"A4":a["A4"].get("status",""),
                    "A5":a["A5"].get("status",""),"A6":a["A6"].get("status",""),
                    "A7":a["A7"].get("overall",""),
                } for a in st.session_state.audit_log]
                buf = BytesIO()
                pd.DataFrame(export_rows).to_excel(buf, index=False, engine="xlsxwriter")
                buf.seek(0)
                st.download_button("📥 DOWNLOAD AUDIT LOG (.xlsx)", buf,
                                    "pykupz_audit.xlsx", key="cmd_dl_btn")

            st.markdown(f"""
            ---
            - **Tickers in universe:** {len(MASTER_UNIVERSE)}
            - **Audits cached:** {len(st.session_state.audit_cache)}
            - **Log entries:** {len(st.session_state.audit_log)}
            - **Auto-refresh:** every 60s (refresh #{refresh_count})
            - **Last startup audit:** {st.session_state.last_run or "—"}
            - **Data source:** Yahoo Finance (yfinance) — 100% live
            - **Charts:** Overlay (Price/PE/PS/RevGrw/EPSGrw) · Full Financial · Candlestick · Waterfall · Scorecard · Correlation
            """)

    # ── FOOTER ──
    st.markdown(f"""
    <div style="text-align:center;font-family:IBM Plex Mono,monospace;font-size:9px;
    color:#162040;letter-spacing:3px;padding:10px 0 4px;border-top:1px solid #162040;margin-top:10px;">
      PYKUPZ ANALYTICS TERMINAL · MARKET INTELLIGENCE · {len(MASTER_UNIVERSE)} TICKERS · YAHOO FINANCE ·
      AUTO-REFRESH 60s · {now.strftime("%Y-%m-%d %H:%M:%S")} · NOT FINANCIAL ADVICE
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════════════════
# FIXES IN THIS VERSION:
#  1. StreamlitDuplicateElementId — ALL widgets now have unique key= parameters:
#       fin_ticker_sel, fin_view_sel, fin_period_sel, fin_corr_sel (tab2)
#       aud_ticker_sel, aud_run_btn, aud_batch_btn                 (tab3)
#       cmd_lookup_input, cmd_uni_radio, cmd_dl_btn                (tab6)
#       rank_uni, rank_topn, rank_sort                             (tab1)
#  2. New OVERLAY chart — stock price (daily continuous) shared x-axis with
#     P/E, P/S, Revenue Growth %, EPS Growth % in 5 stacked panels
#  3. New VALUATION SCORE CARD — institutional multi-metric radar
#  4. _extract_annual_series() — shared function avoids 5× duplicate data fetches
#
# HOW TO RUN:
#   pip install streamlit streamlit-autorefresh pandas plotly yfinance numpy scipy openpyxl xlsxwriter
#   streamlit run pykupz_terminal.py
# ═══════════════════════════════════════════════════════════════════════════════
