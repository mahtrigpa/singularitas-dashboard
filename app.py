# -*- coding: utf-8 -*-
"""
==================================================================================
 SINGULARITAS // NEXUS CONTROL DASHBOARD
 Verifiable AI Compute & Multi-Agent Infrastructure
----------------------------------------------------------------------------------
 Panel de control interactivo construido en Streamlit. Diseñado como cara
 pública / técnica del proyecto "Singularitas" para comités de evaluación
 (NVIDIA Inception, fondos de Venture Capital, etc).

 Ejecutar con:   streamlit run app.py
==================================================================================
"""

import json
import random
import time
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==================================================================================
# 0. CONFIGURACIÓN DE PÁGINA
# ==================================================================================

st.set_page_config(
    page_title="SINGULARITAS // Nexus Control",
    page_icon="⚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================================================
# 1. TEMA VISUAL — INYECCIÓN DE CSS (Terminal Cuántica / Centro de Comando IA)
# ==================================================================================
# Paleta de tokens:
#   --bg-void        #04060A   fondo principal casi negro
#   --bg-panel       #0A0F14   paneles / tarjetas
#   --bg-panel-alt   #0D1620   paneles secundarios / terminal
#   --neon-green     #00FFA3   acento primario (verificación / éxito)
#   --neon-cyan      #29F1FF   acento secundario (datos / info)
#   --gold           #D4AF37   acento sutil (alertas / branding premium)
#   --danger         #FF3B5C   fallas / advertencias
#   --text-primary   #D7FFEF   texto principal
#   --text-muted     #6E8C84   texto secundario

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&display=swap');

:root{
    --bg-void: #04060A;
    --bg-panel: #0A0F14;
    --bg-panel-alt: #0D1620;
    --border-glow: rgba(0,255,163,0.18);
    --neon-green: #00FFA3;
    --neon-cyan: #29F1FF;
    --gold: #D4AF37;
    --danger: #FF3B5C;
    --text-primary: #D7FFEF;
    --text-muted: #6E8C84;
}

html, body, [class*="css"]{
    font-family: 'Rajdhani', sans-serif;
}

.stApp{
    background: radial-gradient(circle at 15% 0%, #0A1410 0%, #04060A 45%, #03050A 100%);
    color: var(--text-primary);
}

/* ---------- Encabezados ---------- */
h1, h2, h3{
    font-family: 'Orbitron', sans-serif !important;
    color: var(--neon-green) !important;
    letter-spacing: 1px;
    text-shadow: 0 0 10px rgba(0,255,163,0.35);
}
h4, h5, h6{
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--neon-cyan) !important;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg, #060A0E 0%, #03050A 100%);
    border-right: 1px solid var(--border-glow);
}
section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] label{
    color: var(--text-primary) !important;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"]{
    gap: 4px;
    border-bottom: 1px solid var(--border-glow);
}
.stTabs [data-baseweb="tab"]{
    background: transparent;
    color: var(--text-muted);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
    padding: 10px 18px;
}
.stTabs [aria-selected="true"]{
    color: var(--neon-green) !important;
    border-bottom: 2px solid var(--neon-green) !important;
    text-shadow: 0 0 8px rgba(0,255,163,0.5);
}

/* ---------- Botones ---------- */
.stButton > button, .stDownloadButton > button{
    background: linear-gradient(135deg, rgba(0,255,163,0.12), rgba(41,241,255,0.06));
    border: 1px solid var(--neon-green);
    color: var(--neon-green);
    font-family: 'Share Tech Mono', monospace;
    border-radius: 3px;
    letter-spacing: 0.5px;
    transition: all .15s ease-in-out;
}
.stButton > button:hover, .stDownloadButton > button:hover{
    box-shadow: 0 0 14px rgba(0,255,163,0.55);
    border-color: var(--neon-cyan);
    color: var(--neon-cyan);
}
.stFormSubmitButton > button{
    background: linear-gradient(135deg, rgba(212,175,55,0.18), rgba(212,175,55,0.05));
    border: 1px solid var(--gold) !important;
    color: var(--gold) !important;
}

