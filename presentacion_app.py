"""
presentacao_app.py  ·  PDO · DESSEM · Apresentação
Controles no Sidebar — simples, robusto, sem hack de header fixo.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import zipfile
import gdown

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP: Baixar DATABASE do Google Drive (só na primeira vez)
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def setup_database():
    SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(SCRIPT_DIR, "DATABASE")
    if os.path.exists(DATABASE_PATH):
        return DATABASE_PATH
    try:
        GOOGLE_DRIVE_FILE_ID = "1t32md3cZfZfJQNuQZtoebWy7ze0v20j8"
        zip_path = os.path.join(SCRIPT_DIR, "DATABASE.zip")
        st.info("⏳ Primeira vez! Baixando DATABASE do Google Drive...")
        gdown.download(
            f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}",
            zip_path, quiet=False
        )
        st.info("📦 Descompactando arquivos...")
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(SCRIPT_DIR)
        try:
            os.remove(zip_path)
        except:
            pass
        st.success("✅ Dados prontos!")
        return DATABASE_PATH
    except Exception as e:
        st.error(f"❌ Erro ao baixar dados: {e}")
        st.stop()

DATABASE_PATH = setup_database()

# ═══════════════════════════════════════════════════════════════════════════════
# 0. CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OPSP.DT - Interface DESSEM",
    layout="wide",
    initial_sidebar_state="expanded",
)

COR_HIDRO  = "#3B82F6"
COR_RENOV  = "#22C55E"
COR_TERM   = "#EF4444"
COR_NUC    = "#6D28D9"
COR_ACCENT = "#0EA5E9"
COR_BG     = "#FFFFFF"
COR_TEXT   = "#0F172A"
COR_MUTED  = "#64748B"
COR_BORDER = "#E2E8F0"


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CSS GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Forçar tema claro em TUDO — bloqueia modo noite ─────────────────────── */
html, body, [class*="css"], [data-testid="stAppViewContainer"],
[data-testid="stApp"], .stApp, .main, section.main {{
    font-family: 'Inter', -apple-system, sans-serif !important;
    background-color: #FFFFFF !important;
    color: {COR_TEXT} !important;
    color-scheme: light !important;
}}

/* Forçar todos os textos escuros independente do tema */
p, span, div, label, h1, h2, h3, h4, h5, h6 {{
    color: {COR_TEXT} !important;
}}

/* Botões e inputs — sempre fundo branco */
button, input, select, textarea,
[data-testid="stSelectbox"] > div,
[data-testid="stSlider"] > div {{
    background-color: #FFFFFF !important;
    color: {COR_TEXT} !important;
    border-color: {COR_BORDER} !important;
}}

/* Dropdown do selectbox — sempre branco */
[data-baseweb="select"] > div,
[data-baseweb="popover"] {{
    background-color: #FFFFFF !important;
    color: {COR_TEXT} !important;
}}

/* Opções do dropdown */
[role="option"], [role="listbox"] {{
    background-color: #FFFFFF !important;
    color: {COR_TEXT} !important;
}}
[role="option"]:hover {{
    background-color: {COR_BORDER} !important;
}}

/* Header do Streamlit */
[data-testid="stHeader"] {{
    background-color: #FFFFFF !important;
}}

/* Toolbar e menu */
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
    background-color: #FFFFFF !important;
}}

.stApp {{
    background-color: {COR_BG};
}}

.block-container {{
    padding-top: 2rem !important;
    padding-bottom: 40px !important;
    max-width: 100% !important;
}}

[data-testid="stAppViewBlockContainer"] {{
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}}

/* ── Sidebar — sempre branco ──────────────────────────────────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {{
    background: white !important;
    background-color: white !important;
    border-right: 1.5px solid {COR_BORDER} !important;
}}

/* Textos dentro do sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {{
    color: {COR_TEXT} !important;
}}

[data-testid="stSidebar"] .stSlider > div > div > div {{
    background: {COR_ACCENT} !important;
}}

/* ── KPI cards ────────────────────────────────────────────────────────────── */
.kpi-card {{
    background: white;
    border: 1px solid {COR_BORDER};
    border-radius: 14px;
    padding: 14px 18px;
    border-left: 4px solid var(--accent-color, {COR_ACCENT});
    min-height: 120px;
}}
.kpi-label {{
    font-size: 10.5px; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase;
    color: {COR_MUTED}; margin-bottom: 5px;
}}
.kpi-value {{ font-size: 22px; font-weight: 700; color: {COR_TEXT}; }}
.kpi-sub   {{ font-size: 11px; color: {COR_MUTED}; margin-top: 3px; }}

/* ── Títulos de seção ─────────────────────────────────────────────────────── */
.section-title    {{ font-size: 18px; font-weight: 700; color: {COR_TEXT}; margin: 28px 0 4px 0; }}
.section-subtitle {{ font-size: 12.5px; color: {COR_MUTED}; margin-bottom: 14px; }}
.section-divider  {{ border: none; border-top: 1.5px solid {COR_BORDER}; margin: 32px 0 24px 0; }}

/* ── Fonte block ──────────────────────────────────────────────────────────── */
.fonte-block {{
    background: white; border: 1px solid {COR_BORDER}; border-radius: 14px;
    padding: 14px 18px; border-top: 4px solid var(--fonte-cor, {COR_ACCENT});
}}
.fonte-nome  {{ font-size: 15px; font-weight: 700; }}
.fonte-atual {{ font-size: 30px; font-weight: 800; }}
.fonte-row   {{ font-size: 12px; color: {COR_MUTED}; }}

/* ── Hora grande ──────────────────────────────────────────────────────────── */
.hora-grande {{
    font-size: 60px; font-weight: 800; text-align: center;
    color: {COR_ACCENT}; line-height: 1.1;
}}

/* ── Sidebar label estilo ─────────────────────────────────────────────────── */
.sb-label {{
    font-size: 10px; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; color: {COR_MUTED};
    margin-bottom: 2px; margin-top: 12px;
}}
</style>
""", unsafe_allow_html=True)



