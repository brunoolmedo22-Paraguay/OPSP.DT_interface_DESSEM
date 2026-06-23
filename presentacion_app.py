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
# 🆕 NOVO: Baixar DATABASE do Google Drive
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def setup_database():
    """
    Baixa DATABASE.zip do Google Drive e descompacta automaticamente.
    """
    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_PATH = os.path.join(SCRIPT_DIR, "DATABASE")
    
    # Se DATABASE já existe, não precisa baixar novamente
    if os.path.exists(DATABASE_PATH):
        return DATABASE_PATH
    
    try:
        # ⭐ SEU ID (já preenchido!)
        GOOGLE_DRIVE_FILE_ID = "1t32md3cZfZfJQNuQZtoebWy7ze0v20j8"
        
        zip_path = os.path.join(SCRIPT_DIR, "DATABASE.zip")
        
        # Baixar do Google Drive
        st.info("Primeira vez! Baixando DATABASE.zip (pode levar alguns minutos)...")
        gdown.download(
            f'https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}',
            zip_path,
            quiet=False
        )
        
        st.success("Download completo!")
        
        # Descompactar
        st.info("Descompactando arquivos...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(SCRIPT_DIR)
        
        st.success("Arquivos prontos!")
        
        # Deletar ZIP depois (economiza espaço)
        try:
            os.remove(zip_path)
        except:
            pass
        
        return DATABASE_PATH
    
    except Exception as e:
        st.error(f"Erro ao baixar: {e}")
        st.stop()

# Executar no início
DATABASE_PATH = setup_database()

# ═══════════════════════════════════════════════════════════════════════════════
# Resto do código continua IGUAL (não mude nada daqui para baixo)
# ═══════════════════════════════════════════════════════════════════════════════
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
COR_BG     = "#F5FBFF"
COR_TEXT   = "#0F172A"
COR_MUTED  = "#64748B"
COR_BORDER = "#E2E8F0"


# ═══════════════════════════════════════════════════════════════════════════════
# 1. CSS GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
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

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: white !important;
    border-right: 1.5px solid {COR_BORDER} !important;
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

# ═══════════════════════════════════════════════════════════════════════════════
# 3. CAMINHOS RELATIVOS À PASTA BASE
# ═══════════════════════════════════════════════════════════════════════════════
# Obter o diretório onde este script está localizado (pasta base do projeto)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Pasta DATABASE dentro da pasta base
DATABASE_PATH = os.path.join(SCRIPT_DIR, "DATABASE")
# Exibição do caminho (para debug no sidebar)
DISPLAY_PATH = "DATABASE"

DATAS_LIST  = list(MAPA_DATAS.keys())
SUBSISTEMAS = ["SIN", "SE", "S", "NE", "N"]



# ═══════════════════════════════════════════════════════════════════════════════
# 4. AUXILIARES
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
# 5. LEITURA DE DADOS
# ═══════════════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def carregar_sist(arq_sist):
    """
    Carrega arquivo pdo_sist.dat
    Extrai: IPER, SIST, CMO, DEMANDA, G_RENOV, G_HIDRO, G_TERM, EARM
    """
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
    """
    Carrega arquivo pdo_term.dat
    Extrai: IPER, NOME, SIST, GERACAO, GMIN, GMAX, CVU
    """
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
# 6. SIDEBAR — todos os controles aqui
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
        f"Base: <code style='font-size:9px;'>./{DISPLAY_PATH}</code></div>",
        unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CARREGAR DADOS
# ═══════════════════════════════════════════════════════════════════════════════
base_path = os.path.join(DATABASE_PATH, pasta_ativa)
arq_sist  = os.path.join(base_path, "pdo_sist.dat")
arq_term  = os.path.join(base_path, "pdo_term.dat")

if not os.path.exists(arq_sist):
    st.error(
        f"❌ Arquivo não encontrado: `pdo_sist.dat`\n\n"
        f"**Verificar:**\n"
        f"- Pasta esperada: `./{DISPLAY_PATH}/{pasta_ativa}/`\n"
        f"- Arquivo obrigatório: `pdo_sist.dat`\n\n"
        f"**Dica:** Se estiver rodando localmente, certifique-se que os arquivos DESSEM estão em:\n"
        f"`DATABASE/DS_ONS_032026_RV0D06/pdo_sist.dat` (e outras datas)"
    )
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
# 8. TÍTULO + KPIs
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(
    f"<h1 style='font-size:30px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"Plataforma de Visualização de Resultados do Modelo DESSEM – ONS</h1>",
    unsafe_allow_html=True)
st.markdown(
    f"<p style='font-size:13px;color:{COR_MUTED};margin-top:0;margin-bottom:20px;'>"
    f"{nome_regiao} · {data_sel} · Hora {hora_str_sb}"
    f"</p>",
    unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
kpi_card(k1,"CMO", f"R$ {s_cmo['max']:.2f}/MWh", f"Máx às {s_cmo['tmax']}", COR_ACCENT)
kpi_card(k2,"Demanda Total", f"{s_dem['max']/1000:.2f} GW", f"Máx às {s_dem['tmax']}", COR_TEXT)
kpi_card(k3,"Geração Hidro", f"{s_hidro['max']/1000:.2f} GW", f"Máx às {s_hidro['tmax']}", COR_HIDRO)
kpi_card(k4,"EARM", f"{s_earm['min']:.1f}%", f"Mín às {s_earm['tmin']}", COR_RENOV)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"1. Mix de geração (curva do dia)</h1>",
    unsafe_allow_html=True)

st.markdown(f"<div class='section-subtitle'>Distribuição de fontes: renovável, hidráulica, térmica e nuclear</div>",
    unsafe_allow_html=True)

hora_disp = iper_para_hora(iper_sel)

fig_mix = go.Figure()
fig_mix.add_trace(go.Scatter(x=df["Hora_Str"], y=df["G_RENOV"],  mode="lines", stackgroup="one",
    name="Renovável (Solar+Eólica)", line=dict(width=0), fillcolor=COR_RENOV))
fig_mix.add_trace(go.Scatter(x=df["Hora_Str"], y=df["G_HIDRO"],  mode="lines", stackgroup="one",
    name="Hidráulica", line=dict(width=0), fillcolor=COR_HIDRO))
fig_mix.add_trace(go.Scatter(x=df["Hora_Str"], y=df["G_TERM"],   mode="lines", stackgroup="one",
    name="Térmica", line=dict(width=0), fillcolor=COR_TERM))
fig_mix.add_trace(go.Scatter(x=df["Hora_Str"], y=df["GER_TOTAL"], mode="lines",
    name="Total", line=dict(color=COR_TEXT, width=3)))

add_vline(fig_mix, hora_disp, df["GER_TOTAL"].max() * 1.1)
fig_mix.update_layout(**PLOTLY_LAYOUT, height=500, xaxis_title="Horário do Dia",
    yaxis_title="Potência (MW)", xaxis=dict(tickvals=TICKS_2H, tickmode="array"))
st.plotly_chart(fig_mix, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"2. CMO e demanda</h1>",
    unsafe_allow_html=True)

fig_cmo = make_subplots(specs=[[{"secondary_y": True}]])
fig_cmo.add_trace(go.Scatter(x=df["Hora_Str"], y=df["CMO"], mode="lines",
    name="CMO", line=dict(color=COR_ACCENT, width=3)), secondary_y=False)
fig_cmo.add_trace(go.Scatter(x=df["Hora_Str"], y=df["DEMANDA"], mode="lines",
    name="Demanda", line=dict(color=COR_TEXT, width=2.5, dash="dot")), secondary_y=True)

add_vline(fig_cmo, hora_disp, df["CMO"].max() * 1.1, row=1, col=1)
fig_cmo.update_layout(**PLOTLY_LAYOUT, height=500, xaxis_title="Horário do Dia",
    xaxis=dict(tickvals=TICKS_2H, tickmode="array"))
fig_cmo.update_yaxes(title_text="CMO (R$/MWh)", secondary_y=False)
fig_cmo.update_yaxes(title_text="Demanda (MW)", secondary_y=True)
st.plotly_chart(fig_cmo, use_container_width=True)

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<h1 style='font-size:24px;font-weight:800;color:{COR_TEXT};"
    f"letter-spacing:-0.6px;margin-bottom:2px;margin-top:0;'>"
    f"3. Share de fontes</h1>",
    unsafe_allow_html=True)

