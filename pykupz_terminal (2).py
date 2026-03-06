"""
PYKUPZ LIVE TERMINAL — HEDGE FUND EDITION
Fully Automated · No Excel · 100% Live Internet Data · 7 Audit Algorithms
Auto-refresh every 60s · Auto-audit on startup · Auto-rankings

requirements.txt:
streamlit>=1.32.0
streamlit-autorefresh>=1.0.1
yfinance>=0.2.40
pandas>=2.0.0
plotly>=5.20.0
numpy>=1.26.0
scipy>=1.12.0
requests>=2.31.0
openpyxl>=3.1.0
xlsxwriter>=3.2.0
"""

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
import scipy.stats as stats
from io import BytesIO

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PYKUPZ LIVE TERMINAL",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# AUTO-REFRESH EVERY 60 SECONDS
# ─────────────────────────────────────────────────────────────────
refresh_count = st_autorefresh(interval=60000, key="autorefresh")

# ─────────────────────────────────────────────────────────────────
# GLOBAL THEME
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600;700&family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');
:root{--bg:#03070f;--sf:#070d1a;--s2:#0b1220;--s3:#0f1830;--bd:#162040;--ac:#00e5ff;--gn:#00ff9d;--rd:#ff2d55;--am:#ffb800;--pu:#9d4edd;--tx:#b8cce0;--dm:#3a5070;--wh:#e8f2ff;}
*,html,body{box-sizing:border-box;}
html,body,.main,[class*="css"],.block-container{background:var(--bg)!important;color:var(--tx)!important;font-family:'Inter',sans-serif!important;}
.block-container{padding:0.5rem 1.5rem 2rem!important;max-width:100%!important;}
.hf-header{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(90deg,#03070f 0%,#0a1628 50%,#03070f 100%);border-bottom:1px solid var(--ac);padding:10px 0;margin-bottom:4px;box-shadow:0 1px 30px rgba(0,229,255,0.08);}
.hf-logo{font-family:'Bebas Neue',monospace;font-size:32px;letter-spacing:8px;color:var(--ac);text-shadow:0 0 20px rgba(0,229,255,0.5);}
.hf-sub{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--dm);letter-spacing:3px;margin-top:2px;}
.hf-clock{font-family:'IBM Plex Mono',monospace;font-size:22px;color:var(--gn);text-shadow:0 0 10px rgba(0,255,157,0.4);}
.hf-status{font-family:'IBM Plex Mono',monospace;font-size:9px;color:var(--dm);letter-spacing:2px;margin-top:3px;text-align:right;}
.tape-wrap{background:var(--sf);border-top:1px solid var(--bd);border-bottom:1px solid var(--bd);padding:6px 0;overflow:hidden;white-space:nowrap;margin:4px 0 12px 0;}
.tape-inner{display:inline-block;animation:scroll-tape 80s linear infinite;font-family:'IBM Plex Mono',monospace;font-size:12px;}
@keyframes scroll-tape{from{transform:translateX(0);}to{transform:translateX(-50%);}}
.tape-up{color:var(--gn);margin:0 20px;}.tape-down{color:var(--rd);margin:0 20px;}.tape-flat{color:var(--dm);margin:0 20px;}
.card{background:var(--sf);border:1px solid var(--bd);border-radius:6px;padding:14px 18px;position:relative;overflow:hidden;}
.card::after{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--ac);}
.card.green::after{background:var(--gn);}.card.red::after{background:var(--rd);}.card.amber::after{background:var(--am);}
.card-val{font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;color:var(--wh);margin-bottom:2px;}
.card-lbl{font-size:9px;color:var(--dm);letter-spacing:2px;text-transform:uppercase;}
.card-chg{font-family:'IBM Plex Mono',monospace;font-size:12px;margin-top:4px;}
.up{color:var(--gn);}.down{color:var(--rd);}.flat{color:var(--dm);}
.idx-bar{display:flex;gap:12px;flex-wrap:wrap;background:var(--sf);border:1px solid var(--bd);border-radius:6px;padding:10px 16px;margin-bottom:10px;}
.idx-item{font-family:'IBM Plex Mono',monospace;font-size:12px;min-width:140px;}
.idx-name{color:var(--dm);font-size:10px;letter-spacing:1px;}
.sec-hdr{font-family:'Bebas Neue',monospace;font-size:18px;letter-spacing:4px;color:var(--ac);border-bottom:1px solid var(--bd);padding-bottom:6px;margin:16px 0 10px 0;}
.audit-block{background:var(--s2);border:1px solid var(--bd);border-radius:6px;padding:12px 16px;margin-bottom:8px;font-family:'IBM Plex Mono',monospace;font-size:11px;}
.algo-row{display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--bd);font-family:'IBM Plex Mono',monospace;font-size:11px;}
.algo-row:last-child{border-bottom:none;}
.algo-name{color:var(--dm);width:220px;flex-shrink:0;}
.stDataFrame>div{background:var(--sf)!important;border-radius:6px;}
div[data-testid="stDataFrame"]{background:var(--sf)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--s2)!important;border-bottom:1px solid var(--bd)!important;gap:2px;}
.stTabs [data-baseweb="tab"]{font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;letter-spacing:2px!important;color:var(--dm)!important;padding:8px 18px!important;}
.stTabs [aria-selected="true"]{color:var(--ac)!important;border-bottom:2px solid var(--ac)!important;}
.stButton button{background:transparent!important;border:1px solid var(--ac)!important;color:var(--ac)!important;font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;letter-spacing:2px!important;border-radius:4px!important;}
.stButton button:hover{background:rgba(0,229,255,0.08)!important;}
.stSelectbox>div>div,.stTextInput input{background:var(--s2)!important;border-color:var(--bd)!important;color:var(--wh)!important;font-family:'IBM Plex Mono',monospace!important;}
.stTextInput input{color:var(--ac)!important;}
section[data-testid="stSidebar"]{background:var(--sf)!important;border-right:1px solid var(--bd)!important;}
.streamlit-expanderHeader{background:var(--s2)!important;color:var(--ac)!important;font-family:'IBM Plex Mono',monospace!important;font-size:11px!important;}
details{border:1px solid var(--bd)!important;border-radius:6px!important;}
::-webkit-scrollbar{width:3px;height:3px;}::-webkit-scrollbar-track{background:var(--bg);}::-webkit-scrollbar-thumb{background:var(--ac);border-radius:2px;}
p,span,li{font-family:'Inter',sans-serif!important;}
code{background:var(--s3)!important;color:var(--ac)!important;font-family:'IBM Plex Mono',monospace!important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# HARDCODED UNIVERSE (from Pyk-Inv-List analysis)
# ─────────────────────────────────────────────────────────────────
Q1_2026 = ["NVDA","ANET","PLTR","HUBS","HIMS","LLY","CRWD","DKNG","APP",
           "AFRM","ONON","SHOP","NU","NFLX","AVGO","SPOT","META","MU",
           "FTNT","SOFI","AMD","RDDT","TTD","AMZN","ROKU","MELI","PANW","XYZ"]

STB_ALL = ["NVDA","ANET","DT","MELI","SHOP","TSM","GOOG","AMZN","ISRG",
           "MSFT","SPOT","PLTR","CRWD","NFLX","CRM","AMD","ASML","META",
           "IBKR","AXP","FTNT","NVO","HUBS","DUOL","NET","DOCS","HIMS",
           "APP","LLY","DKNG","NU","AVGO","ONON","SOFI","TTD","PANW"]

BONUS_PORTFOLIO = [
    {"ticker":"CRWD",  "name":"Crowdstrike",    "buy_price":150.90, "qty":0.404},
    {"ticker":"WPLCF", "name":"Wise PLC",        "buy_price":9.90,   "qty":6.16},
    {"ticker":"SHOP",  "name":"Shopify",          "buy_price":82.68,  "qty":0.737},
    {"ticker":"XYZ",   "name":"Block Inc",        "buy_price":98.92,  "qty":1.203},
    {"ticker":"HIMS",  "name":"Hims & Hers",      "buy_price":18.50,  "qty":5.40},
    {"ticker":"NVO",   "name":"Novo Nordisk",     "buy_price":95.00,  "qty":1.05},
    {"ticker":"FTNT",  "name":"Fortinet",         "buy_price":65.00,  "qty":1.54},
    {"ticker":"NU",    "name":"Nu Holdings",      "buy_price":12.00,  "qty":8.33},
]

INDICES = {"S&P 500":"^GSPC","NASDAQ":"^IXIC","DOW":"^DJI","VIX":"^VIX",
           "10Y YIELD":"^TNX","GOLD":"GC=F","OIL":"CL=F","BTC":"BTC-USD"}

SECTOR_ETFS = {"Technology":"XLK","Healthcare":"XLV","Financials":"XLF",
               "Consumer":"XLY","Energy":"XLE","Industrials":"XLI","Utilities":"XLU"}

# ─────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────
for k, v in {"audit_cache":{},"audit_log":[],"startup_done":False,"last_run_time":None}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────
# DATA FETCHERS  (cached with TTL)
# ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def get_price(ticker):
    try:
        h = yf.Ticker(ticker).history(period="5d")
        if h.empty or len(h) < 2:
            return None, None, None
        price = float(h["Close"].iloc[-1])
        prev  = float(h["Close"].iloc[-2])
        chg   = (price - prev) / prev
        vol   = float(h["Volume"].iloc[-1]) if "Volume" in h else 0
        return price, chg, vol
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
def get_financials(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.income_stmt, t.cash_flow, t.balance_sheet
    except Exception:
        return None, None, None

@st.cache_data(ttl=3600, show_spinner=False)
def get_earnings_hist(ticker):
    try:
        return yf.Ticker(ticker).earnings_history
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────────
# AUDIT ALGORITHMS
# ─────────────────────────────────────────────────────────────────
def algo1_reconcile(ticker, price):
    sources = {}
    try:
        t    = yf.Ticker(ticker)
        info = t.info
        sources["Yahoo Info"] = (info.get("currentPrice") or info.get("regularMarketPrice"), 0.40)
        sources["Fast Info"]  = (getattr(t.fast_info, "last_price", None), 0.30)
        h = t.history(period="2d")
        sources["Historical"] = (float(h["Close"].iloc[-1]) if not h.empty else None, 0.20)
        sources["Prev Close"] = (info.get("previousClose"), 0.10)

        prices = [(v, w) for v, w in sources.values() if v is not None]
        if not prices:
            return {"status":"⚪ NO DATA","weighted":price,"spread":None}
        tw  = sum(w for _, w in prices)
        wav = sum(p * w for p, w in prices) / tw
        vals = [p for p, _ in prices]
        spread = (max(vals)-min(vals))/np.mean(vals)*100 if np.mean(vals) else 0
        status = "✅ AUDITED" if spread < 0.5 else "⚠️ MINOR DISCREPANCY" if spread < 2 else "🚨 DISCREPANCY"
        return {"status":status,"weighted":round(wav,4),"spread":round(spread,3)}
    except Exception:
        return {"status":"❌ ERROR","weighted":price,"spread":None}

def algo2_anomaly(ticker, price):
    try:
        h = get_hist(ticker, "5y")
        if h.empty or len(h) < 30:
            return {"status":"⚪ INSUFFICIENT DATA","z":None,"flag":False}
        monthly = h["Close"].resample("ME").last().dropna()
        if len(monthly) < 12:
            return {"status":"⚪ INSUFFICIENT DATA","z":None,"flag":False}
        mu  = float(monthly.mean())
        sig = float(monthly.std())
        if sig == 0:
            return {"status":"⚪ ZERO STD","z":0,"flag":False}
        z = (price - mu) / sig
        if   abs(z) > 3: status, flag = f"🚨 STATISTICAL OUTLIER (z={z:.1f})", True
        elif abs(z) > 2: status, flag = f"⚠️ ELEVATED >2σ (z={z:.1f})", True
        else:            status, flag = f"✅ NORMAL RANGE (z={z:.1f})", False
        return {"status":status,"z":round(z,2),"mean":round(mu,2),"std":round(sig,2),"flag":flag}
    except Exception:
        return {"status":"⚪ ERROR","z":None,"flag":False}

def algo3_cashflow(ticker):
    try:
        income, cf, _ = get_financials(ticker)
        if income is None or income.empty:
            return {"status":"⚪ NO FILING DATA","issues":[],"checks":{}}
        def val(df, *keys):
            for k in keys:
                if df is not None and k in df.index:
                    v = df.loc[k].iloc[0]
                    return float(v) if pd.notna(v) else None
            return None
        ebitda = val(income,"EBITDA","Normalized EBITDA")
        ebit   = val(income,"EBIT","Operating Income")
        ni     = val(income,"Net Income","Net Income Common Stockholders")
        da     = val(income,"Reconciled Depreciation","Depreciation And Amortization")
        fcf    = val(cf,"Free Cash Flow")
        opcf   = val(cf,"Operating Cash Flow")
        issues, checks = [], {}
        if ebitda and ebit and da:
            diff = abs(ebitda-(ebit+abs(da)))/abs(ebitda)*100
            checks["EBITDA→EBIT"] = "✅" if diff < 5 else "⚠️"
            if diff >= 5: issues.append(f"EBITDA-EBIT gap {diff:.1f}%")
        if fcf and opcf:
            checks["FCF≤OCF"] = "✅" if fcf <= opcf*1.05 else "⚠️"
            if fcf > opcf*1.05: issues.append("FCF > OCF unusual")
        if ni and ebitda:
            checks["NI<EBITDA"] = "✅" if ni < ebitda else "⚠️"
        overall = "✅ CHAIN INTACT" if not issues else f"🚨 {len(issues)} ISSUE(S)"
        return {"status":overall,"issues":issues,"checks":checks}
    except Exception:
        return {"status":"⚪ PARSE ERROR","issues":[],"checks":{}}

def algo4_freshness(ticker):
    try:
        h = get_hist(ticker,"5d")
        if h.empty:
            return {"status":"🔴 NO DATA","score":0,"flag":True}
        last_dt = h.index[-1]
        if hasattr(last_dt,"to_pydatetime"):
            last_dt = last_dt.to_pydatetime()
        try:
            age = (datetime.now(last_dt.tzinfo)-last_dt).days
        except Exception:
            age = (datetime.now()-last_dt.replace(tzinfo=None)).days
        if   age < 1:  score, label = 100, "🟢 REAL-TIME"
        elif age < 7:  score, label = 80,  "🟡 RECENT"
        elif age < 30: score, label = 60,  "🟠 MODERATE"
        else:          score, label = 30,  "🔴 STALE"
        return {"status":label,"score":score,"age_days":age,"flag":score<70}
    except Exception:
        return {"status":"⚪ ERROR","score":0,"flag":True}

def algo5_trend(ticker):
    try:
        income, _, _ = get_financials(ticker)
        if income is None or income.empty or "Total Revenue" not in income.index:
            return {"status":"⚪ NO REVENUE DATA","cagr_3y":None,"flag":False}
        rev  = income.loc["Total Revenue"].dropna().sort_index()
        vals = [float(v) for v in rev.values[::-1] if pd.notna(v)]
        if len(vals) < 3:
            return {"status":"⚪ INSUFFICIENT HISTORY","cagr_3y":None,"flag":False}
        cagr = (vals[-1]/vals[0])**(1/max(len(vals)-1,1))-1 if vals[0]!=0 else 0
        growths = [(vals[i]-vals[i-1])/abs(vals[i-1]) for i in range(1,len(vals)) if vals[i-1]!=0]
        flag = False
        if len(growths) >= 3:
            mu_g, sg = np.mean(growths), np.std(growths)
            z = (growths[-1]-mu_g)/sg if sg>0 else 0
            if abs(z) > 2:
                return {"status":f"📉 TREND BREAK (z={z:.1f})","cagr_3y":round(cagr*100,1),"flag":True}
        return {"status":"✅ TREND INTACT","cagr_3y":round(cagr*100,1),"flag":False}
    except Exception:
        return {"status":"⚪ ERROR","cagr_3y":None,"flag":False}

def algo6_guidance(ticker):
    try:
        eh = get_earnings_hist(ticker)
        if eh is None or eh.empty:
            return {"status":"⚪ NO DATA","accuracy":None,"flag":False,"quarters":[]}
        cols = eh.columns.tolist()
        ec   = next((c for c in cols if "estimate" in c.lower()),None)
        ac   = next((c for c in cols if "actual"   in c.lower()),None)
        if not ec or not ac:
            return {"status":"⚪ NO EPS COLS","accuracy":None,"flag":False,"quarters":[]}
        recent = eh[[ec,ac]].dropna().tail(8)
        beats  = int((recent[ac] >= recent[ec]).sum())
        total  = len(recent)
        if total == 0:
            return {"status":"⚪ NO QUARTERS","accuracy":None,"flag":False,"quarters":[]}
        acc  = beats/total*100
        flag = acc < 50
        status = f"✅ {acc:.0f}% BEAT RATE" if acc>=75 else f"⚠️ {acc:.0f}% BEAT RATE" if acc>=50 else f"🚨 {acc:.0f}% — LOW ACCURACY"
        quarters = [{"date":str(idx)[:10],"est":round(float(r[ec]),2),"act":round(float(r[ac]),2),
                     "result":"✅ BEAT" if r[ac]>=r[ec] else "❌ MISS"}
                    for idx,r in recent.iterrows()]
        return {"status":status,"accuracy":round(acc,1),"flag":flag,"quarters":quarters}
    except Exception:
        return {"status":"⚪ ERROR","accuracy":None,"flag":False,"quarters":[]}

def algo7_hypothesis(ticker, price, info):
    checks=[]; validated=0; total=0
    pe  = info.get("trailingPE")
    fpe = info.get("forwardPE")
    eps = info.get("trailingEps")
    rev = info.get("totalRevenue")
    mc  = info.get("marketCap")

    def chk(name, fair, live, tol=25):
        nonlocal validated, total
        total += 1
        if fair and live and fair>0:
            dev = (live-fair)/fair*100
            ok  = abs(dev)<tol
            if ok: validated += 1
            return {"name":name,"fair":round(fair,2),"live":round(live,2),
                    "dev":round(dev,1),"status":"✅ VALIDATED" if ok else "⚠️ DEVIATING"}
        return None

    if pe and eps and eps>0:
        c = chk("P/E Implied Price", pe*eps, price)
        if c: checks.append(c)
    if fpe and eps and eps>0:
        c = chk("Fwd P/E Implied", fpe*eps, price)
        if c: checks.append(c)
    if rev and mc and rev>0:
        c = chk("P/S vs 2.5x Bench", 2.5, mc/rev, tol=100)
        if c: checks.append(c)

    pct = validated/total*100 if total>0 else 0
    if   pct>=75: overall = f"🏆 VALIDATED ({validated}/{total})"
    elif pct>=50: overall = f"⚠️ PARTIAL ({validated}/{total})"
    else:         overall = f"🚨 CHALLENGED ({validated}/{total})"
    return {"overall":overall,"checks":checks,"score":pct}

def run_full_audit(ticker):
    price, chg, vol = get_price(ticker)
    info = get_info(ticker)
    if not price:
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0.0
    a1 = algo1_reconcile(ticker, price)
    a2 = algo2_anomaly(ticker, price)
    a3 = algo3_cashflow(ticker)
    a4 = algo4_freshness(ticker)
    a5 = algo5_trend(ticker)
    a6 = algo6_guidance(ticker)
    a7 = algo7_hypothesis(ticker, price, info)
    flags = [a2.get("flag",False), bool(a3.get("issues")),
             a4.get("flag",False), a5.get("flag",False), a6.get("flag",False)]
    score = max(0, 100 - sum(flags)*15)
    return {"ticker":ticker,"price":price,"change":chg,"info":info,"score":score,
            "timestamp":datetime.now().strftime("%H:%M:%S"),
            "A1":a1,"A2":a2,"A3":a3,"A4":a4,"A5":a5,"A6":a6,"A7":a7}

# ─────────────────────────────────────────────────────────────────
# RANKING ENGINE
# ─────────────────────────────────────────────────────────────────
def rank_score(info):
    score = 0.0
    try:
        rg  = (info.get("revenueGrowth")  or 0)*100
        eg  = (info.get("earningsGrowth") or 0)*100
        pe  =  info.get("trailingPE")      or 0
        ps  =  info.get("priceToSalesTrailing12Months") or 0
        fcf =  info.get("freeCashflow")    or 0
        td  =  info.get("totalDebt")       or 0
        tc  =  info.get("totalCash")       or 0
        rev =  info.get("totalRevenue")    or 1
        nd  = (td - tc) / rev if rev else 0

        score += min(max(rg+50,0),150)/150*30     # rev growth  30%
        score += min(max(eg+50,0),150)/150*20     # eps growth  20%
        score += 20 if fcf>0 else 10 if fcf==0 else 0  # FCF 20%
        if nd<0: score+=10
        elif nd<1: score+=7
        elif nd<3: score+=3                        # net debt 10%
        if 0<pe<80:  score+=10
        if 0<ps<20:  score+=10                    # valuation 20%
    except Exception:
        pass
    return round(min(score, 100), 1)

def signal(score, chg):
    if score>=75 and (chg or 0)>-0.03: return "STRONG BUY"
    elif score>=60: return "BUY"
    elif score>=45: return "HOLD"
    else:           return "WATCH"

# ─────────────────────────────────────────────────────────────────
# STARTUP AUTO-AUDIT  (runs once then on every refresh cycle)
# ─────────────────────────────────────────────────────────────────
def startup_audit():
    top10 = Q1_2026[:10]
    bar   = st.progress(0, text="⚡ AUTO-AUDITING TOP 10 PICKS ON STARTUP...")
    for i, t in enumerate(top10):
        try:
            res = run_full_audit(t)
            st.session_state.audit_cache[t] = res
            st.session_state.audit_log.append(res)
        except Exception:
            pass
        bar.progress((i+1)/len(top10), text=f"⚡ Auditing {t}... ({i+1}/{len(top10)})")
    bar.empty()
    st.session_state.startup_done = True
    st.session_state.last_run_time = datetime.now().strftime("%H:%M:%S")

# ─────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────
def fmt_mcap(v):
    if not v: return "—"
    if v>=1e12: return f"${v/1e12:.2f}T"
    if v>=1e9:  return f"${v/1e9:.1f}B"
    if v>=1e6:  return f"${v/1e6:.0f}M"
    return f"${v:.0f}"

def fmt_pct(v, mult=True):
    if v is None: return "—"
    try:
        f = float(v)
        if mult: f *= 100
        return f"{f:+.2f}%"
    except Exception:
        return "—"

CHART = dict(
    paper_bgcolor="#03070f", plot_bgcolor="#070d1a",
    font=dict(family="IBM Plex Mono", color="#b8cce0", size=11),
    margin=dict(l=8,r=8,t=36,b=8),
    xaxis=dict(gridcolor="#162040",showgrid=True,zeroline=False),
    yaxis=dict(gridcolor="#162040",showgrid=True,zeroline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)",bordercolor="#162040"),
)

# ─────────────────────────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────────────────────────
def chart_price(ticker, period="1y"):
    h = get_hist(ticker, period)
    if h.empty: return go.Figure()
    fig = make_subplots(rows=2,cols=1,shared_xaxes=True,row_heights=[0.75,0.25],vertical_spacing=0.03)
    ma20 = h["Close"].rolling(20).mean()
    ma50 = h["Close"].rolling(50).mean()
    std  = h["Close"].rolling(20).std()
    bbu  = ma20+2*std; bbl = ma20-2*std
    fig.add_trace(go.Candlestick(x=h.index,open=h["Open"],high=h["High"],low=h["Low"],close=h["Close"],
                                  name="OHLC",increasing_fillcolor="#00ff9d",decreasing_fillcolor="#ff2d55",
                                  increasing_line_color="#00ff9d",decreasing_line_color="#ff2d55"),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=ma20,mode="lines",name="MA20",line=dict(color="#ffb800",width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=ma50,mode="lines",name="MA50",line=dict(color="#9d4edd",width=1,dash="dot")),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=bbu,mode="lines",name="BB+",line=dict(color="#00e5ff",width=0.7,dash="dash")),row=1,col=1)
    fig.add_trace(go.Scatter(x=h.index,y=bbl,mode="lines",name="BB-",line=dict(color="#00e5ff",width=0.7,dash="dash"),
                              fill="tonexty",fillcolor="rgba(0,229,255,0.03)"),row=1,col=1)
    colors = ["#00ff9d" if c>=o else "#ff2d55" for c,o in zip(h["Close"],h["Open"])]
    fig.add_trace(go.Bar(x=h.index,y=h["Volume"],name="Vol",marker_color=colors,opacity=0.5),row=2,col=1)
    fig.update_layout(**CHART,title=dict(text=f"⚡ {ticker} — CANDLESTICK + BOLLINGER BANDS",font=dict(color="#00e5ff",size=14)),height=500)
    fig.update_xaxes(rangeslider_visible=False)
    return fig

def chart_ranking(df):
    df = df.sort_values("Score",ascending=True).tail(25)
    colors = ["#00ff9d" if s>=70 else "#ffb800" if s>=50 else "#ff2d55" for s in df["Score"]]
    fig = go.Figure(go.Bar(x=df["Score"],y=df["Ticker"],orientation="h",marker_color=colors,
                            text=[f"{s:.0f}" for s in df["Score"]],textposition="outside",
                            textfont=dict(color="#b8cce0",size=10,family="IBM Plex Mono")))
    fig.update_layout(**CHART,title=dict(text="📊 LIVE STB RANKING",font=dict(color="#00e5ff",size=14)),
                      height=520,xaxis_range=[0,115])
    return fig

def chart_sector(data):
    colors = ["#00ff9d" if v>0 else "#ff2d55" for v in data.values()]
    fig = go.Figure(go.Bar(x=list(data.keys()),y=list(data.values()),marker_color=colors,
                            text=[f"{v:+.2f}%" for v in data.values()],textposition="outside",
                            textfont=dict(color="#b8cce0",size=10,family="IBM Plex Mono")))
    fig.update_layout(**CHART,title=dict(text="🏭 SECTOR PERFORMANCE (ETF)",font=dict(color="#00e5ff",size=14)),
                      height=300,yaxis=dict(gridcolor="#162040",zeroline=True,zerolinecolor="#3a5070"))
    return fig

def chart_correlation(tickers):
    rets = {}
    for t in tickers:
        h = get_hist(t,"1y")
        if not h.empty and len(h)>20:
            rets[t] = h["Close"].pct_change().dropna()
    if len(rets)<3: return go.Figure()
    df   = pd.DataFrame(rets).dropna()
    corr = df.corr()
    fig  = go.Figure(go.Heatmap(z=corr.values,x=corr.columns,y=corr.index,
                                 colorscale=[[0,"#ff2d55"],[0.5,"#070d1a"],[1,"#00ff9d"]],
                                 text=[[f"{v:.2f}" for v in r] for r in corr.values],
                                 texttemplate="%{text}",textfont=dict(size=9,family="IBM Plex Mono"),
                                 zmin=-1,zmax=1))
    fig.update_layout(**CHART,title=dict(text="🔗 1Y RETURN CORRELATION",font=dict(color="#00e5ff",size=14)),height=480)
    return fig

def chart_pnl():
    tickers = [r["ticker"] for r in BONUS_PORTFOLIO]
    pnls    = []
    for r in BONUS_PORTFOLIO:
        p,_,_ = get_price(r["ticker"])
        if p and r["buy_price"]:
            pnls.append((r["ticker"],(p-r["buy_price"])/r["buy_price"]*100))
        else:
            pnls.append((r["ticker"],0.0))
    colors = ["#00ff9d" if v>=0 else "#ff2d55" for _,v in pnls]
    fig = go.Figure(go.Bar(x=[t for t,_ in pnls],y=[v for _,v in pnls],marker_color=colors,
                            text=[f"{v:+.1f}%" for _,v in pnls],textposition="outside",
                            textfont=dict(color="#b8cce0",size=11,family="IBM Plex Mono")))
    fig.update_layout(**CHART,title=dict(text="💰 BONUS PORTFOLIO P&L",font=dict(color="#00e5ff",size=14)),
                      height=320,yaxis=dict(gridcolor="#162040",zeroline=True,zerolinecolor="#3a5070"))
    return fig

def chart_waterfall(ticker):
    income,_,_ = get_financials(ticker)
    if income is None or income.empty or "Total Revenue" not in income.index:
        return go.Figure()
    rev  = income.loc["Total Revenue"].dropna().sort_index()
    vals = [float(v)/1e9 for v in rev.values[::-1]]
    yrs  = [str(d.year) for d in rev.index[::-1]]
    fig  = go.Figure(go.Waterfall(x=yrs,y=vals,measure=["absolute"]+["relative"]*(len(vals)-1),
                                   increasing=dict(marker_color="#00ff9d"),decreasing=dict(marker_color="#ff2d55"),
                                   totals=dict(marker_color="#00e5ff"),connector=dict(line=dict(color="#162040",width=1)),
                                   text=[f"${v:.1f}B" for v in vals],textfont=dict(family="IBM Plex Mono",size=10,color="#b8cce0")))
    fig.update_layout(**CHART,title=dict(text=f"{ticker} — REVENUE WATERFALL",font=dict(color="#00e5ff",size=14)),height=350)
    return fig


@st.cache_data(ttl=3600, show_spinner=False)
def get_full_financials(ticker):
    """Pull all available annual income, cashflow, balance sheet data."""
    try:
        t = yf.Ticker(ticker)
        income  = t.income_stmt
        cf      = t.cash_flow
        bal     = t.balance_sheet
        hist    = t.history(period="max")
        return income, cf, bal, hist
    except Exception:
        return None, None, None, pd.DataFrame()


def _safe_row(df, *keys):
    """Extract a row from financials df by trying multiple key names."""
    if df is None or df.empty:
        return None
    for k in keys:
        if k in df.index:
            row = df.loc[k].dropna()
            return row
    return None


def chart_rev_vs_price(ticker):
    """Revenue growth bars overlaid with stock price line — dual axis."""
    income, _, _, hist = get_full_financials(ticker)
    if income is None or income.empty:
        return go.Figure().update_layout(**CHART, title=dict(text="No data", font=dict(color="#00e5ff", size=13)))

    rev_row = _safe_row(income, "Total Revenue", "Revenue")
    if rev_row is None:
        return go.Figure().update_layout(**CHART, title=dict(text="No revenue data", font=dict(color="#00e5ff", size=13)))

    rev_row = rev_row.sort_index()
    years   = [str(d.year) for d in rev_row.index]
    rev_b   = [float(v)/1e9 for v in rev_row.values]

    # Revenue growth %
    rev_growth = [None]
    for i in range(1, len(rev_b)):
        if rev_b[i-1] and rev_b[i-1] != 0:
            rev_growth.append((rev_b[i]-rev_b[i-1])/abs(rev_b[i-1])*100)
        else:
            rev_growth.append(None)

    # Stock price at year-end for each year
    prices_at_year = []
    for d in rev_row.index:
        yr = d.year
        if not hist.empty:
            yr_hist = hist[hist.index.year == yr]
            if not yr_hist.empty:
                prices_at_year.append(float(yr_hist["Close"].iloc[-1]))
            else:
                prices_at_year.append(None)
        else:
            prices_at_year.append(None)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Revenue bars
    bar_colors = ["#00ff9d" if (g or 0) >= 0 else "#ff2d55" for g in rev_growth]
    fig.add_trace(go.Bar(
        x=years, y=rev_b, name="Revenue ($B)",
        marker_color=bar_colors, opacity=0.75,
        text=[f"${v:.1f}B" for v in rev_b],
        textposition="outside",
        textfont=dict(size=9, family="IBM Plex Mono", color="#b8cce0"),
    ), secondary_y=False)

    # Revenue growth % line
    fig.add_trace(go.Scatter(
        x=years, y=rev_growth, name="Rev Growth %",
        mode="lines+markers+text",
        line=dict(color="#ffb800", width=2),
        marker=dict(size=8, color="#ffb800"),
        text=[f"{g:.1f}%" if g is not None else "" for g in rev_growth],
        textposition="top center",
        textfont=dict(size=9, family="IBM Plex Mono", color="#ffb800"),
    ), secondary_y=False)

    # Stock price line (right axis)
    valid_prices = [(y, p) for y, p in zip(years, prices_at_year) if p is not None]
    if valid_prices:
        fig.add_trace(go.Scatter(
            x=[y for y,_ in valid_prices], y=[p for _,p in valid_prices],
            name="Stock Price ($)",
            mode="lines+markers",
            line=dict(color="#00e5ff", width=2.5, dash="dot"),
            marker=dict(size=8, color="#00e5ff", symbol="diamond"),
        ), secondary_y=True)

    fig.update_layout(
        **CHART,
        title=dict(text=f"⚡ {ticker} — REVENUE GROWTH vs STOCK PRICE", font=dict(color="#00e5ff", size=14)),
        height=420, barmode="group",
        legend=dict(orientation="h", y=1.08, bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_yaxes(title_text="Revenue ($B) / Growth %", secondary_y=False,
                     gridcolor="#162040", titlefont=dict(color="#00ff9d", size=10))
    fig.update_yaxes(title_text="Stock Price ($)", secondary_y=True,
                     gridcolor="rgba(0,229,255,0.1)", titlefont=dict(color="#00e5ff", size=10))
    return fig


def chart_multiyear_map(ticker, metric="PE"):
    """
    Multi-year map of PE / PS / EPS / Revenue Growth / EBITDA Margin / FCF.
    Shows all available annual data side by side.
    """
    income, cf, bal, hist = get_full_financials(ticker)
    info = get_info(ticker)

    # Build year-indexed series for every metric
    metrics_data = {}

    if income is not None and not income.empty:
        rev_row  = _safe_row(income, "Total Revenue", "Revenue")
        ni_row   = _safe_row(income, "Net Income", "Net Income Common Stockholders")
        ebitda_r = _safe_row(income, "EBITDA", "Normalized EBITDA")
        da_row   = _safe_row(income, "Reconciled Depreciation","Depreciation And Amortization")
        ebit_row = _safe_row(income, "EBIT","Operating Income")
        shares_r = _safe_row(income, "Diluted Average Shares","Basic Average Shares")

        # Revenue
        if rev_row is not None:
            rev_s = rev_row.sort_index()
            metrics_data["Revenue ($B)"] = {str(d.year): float(v)/1e9 for d, v in zip(rev_s.index, rev_s.values)}
            # Revenue growth %
            vals  = list(rev_s.values)
            dates = [str(d.year) for d in rev_s.index]
            rg = {}
            for i in range(1, len(vals)):
                if vals[i-1] and vals[i-1] != 0:
                    rg[dates[i]] = round((vals[i]-vals[i-1])/abs(vals[i-1])*100, 1)
            metrics_data["Rev Growth %"] = rg

        # EBITDA & margin
        if ebitda_r is not None:
            ebitda_s = ebitda_r.sort_index()
            metrics_data["EBITDA ($B)"] = {str(d.year): float(v)/1e9 for d,v in zip(ebitda_s.index, ebitda_s.values)}
            if rev_row is not None:
                rev_s2 = rev_row.sort_index()
                margins = {}
                for d, ev in zip(ebitda_s.index, ebitda_s.values):
                    yr = str(d.year)
                    rv = metrics_data["Revenue ($B)"].get(yr)
                    if rv and rv != 0:
                        margins[yr] = round(float(ev)/1e9/rv*100, 1)
                metrics_data["EBITDA Margin %"] = margins

        # EPS
        if ni_row is not None and shares_r is not None:
            ni_s  = ni_row.sort_index()
            sh_s  = shares_r.sort_index()
            eps_d = {}
            for d, nv in zip(ni_s.index, ni_s.values):
                yr = str(d.year)
                sh_match = sh_s[sh_s.index.year == d.year]
                if not sh_match.empty and float(sh_match.iloc[0]) > 0:
                    eps_d[yr] = round(float(nv)/float(sh_match.iloc[0]), 3)
            if eps_d:
                metrics_data["EPS ($)"] = eps_d
                # EPS growth
                eps_vals = list(eps_d.values())
                eps_yrs  = list(eps_d.keys())
                epsg = {}
                for i in range(1, len(eps_vals)):
                    if eps_vals[i-1] and eps_vals[i-1] != 0:
                        epsg[eps_yrs[i]] = round((eps_vals[i]-eps_vals[i-1])/abs(eps_vals[i-1])*100, 1)
                metrics_data["EPS Growth %"] = epsg

    # FCF
    if cf is not None and not cf.empty:
        fcf_row = _safe_row(cf, "Free Cash Flow")
        if fcf_row is not None:
            fcf_s = fcf_row.sort_index()
            metrics_data["FCF ($B)"] = {str(d.year): round(float(v)/1e9,2) for d,v in zip(fcf_s.index, fcf_s.values)}

    # PE & PS from historical prices + revenue/earnings
    if hist is not None and not hist.empty:
        pe_hist, ps_hist = {}, {}
        for yr_str, rev_b in metrics_data.get("Revenue ($B)", {}).items():
            try:
                yr_int  = int(yr_str)
                yr_hist = hist[hist.index.year == yr_int]
                if yr_hist.empty: continue
                avg_p   = float(yr_hist["Close"].mean())
                mc_approx = avg_p * (info.get("sharesOutstanding",1) or 1)
                rev_full  = rev_b * 1e9
                if rev_full > 0:
                    ps_hist[yr_str] = round(mc_approx/rev_full, 2)
                ni_yr = metrics_data.get("EBITDA ($B)",{}).get(yr_str)
                if ni_yr and ni_yr > 0:
                    pe_approx = mc_approx / (ni_yr*1e9)
                    if 0 < pe_approx < 2000:
                        pe_hist[yr_str] = round(pe_approx, 1)
            except Exception:
                pass
        if pe_hist: metrics_data["P/E (approx)"] = pe_hist
        if ps_hist: metrics_data["P/S (approx)"] = ps_hist

    if not metrics_data:
        return go.Figure().update_layout(**CHART, title=dict(text="No financial data available", font=dict(color="#00e5ff",size=13)))

    # Determine which metric to show
    available = list(metrics_data.keys())
    sel = metric if metric in available else available[0]
    data = metrics_data[sel]

    years  = sorted(data.keys())
    values = [data[y] for y in years]

    # Color logic
    if "Growth" in sel or "Margin" in sel:
        colors = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in values]
    elif "FCF" in sel:
        colors = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in values]
    else:
        colors = ["#00e5ff"] * len(values)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years, y=values,
        marker_color=colors,
        text=[f"{v:.1f}" for v in values],
        textposition="outside",
        textfont=dict(size=10, family="IBM Plex Mono", color="#b8cce0"),
        name=sel,
    ))

    # Add trend line
    if len(years) >= 3:
        try:
            x_num = list(range(len(years)))
            z     = np.polyfit(x_num, values, 1)
            p     = np.poly1d(z)
            trend = [p(xi) for xi in x_num]
            fig.add_trace(go.Scatter(
                x=years, y=trend, mode="lines", name="Trend",
                line=dict(color="#9d4edd", width=2, dash="dot"),
            ))
        except Exception:
            pass

    fig.update_layout(
        **CHART,
        title=dict(text=f"⚡ {ticker} — {sel} (ALL AVAILABLE YEARS)", font=dict(color="#00e5ff", size=14)),
        height=380,
        yaxis=dict(gridcolor="#162040", zeroline=True, zerolinecolor="#3a5070"),
        legend=dict(orientation="h", y=1.06, bgcolor="rgba(0,0,0,0)"),
    )
    return fig, available, metrics_data