# ═══════════════════════════════════════════════════════════════════════════════
# 2. MAPA DE DATAS
# ═══════════════════════════════════════════════════════════════════════════════
MAPA_DATAS = {
    "15/06/2026": "DS_ONS_062026_RV2D15",
    "14/06/2026": "DS_ONS_062026_RV2D14",
    "13/06/2026": "DS_ONS_062026_RV2D13",
    "12/06/2026": "DS_ONS_062026_RV1D12",
    "11/06/2026": "DS_ONS_062026_RV1D11",
    "10/06/2026": "DS_ONS_062026_RV1D10",
    "09/06/2026": "DS_ONS_062026_RV1D09",
    "08/06/2026": "DS_ONS_062026_RV1D08",
    "07/06/2026": "DS_ONS_062026_RV1D07",
    "06/06/2026": "DS_ONS_062026_RV1D06",
    "05/06/2026": "DS_ONS_062026_RV0D05",
    "04/06/2026": "DS_ONS_062026_RV0D04",
    "03/06/2026": "DS_ONS_062026_RV0D03",
    "02/06/2026": "DS_ONS_062026_RV0D02",
    "01/06/2026": "DS_ONS_062026_RV0D01",
    "31/05/2026": "DS_ONS_062026_RV0D31",
    "30/05/2026": "DS_ONS_052026_RV0D30",
    "29/05/2026": "DS_ONS_052026_RV4D29",
    "28/05/2026": "DS_ONS_052026_RV4D28",
    "27/05/2026": "DS_ONS_052026_RV4D27",
    "26/05/2026": "DS_ONS_052026_RV4D26",
    "25/05/2026": "DS_ONS_052026_RV4D25",
    "24/05/2026": "DS_ONS_052026_RV4D24",
    "23/05/2026": "DS_ONS_052026_RV4D23",
    "22/05/2026": "DS_ONS_052026_RV3D22",
    "21/05/2026": "DS_ONS_052026_RV3D21",
    "20/05/2026": "DS_ONS_052026_RV3D20",
    "19/05/2026": "DS_ONS_052026_RV3D19",
    "06/05/2026": "DS_ONS_052026_RV1D06",
    "05/05/2026": "DS_ONS_052026_RV1D05",
    "04/05/2026": "DS_ONS_052026_RV1D04",
    "03/05/2026": "DS_ONS_052026_RV1D03",
    "25/04/2026": "DS_ONS_052026_RV0D25",
    "24/04/2026": "DS_ONS_042026_RV3D24",
    "23/04/2026": "DS_ONS_042026_RV3D23",
    "31/03/2026": "DS_ONS_042026_RV0D31_SegundoNivelContingencia",
    "30/03/2026": "DS_ONS_042026_RV0D30",
    "29/03/2026": "DS_ONS_042026_RV0D29",
    "09/03/2026": "DS_ONS_032026_RV1D09",
    "08/03/2026": "DS_ONS_032026_RV1D08_1° nível de contingência",
    "07/03/2026": "DS_ONS_032026_RV1D07",
    "06/03/2026": "DS_ONS_032026_RV0D06",
}

BASE_PATH   = DATABASE_PATH
DATAS_LIST  = list(MAPA_DATAS.keys())
SUBSISTEMAS = ["SIN", "SE", "S", "NE", "N"]



# ═══════════════════════════════════════════════════════════════════════════════
# 3. AUXILIARES
# ═══════════════════════════════════════════════════════════════════════════════
def to_float(v):
    v = str(v).strip()
    if v in ("", "-", "None"): return 0.0
    try:    return float(v.replace(",", "."))
    except: return 0.0

def iper_para_hora(iper_val):
    mins = (iper_val - 1) * 30
    return f"{int(mins // 60):02d}:{int(mins % 60):02d}"

def rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def add_vline(fig, hora, y_max, row=None, col=None, label=True):
    """Linha vertical cinza tracejada no IPER selecionado, com label opcional no topo."""
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(
        x=[hora, hora], y=[0, y_max],
        mode="lines", showlegend=False,
        line=dict(color="#94A3B8", width=1.8, dash="dash"),
        hoverinfo="skip",
    ), **kw)
    if label:
        ann = dict(x=hora, y=y_max, text=f"<b>{hora}</b>",
            showarrow=False, yanchor="bottom",
            font=dict(size=10, color="#475569"),
            bgcolor="white", bordercolor="#94A3B8", borderwidth=1)
        if row:
            ann["xref"] = f"x{(row-1)*2+col}"
            ann["yref"] = f"y{(row-1)*2+col}"
        fig.add_annotation(**ann)

PLOTLY_LAYOUT = dict(
    template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Inter, -apple-system, sans-serif", color=COR_TEXT),
    hovermode="x unified",
)
TICKS_2H = [iper_para_hora(i) for i in range(1, 49, 4)]