fig_share = go.Figure()
fig_share.add_trace(go.Scatter(x=df["Hora_Str"], y=df["SHARE_HIDRO"],
    name="Hidráulica %", line=dict(color=COR_HIDRO, width=2.5)))
fig_share.add_trace(go.Scatter(x=df["Hora_Str"], y=df["SHARE_RENOV"],
    name="Renovável %", line=dict(color=COR_RENOV, width=2.5)))
fig_share.add_trace(go.Scatter(x=df["Hora_Str"], y=df["SHARE_TERM"],
    name="Térmica %", line=dict(color=COR_TERM, width=2.5)))

add_vline(fig_share, hora_disp, 100)
fig_share.update_layout(**PLOTLY_LAYOUT, height=500, xaxis_title="Horário do Dia",
    yaxis_title="Percentual (%)", xaxis=dict(tickvals=TICKS_2H, tickmode="array"),
    yaxis=dict(range=[0, 100]))
st.plotly_chart(fig_share, use_container_width=True)

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

df_vale = df[(df["IPER"] >= 21) & (df["IPER"] <= 32)]

if not df_vale.empty:
    idx_min = df_vale["DEMANDA_LIQUIDA"].idxmin()
    val_min = df.loc[idx_min, "DEMANDA_LIQUIDA"]
    hora_ini_rampa = df.loc[idx_min, "Hora_Str"]

    df_pos = df.loc[idx_min:]
    idx_max = df_pos["DEMANDA_LIQUIDA"].idxmax()
    val_max = df.loc[idx_max, "DEMANDA_LIQUIDA"]
    hora_fim_rampa = df.loc[idx_max, "Hora_Str"]

    maior_rampa_mw = val_max - val_min
    maior_rampa_hidro_mw = df.loc[idx_max, "G_HIDRO"] - df.loc[idx_min, "G_HIDRO"]

    hora_ini_hidro = hora_ini_rampa
    hora_fim_hidro = hora_fim_rampa

    dt_min = max((idx_max - idx_min) * 30, 1)
    taxa_rampa_mw_min = maior_rampa_mw / dt_min

maior_rampa_gw   = maior_rampa_mw / 1000.0
maior_rampa_h_gw = maior_rampa_hidro_mw / 1000.0

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
_ym_pato = df["DEMANDA"].max() * 1.08
fig_pato.add_trace(go.Scatter(x=[hora_disp,hora_disp], y=[0, _ym_pato],
    mode="lines", showlegend=False,
    line=dict(color="#94A3B8", width=1.8, dash="dash"), hoverinfo="skip"))
fig_pato.add_annotation(x=hora_disp, y=_ym_pato, text=f"<b>{hora_disp}</b>",
    showarrow=False, yanchor="bottom", font=dict(size=10, color="#475569"),
    bgcolor="white", bordercolor="#94A3B8", borderwidth=1)
st.plotly_chart(fig_pato, use_container_width=True)

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

st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
st.markdown(
    f"<div style='font-size:11px;color:{COR_MUTED};text-align:center;padding-bottom:16px;'>"
    f"PDO · DESSEM · {nome_regiao} · Pasta: <code>{pasta_ativa}</code> · "
    f"Data selecionada: <b>{data_sel}</b> · Desenvolvido por: Estagiario da OPSP.DT"
    f"</div>", unsafe_allow_html=True)