/* ---------- Inputs ---------- */
.stNumberInput input, .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"]{
    background-color: var(--bg-panel) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-glow) !important;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploaderDropzone"]{
    background-color: var(--bg-panel) !important;
    border: 1.5px dashed var(--gold) !important;
    border-radius: 6px;
}

/* ---------- Métricas nativas ---------- */
div[data-testid="stMetric"]{
    background: var(--bg-panel);
    border: 1px solid var(--border-glow);
    border-radius: 8px;
    padding: 0.9rem 1rem;
}
div[data-testid="stMetricLabel"]{ color: var(--text-muted) !important; }
div[data-testid="stMetricValue"]{ color: var(--neon-green) !important; font-family: 'Share Tech Mono', monospace; }

/* ---------- Expanders ---------- */
details{
    background: var(--bg-panel);
    border: 1px solid var(--border-glow);
    border-radius: 6px;
}
summary{ color: var(--neon-cyan) !important; font-family: 'Share Tech Mono', monospace; }

/* ---------- Divisores ---------- */
hr{ border-color: var(--border-glow) !important; }

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar{ width: 8px; height: 8px; }
::-webkit-scrollbar-track{ background: var(--bg-void); }
::-webkit-scrollbar-thumb{ background: var(--neon-green); border-radius: 4px; }

/* ---------- Componentes custom ---------- */
.sng-eyebrow{
    font-family:'Share Tech Mono', monospace;
    color: var(--text-muted);
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: -6px;
}
.sng-card{
    background: var(--bg-panel);
    border: 1px solid var(--border-glow);
    border-left: 3px solid var(--accent, var(--neon-green));
    border-radius: 6px;
    padding: 14px 18px;
    margin-bottom: 6px;
}
.sng-card .label{
    font-family: 'Share Tech Mono', monospace;
    color: var(--text-muted);
    font-size: 0.72rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}
.sng-card .value{
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    color: var(--accent, var(--neon-green));
    text-shadow: 0 0 10px rgba(0,255,163,0.35);
}
.sng-card .value .unit{
    font-size: 0.95rem;
    color: var(--text-muted);
    font-family: 'Share Tech Mono', monospace;
    margin-left: 4px;
}

.sng-terminal{
    background: #02050A;
    border: 1px solid var(--border-glow);
    border-radius: 6px;
    padding: 14px 16px;
    height: 270px;
    overflow-y: auto;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.55;
    background-image: repeating-linear-gradient(0deg, rgba(0,255,163,0.025) 0px, rgba(0,255,163,0.025) 1px, transparent 1px, transparent 3px);
}
.sng-terminal .ln-pass{ color: var(--neon-green); }
.sng-terminal .ln-fail{ color: var(--danger); }
.sng-terminal .ln-info{ color: var(--neon-cyan); }
.sng-terminal .ts{ color: var(--text-muted); }
.sng-cursor{
    display:inline-block; width:7px; height:13px; background: var(--neon-green);
    animation: blink 1s steps(1) infinite; vertical-align: -2px;
}
@keyframes blink{ 50%{ opacity:0; } }

.sng-badge{
    display: inline-flex; align-items:center; gap:8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem; letter-spacing: 1px;
    padding: 4px 10px; border-radius: 20px;
    border: 1px solid var(--border-glow);
    background: rgba(255,255,255,0.02);
}
.sng-dot{ width:8px; height:8px; border-radius:50%; display:inline-block; }
.dot-online{ background: var(--neon-green); box-shadow: 0 0 8px var(--neon-green); }
.dot-standby{ background: var(--gold); box-shadow: 0 0 8px var(--gold); }
.dot-offline{ background: var(--danger); box-shadow: 0 0 8px var(--danger); }

.sng-node-card{
    background: var(--bg-panel);
    border: 1px solid var(--border-glow);
    border-radius: 8px;
    padding: 16px;
}
.sng-node-card h5{ margin: 0 0 8px 0; }