def kpi_card(col, label, value, sub="", cor=COR_ACCENT):
    col.markdown(
        f"<div class='kpi-card' style='--accent-color:{cor}'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div>"
        f"<div class='kpi-sub'>{sub}</div>"
        f"</div>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 4. LEITURA DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def carregar_sist(arq_sist):
    dados = []
    with open(arq_sist, "r", encoding="latin1") as f:
        for linha in f:
            if ";" not in linha: continue
            p = [x.strip() for x in linha.split(";")]
            if len(p) < 20 or not p[0].isdigit(): continue
            try:
                dados.append({"IPER": int(p[0]), "SIST": p[2],
                    "CMO": to_float(p[3]),  "DEMANDA": to_float(p[4]),
                    "G_RENOV": to_float(p[8]),  "G_HIDRO": to_float(p[9]),
                    "G_TERM":  to_float(p[10]), "EARM": to_float(p[19])})
            except: pass
    df = pd.DataFrame(dados)
    if df.empty: return df
    df = df[(df["IPER"] >= 1) & (df["IPER"] <= 48)].copy()
    df["Hora_Str"] = df["IPER"].apply(iper_para_hora)
    return df

@st.cache_data(show_spinner=False)
def carregar_term(arq_term):
    cvu_por_usina, dados_99 = {}, []
    with open(arq_term, "r", encoding="latin1") as f:
        for l in f:
            if ";" not in l: continue
            if any(k in l for k in ("IPER","CustoLinear","MW","---")): continue
            p = [x.strip() for x in l.split(";")]
            if len(p) < 12 or not p[0].isdigit(): continue
            nome, unid = p[3], p[4]
            if unid != "99" and p[11] != "":
                try: cvu_por_usina[nome] = float(p[11])
                except: pass
            if unid == "99":
                try:
                    iv = int(p[0])
                    if 1 <= iv <= 48:
                        dados_99.append({"IPER": iv, "NOME": nome, "SIST": p[5],
                            "GERACAO": to_float(p[6]), "GMIN": to_float(p[7]),
                            "GMAX": to_float(p[8]), "CVU": 0.0})
                except: pass
    df = pd.DataFrame(dados_99)
    if not df.empty:
        df["CVU"]      = df["NOME"].map(cvu_por_usina).fillna(0.0)
        df["Hora_Str"] = df["IPER"].apply(iper_para_hora)
    return df


# ═══════════════════════════════════════════════════════════════════════════════
# 5. SIDEBAR — todos os controles aqui
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(
        f"<div style='font-size:16px;font-weight:800;color:{COR_TEXT};"
        f"padding-bottom:4px;'>CONTROLE DO DASHBOARD</div>"
        f"<div style='font-size:11px;color:{COR_MUTED};margin-bottom:16px;'>"
        f"PDO · DESSEM</div>",
        unsafe_allow_html=True)

    st.markdown(f"<div class='sb-label'>Data de Operação</div>", unsafe_allow_html=True)
    data_sel = st.selectbox(
        "Data",
        DATAS_LIST,
        index=0,
        key="data_sel",
        label_visibility="collapsed",
    )

    pasta_ativa = MAPA_DATAS[data_sel]
    st.markdown(
        f"<div style='font-size:10px;color:{COR_MUTED};background:rgba(14,165,233,0.07);"
        f"border-radius:8px;padding:6px 10px;margin-top:4px;margin-bottom:8px;"
        f"word-break:break-all;'>"
        f"📁 {pasta_ativa}</div>",
        unsafe_allow_html=True)

    st.markdown(f"<div class='sb-label'>Subsistema</div>", unsafe_allow_html=True)
    sist_sel = st.selectbox(
        "Subsistema",
        SUBSISTEMAS,
        index=0,
        key="sist_sel",
        label_visibility="collapsed",
    )

    st.markdown(f"<div class='sb-label'>⏱ Hora (IPER)</div>", unsafe_allow_html=True)
    iper_sel = st.slider(
        "IPER",
        1, 48,
        value=1,
        key="slider_iper",
        label_visibility="collapsed",
    )
    hora_str_sb = iper_para_hora(iper_sel)
    st.markdown(
        f"<div style='text-align:center;font-size:28px;font-weight:800;"
        f"color:{COR_ACCENT};margin:-4px 0 8px 0;'>{hora_str_sb}</div>",
        unsafe_allow_html=True)

    st.markdown("<hr style='margin:16px 0;opacity:0.3;'>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:10px;color:{COR_MUTED};'>"
        f"IPER 1–48 · 00:00 → 23:30<br>"
        f"Base: <code style='font-size:9px;'>./DATABASE</code></div>",
        unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. CARREGAR DADOS
# ═══════════════════════════════════════════════════════════════════════════════
base_path = os.path.join(BASE_PATH, pasta_ativa)
arq_sist  = os.path.join(base_path, "pdo_sist.dat")
arq_term  = os.path.join(base_path, "pdo_term.dat")

if not os.path.exists(arq_sist):
    st.error(f"Arquivo não encontrado: `{arq_sist}`\n\nVerifique se a pasta **{pasta_ativa}** existe em `{BASE_PATH}`.")
    st.stop()

df_sist_raw = carregar_sist(arq_sist)
if df_sist_raw.empty:
    st.error("Não foi possível carregar dados do pdo_sist.dat.")
    st.stop()

tem_term    = os.path.exists(arq_term)
df_term_raw = carregar_term(arq_term) if tem_term else pd.DataFrame()

if sist_sel == "SIN":
    df = df_sist_raw.groupby("IPER").agg(
        CMO=("CMO","mean"), DEMANDA=("DEMANDA","sum"),
        G_RENOV=("G_RENOV","sum"), G_HIDRO=("G_HIDRO","sum"),
        G_TERM=("G_TERM","sum"),  EARM=("EARM","sum"),
    ).reset_index()
    df["SIST"]     = "SIN"
    df["Hora_Str"] = df["IPER"].apply(iper_para_hora)
    nome_regiao    = "Sistema Interligado Nacional (SIN)"
    df_term        = df_term_raw.copy() if not df_term_raw.empty else pd.DataFrame()
else:
    df = df_sist_raw[df_sist_raw["SIST"] == sist_sel].sort_values("IPER").copy()
    nome_regiao = f"Subsistema {sist_sel}"
    df_term = (df_term_raw[df_term_raw["SIST"] == sist_sel].copy()
               if not df_term_raw.empty and "SIST" in df_term_raw.columns
               else pd.DataFrame())

df["GER_TOTAL"]       = df["G_RENOV"] + df["G_HIDRO"] + df["G_TERM"]
df["SHARE_HIDRO"]     = 100 * df["G_HIDRO"] / (df["GER_TOTAL"] + 1e-9)
df["SHARE_RENOV"]     = 100 * df["G_RENOV"] / (df["GER_TOTAL"] + 1e-9)
df["SHARE_TERM"]      = 100 * df["G_TERM"]  / (df["GER_TOTAL"] + 1e-9)
df["DEMANDA_LIQUIDA"] = df["DEMANDA"] - df["G_RENOV"]

def stat_info(df, col):
    idx_max = df[col].idxmax()
    idx_min = df[col].idxmin()

    return {
        "max": df.loc[idx_max, col],
        "tmax": df.loc[idx_max, "Hora_Str"],
        "min": df.loc[idx_min, col],
        "tmin": df.loc[idx_min, "Hora_Str"],
    }

s_cmo   = stat_info(df, "CMO")
s_dem   = stat_info(df, "DEMANDA")
s_hidro = stat_info(df, "G_HIDRO")
s_renov = stat_info(df, "G_RENOV")
s_term  = stat_info(df, "G_TERM")
s_earm  = stat_info(df, "EARM")

# ═══════════════════════════════════════════════════════════════════════════════
# 7. TÍTULO + KPIs
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f"<h1 style='font-size:30px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"Plataforma de Visualização de Resultados do Modelo DESSEM – ONS</h1>"
    f"<p style='font-size:18px;color:{COR_MUTED};'>"
    f"PDO · DESSEM · {nome_regiao} · {data_sel}</p>",
    unsafe_allow_html=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

total_med = df["GER_TOTAL"].mean() + 1e-9
cmo_med   = df["CMO"].mean()
dem_med   = df["DEMANDA"].mean()
hidro_med = df["G_HIDRO"].mean()
renov_med = df["G_RENOV"].mean()
term_med  = df["G_TERM"].mean()
earm_med  = df["EARM"].mean()

k1,k2,k3,k4,k5,k6 = st.columns(6)

kpi_card(
    k1,
    "CMO Médio",
    f"{cmo_med:,.0f} R$/MWh",
    f"Máximo {s_cmo['max']:,.0f} · {s_cmo['tmax']}<br>"
    f"Mínimo {s_cmo['min']:,.0f} · {s_cmo['tmin']}",
    COR_ACCENT
)

kpi_card(
    k2,
    "Demanda Média",
    f"{dem_med:,.0f} MW",
    f"Máximo {s_dem['max']:,.0f} · {s_dem['tmax']}<br>"
    f"Mínimo {s_dem['min']:,.0f} · {s_dem['tmin']}",
    COR_TEXT
)

kpi_card(
    k3,
    "Geração Hidro",
    f"{hidro_med:,.0f} MW",
    f"Máximo {s_hidro['max']:,.0f} · {s_hidro['tmax']}<br>"
    f"Mínimo {s_hidro['min']:,.0f} · {s_hidro['tmin']}",
    COR_HIDRO
)

kpi_card(
    k4,
    "Geração Renovável",
    f"{renov_med:,.0f} MW",
    f"Máximo {s_renov['max']:,.0f} · {s_renov['tmax']}<br>"
    f"Mínimo {s_renov['min']:,.0f} · {s_renov['tmin']}",
    COR_RENOV
)

kpi_card(
    k5,
    "Geração Térmica",
    f"{term_med:,.0f} MW",
    f"Máximo {s_term['max']:,.0f} · {s_term['tmax']}<br>"
    f"Mínimo {s_term['min']:,.0f} · {s_term['tmin']}",
    COR_TERM
)

kpi_card(
    k6,
    "EARM Médio",
    f"{earm_med:,.0f}",
    f"Máximo {s_earm['max']:,.0f} · {s_earm['tmax']}<br>"
    f"Mínimo {s_earm['min']:,.0f} · {s_earm['tmin']}",
    "#8B5CF6"
)

# ═══════════════════════════════════════════════════════════════════════════════
# 8. PARTICIPAÇÃO POR FONTE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"1. Participação por Fonte na Geração total</h1>",
    unsafe_allow_html=True)

def fonte_stats(df, col_share, col_hora):
    if df.empty or df[col_share].dropna().empty:
        return {"max": 0, "min": 0, "mean": 0, "t_max": "-", "t_min": "-"}
    idx_max = df[col_share].idxmax(); idx_min = df[col_share].idxmin()
    return {"max": df.loc[idx_max, col_share], "min": df.loc[idx_min, col_share],
            "mean": df[col_share].mean(),
            "t_max": df.loc[idx_max, col_hora], "t_min": df.loc[idx_min, col_hora]}

s_hidro = fonte_stats(df, "SHARE_HIDRO", "Hora_Str")
s_renov = fonte_stats(df, "SHARE_RENOV", "Hora_Str")
s_term  = fonte_stats(df, "SHARE_TERM",  "Hora_Str")

tmp     = df[df["IPER"] == iper_sel]
if tmp.empty: tmp = df[df["IPER"] == df["IPER"].min()]
row_sel   = tmp.iloc[0]
hora_disp = row_sel["Hora_Str"]

def bloco_fonte(col, nome, stats, atual_val, cor):
    col.markdown(
        f"<div class='fonte-block' style='--fonte-cor:{cor};'>"
        f"<div class='fonte-nome'>{nome}</div>"
        f"<div class='kpi-label'>Atual (%)</div>"
        f"<div class='fonte-atual'>{atual_val:.1f}%</div>"
        f"<div class='fonte-row'>"
        f"<b>Máximo:</b> {stats['max']:.1f}% &nbsp;⏱ {stats['t_max']}<br>"
        f"<b>Mínimo:</b> {stats['min']:.1f}% &nbsp;⏱ {stats['t_min']}<br>"
        f"<b>Média:</b> {stats['mean']:.1f}%"
        f"</div></div>", unsafe_allow_html=True)

col_h, col_r, col_t, col_ctrl = st.columns([1, 1, 1, 1.2])
bloco_fonte(col_h, "Hidro",     s_hidro, row_sel["SHARE_HIDRO"], COR_HIDRO)
bloco_fonte(col_r, "Renovável", s_renov, row_sel["SHARE_RENOV"], COR_RENOV)
bloco_fonte(col_t, "Térmica",   s_term,  row_sel["SHARE_TERM"],  COR_TERM)
with col_ctrl:
    st.markdown(f"<div class='hora-grande'>{hora_disp}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center;font-size:12px;color:{COR_MUTED};'>"
                f"IPER {iper_sel} · ajuste o slider na barra lateral</div>", unsafe_allow_html=True)

st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)