def chart_all_metrics_grid(ticker):
    """4-panel grid: Revenue, EBITDA, EPS Growth, FCF side by side."""
    income, cf, _, hist = get_full_financials(ticker)
    if income is None or income.empty:
        return go.Figure().update_layout(**CHART, title=dict(text="No data", font=dict(color="#00e5ff",size=13)))

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["Revenue ($B)", "EBITDA ($B)", "EPS Growth %", "FCF ($B)"],
        vertical_spacing=0.18, horizontal_spacing=0.10,
    )

    def add_bars(df, *keys, row, col, color="#00e5ff", divisor=1e9, pct_of_prev=False):
        row_data = _safe_row(df, *keys)
        if row_data is None: return
        s = row_data.sort_index()
        years = [str(d.year) for d in s.index]
        vals  = [float(v)/divisor for v in s.values]
        if pct_of_prev:
            g_vals = [None]
            for i in range(1, len(vals)):
                if vals[i-1] and vals[i-1] != 0:
                    g_vals.append((vals[i]-vals[i-1])/abs(vals[i-1])*100)
                else:
                    g_vals.append(None)
            plot_vals = g_vals
            cols = ["#00ff9d" if (v or 0)>=0 else "#ff2d55" for v in g_vals]
        else:
            plot_vals = vals
            cols = [color]*len(vals)
        fig.add_trace(go.Bar(x=years,y=plot_vals,marker_color=cols,
                             text=[f"{v:.1f}" if v is not None else "" for v in plot_vals],
                             textposition="outside",textfont=dict(size=8,family="IBM Plex Mono",color="#b8cce0"),
                             showlegend=False),row=row,col=col)

    add_bars(income,"Total Revenue","Revenue",      row=1,col=1,color="#00e5ff")
    add_bars(income,"EBITDA","Normalized EBITDA",   row=1,col=2,color="#00ff9d")
    add_bars(income,"Net Income","Net Income Common Stockholders", row=2,col=1,color="#ffb800",pct_of_prev=True)
    if cf is not None:
        add_bars(cf,"Free Cash Flow",               row=2,col=2,color="#9d4edd")

    fig.update_layout(
        paper_bgcolor="#03070f", plot_bgcolor="#070d1a",
        font=dict(family="IBM Plex Mono", color="#b8cce0", size=10),
        title=dict(text=f"⚡ {ticker} — FULL FINANCIAL GRID (ALL YEARS)", font=dict(color="#00e5ff",size=14)),
        height=580, margin=dict(l=8,r=8,t=60,b=8),
        showlegend=False,
    )
    for i in range(1,3):
        for j in range(1,3):
            fig.update_xaxes(gridcolor="#162040",row=i,col=j)
            fig.update_yaxes(gridcolor="#162040",zeroline=True,zerolinecolor="#3a5070",row=i,col=j)
    return fig

