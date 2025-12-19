# IFA QUANTUM | INSTITUTIONAL TERMINAL
# Developed by: Santino Domeniconi
# Copyright (c) 2025 - All Rights Reserved

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from io import BytesIO
import os

st.set_page_config(
    page_title="IFA QUANTUM",
    layout="wide",
    initial_sidebar_state="expanded"
)

LANG_MAP = {"Español": "ES", "English": "EN"}
LANG_MAP_REVERSE = {v: k for k, v in LANG_MAP.items()}
LANG_OPTIONS = list(LANG_MAP.keys())

if not os.path.exists(".streamlit"):
    os.makedirs(".streamlit")

config_toml = """
[theme]
base="dark"
primaryColor="#EF4444" 
backgroundColor="#0f172a"
secondaryBackgroundColor="#1e293b"
textColor="#f8fafc"
font="sans serif"
"""
try:
    with open(".streamlit/config.toml", "w") as f:
        f.write(config_toml.strip())
except:
    pass

# CSS - AQUI ESTA LA CORRECCION VISUAL
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp { 
        background-color: #020617;
        background-image: 
            radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
    }

    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.95) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #000000 !important;
        fill: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }
    ul[data-baseweb="menu"] { background-color: #FFFFFF !important; }
    li[data-baseweb="option"] { color: #000000 !important; }
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #E2E8F0 !important;
        color: #000000 !important;
    }
    
    /* ESTILOS DE INPUTS Y TEXTAREAS */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
    }
    
    /* --- CORRECCION: PLACEHOLDERS GRIS OSCURO --- */
    [data-testid="stSidebar"] input::placeholder,
    [data-testid="stSidebar"] textarea::placeholder {
        color: #64748b !important; /* Gris oscuro para visibilidad */
        opacity: 1 !important;
    }
    /* -------------------------------------------- */

    [data-testid="stSidebar"] [data-testid="stDateInput"] div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stDateInput"] input {
          color: #000000 !important;
    }

    [data-testid="stTooltipIcon"] {
        opacity: 1 !important;
        filter: brightness(0) invert(1) !important;
    }
    [data-testid="stTooltipIcon"] > svg {
        width: 18px !important;
        height: 18px !important;
    }

    .stButton > button, [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
        color: #FFFFFF !important; 
        border: none !important;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 700;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
        text-transform: uppercase;
        margin: 0 auto;
        display: block;
        width: 100%;
    }
    
    [data-testid="stDownloadButton"] > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: #FFFFFF !important; 
    }
    [data-testid="stDownloadButton"] > button:hover {
        color: #FFFFFF !important;
    }

    [data-testid="stMetric"] {
        background: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    [data-testid="stMetricLabel"] { color: #FFFFFF !important; font-size: 0.85rem !important; opacity: 0.9; }
    [data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-weight: 800 !important; font-size: 2rem !important; }

    .feature-card {
        background: rgba(20, 20, 20, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .landing-title {
        font-size: 4rem; font-weight: 900; text-align: center;
        background: linear-gradient(to right, #60A5FA, #34D399);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }

    [data-testid="stDataFrame"] { background: transparent !important; }
    h1, h2, h3, h4, h5 { color: white !important; }
    .footer { color: #94A3B8 !important; text-align: center; padding: 20px; font-size: 0.8rem; }
    div[data-testid="column"] { background: transparent !important; }
    
    button[data-baseweb="tab"] {
        color: #FFFFFF !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #60A5FA !important;
        border-bottom-color: #60A5FA !important;
    }
    
    .yahoo-btn {
        background-color: #723499; /* Yahoo Purple */
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 4px 12px;
        height: 28px;
        display: flex;
        justify-content: center;
        align-items: center;
        text-decoration: none;
        margin-left: 10px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(114, 52, 153, 0.4);
        width: fit-content;
    }

    .yahoo-btn:hover {
        background-color: #6001d2; 
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(114, 52, 153, 0.6);
    }

    .yahoo-btn svg {
        fill: none;
        width: 14px;
        height: 14px;
        display: block;
        margin-right: 6px;
    }
    
    .yahoo-text {
        color: #FFFFFF;
        font-size: 0.75rem;
        font-weight: 700;
        white-space: nowrap;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }

    .ticker-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .ticker-title {
        color: #FFFFFF; 
        font-size: 0.9rem; 
        font-weight: 600;
    }
    
    .highlight-card {
        background: rgba(30, 41, 59, 0.9) !important; 
        border: 2px solid #3B82F6 !important; 
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.3) !important;
    }

</style>
""", unsafe_allow_html=True)

# LÓGICA DE TRADUCCIÓN Y ESTADO
if 'started' not in st.session_state: st.session_state.started = False
if 'lang' not in st.session_state: st.session_state.lang = "ES"

TRANSLATIONS = {
    "ES": {
        "landing_title": "IFA QUANTUM", "landing_sub": "Plataforma de Gestión de Activos Institucional",
        "feat_1": "Datos en Vivo", "feat_1_d": "Conexión directa a mercados globales vía API de alta frecuencia",
        "feat_2": "Motor Markowitz", "feat_2_d": "Algoritmos de frontera eficiente para maximizar el Ratio de Sharpe",
        "feat_3": "Stress Testing", "feat_3_d": "Simulaciones de Monte Carlo para análisis de escenarios de riesgo",
        "enter": "Iniciar Terminal", "config": "Configuración", "assets": "Selección de Activos",
        "sim_cap": "Simular Capital Real", "amount": "Capital (USD)", "sims": "Iteraciones",
        "date": "Inicio de Análisis", "run": "EJECUTAR MODELO", "exit": "CERRAR SESIÓN",
        "mkt": "Análisis de Mercado", "proc": "Procesando datos...",
        "t1": "Frontera Eficiente", "t2": "Asignación y Compra", 
        "t3": "Análisis de Caída", 
        "t4": "Exportar Datos", "t5": "Correlaciones", 
        "t6": "Análisis de Riesgo", 
        "ret": "Retorno Esperado", "vol": "Volatilidad",
        "sha": "Ratio Sharpe", "cap": "Proyección", "alloc": "Asignación Óptima",
        "down": "Descargar Reporte en Formato Excel", "err_min": "Seleccione al menos 2 activos",
        "buy_order": "Orden de Compra Sugerida", "empty_title": "Sistema Preparado",
        "empty_desc": "Configure los parámetros en el panel lateral para iniciar el cálculo",
        "col_asset": "Activo", "col_weight": "Porcentaje", "col_val": "Valor ($)",
        "opt_port": "Máximo Ratio Sharpe", "sb_width": "Ancho Barra Lateral (px)",
        "m_invest": "Ganancia Neta", "fx_rate": "Tipo de Cambio", "fx_help": "Valor de 1 USD en moneda local",
        "start_p": "Inicio", "yield": "Rendimiento", "type": "Tipo",
        "var": "VaR 95% (Diario)", "cvar": "CVaR 95% (Déficit Esperado)", "sortino": "Ratio Sortino",
        "dist_title": "Distribución de Retornos del Portafolio", "confidence": "Nivel de Confianza",
        "dd_trace": "Caída Acumulada",
        "fav_label": "Favoritos",
        "manual_usd_tickers_label": "Activos Internacionales (USD)", 
        "ph_intl": "Ej: GLD, QQQ, TSLA, BTC-USD", 
        "ph_loc": "Ej: EDN.BA, AGRO.BA, GGAL.BA",
        "sec_intl": "Activos Internacionales (USD)", 
        "sec_loc": "Activos Locales (Ajuste por tipo de cambio)" 
    },
    "EN": {
        "landing_title": "IFA QUANTUM", "landing_sub": "Institutional Asset Management Platform",
        "feat_1": "Live Market Data", "feat_1_d": "Direct connection to global markets via high-frequency API",
        "feat_2": "Markowitz Engine", "feat_2_d": "Efficient frontier algorithms to maximize Sharpe Ratio",
        "feat_3": "Stress Testing", "feat_3_d": "Monte Carlo simulations for risk scenario analysis",
        "enter": "Launch Terminal", "config": "Configuration", "assets": "Asset Selection",
        "sim_cap": "Simulate Capital", "amount": "Capital (USD)", "sims": "Iterations",
        "date": "Start Date", "run": "RUN MODEL", "exit": "LOG OUT",
        "mkt": "Market Analysis", "proc": "Processing data...",
        "t1": "Efficient Frontier", "t2": "Allocation & Buy Order", "t3": "Drawdown Analysis",
        "t4": "Export Data", "t5": "Correlations",
        "t6": "Risk Engine",
        "ret": "Expected Return", "vol": "Volatility",
        "sha": "Sharpe Ratio", "cap": "Projection", "alloc": "Optimal Allocation",
        "down": "Download Report in Excel Format", "err_min": "Select at least 2 assets",
        "buy_order": "Suggested Buy Order", "empty_title": "System Ready",
        "empty_desc": "Configure parameters in the sidebar to start calculations",
        "col_asset": "Asset", "col_weight": "Percentage", "col_val": "Value ($)",
        "opt_port": "Max Sharpe Ratio", "sb_width": "Sidebar Width (px)",
        "m_invest": "Net Profit", "fx_rate": "Exchange Rate", "fx_help": "1 USD value in local currency",
        "start_p": "Start", "yield": "Yield", "type": "Type",
        "var": "VaR 95% (Daily)", "cvar": "CVaR 95% (Expected Shortfall)", "sortino": "Sortino Ratio",
        "dist_title": "Portfolio Return Distribution", "confidence": "Confidence Level",
        "dd_trace": "Cumulative Drawdown",
        "fav_label": "Favorites",
        "manual_usd_tickers_label": "International Assets (USD)",
        "ph_intl": "Ex: GLD, QQQ, TSLA, BTC-USD", 
        "ph_loc": "Ex: EDN.BA, AGRO.BA, GGAL.BA",
        "sec_intl": "International Assets (USD)", 
        "sec_loc": "Local Assets (Exchange Rate Adjusted)" 
    }
}

ASSET_TYPE_MAP = {
    "ES": {"EQUITY": "ACCIÓN", "CRYPTOCURRENCY": "CRIPTO", "ETF": "ETF", "FUTURE": "FUTURO", "INDEX": "ÍNDICE", "CURRENCY": "DIVISA", "Unknown": "-"},
    "EN": {"EQUITY": "STOCK", "CRYPTOCURRENCY": "CRYPTO", "ETF": "ETF", "FUTURE": "FUTURE", "INDEX": "INDEX", "CURRENCY": "CURRENCY", "Unknown": "-"}
}

def txt(key): return TRANSLATIONS[st.session_state.lang][key]
COMMON_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "GLD", "BTC-USD", "ETH-USD", "SPY", "QQQ", "V", "KO", "PEP"]

# --- FUNCIONES DE DATOS (VERSIÓN FIX ZONA HORARIA) ---
@st.cache_data(ttl=3600)
def get_mixed_currency_data(intl_tickers, local_tickers, start_date, fx_rate):
    """
    Descarga tolerante a fallos y normaliza Zonas Horarias (TZ) para evitar errores de Merge.
    """
    df_intl = pd.DataFrame()
    df_local = pd.DataFrame()

    # 1. Internacionales
    if intl_tickers:
        try:
            data_i = yf.download(intl_tickers, start=start_date, progress=False, auto_adjust=False)
            if isinstance(data_i.columns, pd.MultiIndex):
                try: df_intl = data_i['Adj Close']
                except KeyError: df_intl = data_i['Close']
            else:
                if 'Adj Close' in data_i.columns: df_intl = data_i[['Adj Close']]
                elif 'Close' in data_i.columns: df_intl = data_i[['Close']]
                else: df_intl = data_i
            
            # ELIMINAR ZONA HORARIA
            if not df_intl.empty:
                df_intl.index = df_intl.index.tz_localize(None)

            if len(intl_tickers) == 1:
                if isinstance(df_intl, pd.Series): df_intl = df_intl.to_frame(name=intl_tickers[0])
                elif isinstance(df_intl, pd.DataFrame): df_intl.columns = intl_tickers
        except Exception as e: st.warning(f"Error Int: {e}")

    # 2. Locales
    if local_tickers:
        try:
            data_l = yf.download(local_tickers, start=start_date, progress=False, auto_adjust=False)
            if isinstance(data_l.columns, pd.MultiIndex):
                try: df_local = data_l['Adj Close']
                except KeyError: df_local = data_l['Close']
            else:
                if 'Adj Close' in data_l.columns: df_local = data_l[['Adj Close']]
                elif 'Close' in data_l.columns: df_local = data_l[['Close']]
                else: df_local = data_l
            
            # ELIMINAR ZONA HORARIA
            if not df_local.empty:
                df_local.index = df_local.index.tz_localize(None)
            
            if len(local_tickers) == 1:
                if isinstance(df_local, pd.Series): df_local = df_local.to_frame(name=local_tickers[0])
                elif isinstance(df_local, pd.DataFrame): df_local.columns = local_tickers
            
            # Ajuste FX
            if fx_rate and fx_rate != 0:
                df_local = df_local / fx_rate
        except Exception as e: st.warning(f"Error Loc: {e}")

    if df_intl.empty and df_local.empty: return pd.DataFrame()
    
    full_df = pd.concat([df_intl, df_local], axis=1)
    
    full_df = full_df.ffill()
    full_df = full_df.dropna(how='all')
    full_df = full_df.dropna(axis=1, how='all')
    full_df = full_df.bfill().dropna()

    return full_df

@st.cache_data(ttl=3600)
def get_asset_details_v2(tickers):
    details = {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            info = tk.info
            y, d = info.get('yield', None), info.get('dividendYield', None)
            val_str = f"{(y if y else d)*100:.2f}%" if (y or d) else "-"
            q_type = info.get('quoteType', 'Unknown')
            details[t] = {"Type": q_type, "Yield": val_str, "Valid": True} 
        except: details[t] = {"Type": "Unknown", "Yield": "-", "Valid": False} 
    return details

# PANTALLA DE INICIO
def show_landing():
    col_l1, col_l2 = st.columns([10, 2])
    with col_l2:
        curr = LANG_MAP_REVERSE[st.session_state.lang]
        sel = st.selectbox("IDIOMA/LANGUAGE", LANG_OPTIONS, index=LANG_OPTIONS.index(curr), label_visibility="collapsed")
        if LANG_MAP[sel] != st.session_state.lang:
            st.session_state.lang = LANG_MAP[sel]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<div class="landing-title">{txt("landing_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="text-align: center; color: white; font-size: 1.5rem; margin-bottom: 4rem;">{txt("landing_sub")}</div>', unsafe_allow_html=True)
    
    icon_chart = """<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>"""
    icon_cpu = """<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>"""
    icon_shield = """<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>"""

    c1, c2, c3 = st.columns(3, gap="large")
    def render_card(icon, title, desc):
        return f"""
        <div class="feature-card">
            <div style="margin-bottom: 20px;">{icon}</div>
            <h3 style="margin-bottom: 10px; color: white; font-weight: 700;">{title}</h3>
            <p style="color: #FFFFFF; font-size: 1rem; line-height: 1.6;">{desc}</p>
        </div>
        """
    with c1: st.markdown(render_card(icon_chart, txt("feat_1"), txt("feat_1_d")), unsafe_allow_html=True)
    with c2: st.markdown(render_card(icon_cpu, txt("feat_2"), txt("feat_2_d")), unsafe_allow_html=True)
    with c3: st.markdown(render_card(icon_shield, txt("feat_3"), txt("feat_3_d")), unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    _, btn_col, _ = st.columns([5, 3, 5])
    with btn_col:
        st.markdown("""<style>div.stButton > button:first-child { min-height: 65px; font-size: 1.3rem; margin: 0 auto; }</style>""", unsafe_allow_html=True)
        if st.button(txt("enter"), use_container_width=True):
            st.session_state.started = True
            st.rerun()

# DASHBOARD PRINCIPAL
def show_dashboard():
    with st.sidebar:
        st.markdown(f"<h2 style='text-align: center; background: linear-gradient(to right, #60A5FA, #34D399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; margin-bottom: 20px;'>IFA QUANTUM</h2>", unsafe_allow_html=True)
        curr_s = LANG_MAP_REVERSE[st.session_state.lang]
        sel_s = st.selectbox("Idioma / Language", LANG_OPTIONS, index=LANG_OPTIONS.index(curr_s))
        if LANG_MAP[sel_s] != st.session_state.lang:
            st.session_state.lang = LANG_MAP[sel_s]
            st.rerun()
            
        st.markdown("---")
        st.write(f"### {txt('config')}")
        sb_width = st.slider(txt("sb_width"), 250, 500, 320, 10)
        st.markdown(f"""<style>[data-testid="stSidebar"] {{ min-width: {sb_width}px !important; max-width: {sb_width}px !important; }}</style>""", unsafe_allow_html=True)

        with st.form("conf_form"):
            st.write(f"### {txt('assets')}")
            
            # INTERNACIONALES (USD)
            st.markdown(f"##### {txt('sec_intl')}")
            predefined_tickers = st.multiselect(
                txt("fav_label"), 
                COMMON_TICKERS, 
                default=["AAPL", "MSFT", "NVDA", "BTC-USD"]
            )
            
            manual_intl_input = st.text_area(
                txt("manual_usd_tickers_label"), 
                placeholder=txt("ph_intl"),
                height=68
            )
            
            # LOCALES
            st.markdown(f"##### {txt('sec_loc')}") 
            local_tickers_input = st.text_area(
                "manual_loc_label_fix", # Label único
                label_visibility="collapsed", 
                placeholder=txt("ph_loc"),
                height=68
            )

            list_intl = [t.strip().upper() for t in manual_intl_input.replace('\n', ',').split(',') if t.strip()]
            final_intl = list(set(predefined_tickers + list_intl))
            final_local = [t.strip().upper() for t in local_tickers_input.replace('\n', ',').split(',') if t.strip()]

            total_assets = len(final_intl) + len(final_local)
            if total_assets > 0:
                st.caption(f"Activos: {len(final_intl)} Intl + {len(final_local)} Loc")

            st.markdown("---")
            st.caption("Parámetros")
            
            # TIPO DE CAMBIO
            fx_rate = st.number_input(
                f"{txt('fx_rate')} (USD/Local)", 
                min_value=1.0, value=1200.0, step=10.0
            )
            
            sel_sims = st.slider(txt("sims"), 1000, 20000, 5000, step=1000)
            c_date = st.date_input(txt("date"), date.today()-timedelta(days=365))
            
            st.markdown("---")
            use_cap = st.checkbox(txt("sim_cap"), value=True)
            val_cap = st.number_input(txt("amount"), min_value=100, value=10000, step=1000, format="%d") if use_cap else 10000
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button(txt("run"), use_container_width=True)

        st.markdown("<div style='margin-top: auto; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        if st.button(txt("exit"), use_container_width=True):
            st.session_state.started = False
            st.rerun()

    if not submitted and 'run_data' not in st.session_state:
        st.markdown(f"""<div style="text-align:center; margin-top:15vh; opacity:0.6;"><h2 style="color:white;">{txt('empty_title')}</h2><p style="color:white;">{txt('empty_desc')}</p></div>""", unsafe_allow_html=True)
        return

    if submitted:
        if (len(final_intl) + len(final_local)) < 2:
            st.error(txt("err_min"))
            return
        with st.spinner(txt("proc")):
            import time
            time.sleep(0.5)
            
            df = get_mixed_currency_data(final_intl, final_local, c_date, fx_rate)
            
            if df.empty or len(df.columns) < 2:
                st.error("Error: Datos insuficientes, Verifique los tickets")
                valid_tickers_on_fail = []
                temp_details = get_asset_details_v2(final_intl + final_local)
                for t, info in temp_details.items():
                    if info['Valid']:
                        valid_tickers_on_fail.append(t)
                
                if len(valid_tickers_on_fail) < 2:
                    st.error(f"Error: No se pudieron obtener datos válidos para al menos 2 activos. Tickets fallidos: {', '.join(set(final_intl + final_local) - set(valid_tickers_on_fail))}")
                    return

                df = df[valid_tickers_on_fail]
                valid_tickers = valid_tickers_on_fail
            else:
                valid_tickers = df.columns.tolist()

            asset_details = get_asset_details_v2(valid_tickers)
            log_ret = np.log(df / df.shift(1))
            mean_ret = log_ret.mean() * 252
            cov_mat = log_ret.cov() * 252
            weights = np.random.random((sel_sims, len(valid_tickers)))
            weights /= weights.sum(axis=1)[:, np.newaxis]
            port_ret = np.dot(weights, mean_ret.values)
            port_vol = np.sqrt(np.einsum('ij,jk,ik->i', weights, cov_mat.values, weights))
            port_sharpe = (port_ret - 0.04) / port_vol
            best_idx = port_sharpe.argmax()
            
            st.session_state.run_data = {
                'df': df, 'details': asset_details,
                'res': (port_ret, port_vol, port_sharpe),
                'best': (weights[best_idx], port_ret[best_idx], port_vol[best_idx], port_sharpe[best_idx]),
                'tickers': valid_tickers, 'cap': val_cap if use_cap else None, 'weights': weights 
            }

    data = st.session_state.run_data
    tickers = data['tickers']
    df = data['df']
    details = data['details']
    best_w, best_r, best_v, best_s = data['best']
    sim_r, sim_v, sim_s = data['res']
    capital = data['cap']

    st.markdown(f"<h3 style='color: white; margin-bottom: 20px;'>{txt('mkt')}</h3>", unsafe_allow_html=True)
    cols = st.columns(min(len(tickers), 4))

    yahoo_svg = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>'

    for i, t in enumerate(tickers):
        col_idx = i % 4
        if col_idx == 0 and i > 0:
            st.write("")
            cols = st.columns(min(len(tickers) - i, 4))
        
        try:
            curr_p = df[t].iloc[-1]
            start_p = df[t].iloc[0]
            delta = ((curr_p - start_p) / start_p) * 100
            arrow = "▲" if delta >= 0 else "▼"
            color = "#4ADE80" if delta >= 0 else "#F87171"
            info = details.get(t, {})
            
            raw_type = info.get('Type', 'Unknown')
            display_type = ASSET_TYPE_MAP[st.session_state.lang].get(raw_type, raw_type)
            
            is_valid_ticker = info.get('Valid', False)
            card_class = "highlight-card" if is_valid_ticker else ""

            yahoo_url = f"https://finance.yahoo.com/quote/{t}"
            
            html_card = f"""
<div class="{card_class}" style='background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-bottom: 10px;'>
    <div class='ticker-header'>
        <div class='ticker-title'>{t}</div>
        <a href="{yahoo_url}" target="_blank" class="yahoo-btn" title="Ver en Yahoo Finance">
            {yahoo_svg}
            <span class="yahoo-text">Yahoo Finance</span>
        </a>
    </div>
    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;'>
        <div style='font-size: 1.4rem; font-weight: 800; color: #FFFFFF;'>${curr_p:,.2f}</div>
        <div style='color: {color}; font-weight: 900; font-size: 0.9rem; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 6px; white-space: nowrap;'>{arrow} {delta:.2f}%</div>
    </div>
    <div style='font-size: 0.8rem; color: #FFFFFF; margin-bottom: 12px; opacity: 0.8;'>{txt('start_p')}: ${start_p:,.2f}</div>
    <div style='border-top: 1px solid rgba(255,255,255,0.2); padding-top: 10px;'>
        <div style='display: flex; justify-content: space-between; font-size: 0.75rem; color: #FFFFFF;'>
            <span style='opacity: 0.7;'>{txt('yield')}:</span> <span style='font-weight: 600;'>{info.get('Yield','-')}</span>
        </div>
        <div style='display: flex; justify-content: space-between; font-size: 0.75rem; color: #FFFFFF; margin-top: 4px;'>
            <span style='opacity: 0.7;'>{txt('type')}:</span> <span style='font-weight: 600;'>{display_type}</span>
        </div>
    </div>
</div>"""
            cols[col_idx].markdown(html_card, unsafe_allow_html=True)
        except: cols[col_idx].write("-")

    st.markdown("---")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(txt("ret"), f"{best_r:.1%}")
    k2.metric(txt("vol"), f"{best_v:.1%}")
    k3.metric(txt("sha"), f"{best_s:.2f}")
    k4.metric(txt("cap"), f"${capital*(1+best_r):,.0f}" if capital else "-", f"{txt('m_invest')}: ${capital*best_r:,.0f}" if capital else None)
    
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab6, tab4, tab5 = st.tabs([txt('t1'), txt('t2'), txt('t3'), txt('t6'), txt('t5'), txt('t4')])
    
    common = dict(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#FFFFFF', family="Inter"), 
        title_font=dict(color='#FFFFFF'),
        xaxis=dict(gridcolor='#334155', title_font=dict(color='#FFFFFF'), tickfont=dict(color='#FFFFFF')), 
        yaxis=dict(gridcolor='#334155', title_font=dict(color='#FFFFFF'), tickfont=dict(color='#FFFFFF')),
        legend=dict(font=dict(color='#FFFFFF'))
    )

    with tab1:
        fig = px.scatter(x=sim_v, y=sim_r, color=sim_s, color_continuous_scale='Viridis', labels={'x':txt('vol'), 'y':txt('ret')}, title=txt('t1'))
        fig.add_trace(go.Scatter(x=[best_v], y=[best_r], mode='markers', marker=dict(color='#EF4444', size=20, symbol='star'), name=txt('opt_port')))
        fig.update_layout(**common, height=550)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        c_pie, c_tbl = st.columns(2)
        with c_pie:
            mask = best_w > 0.01
            fig_p = px.pie(names=np.array(tickers)[mask], values=best_w[mask], hole=0.6, title=txt("alloc"), color_discrete_sequence=px.colors.qualitative.Bold)
            fig_p.update_layout(**common, height=450)
            st.plotly_chart(fig_p, use_container_width=True)
        with c_tbl:
            if capital:
                odf = pd.DataFrame({txt('col_asset'): tickers, txt('col_weight'): best_w, txt('col_val'): best_w * capital}).sort_values(txt('col_weight'), ascending=False)
                st.dataframe(odf.style.format({txt('col_weight'):'{:.1%}', txt('col_val'):'${:,.2f}'}).background_gradient('Blues', subset=[txt('col_weight')]), use_container_width=True, height=400)

    with tab3:
        dd = (1 + (df.pct_change().dropna() @ best_w)).cumprod()
        dd = (dd / dd.cummax()) - 1
        fig_d = go.Figure(go.Scatter(x=dd.index, y=dd, fill='tozeroy', line=dict(color='#EF4444'), name=txt('dd_trace')))
        fig_d.update_layout(
            **common, 
            title=dict(
                text=txt('t3'),
                font=dict(color='#FFFFFF', size=20, family="Inter")
            ),
            height=450
        )
        fig_d.update_yaxes(tickformat='.1%')
        st.plotly_chart(fig_d, use_container_width=True)

    with tab6:
        # RISK ENGINE
        daily_ret = df.pct_change().dropna()
        port_daily = daily_ret.dot(best_w)
        
        var_95 = np.percentile(port_daily, 5)
        cvar_95 = port_daily[port_daily <= var_95].mean()
        downside_std = port_daily[port_daily < 0].std()
        sortino = (port_daily.mean() / downside_std * np.sqrt(252)) if downside_std != 0 else 0

        r1, r2, r3 = st.columns(3)
        r1.metric(txt("var"), f"{var_95:.2%}")
        r2.metric(txt("cvar"), f"{cvar_95:.2%}")
        r3.metric(txt("sortino"), f"{sortino:.2f}")

        st.markdown("<br>", unsafe_allow_html=True)
        
        fig_hist = px.histogram(port_daily, nbins=50, title=txt("dist_title"), color_discrete_sequence=['#3B82F6'])
        fig_hist.add_vline(x=var_95, line_width=3, line_dash="dash", line_color="#EF4444", annotation_text="VaR 95%")
        fig_hist.update_layout(**common, height=450, showlegend=False)
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with tab4:
        fig_c = px.imshow(df.pct_change().corr(), text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r", zmin=-1, zmax=1, title=txt('t5'))
        fig_c.update_layout(**common, height=600)
        st.plotly_chart(fig_c, use_container_width=True)

    with tab5:
        buf = BytesIO()
        with pd.ExcelWriter(buf) as writer:
            df.to_excel(writer, sheet_name='Prices')
            pd.DataFrame(data['weights'], columns=tickers).to_excel(writer, sheet_name='Simulations')
        st.download_button(txt('down'), buf.getvalue(), f"Report_{date.today()}.xlsx", "application/vnd.ms-excel", use_container_width=True)

def show_footer():
    st.markdown(f"""<div class="footer">IFA QUANTUM TERMINAL | © {date.today().year} All Rights Reserved | Developed by Santino Domeniconi</div>""", unsafe_allow_html=True)

if st.session_state.started: show_dashboard()
else: show_landing()
show_footer()