col_graf, col_donut = st.columns([2, 1])
with col_graf:
    fig_share = go.Figure()
    for col_s, name, cor in [("SHARE_HIDRO","Hidro",COR_HIDRO),
                               ("SHARE_RENOV","Renovável",COR_RENOV),
                               ("SHARE_TERM","Térmica",COR_TERM)]:
        fig_share.add_trace(go.Scatter(x=df["Hora_Str"], y=df[col_s],
            name=name, line=dict(color=cor, width=3.5)))
    y_max_s = max(df["SHARE_HIDRO"].max(), df["SHARE_RENOV"].max(), df["SHARE_TERM"].max())
    fig_share.add_trace(go.Scatter(x=[hora_disp,hora_disp], y=[0, y_max_s*1.05],
        mode="lines", showlegend=False, line=dict(color="#94A3B8", width=2, dash="dash")))
    fig_share.add_annotation(x=hora_disp, y=y_max_s*1.05, text=f"<b>{hora_disp}</b>",
        showarrow=False, yanchor="bottom", font=dict(size=11, color="#475569"),
        bgcolor="white", bordercolor="#94A3B8", borderwidth=1)
    fig_share.update_layout(**PLOTLY_LAYOUT, height=500,
        yaxis_title="% da geração total", xaxis_title="Hora",
        xaxis=dict(tickvals=TICKS_2H, tickmode="array"))
    st.plotly_chart(fig_share, use_container_width=True)

with col_donut:
    fig_donut = go.Figure(data=[go.Pie(
        labels=["Hidro","Renovável","Térmica"],
        values=[row_sel["SHARE_HIDRO"],row_sel["SHARE_RENOV"],row_sel["SHARE_TERM"]],
        hole=0.55, marker=dict(colors=[COR_HIDRO,COR_RENOV,COR_TERM]),
        textinfo="percent", hovertemplate="%{label}: %{value:.1f}%<extra></extra>")])
    fig_donut.update_layout(template="plotly_white", height=500,
        title=dict(text=f"Composição da matriz no periodo — {hora_disp}", font=dict(size=20)),
        margin=dict(l=10,r=10,t=40,b=10), legend=dict(orientation="h",y=-0.08))
    st.plotly_chart(fig_donut, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 9. ANÁLISE OPERATIVA ENERGÉTICA
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"2. Análise Operativa Energética</h1>",
    unsafe_allow_html=True)

fig_op = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Preço Marginal de Operação (CMO)",
        "Curva de Carga (Demanda Bruta)",
        "Evolução de Geração por Fonte",
        "Residual Load (Curva de Pato)"
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.08
)

hs = df["Hora_Str"]

# ─────────────────────────────────────────────
# 1) CMO
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs, y=df["CMO"],
        name="CMO",
        mode="lines+markers",
        line=dict(color=COR_ACCENT, width=2.5),
        fill="tozeroy",
        fillcolor=rgba(COR_ACCENT, 0.07)
    ),
    row=1, col=1
)

# ─────────────────────────────────────────────
# 2) Demanda Bruta
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs, y=df["DEMANDA"],
        name="Demanda",
        mode="lines",
        line=dict(color="#F59E0B", width=2.5)
    ),
    row=1, col=2
)

# ─────────────────────────────────────────────
# 3) Geração por fonte
# ─────────────────────────────────────────────
fig_op.add_trace(go.Scatter(
    x=hs, y=df["G_RENOV"], name="Renovável",
    line=dict(color=COR_RENOV, width=2)
), row=2, col=1)