# ─────────────────────────────────────────────────────────────────
# ████  MAIN APP  ████
# ─────────────────────────────────────────────────────────────────
def main():
    # STARTUP AUDIT — runs automatically on first load
    if not st.session_state.startup_done:
        startup_audit()

    now = datetime.now()
    mkt = now.weekday() < 5 and 9 <= now.hour < 16
    mkt_html = '<span style="color:#00ff9d">● LIVE</span>' if mkt else '<span style="color:#3a5070">● CLOSED</span>'

    # ── HEADER ──
    st.markdown(f"""
    <div class="hf-header">
      <div>
        <div class="hf-logo">⚡ PYKUPZ LIVE TERMINAL</div>
        <div class="hf-sub">HEDGE FUND EDITION · 7-ALGORITHM AUDIT ENGINE · FULLY AUTOMATED · NO EXCEL NEEDED</div>
      </div>
      <div style="text-align:right">
        <div class="hf-clock">{now.strftime("%H:%M:%S")}</div>
        <div class="hf-status">{mkt_html} &nbsp;|&nbsp; REFRESH #{refresh_count} &nbsp;|&nbsp;
        LAST AUDIT: {st.session_state.last_run_time or "—"} &nbsp;|&nbsp;
        AUDITED: {len(st.session_state.audit_cache)} TICKERS</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── MARKET INDICES BAR ──
    idx_html = '<div class="idx-bar">'
    for name, sym in INDICES.items():
        p, chg, _ = get_price(sym)
        if p:
            cls = "up" if (chg or 0)>0 else "down" if (chg or 0)<0 else "flat"
            arr = "▲" if (chg or 0)>0 else "▼"
            idx_html += (f'<div class="idx-item"><div class="idx-name">{name}</div>'
                         f'<span style="color:#e8f2ff">{p:,.2f}</span> '
                         f'<span class="{cls}">{arr}{abs((chg or 0)*100):.2f}%</span></div>')
    idx_html += "</div>"
    st.markdown(idx_html, unsafe_allow_html=True)

    # ── TICKER TAPE ──
    tape = ""
    for t in Q1_2026:
        p, chg, _ = get_price(t)
        if p and chg is not None:
            cls = "tape-up" if chg>0 else "tape-down" if chg<0 else "tape-flat"
            arr = "▲" if chg>0 else "▼"
            tape += f'<span class="{cls}">{t} ${p:.2f} {arr}{abs(chg*100):.2f}%</span>'
    if tape:
        st.markdown(f'<div class="tape-wrap"><div class="tape-inner">{tape*2}</div></div>', unsafe_allow_html=True)

    # ── TABS ──
    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs([
        "🏆  LIVE RANKINGS",
        "📈  PRICE & CHARTS",
        "🔬  AUDIT ENGINE",
        "💰  PORTFOLIO",
        "🌐  MARKET PULSE",
        "⚙️  COMMAND CENTER",
    ])

    # ════════════════════════════════════════════
    # TAB 1 — LIVE RANKINGS  (auto-computed)
    # ════════════════════════════════════════════
    with tab1:
        st.markdown('<div class="sec-hdr">🏆 LIVE STB RANKINGS — AUTO-COMPUTED EVERY 60s</div>', unsafe_allow_html=True)
        c1,c2,c3 = st.columns(3)
        with c1: uni_choice = st.radio("Universe",["Q1 2026","All STB","Combined"],horizontal=True,label_visibility="collapsed")
        with c2: top_n      = st.slider("Top N",10,40,25,label_visibility="collapsed")
        with c3: sort_col   = st.selectbox("Sort by",["Score","Change %","Market Cap","P/E"],label_visibility="collapsed")

        universe = Q1_2026 if uni_choice=="Q1 2026" else STB_ALL if uni_choice=="All STB" else list(dict.fromkeys(Q1_2026+STB_ALL))

        rows = []
        with st.spinner("⚡ Computing live rankings..."):
            for ticker in universe[:top_n]:
                p,chg,_ = get_price(ticker)
                info     = get_info(ticker)
                sc       = rank_score(info)
                sig      = signal(sc, chg)
                pe       = info.get("trailingPE")
                ps       = info.get("priceToSalesTrailing12Months")
                mc       = info.get("marketCap")
                rg       = info.get("revenueGrowth")
                eg       = info.get("earningsGrowth")
                audit    = st.session_state.audit_cache.get(ticker,{})
                rows.append({
                    "Ticker":    ticker,
                    "Price":     f"${p:.2f}" if p else "—",
                    "Change %":  round((chg or 0)*100, 2),
                    "Score":     sc,
                    "Signal":    sig,
                    "P/E":       round(pe,1) if pe else None,
                    "P/S":       round(ps,2) if ps else None,
                    "Market Cap":fmt_mcap(mc),
                    "Rev Growth":fmt_pct(rg),
                    "EPS Growth":fmt_pct(eg),
                    "Audit":     audit.get("score","—") if audit else "—",
                })

        df = pd.DataFrame(rows)
        if sort_col=="Score":      df = df.sort_values("Score",ascending=False)
        elif sort_col=="Change %": df = df.sort_values("Change %",ascending=False)
        df = df.reset_index(drop=True); df.index += 1

        st.dataframe(df, use_container_width=True, height=580,
            column_config={
                "Score":     st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%.0f"),
                "Change %":  st.column_config.NumberColumn("Chg %",format="%.2f%%"),
                "Audit":     st.column_config.NumberColumn("Audit",format="%d"),
            })

        # Ranking bar chart
        df_c = df[["Ticker","Score"]].copy()
        df_c["Score"] = pd.to_numeric(df_c["Score"],errors="coerce").fillna(0)
        st.plotly_chart(chart_ranking(df_c), use_container_width=True)

    # ════════════════════════════════════════════
    # TAB 2 — PRICE & CHARTS
    # ════════════════════════════════════════════
    with tab2:
        st.markdown('<div class="sec-hdr">📈 PRICE, TECHNICALS & FINANCIAL ANALYSIS</div>', unsafe_allow_html=True)
        all_t = sorted(set(Q1_2026+STB_ALL))

        c1, c2 = st.columns([2, 1])
        with c1:
            ct = st.selectbox("Ticker", all_t, label_visibility="collapsed")
        with c2:
            view_mode = st.selectbox("View", [
                "📈 Candlestick + Bollinger",
                "💹 Revenue Growth vs Price",
                "📊 Full Financial Grid",
                "🗺️ Multi-Year Metric Map",
                "📉 Revenue Waterfall",
                "🔗 Correlation Matrix",
            ], label_visibility="collapsed")

        # ── Live snapshot bar ──
        info = get_info(ct)
        p, chg, _ = get_price(ct)
        snap_cols = st.columns(7)
        snaps = [
            ("PRICE",       f"${p:.2f}" if p else "—",       "up" if (chg or 0)>0 else "down"),
            ("24H CHANGE",  fmt_pct(chg, False),              "up" if (chg or 0)>0 else "down"),
            ("P/E",         f"{info.get('trailingPE','—'):.1f}" if info.get('trailingPE') else "—", ""),
            ("P/S",         f"{info.get('priceToSalesTrailing12Months','—'):.2f}" if info.get('priceToSalesTrailing12Months') else "—", ""),
            ("MCAP",        fmt_mcap(info.get("marketCap")), ""),
            ("REV GROWTH",  fmt_pct(info.get("revenueGrowth")), "up" if (info.get("revenueGrowth") or 0)>0 else "down"),
            ("EPS",         f"${info.get('trailingEps','—'):.2f}" if info.get('trailingEps') else "—", ""),
        ]
        for col, (lbl, val, vcls) in zip(snap_cols, snaps):
            clr = {"up":"var(--gn)","down":"var(--rd)"}.get(vcls,"var(--wh)")
            col.markdown(f'<div class="card"><div class="card-val" style="font-size:15px;color:{clr};">{val}</div><div class="card-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if "Candlestick" in view_mode:
            cp = st.select_slider("Period", options=["1mo","3mo","6mo","1y","2y","5y","max"], value="1y", label_visibility="collapsed")
            st.plotly_chart(chart_price(ct, cp), use_container_width=True)

        elif "Revenue Growth vs Price" in view_mode:
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:var(--dm);margin-bottom:8px;">Revenue bars (left axis) + Stock price at year-end (right axis, dotted cyan). Yellow line = revenue growth %.</div>', unsafe_allow_html=True)
            with st.spinner(f"Loading revenue & price history for {ct}..."):
                st.plotly_chart(chart_rev_vs_price(ct), use_container_width=True)

            # Show the numbers in a table too
            income2, _, _, hist2 = get_full_financials(ct)
            if income2 is not None and not income2.empty:
                rev_r = _safe_row(income2, "Total Revenue","Revenue")
                if rev_r is not None:
                    rev_s = rev_r.sort_index()
                    tbl_rows = []
                    prev_rev = None
                    for d, v in zip(rev_s.index, rev_s.values):
                        rv = float(v)/1e9
                        yr = str(d.year)
                        yr_hist = hist2[hist2.index.year == d.year] if not hist2.empty else pd.DataFrame()
                        avg_p = float(yr_hist["Close"].mean()) if not yr_hist.empty else None
                        yr_end_p = float(yr_hist["Close"].iloc[-1]) if not yr_hist.empty else None
                        grw = f"{(rv-prev_rev)/abs(prev_rev)*100:.1f}%" if prev_rev and prev_rev!=0 else "—"
                        tbl_rows.append({"Year":yr,"Revenue ($B)":f"${rv:.2f}B","Rev Growth":grw,
                                          "Avg Price":f"${avg_p:.2f}" if avg_p else "—",
                                          "Year-End Price":f"${yr_end_p:.2f}" if yr_end_p else "—"})
                        prev_rev = rv
                    st.dataframe(pd.DataFrame(tbl_rows), use_container_width=True, height=220)

        elif "Full Financial Grid" in view_mode:
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:var(--dm);margin-bottom:8px;">Revenue · EBITDA · Net Income Growth % · Free Cash Flow — all available annual data.</div>', unsafe_allow_html=True)
            with st.spinner(f"Loading full financials for {ct}..."):
                st.plotly_chart(chart_all_metrics_grid(ct), use_container_width=True)

            # Detailed table
            income3, cf3, bal3, _ = get_full_financials(ct)
            if income3 is not None and not income3.empty:
                with st.expander("📋 Raw Annual Financials Table"):
                    show_rows = ["Total Revenue","Gross Profit","EBITDA","Operating Income",
                                 "Net Income","Diluted EPS","Reconciled Depreciation"]
                    available_rows = [r for r in show_rows if r in income3.index]
                    if available_rows:
                        df_show = income3.loc[available_rows].copy()
                        df_show = df_show.applymap(lambda x: f"${float(x)/1e9:.2f}B" if pd.notna(x) and abs(float(x))>=1e6 else (f"{float(x):.3f}" if pd.notna(x) else "—"))
                        df_show.columns = [str(c.year) for c in df_show.columns]
                        st.dataframe(df_show, use_container_width=True)

        elif "Multi-Year Metric Map" in view_mode:
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:11px;color:var(--dm);margin-bottom:8px;">Select any metric — shows all available annual data with trend line overlaid.</div>', unsafe_allow_html=True)
            with st.spinner(f"Loading metrics for {ct}..."):
                result = chart_multiyear_map(ct, "Revenue ($B)")

            if isinstance(result, tuple):
                fig_map, available_metrics, metrics_dict = result
                sel_metric = st.selectbox("Select metric to map", available_metrics, label_visibility="collapsed")
                result2 = chart_multiyear_map(ct, sel_metric)
                if isinstance(result2, tuple):
                    st.plotly_chart(result2[0], use_container_width=True)

                # All metrics table side by side
                with st.expander("📋 All Metrics — Year by Year"):
                    all_years = sorted(set(y for d in metrics_dict.values() for y in d.keys()))
                    tbl = {"Year": all_years}
                    for m, d in metrics_dict.items():
                        tbl[m] = [d.get(y, "—") for y in all_years]
                    st.dataframe(pd.DataFrame(tbl), use_container_width=True, height=280)

                # PE/PS/EPS comparison cards
                st.markdown('<div class="sec-hdr" style="font-size:14px;">📊 KEY RATIOS — LATEST vs HISTORICAL AVG</div>', unsafe_allow_html=True)
                ratio_cols = st.columns(4)
                def ratio_card(col, label, current, hist_avg):
                    if current is None: return
                    diff = current - hist_avg if hist_avg else 0
                    clr  = "var(--rd)" if diff > hist_avg*0.2 else "var(--gn)" if diff < -hist_avg*0.1 else "var(--am)"
                    col.markdown(f'<div class="card"><div class="card-val" style="font-size:18px;color:{clr};">{current:.1f}</div>'
                                 f'<div class="card-lbl">{label}</div>'
                                 f'<div class="card-chg flat">5yr avg: {hist_avg:.1f}</div></div>', unsafe_allow_html=True)

                pe_d = metrics_dict.get("P/E (approx)",{})
                ps_d = metrics_dict.get("P/S (approx)",{})
                rg_d = metrics_dict.get("Rev Growth %",{})
                eg_d = metrics_dict.get("EPS Growth %",{})

                if pe_d:
                    vals_pe = [v for v in pe_d.values() if v is not None]
                    ratio_card(ratio_cols[0], "P/E (latest)", list(pe_d.values())[-1] if pe_d else None, np.mean(vals_pe) if vals_pe else 0)
                if ps_d:
                    vals_ps = [v for v in ps_d.values() if v is not None]
                    ratio_card(ratio_cols[1], "P/S (latest)", list(ps_d.values())[-1] if ps_d else None, np.mean(vals_ps) if vals_ps else 0)
                if rg_d:
                    vals_rg = [v for v in rg_d.values() if v is not None]
                    ratio_card(ratio_cols[2], "Rev Growth % (latest)", list(rg_d.values())[-1] if rg_d else None, np.mean(vals_rg) if vals_rg else 0)
                if eg_d:
                    vals_eg = [v for v in eg_d.values() if v is not None]
                    ratio_card(ratio_cols[3], "EPS Growth % (latest)", list(eg_d.values())[-1] if eg_d else None, np.mean(vals_eg) if vals_eg else 0)
            else:
                st.info("Not enough data to build metric map.")

        elif "Revenue Waterfall" in view_mode:
            with st.spinner(f"Loading waterfall for {ct}..."):
                st.plotly_chart(chart_waterfall(ct), use_container_width=True)

        elif "Correlation Matrix" in view_mode:
            sel = st.multiselect("Select tickers", all_t, default=Q1_2026[:14], label_visibility="collapsed")
            if sel:
                with st.spinner("Computing 1yr correlations..."):
                    st.plotly_chart(chart_correlation(sel), use_container_width=True)

    # ════════════════════════════════════════════
    # TAB 3 — AUDIT ENGINE
    # ════════════════════════════════════════════
    with tab3:
        st.markdown('<div class="sec-hdr">🔬 7-ALGORITHM AUDIT ENGINE — AUTO-RUN ON STARTUP</div>', unsafe_allow_html=True)
        a_left, a_right = st.columns([1,2])

        with a_left:
            audit_t = st.selectbox("Select ticker",sorted(set(Q1_2026+STB_ALL)),label_visibility="collapsed")
            run_btn   = st.button("⚡ RUN FULL AUDIT",  use_container_width=True)
            batch_btn = st.button("🔄 BATCH: TOP 15",   use_container_width=True)

            if batch_btn:
                prog = st.progress(0)
                for i,t in enumerate(Q1_2026[:15]):
                    try:
                        res = run_full_audit(t)
                        st.session_state.audit_cache[t] = res
                        st.session_state.audit_log.append(res)
                    except Exception:
                        pass
                    prog.progress((i+1)/15,text=f"Auditing {t}...")
                st.session_state.last_run_time = datetime.now().strftime("%H:%M:%S")
                prog.empty()
                st.success("✅ Batch audit complete")

            if run_btn:
                with st.spinner(f"Running 7 algorithms on {audit_t}..."):
                    res = run_full_audit(audit_t)
                    st.session_state.audit_cache[audit_t] = res
                    st.session_state.audit_log.append(res)
                    st.session_state.last_run_time = datetime.now().strftime("%H:%M:%S")

            if audit_t in st.session_state.audit_cache:
                res   = st.session_state.audit_cache[audit_t]
                score = res.get("score",0)
                pr    = res.get("price",0) or 0
                chg   = res.get("change",0) or 0
                col   = "#00ff9d" if score>=80 else "#ffb800" if score>=60 else "#ff2d55"
                chg_c = "#00ff9d" if chg>=0 else "#ff2d55"
                st.markdown(f"""
                <div style="background:var(--s2);border:1px solid {col};border-radius:8px;padding:16px;margin-top:12px;">
                  <div style="font-family:Bebas Neue,monospace;font-size:26px;color:{col};">{audit_t}</div>
                  <div style="font-family:IBM Plex Mono,monospace;font-size:15px;color:#e8f2ff;">
                    ${pr:.2f} <span style="color:{chg_c}">{chg*100:+.2f}%</span></div>
                  <div style="margin-top:8px;font-size:10px;color:var(--dm);letter-spacing:2px;">AUDIT SCORE</div>
                  <div style="font-family:Bebas Neue,monospace;font-size:48px;color:{col};line-height:1;">
                    {score}<span style="font-size:18px;color:var(--dm)">/100</span></div>
                  <div style="font-size:10px;color:var(--dm);margin-top:4px;">Updated: {res.get('timestamp','—')}</div>
                </div>
                """, unsafe_allow_html=True)

        with a_right:
            if audit_t in st.session_state.audit_cache:
                res = st.session_state.audit_cache[audit_t]
                algo_display = [
                    ("A1 · Multi-Source Reconciliation",  res["A1"].get("status","—")),
                    ("A2 · Statistical Anomaly",           f"{res['A2'].get('status','—')}"),
                    ("A3 · Cash-Flow Logic Chain",         res["A3"].get("status","—")),
                    ("A4 · Data Freshness Score",          f"{res['A4'].get('status','—')} ({res['A4'].get('score','—')}%)"),
                    ("A5 · Historical Trend",              f"{res['A5'].get('status','—')} | CAGR={res['A5'].get('cagr_3y','—')}%"),
                    ("A6 · Guidance Back-Test",            res["A6"].get("status","—")),
                    ("A7 · Hypothesis & Valuation",        res["A7"].get("overall","—")),
                ]
                html = '<div class="audit-block">'
                for name, status in algo_display:
                    ok   = "✅" in status
                    warn = "⚠️" in status
                    clr  = "var(--gn)" if ok else "var(--am)" if warn else "var(--rd)" if "🚨" in status or "📉" in status else "var(--dm)"
                    html += f'<div class="algo-row"><span class="algo-name">{name}</span><span style="color:{clr};text-align:right;">{status}</span></div>'
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)

                # Quarters detail
                q = res["A6"].get("quarters",[])
                if q:
                    with st.expander("📋 EPS Beat/Miss History"):
                        st.dataframe(pd.DataFrame(q),use_container_width=True,height=200)

                # Hypothesis
                ch = res["A7"].get("checks",[])
                if ch:
                    with st.expander("🏆 Hypothesis Checks"):
                        for c in ch:
                            clr = "var(--gn)" if "✅" in c["status"] else "var(--am)"
                            st.markdown(f'<div class="algo-row"><span class="algo-name">{c["name"]}</span>'
                                        f'<span>Fair: <b>${c["fair"]}</b> · Live: <b>${c["live"]}</b> · '
                                        f'<b style="color:{clr}">{c["dev"]:+.1f}%</b> → {c["status"]}</span></div>',
                                        unsafe_allow_html=True)

        # Audit log
        if st.session_state.audit_log:
            st.markdown('<div class="sec-hdr" style="margin-top:16px;">📋 LIVE AUDIT LOG</div>', unsafe_allow_html=True)
            log_rows = []
            for a in reversed(st.session_state.audit_log[-30:]):
                log_rows.append({
                    "Time":   a.get("timestamp",""),
                    "Ticker": a.get("ticker",""),
                    "Score":  a.get("score",0),
                    "Price":  f"${a.get('price',0):.2f}" if a.get("price") else "—",
                    "A1": a["A1"].get("status","")[:16],
                    "A2": a["A2"].get("status","")[:18],
                    "A3": a["A3"].get("status","")[:18],
                    "A4": a["A4"].get("status","")[:12],
                    "A5": a["A5"].get("status","")[:18],
                    "A6": a["A6"].get("status","")[:20],
                })
            st.dataframe(pd.DataFrame(log_rows),use_container_width=True,height=280,
                column_config={"Score":st.column_config.ProgressColumn("Score",min_value=0,max_value=100,format="%d")})

    # ════════════════════════════════════════════
    # TAB 4 — PORTFOLIO
    # ════════════════════════════════════════════
    with tab4:
        st.markdown('<div class="sec-hdr">💰 BONUS PORTFOLIO — LIVE P&L</div>', unsafe_allow_html=True)
        rows = []; total_inv = total_curr = 0

        for r in BONUS_PORTFOLIO:
            p,chg,_ = get_price(r["ticker"])
            if not p: p = r["buy_price"]
            pct  = (p-r["buy_price"])/r["buy_price"]*100 if r["buy_price"] else 0
            curr = p*r["qty"]; inv = r["buy_price"]*r["qty"]
            total_inv += inv; total_curr += curr
            rows.append({
                "Ticker":   r["ticker"],"Name":r["name"],
                "Buy":      f"${r['buy_price']:.2f}","Live":f"${p:.2f}",
                "Qty":      r["qty"],
                "P&L %":    pct,"P&L $":curr-inv,"Curr Value":curr,
                "24H":      (chg or 0)*100,
                "Status":   "🟢 PROFIT" if pct>0 else "🔴 LOSS",
            })

        tp  = total_curr-total_inv
        tpct= tp/total_inv*100 if total_inv else 0
        mc1,mc2,mc3,mc4 = st.columns(4)
        mc1.markdown(f'<div class="card"><div class="card-val">${total_inv:,.0f}</div><div class="card-lbl">TOTAL INVESTED</div></div>',unsafe_allow_html=True)
        mc2.markdown(f'<div class="card"><div class="card-val">${total_curr:,.0f}</div><div class="card-lbl">CURRENT VALUE</div></div>',unsafe_allow_html=True)
        col3 = "green" if tp>=0 else "red"
        pnl_cls  = "up" if tp>=0 else "down"
        rpct_cls = "up" if tpct>=0 else "down"
        mc3.markdown(f'<div class="card {col3}"><div class="card-val {pnl_cls}">${tp:+,.0f}</div><div class="card-lbl">TOTAL P&L $</div></div>',unsafe_allow_html=True)
        mc4.markdown(f'<div class="card {col3}"><div class="card-val {rpct_cls}">{tpct:+.1f}%</div><div class="card-lbl">TOTAL RETURN</div></div>',unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        df_p = pd.DataFrame(rows)
        st.dataframe(df_p, use_container_width=True, height=340,
            column_config={
                "P&L %": st.column_config.NumberColumn("P&L %", format="%.2f%%"),
                "P&L $": st.column_config.NumberColumn("P&L $", format="$%.2f"),
                "24H":   st.column_config.NumberColumn("24H %", format="%.2f%%"),
                "Curr Value":st.column_config.NumberColumn("Value $",format="$%.2f"),
            })
        st.plotly_chart(chart_pnl(), use_container_width=True)

    # ════════════════════════════════════════════
    # TAB 5 — MARKET PULSE
    # ════════════════════════════════════════════
    with tab5:
        st.markdown('<div class="sec-hdr">🌐 MARKET PULSE — SECTORS & INDICES</div>', unsafe_allow_html=True)

        # Sectors
        sec_data = {}
        with st.spinner("Fetching sectors..."):
            for name, sym in SECTOR_ETFS.items():
                _,chg,_ = get_price(sym)
                if chg is not None: sec_data[name] = chg*100
        if sec_data:
            st.plotly_chart(chart_sector(sec_data), use_container_width=True)

        # Indices grid
        st.markdown('<div class="sec-hdr" style="margin-top:4px;">📊 GLOBAL INDICES</div>', unsafe_allow_html=True)
        icols = st.columns(4)
        for i,(name,sym) in enumerate(INDICES.items()):
            p,chg,_ = get_price(sym)
            if p:
                clr = "green" if (chg or 0)>0 else "red" if (chg or 0)<0 else ""
                tc  = "up" if (chg or 0)>0 else "down"
                icols[i%4].markdown(
                    f'<div class="card {clr}" style="margin-bottom:8px;">'
                    f'<div class="card-val" style="font-size:17px;">{p:,.2f}</div>'
                    f'<div class="card-lbl">{name}</div>'
                    f'<div class="card-chg {tc}">{fmt_pct(chg,False)}</div></div>',
                    unsafe_allow_html=True)

        # Earnings calendar
        st.markdown('<div class="sec-hdr" style="margin-top:8px;">📅 UPCOMING EARNINGS (14 DAYS)</div>', unsafe_allow_html=True)
        earns = []
        with st.spinner("Scanning earnings..."):
            for t in list(dict.fromkeys(Q1_2026+STB_ALL))[:30]:
                try:
                    info = get_info(t)
                    ts   = info.get("earningsTimestamp")
                    if ts:
                        dt   = datetime.fromtimestamp(ts)
                        diff = (dt-datetime.now()).days
                        if 0 <= diff <= 14:
                            earns.append({"Ticker":t,"Date":dt.strftime("%Y-%m-%d"),
                                          "Days Away":diff,"Company":info.get("shortName","")})
                except Exception:
                    pass
        if earns:
            st.dataframe(pd.DataFrame(earns).sort_values("Days Away"),use_container_width=True,height=200)
        else:
            st.info("No earnings detected in the next 14 days for tracked tickers.")

    # ════════════════════════════════════════════
    # TAB 6 — COMMAND CENTER
    # ════════════════════════════════════════════
    with tab6:
        st.markdown('<div class="sec-hdr">⚙️ COMMAND CENTER — QUICK LOOKUP & EXPORT</div>', unsafe_allow_html=True)
        cc1,cc2 = st.columns([2,3])

        with cc1:
            st.markdown("**⚡ INSTANT TICKER LOOKUP**")
            lookup = st.text_input("",placeholder="Enter any ticker: NVDA, TSLA, MSFT...",label_visibility="collapsed")
            if lookup:
                t_up = lookup.strip().upper()
                p,chg,_ = get_price(t_up)
                info     = get_info(t_up)
                if p:
                    clr  = "#00ff9d" if (chg or 0)>0 else "#ff2d55"
                    st.markdown(f"""
                    <div class="audit-block">
                      <div style="font-family:Bebas Neue,monospace;font-size:28px;color:var(--ac);">{t_up}</div>
                      <div style="font-family:IBM Plex Mono;font-size:16px;color:#e8f2ff;">
                        ${p:.4f} <span style="color:{clr}">{fmt_pct(chg,False)}</span></div>
                      <div style="margin-top:8px;font-size:11px;font-family:IBM Plex Mono;color:var(--dm);">
                        P/E: {info.get('trailingPE','—')} &nbsp;|&nbsp;
                        P/S: {info.get('priceToSalesTrailing12Months','—')} &nbsp;|&nbsp;
                        MCap: {fmt_mcap(info.get('marketCap'))}</div>
                      <div style="font-size:11px;font-family:IBM Plex Mono;color:var(--dm);">
                        Rev Growth: {fmt_pct(info.get('revenueGrowth'))} &nbsp;|&nbsp;
                        EPS: ${info.get('trailingEps','—')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"⚡ AUDIT {t_up}", use_container_width=False):
                        with st.spinner(f"Auditing {t_up}..."):
                            res = run_full_audit(t_up)
                            st.session_state.audit_cache[t_up] = res
                            st.session_state.audit_log.append(res)
                        st.success(f"Score: {res['score']}/100")
                else:
                    st.warning(f"No data for {t_up} — check ticker symbol")

            st.markdown("---")
            st.markdown("**📋 UNIVERSES**")
            vu = st.radio("",["Q1 2026","STB All","Bonus"],horizontal=True,label_visibility="collapsed")
            if vu=="Q1 2026":
                st.write(" | ".join([f"**{t}**" for t in Q1_2026]))
            elif vu=="STB All":
                st.write(" | ".join([f"**{t}**" for t in STB_ALL]))
            else:
                for r in BONUS_PORTFOLIO:
                    st.markdown(f"**{r['ticker']}** — {r['name']} @ ${r['buy_price']}")

        with cc2:
            st.markdown("**📥 EXPORT AUDIT LOG**")
            if st.session_state.audit_log:
                export = []
                for a in st.session_state.audit_log:
                    export.append({
                        "Ticker":a.get("ticker",""),"Score":a.get("score",""),
                        "Price":a.get("price",""),"Timestamp":a.get("timestamp",""),
                        "A1":a["A1"].get("status",""),"A2":a["A2"].get("status",""),
                        "A3":a["A3"].get("status",""),"A4":a["A4"].get("status",""),
                        "A5":a["A5"].get("status",""),"A6":a["A6"].get("status",""),
                        "A7":a["A7"].get("overall",""),
                    })
                buf = BytesIO()
                pd.DataFrame(export).to_excel(buf,index=False,engine="xlsxwriter")
                buf.seek(0)
                st.download_button("📥 DOWNLOAD AUDIT LOG (.xlsx)", buf,
                                   "pykupz_audit_log.xlsx", use_container_width=False)

            st.markdown("---")
            st.markdown("**ℹ️ TERMINAL STATS**")
            st.markdown(f"""
            - **Tickers tracked:** {len(set(Q1_2026+STB_ALL))}
            - **Audits completed:** {len(st.session_state.audit_cache)}
            - **Audit log entries:** {len(st.session_state.audit_log)}
            - **Auto-refresh:** Every 60 seconds (refresh #{refresh_count})
            - **Last startup audit:** {st.session_state.last_run_time or "—"}
            - **Data source:** Yahoo Finance (yfinance) — 100% live
            - **Algorithms:** 7 (Multi-Source, Z-Score, CF Chain, Freshness, Trend, Guidance, Hypothesis)
            """)

    # ── FOOTER ──
    st.markdown(f"""
    <div style="text-align:center;font-family:IBM Plex Mono,monospace;font-size:9px;
    color:#162040;letter-spacing:3px;padding:12px 0 4px;border-top:1px solid #162040;margin-top:12px;">
      PYKUPZ LIVE TERMINAL · HEDGE FUND EDITION · YAHOO FINANCE DATA ·
      AUTO-REFRESH 60s · {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} · NOT FINANCIAL ADVICE
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════════
# HOW TO RUN:
# 1. pip install streamlit streamlit-autorefresh pandas plotly yfinance numpy scipy openpyxl xlsxwriter
# 2. Save code as pykupz_terminal.py
# 3. streamlit run pykupz_terminal.py
# 4. App opens automatically — fully live, no Excel upload needed
# 5. Deploy: push to GitHub → share.streamlit.io → Deploy → done
# ═══════════════════════════════════════════════════════════════════════