.sng-header-bar{
    display:flex; justify-content:space-between; align-items:center;
    border-bottom: 1px solid var(--border-glow);
    padding-bottom: 14px; margin-bottom: 10px;
}
.sng-header-title{
    font-family:'Orbitron', sans-serif; font-size:1.7rem; color: var(--neon-green);
    text-shadow: 0 0 12px rgba(0,255,163,0.4); letter-spacing:1.5px; margin:0;
}
.sng-header-sub{
    font-family:'Share Tech Mono', monospace; color: var(--text-muted); font-size:0.8rem; margin-top:2px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Plantilla común para gráficas Plotly (look & feel oscuro consistente)
PLOTLY_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Share Tech Mono, monospace", color="#D7FFEF"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=10, r=10, t=40, b=10),
)
GRID_COLOR = "rgba(110,140,132,0.15)"

# ==================================================================================
# 2. CONSTANTES DEL DOMINIO (protocolo de equivalencia / hardware de referencia)
# ==================================================================================

# Protocolo de Equivalencia Singularitas v1.2 (modelo económico simulado)
SNG_FLOP_UNIT = 5.0e15          # 1 SNG = 5 PFLOP de cómputo verificado
H100_EFFECTIVE_FP8_TFLOPS = 900.0     # TFLOPS FP8 sostenidos post-verificación (H100)
B200_EFFECTIVE_FP8_TFLOPS = 2100.0    # TFLOPS FP8 sostenidos post-verificación (Blackwell B200)

NIM_CONTAINERS = [
    "nemotron-70b-instruct-nim",
    "triton-inference-server",
    "riva-asr-nim",
    "nim-llm-router-v2",
    "biomednim-genomics",
    "nim-embed-qa-e5",
]

# ==================================================================================
# 3. ESTADO DE SESIÓN — DATOS SIMULADOS POR DEFECTO
# ==================================================================================

def _gen_history(n=30):
    """Genera una serie histórica simulada de verificación de workloads."""
    rng = np.random.default_rng(7)
    now = datetime.now()
    rows = []
    base = 97.2
    for i in range(n):
        ts = now - timedelta(minutes=(n - i) * 6)
        success = float(np.clip(base + rng.normal(0, 0.8) + (i * 0.03), 93.5, 99.9))
        fail = float(np.clip(100 - success - rng.uniform(0, 0.4), 0.05, 6.0))
        rows.append({"timestamp": ts, "success_rate": round(success, 2), "fail_rate": round(fail, 2)})
    return pd.DataFrame(rows)


def _new_log_line():
    """Crea una línea de log simulando la intercepción de respuestas de contenedores NIM."""
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    container = random.choice(NIM_CONTAINERS)
    whash = "0x" + "".join(random.choices("0123456789abcdef", k=10))
    chash = "".join(random.choices("0123456789abcdef", k=7))
    latency = random.randint(18, 96)
    passed = random.random() > 0.06
    status = "PASS" if passed else "FAIL"
    css_class = "ln-pass" if passed else "ln-fail"
    extra = "consensus=OK" if passed else "consensus=RETRY"
    return (
        f'<span class="ts">[{ts}]</span> :: NIM-CONTAINER[{chash}] :: {container} :: '
        f'WORKLOAD_HASH={whash} :: <span class="{css_class}">VERIFY={status}</span> '
        f':: latency={latency}ms :: {extra}'
    )


def init_state():
    if "booted" in st.session_state:
        return
    st.session_state.booted = True
    st.session_state.fp8_tflops = 4280.6
    st.session_state.fp64_tflops = 67.3
    st.session_state.consensus_integrity = 99.74
    st.session_state.history = _gen_history()
    st.session_state.oracle_logs = [_new_log_line() for _ in range(10)]
    st.session_state.node_status = {
        "NVIDIA H100": {"status": "online", "nodes": 48, "baseline": 50, "optimized": 92},
        "NVIDIA Blackwell B200": {"status": "online", "nodes": 12, "baseline": 54, "optimized": 94},
        "Huawei Ascend 910B": {"status": "standby", "nodes": 0, "baseline": 0, "optimized": 0},
    }
    st.session_state.agents = pd.DataFrame({
        "agent": ["Validator-Alpha", "Orchestrator-Beta", "Inference-Gamma", "Training-Delta", "Reserve Pool"],
        "allocation": [28, 22, 24, 18, 8],
    })
    st.session_state.ingestion_log = []


init_state()