fig_op.add_trace(go.Scatter(
    x=hs, y=df["G_HIDRO"], name="Hidro",
    line=dict(color=COR_HIDRO, width=2)
), row=2, col=1)

fig_op.add_trace(go.Scatter(
    x=hs, y=df["G_TERM"], name="Térmica",
    line=dict(color=COR_TERM, width=2)
), row=2, col=1)
# ─────────────────────────────────────────────
# 3.4) Geração total (soma das fontes)
# ─────────────────────────────────────────────

df["G_TOTAL"] = df["G_RENOV"] + df["G_HIDRO"] + df["G_TERM"]

fig_op.add_trace(go.Scatter(
    x=hs,
    y=df["G_TOTAL"],
    name="Geração Total",
    mode="lines",
    line=dict(color="#111827", width=3.2, dash="solid")
), row=2, col=1)

# ─────────────────────────────────────────────
# 4) Residual Load + Duck Curve (áreas físicas correctas)
# ─────────────────────────────────────────────

dem = df["DEMANDA"]
ren = df["G_RENOV"]

residual = dem - ren
df["RESIDUAL_LOAD"] = residual

# ─────────────────────────────────────────────
# Curva de Demanda
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs, y=dem,
        name="Demanda",
        mode="lines",
        line=dict(color="#F59E0B", width=2.5)
    ),
    row=2, col=2
)

# ─────────────────────────────────────────────
# Curva de Pato (Residual Load)
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs, y=residual,
        name="Residual Load (Duck Curve)",
        mode="lines",
        line=dict(color="#8B5CF6", width=3)
    ),
    row=2, col=2
)

# ─────────────────────────────────────────────
# 🔵 Área azul: bajo la curva de pato (0 → residual)
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs,
        y=residual,
        name="Carga Residual (Área)",
        mode="none",
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.25)"
    ),
    row=2, col=2
)

# ─────────────────────────────────────────────
# 🟢 Área verde: energía renovável (Demanda - Residual)
# ─────────────────────────────────────────────
fig_op.add_trace(
    go.Scatter(
        x=hs,
        y=dem,
        name="Demanda (Base área verde)",
        mode="none",
        fill="tozeroy",
        fillcolor="rgba(34,197,94,0.18)"
    ),
    row=2, col=2
)

fig_op.add_trace(
    go.Scatter(
        x=hs,
        y=residual,
        name="Residual (corte área verde)",
        mode="none",
        fill="tonexty",
        fillcolor="rgba(34,197,94,0.18)",
        showlegend=False
    ),
    row=2, col=2
)

# ─────────────────────────────────────────────
# Línea cero de referencia conceptual
# ─────────────────────────────────────────────
fig_op.add_hline(
    y=0,
    line_dash="dot",
    line_color="#94A3B8",
    row=2, col=2
)

# ─────────────────────────────────────────────
# Layout
# ─────────────────────────────────────────────
fig_op.update_layout(
    **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ["legend", "margin"]},
    margin=dict(l=50, r=30, t=60, b=50),
    height=800,
    legend=dict(
        orientation="h",
        y=-0.12,
        x=0.5,
        xanchor="center",
        font=dict(size=10)
    ),
    showlegend=True
)

# ─────────────────────────────────────────────
# X axis config
# ─────────────────────────────────────────────
for r in range(1, 3):
    for c in range(1, 3):
        fig_op.update_xaxes(
            tickvals=TICKS_2H,
            tickmode="array",
            row=r, col=c
        )

# ─────────────────────────────────────────────
# Y axis labels
# ─────────────────────────────────────────────
fig_op.update_yaxes(title_text="R$/MWh", row=1, col=1)
fig_op.update_yaxes(title_text="MW", row=1, col=2)
fig_op.update_yaxes(title_text="MW", row=2, col=1)
fig_op.update_yaxes(title_text="MW", row=2, col=2)

st.plotly_chart(fig_op, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# 10. DESPACHO POR FONTE — Térmica | Renovável | Hidro | Estatísticas
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"3. Despacho por fonte</h1>",
    unsafe_allow_html=True)

# ── helpers locais ─────────────────────────────────────────────────────────────
def _add_vline_fig(fig, hora, y_max):
    fig.add_trace(go.Scatter(
        x=[hora, hora], y=[0, y_max], mode="lines", showlegend=False,
        line=dict(color="#94A3B8", width=1.8, dash="dash"), hoverinfo="skip"))
    fig.add_annotation(x=hora, y=y_max, text=f"<b>{hora}</b>",
        showarrow=False, yanchor="bottom", font=dict(size=10, color="#475569"),
        bgcolor="white", bordercolor="#94A3B8", borderwidth=1)

# ── pré-calcular renovável e hidro a partir de df (pdo_sist) ──────────────────
# df já tem G_RENOV e G_HIDRO por IPER
renov_media  = df["G_RENOV"].mean()
renov_max    = df["G_RENOV"].max()
renov_min    = df["G_RENOV"].min()
hidro_media  = df["G_HIDRO"].mean()
hidro_max    = df["G_HIDRO"].max()
hidro_min    = df["G_HIDRO"].min()
t_renov_max  = df.loc[df["G_RENOV"].idxmax(), "Hora_Str"]
t_renov_min  = df.loc[df["G_RENOV"].idxmin(), "Hora_Str"]
t_hidro_max  = df.loc[df["G_HIDRO"].idxmax(), "Hora_Str"]
t_hidro_min  = df.loc[df["G_HIDRO"].idxmin(), "Hora_Str"]

# ── dados térmicos pré-calculados (podem não existir) ─────────────────────────
if not df_term.empty:
    df_term_iper = df_term.groupby("IPER").agg(
        GERACAO=("GERACAO", "sum"), GMIN=("GMIN", "sum")).reset_index()
    df_term_iper["Hora_Str"] = df_term_iper["IPER"].apply(iper_para_hora)
    term_media   = df_term_iper["GERACAO"].mean()
    term_max     = df_term_iper["GERACAO"].max()
    term_min     = df_term_iper["GERACAO"].min()
    t_term_max   = df_term_iper.loc[df_term_iper["GERACAO"].idxmax(), "Hora_Str"]
    t_term_min   = df_term_iper.loc[df_term_iper["GERACAO"].idxmin(), "Hora_Str"]
    inflex_media = df_term_iper["GMIN"].mean()
    contem_angra = df_term["NOME"].fillna("").str.contains("ANGRA", case=False).any()
    cvu_pond = ((df_term["CVU"] * df_term["GERACAO"]).sum() / df_term["GERACAO"].sum()
                if df_term["GERACAO"].sum() > 0 else df_term["CVU"].mean())
else:
    df_term_iper = pd.DataFrame()
    term_media = term_max = term_min = inflex_media = cvu_pond = 0.0
    t_term_max = t_term_min = "--"
    contem_angra = False

ticks_src = df["Hora_Str"].iloc[::4].tolist()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1  →  Col esq: Térmica   |   Col dir: Renovável
# ══════════════════════════════════════════════════════════════════════════════
col_term_blk, col_renov_blk = st.columns(2)

# ─────────────────────────────────────────────────────────────────────────────
# Col esq — TÉRMICA
# ─────────────────────────────────────────────────────────────────────────────
with col_term_blk:
    st.markdown(
        f"<div style='font-size:15px;font-weight:700;color:{COR_TERM};"
        f"margin-bottom:10px;'>Despacho Térmico</div>",
        unsafe_allow_html=True)

    if df_term.empty:
        st.info("pdo_term.dat não encontrado — seção indisponível.")
    else:

        fig_term = go.Figure()
        if contem_angra:
            df_angra  = df_term[df_term["NOME"].str.contains("ANGRA", case=False)].groupby("IPER").agg({"GERACAO": "sum"}).reset_index()
            df_outras = df_term[~df_term["NOME"].str.contains("ANGRA", case=False)].groupby("IPER").agg({"GERACAO": "sum"}).reset_index()
            df_angra["Hora_Str"]  = df_angra["IPER"].apply(iper_para_hora)
            df_outras["Hora_Str"] = df_outras["IPER"].apply(iper_para_hora)
            fig_term.add_trace(go.Scatter(
                x=df_angra["Hora_Str"], y=df_angra["GERACAO"],
                mode="lines", name="Nuclear (Angra 1 e 2)", stackgroup="one",
                fillcolor=rgba("#6D28D9", 0.30), line=dict(color=COR_NUC, width=2)))
            fig_term.add_trace(go.Scatter(
                x=df_outras["Hora_Str"], y=df_outras["GERACAO"],
                mode="lines", name="Demais Térmicas", stackgroup="one",
                fillcolor=rgba(COR_TERM, 0.25), line=dict(color=COR_TERM, width=2)))
        else:
            fig_term.add_trace(go.Scatter(
                x=df_term_iper["Hora_Str"], y=df_term_iper["GERACAO"],
                mode="lines", name="Geração Térmica Total",
                fill="tozeroy", fillcolor=rgba(COR_TERM, 0.12),
                line=dict(color=COR_TERM, width=3)))
            fig_term.add_trace(go.Scatter(
                x=df_term_iper["Hora_Str"], y=df_term_iper["GMIN"],
                mode="lines", name="Inflexibilidade (GMin)",
                line=dict(color="#94A3B8", width=1.5, dash="dot")))
        _ym_t = df_term_iper["GERACAO"].max() * 1.05
        _add_vline_fig(fig_term, hora_disp, _ym_t)
        fig_term.update_layout(
            **PLOTLY_LAYOUT, height=360,
            xaxis_title="Hora", yaxis_title="Potência (MW)",
            xaxis=dict(tickvals=ticks_src, tickmode="array"),
            margin=dict(l=50, r=20, t=20, b=45),
            legend=dict(orientation="h", y=-0.22, font=dict(size=10)))
        st.plotly_chart(fig_term, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# Col dir — RENOVÁVEL
# ─────────────────────────────────────────────────────────────────────────────
with col_renov_blk:
    st.markdown(
        f"<div style='font-size:15px;font-weight:700;color:{COR_RENOV};"
        f"margin-bottom:10px;'>Geração Renovável</div>",
        unsafe_allow_html=True)


    fig_renov = go.Figure()
    fig_renov.add_trace(go.Scatter(
        x=df["Hora_Str"], y=df["G_RENOV"],
        mode="lines", name="Geração Renovável",
        fill="tozeroy", fillcolor=rgba(COR_RENOV, 0.18),
        line=dict(color=COR_RENOV, width=3)))
    # linha de média
    fig_renov.add_hline(y=renov_media, line_dash="dot",
        line_color="#16A34A", annotation_text=f"Média {renov_media:,.0f} MW",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#16A34A"))
    _ym_r = df["G_RENOV"].max() * 1.05
    _add_vline_fig(fig_renov, hora_disp, _ym_r)
    fig_renov.update_layout(
        **PLOTLY_LAYOUT, height=360,
        xaxis_title="Hora", yaxis_title="Potência (MW)",
        xaxis=dict(tickvals=ticks_src, tickmode="array"),
        margin=dict(l=50, r=20, t=20, b=45),
        legend=dict(orientation="h", y=-0.22, font=dict(size=10)))
    st.plotly_chart(fig_renov, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2  →  Col esq: Hidro (gráfico largo)   |   Col dir: Tabela estatísticas
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
col_hidro_blk, col_stats_blk = st.columns([1, 1])

# ─────────────────────────────────────────────────────────────────────────────
# Col esq — HIDRO
# ─────────────────────────────────────────────────────────────────────────────
with col_hidro_blk:
    st.markdown(
        f"<div style='font-size:15px;font-weight:700;color:{COR_HIDRO};"
        f"margin-bottom:10px;'>Geração Hidráulica</div>",
        unsafe_allow_html=True)


    fig_hidro = go.Figure()
    fig_hidro.add_trace(go.Scatter(
        x=df["Hora_Str"], y=df["G_HIDRO"],
        mode="lines", name="Geração Hidráulica",
        fill="tozeroy", fillcolor=rgba(COR_HIDRO, 0.18),
        line=dict(color=COR_HIDRO, width=3)))
    fig_hidro.add_hline(y=hidro_media, line_dash="dot",
        line_color="#1D4ED8", annotation_text=f"Média {hidro_media:,.0f} MW",
        annotation_position="bottom right",
        annotation_font=dict(size=10, color="#1D4ED8"))
    _ym_h = df["G_HIDRO"].max() * 1.05
    _add_vline_fig(fig_hidro, hora_disp, _ym_h)
    fig_hidro.update_layout(
        **PLOTLY_LAYOUT, height=360,
        xaxis_title="Hora", yaxis_title="Potência (MW)",
        xaxis=dict(tickvals=ticks_src, tickmode="array"),
        margin=dict(l=50, r=20, t=20, b=45),
        legend=dict(orientation="h", y=-0.22, font=dict(size=10)))
    st.plotly_chart(fig_hidro, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# Col dir — TABELA DE ESTATÍSTICAS POR FONTE
# ─────────────────────────────────────────────────────────────────────────────
with col_stats_blk:
    st.markdown(
        f"<div style='font-size:15px;font-weight:700;color:{COR_TEXT};"
        f"margin-bottom:10px;'>Estatísticas por Fonte</div>",
        unsafe_allow_html=True)

    # monta tabela — inclui térmica só se disponível
    stats_rows = [
        {
            "Fonte":    "Hidráulica",
            "Máximo":   f"{hidro_max:,.0f} MW",
            "Horário ↑": t_hidro_max,
            "Mínimo":   f"{hidro_min:,.0f} MW",
            "Horário ↓": t_hidro_min,
            "Média":    f"{hidro_media:,.0f} MW",
            "_cor":     COR_HIDRO,
        },
        {
            "Fonte":    "Renovável",
            "Máximo":   f"{renov_max:,.0f} MW",
            "Horário ↑": t_renov_max,
            "Mínimo":   f"{renov_min:,.0f} MW",
            "Horário ↓": t_renov_min,
            "Média":    f"{renov_media:,.0f} MW",
            "_cor":     COR_RENOV,
        },
        {
            "Fonte":    "Térmica",
            "Máximo":   f"{term_max:,.0f} MW",
            "Horário ↑": t_term_max,
            "Mínimo":   f"{term_min:,.0f} MW",
            "Horário ↓": t_term_min,
            "Média":    f"{term_media:,.0f} MW",
            "_cor":     COR_TERM,
        },
        {
            "Fonte":    "Total",
            "Máximo":   f"{df['GER_TOTAL'].max():,.0f} MW",
            "Horário ↑": df.loc[df['GER_TOTAL'].idxmax(), 'Hora_Str'],
            "Mínimo":   f"{df['GER_TOTAL'].min():,.0f} MW",
            "Horário ↓": df.loc[df['GER_TOTAL'].idxmin(), 'Hora_Str'],
            "Média":    f"{df['GER_TOTAL'].mean():,.0f} MW",
            "_cor":     COR_TEXT,
        },
    ]

    # renderizar como cards HTML
    for row in stats_rows:
        cor = row["_cor"]
        st.markdown(
            f"<div style='background:white;border:1px solid {COR_BORDER};"
            f"border-left:4px solid {cor};border-radius:10px;"
            f"padding:10px 14px;margin-bottom:8px;'>"
            f"<div style='font-size:12px;font-weight:700;color:{cor};"
            f"margin-bottom:1px;'>{row['Fonte']}</div>"
            f"<div style='display:flex;gap:160px;flex-wrap:wrap;'>"
            f"<div><span style='font-size:9.5px;font-weight:600;color:{COR_MUTED};"
            f"text-transform:uppercase;letter-spacing:.06em;'>Máximo</span><br>"
            f"<span style='font-size:13px;font-weight:700;color:{COR_TEXT};'>{row['Máximo']}</span>"
            f"<span style='font-size:10px;color:{COR_MUTED};margin-left:4px;'>⏱ {row['Horário ↑']}</span></div>"
            f"<div><span style='font-size:9.5px;font-weight:600;color:{COR_MUTED};"
            f"text-transform:uppercase;letter-spacing:.06em;'>Mínimo</span><br>"
            f"<span style='font-size:13px;font-weight:700;color:{COR_TEXT};'>{row['Mínimo']}</span>"
            f"<span style='font-size:10px;color:{COR_MUTED};margin-left:4px;'>⏱ {row['Horário ↓']}</span></div>"
            f"<div><span style='font-size:9.5px;font-weight:600;color:{COR_MUTED};"
            f"text-transform:uppercase;letter-spacing:.06em;'>Média</span><br>"
            f"<span style='font-size:13px;font-weight:700;color:{COR_TEXT};'>{row['Média']}</span></div>"
            f"</div></div>",
            unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 11 CURVA DE PATO (RAMPA REAL: VALLLE → PICO VESPERTINO)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"4. Curva de pato e rampa</h1>",
    unsafe_allow_html=True)

hora_ini_rampa = hora_fim_rampa = ""
hora_ini_hidro = hora_fim_hidro = ""

maior_rampa_mw = 0.0
maior_rampa_hidro_mw = 0.0

taxa_rampa_mw_min = 0.0

# ─────────────────────────────────────────────────────────────
# 1. Encontrar valle solar (mínimo entre 10h y 16h)
# ─────────────────────────────────────────────────────────────

df_vale = df[(df["IPER"] >= 21) & (df["IPER"] <= 32)]  # ~10:00 a 16:00

if not df_vale.empty:

    idx_min = df_vale["DEMANDA_LIQUIDA"].idxmin()
    val_min = df.loc[idx_min, "DEMANDA_LIQUIDA"]

    hora_ini_rampa = df.loc[idx_min, "Hora_Str"]

    # ─────────────────────────────────────────────────────────
    # 2. Buscar pico posterior (desde el valle hasta fin del día)
    # ─────────────────────────────────────────────────────────

    df_pos = df.loc[idx_min:]

    idx_max = df_pos["DEMANDA_LIQUIDA"].idxmax()
    val_max = df.loc[idx_max, "DEMANDA_LIQUIDA"]

    hora_fim_rampa = df.loc[idx_max, "Hora_Str"]

    maior_rampa_mw = val_max - val_min

    # ─────────────────────────────────────────────────────────
    # 3. Rampa hidráulica en el mismo intervalo
    # ─────────────────────────────────────────────────────────

    maior_rampa_hidro_mw = (
        df.loc[idx_max, "G_HIDRO"] - df.loc[idx_min, "G_HIDRO"]
    )

    hora_ini_hidro = hora_ini_rampa
    hora_fim_hidro = hora_fim_rampa

    # ─────────────────────────────────────────────────────────
    # 4. Gradiente real (en minutos)
    # ─────────────────────────────────────────────────────────

    dt_min = max((idx_max - idx_min) * 30, 1)
    taxa_rampa_mw_min = maior_rampa_mw / dt_min


# ─────────────────────────────────────────────────────────────
# Conversión
# ─────────────────────────────────────────────────────────────

maior_rampa_gw   = maior_rampa_mw / 1000.0
maior_rampa_h_gw = maior_rampa_hidro_mw / 1000.0

# ─────────────────────────────────────────────────────────────
# Queda renovable (igual que antes)
# ─────────────────────────────────────────────────────────────

max_renov = df["G_RENOV"].max()
pos_pico = df.index.get_loc(df["G_RENOV"].idxmax())
df_pos_pico = df.iloc[pos_pico + 1:]

queda_solar_gw = (
    (max_renov - df_pos_pico["G_RENOV"].min()) / 1000.0
    if not df_pos_pico.empty and max_renov > 0
    else 0.0
)

kr1,kr2,kr3,kr4 = st.columns(4)
kpi_card(kr1,"Maior Rampa Líquida",  f"{maior_rampa_gw:.2f} GW",   f"{hora_ini_rampa} → {hora_fim_rampa}", COR_HIDRO)
kpi_card(kr2,"Rampa Hidráulica Máx", f"{maior_rampa_h_gw:.2f} GW", f"{hora_ini_hidro} → {hora_fim_hidro}", COR_HIDRO)
kpi_card(kr3,"Gradiente Médio",           f"{taxa_rampa_mw_min:.1f} MW/min","ao longo da janela crítica",       COR_TEXT)
kpi_card(kr4,"Queda Renovável",           f"{queda_solar_gw:.2f} GW",    "do pico ao mínimo pós-pico",          COR_RENOV)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

fig_pato = go.Figure()
fig_pato.add_trace(go.Scatter(x=df["Hora_Str"], y=df["DEMANDA"], mode="lines",
    name="Demanda Bruta", line=dict(color="#F59E0B",width=3)))
fig_pato.add_trace(go.Scatter(x=df["Hora_Str"], y=df["DEMANDA_LIQUIDA"], mode="lines",
    name="Demanda Líquida", line=dict(color="#1E40AF",width=3.5),
    fill="tonexty", fillcolor=rgba("#FCD34D",0.15)))
fig_pato.add_trace(go.Scatter(x=df["Hora_Str"], y=df["G_HIDRO"], mode="lines",
    name="Geração Hidráulica", line=dict(color=COR_HIDRO,width=2,dash="dot")))

if hora_ini_hidro and hora_fim_hidro:
    df_jan = df[(df["IPER"] >= df.loc[df["Hora_Str"] == hora_ini_hidro, "IPER"].values[0]) & (df["IPER"] <= df.loc[df["Hora_Str"] == hora_fim_hidro, "IPER"].values[0])]
    if not df_jan.empty:
        y_topo = df["DEMANDA"].max() * 1.08
        hj = df_jan["Hora_Str"].tolist()
        fig_pato.add_trace(go.Scatter(x=hj+hj[::-1], y=[y_topo]*len(hj)+[0]*len(hj),
            fill="toself", mode="none", showlegend=False, fillcolor=rgba(COR_HIDRO,0.10)))
        for h_v in [hora_ini_hidro, hora_fim_hidro]:
            fig_pato.add_trace(go.Scatter(x=[h_v,h_v], y=[0,y_topo], mode="lines",
                showlegend=False, line=dict(color=COR_HIDRO,width=1.5,dash="dash")))
        fig_pato.add_annotation(x=df_jan.iloc[len(df_jan)//2]["Hora_Str"],
            y=df_jan["DEMANDA"].max()*0.98,
            text=f"<b>Rampa Hidro<br>+{maior_rampa_h_gw:.2f} GW</b>",
            showarrow=True, arrowhead=2, arrowcolor=COR_HIDRO,
            font=dict(color=COR_HIDRO,size=12), bgcolor="white",
            bordercolor=COR_HIDRO, borderwidth=1.5, borderpad=5, ax=0, ay=-45)

fig_pato.update_layout(**PLOTLY_LAYOUT, height=600, xaxis_title="Horário do Dia",
    yaxis_title="Potência (MW)", xaxis=dict(tickvals=TICKS_2H, tickmode="array"))
# Linha IPER
_ym_pato = df["DEMANDA"].max() * 1.08
fig_pato.add_trace(go.Scatter(x=[hora_disp,hora_disp], y=[0, _ym_pato],
    mode="lines", showlegend=False,
    line=dict(color="#94A3B8", width=1.8, dash="dash"), hoverinfo="skip"))
fig_pato.add_annotation(x=hora_disp, y=_ym_pato, text=f"<b>{hora_disp}</b>",
    showarrow=False, yanchor="bottom", font=dict(size=10, color="#475569"),
    bgcolor="white", bordercolor="#94A3B8", borderwidth=1)
st.plotly_chart(fig_pato, use_container_width=True)




# ═══════════════════════════════════════════════════════════════════════════════
# 12. CURVA DE DURAÇÃO
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"5. Curva de duração da potencia</h1>",
    unsafe_allow_html=True)

order_gen = np.argsort(df["GER_TOTAL"].values)[::-1]
ger_total = df["GER_TOTAL"].values[order_gen]
renov_ord = df["G_RENOV"].values[order_gen]
hidro_ord = df["G_HIDRO"].values[order_gen]
term_ord  = df["G_TERM"].values[order_gen]
x_dur     = np.arange(len(df)+1) * (0.5/24.0) * 100
renov_s   = np.append(renov_ord, renov_ord[-1])
hidro_s   = np.append(hidro_ord, hidro_ord[-1])
term_s    = np.append(term_ord,  term_ord[-1])
total_s   = np.append(ger_total, ger_total[-1])

fig_dur = go.Figure()
fig_dur.add_trace(go.Scatter(x=x_dur, y=renov_s, mode="lines", line_shape="hv",
    fill="tozeroy", fillcolor=rgba(COR_RENOV,0.5), name="Renovável", line=dict(color=COR_RENOV,width=2)))
fig_dur.add_trace(go.Scatter(x=x_dur, y=renov_s+hidro_s, mode="lines", line_shape="hv",
    fill="tonexty", fillcolor=rgba(COR_HIDRO,0.5), name="Hidráulica", line=dict(color=COR_HIDRO,width=2)))
fig_dur.add_trace(go.Scatter(x=x_dur, y=renov_s+hidro_s+term_s, mode="lines", line_shape="hv",
    fill="tonexty", fillcolor=rgba(COR_TERM,0.5), name="Térmica", line=dict(color=COR_TERM,width=2)))
fig_dur.add_trace(go.Scatter(x=x_dur, y=total_s, mode="lines", line_shape="hv",
    name="Geração Total", line=dict(color=COR_TEXT,width=3)))
fig_dur.update_layout(**PLOTLY_LAYOUT, height=600,
    xaxis_title="% do dia (ordenado por geração total decrescente)", yaxis_title="MW",
    margin=dict(l=50,r=30,t=20,b=55))
# Linha IPER — posição percentual do IPER no eixo de duração
# O IPER selecionado ocupa a posição onde seu valor de GER_TOTAL cai na ordenação
_iper_rank    = np.sum(df["GER_TOTAL"].values >= df.loc[df["IPER"]==iper_sel,"GER_TOTAL"].values[0]
                       if not df[df["IPER"]==iper_sel].empty else df["GER_TOTAL"].values >= 0)
_x_dur_iper   = float(_iper_rank) / len(df) * 100
_ym_dur       = float(total_s.max()) * 1.05
fig_dur.add_trace(go.Scatter(x=[_x_dur_iper, _x_dur_iper], y=[0, _ym_dur],
    mode="lines", showlegend=False,
    line=dict(color="#94A3B8", width=1.8, dash="dash"), hoverinfo="skip"))
fig_dur.add_annotation(x=_x_dur_iper, y=_ym_dur,
    text=f"<b>IPER {iper_sel} ({hora_disp})</b>",
    showarrow=False, yanchor="bottom", font=dict(size=10, color="#475569"),
    bgcolor="white", bordercolor="#94A3B8", borderwidth=1)
st.plotly_chart(fig_dur, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 13. RODAPÉ
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<div style='font-size:11px;color:{COR_MUTED};text-align:center;padding-bottom:16px;'>"
    f"PDO · DESSEM · {nome_regiao} · Pasta: <code>{pasta_ativa}</code> · "
    f"Data selecionada: <b>{data_sel}</b> · Desenvolvido por: Estagiario da OPSP.DT"
    f"</div>", unsafe_allow_html=True)