def system_status_label():
    ci = st.session_state.consensus_integrity
    if ci >= 99.0:
        return "OPERATIONAL", "dot-online"
    elif ci >= 95.0:
        return "DEGRADED", "dot-standby"
    return "CRITICAL", "dot-offline"


# ==================================================================================
# 4. ENCABEZADO GLOBAL
# ==================================================================================

status_label, status_dot = system_status_label()
st.markdown(
    f"""
    <div class="sng-header-bar">
        <div>
            <p class="sng-header-title">⚛ SINGULARITAS // NEXUS CONTROL</p>
            <p class="sng-header-sub">VERIFIABLE AI COMPUTE &amp; MULTI-AGENT INFRASTRUCTURE — BUILD DE EVALUACIÓN TÉCNICA</p>
        </div>
        <div class="sng-badge">
            <span class="sng-dot {status_dot}"></span> SYSTEM // {status_label}
            &nbsp;|&nbsp; {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================================================================================
# 5. SIDEBAR — INGESTA DE DATOS PASO A PASO
# ==================================================================================

with st.sidebar:
    st.markdown(
        """
        <p style="font-family:'Orbitron',sans-serif; color:#00FFA3; font-size:1.1rem; letter-spacing:1px;">
        ⚛ SINGULARITAS</p>
        <p style="font-family:'Share Tech Mono',monospace; color:#6E8C84; font-size:0.75rem; margin-top:-10px;">
        NEXUS CONTROL // v0.9.3-alpha</p>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.markdown("##### 📡 Carga de Log JSON de GPU")
    uploaded_json = st.file_uploader(
        "Arrastra un log de telemetría GPU (.json)",
        type=["json"],
        key="gpu_log_uploader",
        help='Claves esperadas: fp8_tflops, fp64_tflops, consensus_integrity, success_rate',
    )
    if uploaded_json is not None:
        try:
            payload = json.loads(uploaded_json.read().decode("utf-8"))
            if "fp8_tflops" in payload:
                st.session_state.fp8_tflops = float(payload["fp8_tflops"])
            if "fp64_tflops" in payload:
                st.session_state.fp64_tflops = float(payload["fp64_tflops"])
            if "consensus_integrity" in payload:
                st.session_state.consensus_integrity = float(payload["consensus_integrity"])
            if "success_rate" in payload:
                new_row = {
                    "timestamp": datetime.now(),
                    "success_rate": float(payload["success_rate"]),
                    "fail_rate": round(100 - float(payload["success_rate"]), 2),
                }
                st.session_state.history = pd.concat(
                    [st.session_state.history, pd.DataFrame([new_row])], ignore_index=True
                )
            st.session_state.oracle_logs.insert(0, _new_log_line())
            st.success("Log de GPU ingerido y métricas sincronizadas.")
        except Exception as e:
            st.error(f"No se pudo procesar el JSON: {e}")

    st.divider()
    st.markdown("##### ✍️ Actualización Manual de Métricas")
    with st.form("manual_metrics_form", border=False):
        m_fp8 = st.number_input("TFLOPS FP8 validados", value=float(st.session_state.fp8_tflops), step=10.0)
        m_fp64 = st.number_input("TFLOPS FP64 estandarizados", value=float(st.session_state.fp64_tflops), step=1.0)
        m_ci = st.slider("Integridad del Consenso (%)", 80.0, 100.0, float(st.session_state.consensus_integrity), 0.01)
        submitted = st.form_submit_button("⇪ Inyectar al Oráculo")
        if submitted:
            st.session_state.fp8_tflops = m_fp8
            st.session_state.fp64_tflops = m_fp64
            st.session_state.consensus_integrity = m_ci
            new_row = {
                "timestamp": datetime.now(),
                "success_rate": round(m_ci - random.uniform(0, 1.2), 2),
                "fail_rate": round(100 - m_ci + random.uniform(0, 1.2), 2),
            }
            st.session_state.history = pd.concat(
                [st.session_state.history, pd.DataFrame([new_row])], ignore_index=True
            )
            st.session_state.oracle_logs.insert(0, _new_log_line())
            st.toast("Métricas sincronizadas con el Oráculo.", icon="⚛")

    st.divider()
    if st.button("🔄 Reiniciar Simulación", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown(
        """<p style="font-family:'Share Tech Mono',monospace; color:#6E8C84; font-size:0.68rem;">
        Datos mostrados son simulados por defecto y se actualizan con la
        información que cargues en este panel.</p>""",
        unsafe_allow_html=True,
    )

# ==================================================================================
# 6. CONTENIDO PRINCIPAL — PESTAÑAS
# ==================================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🛰️  NEXUS VALIDATION ORACLE",
    "⚙️  GPU FLEET & ORCHESTRATION",
    "💱  TOKENOMICS & COMPUTE EXCHANGE",
    "📥  RESEARCH DATA INGESTION",
])

# ---------------------------------------------------------------------------------
# TAB 1 — NEXUS VALIDATION ORACLE
# ---------------------------------------------------------------------------------
with tab1:
    st.markdown("#### Métricas de Verificación en Tiempo Real")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""<div class="sng-card" style="--accent:#00FFA3">
            <div class="label">TFLOPS FP8 Validados</div>
            <div class="value">{st.session_state.fp8_tflops:,.1f}<span class="unit">TFLOPS</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""<div class="sng-card" style="--accent:#29F1FF">
            <div class="label">TFLOPS FP64 Estandarizados</div>
            <div class="value">{st.session_state.fp64_tflops:,.1f}<span class="unit">TFLOPS</span></div>
            </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""<div class="sng-card" style="--accent:#D4AF37">
            <div class="label">Integridad del Consenso</div>
            <div class="value">{st.session_state.consensus_integrity:,.2f}<span class="unit">%</span></div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.write("")
    col_chart, col_term = st.columns([1.4, 1])

    with col_chart:
        st.markdown("##### Tasa de Veracidad y Verificación de Workloads")
        hist = st.session_state.history
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["timestamp"], y=hist["success_rate"], name="Verificación exitosa",
            mode="lines", line=dict(color="#00FFA3", width=2.5),
            fill="tozeroy", fillcolor="rgba(0,255,163,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=hist["timestamp"], y=hist["fail_rate"], name="Fallas detectadas",
            mode="lines", line=dict(color="#FF3B5C", width=1.8, dash="dot"),
        ))
        fig.update_layout(**PLOTLY_DARK, height=340, yaxis_title="%", legend=dict(orientation="h", y=1.12))
        fig.update_xaxes(gridcolor=GRID_COLOR, showline=False)
        fig.update_yaxes(gridcolor=GRID_COLOR, showline=False, range=[0, 105])
        st.plotly_chart(fig, use_container_width=True)

    with col_term:
        st.markdown("##### Oracle Terminal — Intercepción NVIDIA NIM")
        if st.button("↻ Re-sincronizar feed del Oráculo"):
            st.session_state.oracle_logs.insert(0, _new_log_line())
            st.session_state.oracle_logs = st.session_state.oracle_logs[:40]

        log_html = "<br>".join(st.session_state.oracle_logs[:14])
        st.markdown(
            f"""<div class="sng-terminal">{log_html}<br><span class="ln-info">root@oracle:~$</span> <span class="sng-cursor"></span></div>""",
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------------
# TAB 2 — GPU FLEET & ORCHESTRATION
# ---------------------------------------------------------------------------------
with tab2:
    st.markdown("#### Eficiencia de Cómputo de la Flota")

    node_status = st.session_state.node_status

    col_chart, col_nodes = st.columns([1.3, 1])

    with col_chart:
        st.markdown("##### Utilización: Línea Base Tradicional vs. Optimización Singularitas (Bin Packing)")
        # Solo se grafican nodos con flota activa; los slots en standby se muestran
        # como indicador de estado a la derecha.
        active_labels = [k for k, v in node_status.items() if v["nodes"] > 0]
        labels = active_labels
        baseline_vals = [node_status[k]["baseline"] for k in labels]
        optimized_vals = [node_status[k]["optimized"] for k in labels]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=labels, y=baseline_vals, name="Línea base (sin optimizar)",
            marker_color="rgba(110,140,132,0.55)",
        ))
        fig2.add_trace(go.Bar(
            x=labels, y=optimized_vals, name="Optimización Singularitas",
            marker_color="#00FFA3",
        ))
        fig2.update_layout(**PLOTLY_DARK, height=380, barmode="group", yaxis_title="Utilización (%)")
        fig2.update_xaxes(gridcolor=GRID_COLOR)
        fig2.update_yaxes(gridcolor=GRID_COLOR, range=[0, 105])
        st.plotly_chart(fig2, use_container_width=True)
        st.caption(
            "La técnica de *bin packing* de Singularitas reasigna workloads fraccionados "
            "entre GPUs físicas para eliminar el desperdicio de ciclos ociosos."
        )

    with col_nodes:
        st.markdown("##### Estado de Nodos de Cómputo")
        for name, info in node_status.items():
            if info["status"] == "online":
                dot, label = "dot-online", "ONLINE"
            elif info["status"] == "standby":
                dot, label = "dot-standby", "SLOT LISTO — INTEGRACIÓN PENDIENTE"
            else:
                dot, label = "dot-offline", "OFFLINE"

            util_txt = f'{info["optimized"]}% util.' if info["nodes"] > 0 else "—"
            st.markdown(
                f"""
                <div class="sng-node-card" style="margin-bottom:12px;">
                    <h5>{name}</h5>
                    <span class="sng-badge"><span class="sng-dot {dot}"></span>{label}</span>
                    <p style="font-family:'Share Tech Mono',monospace; color:#6E8C84; font-size:0.78rem; margin-top:8px;">
                        Nodos activos: {info['nodes']}  ·  {util_txt}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.caption(
            "El slot para Huawei Ascend queda reservado en la malla de orquestación "
            "para integración futura sin reescritura de arquitectura."
        )

# ---------------------------------------------------------------------------------
# TAB 3 — TOKENOMICS & COMPUTE EXCHANGE
# ---------------------------------------------------------------------------------
with tab3:
    st.markdown("#### Simulación Económica del Cómputo Verificable")

    col_conv, col_dist = st.columns([1, 1.1])

    with col_conv:
        st.markdown("##### Convertidor SNG → Cómputo Físico")
        sng_amount = st.number_input("Cantidad de tokens SNG", min_value=0.0, value=1000.0, step=50.0)

        h100_hours = (sng_amount * SNG_FLOP_UNIT) / (H100_EFFECTIVE_FP8_TFLOPS * 1e12) / 3600
        b200_minutes = (sng_amount * SNG_FLOP_UNIT) / (B200_EFFECTIVE_FP8_TFLOPS * 1e12) / 60

        mc1, mc2 = st.columns(2)
        with mc1:
            st.markdown(
                f"""<div class="sng-card" style="--accent:#00FFA3">
                <div class="label">Equivalente en H100</div>
                <div class="value">{h100_hours:,.2f}<span class="unit">horas</span></div>
                </div>""",
                unsafe_allow_html=True,
            )
        with mc2:
            st.markdown(
                f"""<div class="sng-card" style="--accent:#29F1FF">
                <div class="label">Equivalente en Blackwell B200</div>
                <div class="value">{b200_minutes:,.2f}<span class="unit">min</span></div>
                </div>""",
                unsafe_allow_html=True,
            )

        with st.expander("⚙ Protocolo de Equivalencia Singularitas v1.2"):
            st.markdown(
                f"""
                - **1 SNG** = `{SNG_FLOP_UNIT:.1e}` FLOPs de cómputo verificado.
                - H100 efectivo post-verificación: `{H100_EFFECTIVE_FP8_TFLOPS:.0f}` TFLOPS FP8 sostenidos.
                - Blackwell B200 efectivo post-verificación: `{B200_EFFECTIVE_FP8_TFLOPS:.0f}` TFLOPS FP8 sostenidos.

                *Modelo económico simulado con fines de demostración técnica;
                no constituye una oferta financiera ni asesoría de inversión.*
                """
            )

    with col_dist:
        st.markdown("##### Distribución de Cómputo entre Agentes Autónomos")
        agents_df = st.session_state.agents
        fig3 = go.Figure(data=[go.Pie(
            labels=agents_df["agent"],
            values=agents_df["allocation"],
            hole=0.55,
            marker=dict(colors=["#00FFA3", "#29F1FF", "#D4AF37", "#6E8C84", "#1B2A28"]),
            textfont=dict(color="#D7FFEF", family="Share Tech Mono, monospace"),
        )])
        fig3.update_layout(**PLOTLY_DARK, height=380, showlegend=True)
        st.plotly_chart(fig3, use_container_width=True)

        with st.expander("✎ Ajustar distribución manualmente"):
            edited = st.data_editor(
                agents_df, hide_index=True, use_container_width=True, key="agents_editor"
            )
            if st.button("Aplicar distribución"):
                st.session_state.agents = edited
                st.rerun()

# ---------------------------------------------------------------------------------
# TAB 4 — RESEARCH DATA INGESTION
# ---------------------------------------------------------------------------------
with tab4:
    st.markdown("#### Ingesta de Información de Investigación")

    col_up, col_form = st.columns(2)

    with col_up:
        st.markdown("##### 📂 Subir Reporte Técnico / Métricas")
        report_file = st.file_uploader(
            "Arrastra un archivo (.json, .csv, .txt, .pdf)",
            type=["json", "csv", "txt", "pdf"],
            key="report_uploader",
        )
        if report_file is not None:
            progress = st.progress(0, text="Procesando archivo...")
            for pct in (25, 55, 80, 100):
                time.sleep(0.08)
                progress.progress(pct, text=f"Procesando archivo... {pct}%")
            entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fuente": report_file.name,
                "tipo": report_file.type or "desconocido",
                "valor": None,
                "notas": "",
                "estado": "PROCESADO",
            }
            if report_file.name.lower().endswith(".json"):
                try:
                    payload = json.loads(report_file.getvalue().decode("utf-8"))
                    if "fp8_tflops" in payload:
                        st.session_state.fp8_tflops = float(payload["fp8_tflops"])
                    if "fp64_tflops" in payload:
                        st.session_state.fp64_tflops = float(payload["fp64_tflops"])
                    if "consensus_integrity" in payload:
                        st.session_state.consensus_integrity = float(payload["consensus_integrity"])
                except Exception:
                    entry["estado"] = "PROCESADO (sin métricas reconocidas)"
            st.session_state.ingestion_log.insert(0, entry)
            st.session_state.oracle_logs.insert(0, _new_log_line())
            st.success(f"Archivo «{report_file.name}» procesado e integrado al estado del sistema.")

    with col_form:
        st.markdown("##### ✍️ Registro Manual de Métrica Personalizada")
        with st.form("custom_metric_form", border=False):
            title = st.text_input("Título del reporte", placeholder="Ej. Benchmark interno Q3 — clúster B200")
            hw = st.selectbox("Tipo de hardware", ["NVIDIA H100", "NVIDIA Blackwell B200", "Huawei Ascend 910B", "Otro"])
            metric_val = st.number_input("Valor de rendimiento (TFLOPS o % integridad)", value=0.0, step=0.1)
            notes = st.text_area("Notas", placeholder="Observaciones del experimento...")
            submit_report = st.form_submit_button("⇪ Registrar e Ingerir")
            if submit_report:
                if not title:
                    st.warning("Indica un título para el reporte antes de ingerirlo.")
                else:
                    st.session_state.ingestion_log.insert(0, {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "fuente": title,
                        "tipo": hw,
                        "valor": metric_val,
                        "notas": notes,
                        "estado": "REGISTRADO",
                    })
                    st.session_state.oracle_logs.insert(0, _new_log_line())
                    st.toast("Reporte registrado en el sistema de ingesta.", icon="📥")

    st.divider()
    st.markdown("##### 🗒 Historial de Ingesta")
    if st.session_state.ingestion_log:
        log_df = pd.DataFrame(st.session_state.ingestion_log)
        st.dataframe(log_df, use_container_width=True, hide_index=True)
    else:
        st.caption("Aún no se ha ingerido información en esta sesión. Sube un archivo o registra una métrica manual arriba.")

    status_label, status_dot = system_status_label()
    st.markdown(
        f"""<span class="sng-badge"><span class="sng-dot {status_dot}"></span>
        Estado general del sistema tras última ingesta: <b>{status_label}</b></span>""",
        unsafe_allow_html=True,
    )
