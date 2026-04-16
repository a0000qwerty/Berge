import streamlit as st
from pathlib import Path

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Financiero Portuario",
    page_icon=Path("assets/icon.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Estilos personalizados ───────────────────────────────────────────────────
def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("./assets/styles.css")


# ── Inicialización del estado ─────────────────────────────────────────────────
if "servicios" not in st.session_state:
    st.session_state.servicios = [{"nombre": "", "precio": 0.0}]

if "equipos" not in st.session_state:
    st.session_state.equipos = [{"nombre": "", "precio": 0.0}]


# ── Helpers ───────────────────────────────────────────────────────────────────
def añadir_servicio():
    st.session_state.servicios.append({"nombre": "", "precio": 0.0})

def eliminar_servicio(i):
    st.session_state.servicios.pop(i)

def añadir_equipo():
    st.session_state.equipos.append({"nombre": "", "precio": 0.0})

def eliminar_equipo(i):
    st.session_state.equipos.pop(i)

def formato_eur(valor):
    return f"€{valor:,.0f}".replace(",", ".")

def coste_total_equipos():
    return sum(e["precio"] for e in st.session_state.equipos)

def coste_total_servicios():
    return sum(s["precio"] for s in st.session_state.servicios)


# ── HEADER ────────────────────────────────────────────────────────────────────
st.logo("assets/logo.png")
st.markdown("""
<div class="main-header">
    <h1>ANÁLISIS FINANCIERO PORTUARIO</h1>
    <p>Modelo de rentabilidad y financiación de proyectos · Gestión de Tráfico Portuario</p>
</div>
""", unsafe_allow_html=True)


# ── LAYOUT: columna principal + columna resumen ────────────────────────────────
col_form, col_summary = st.columns([2, 1], gap="large")


with col_form:

    # ── SECCIÓN 1: Parámetros generales ──────────────────────────────────────
    st.markdown('<div class="section-label">01 · Parámetros del Proyecto</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        años_proyecto = st.number_input(
            "Duración del proyecto (años)",
            min_value=1, max_value=50, value=10, step=1
        )
    with c2:
        num_buques = st.number_input(
            "Número de buques",
            min_value=1, max_value=10000, value=50, step=1
        )

    c3, c4 = st.columns(2)
    with c3:
        toneladas_anuales = st.number_input(
            "Toneladas manejadas al año",
            min_value=0, max_value=100_000_000, value=500_000, step=1000,
            format="%d"
        )
    with c4:
        tipo_carga = st.selectbox(
            "Tipo de carga",
            options=[
                "Contenedores (TEU)",
                "Granel sólido",
                "Granel líquido",
                "Carga general",
                "Ro-Ro (vehículos)",
                "Carga refrigerada",
                "Mercancías peligrosas",
            ]
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECCIÓN 2: Servicios ──────────────────────────────────────────────────
    st.markdown('<div class="section-label">02 · Servicios Necesarios</div>', unsafe_allow_html=True)

    for i, servicio in enumerate(st.session_state.servicios):
        st.markdown(f'<div class="item-index">SERVICIO #{i+1:02d}</div>', unsafe_allow_html=True)
        with st.container():
            ca, cb, cc = st.columns([3, 2, 0.5])
            with ca:
                st.session_state.servicios[i]["nombre"] = st.text_input(
                    "Nombre del servicio",
                    value=servicio["nombre"],
                    key=f"srv_nombre_{i}",
                    label_visibility="collapsed",
                    placeholder="Ej: Practicaje, Remolque, Estiba..."
                )
            with cb:
                st.session_state.servicios[i]["precio"] = st.number_input(
                    "Coste (€)",
                    value=servicio["precio"],
                    min_value=0.0,
                    step=100.0,
                    format="%.2f",
                    key=f"srv_precio_{i}",
                    label_visibility="collapsed",
                )
            with cc:
                st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
                if st.button("✕", key=f"del_srv_{i}", help="Eliminar servicio"):
                    eliminar_servicio(i)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    st.button("＋ Añadir servicio", on_click=añadir_servicio, key="btn_srv")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECCIÓN 3: Equipos ────────────────────────────────────────────────────
    st.markdown('<div class="section-label">03 · Equipos Necesarios</div>', unsafe_allow_html=True)

    for i, equipo in enumerate(st.session_state.equipos):
        st.markdown(f'<div class="item-index">EQUIPO #{i+1:02d}</div>', unsafe_allow_html=True)
        ca, cb, cc = st.columns([3, 2, 0.5])
        with ca:
            st.session_state.equipos[i]["nombre"] = st.text_input(
                "Nombre del equipo",
                value=equipo["nombre"],
                key=f"eq_nombre_{i}",
                label_visibility="collapsed",
                placeholder="Ej: Grúa pórtico, Pala, Reach stacker..."
            )
        with cb:
            st.session_state.equipos[i]["precio"] = st.number_input(
                "Coste (€)",
                value=equipo["precio"],
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=f"eq_precio_{i}",
                label_visibility="collapsed",
            )
        with cc:
            st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
            if st.button("✕", key=f"del_eq_{i}", help="Eliminar equipo"):
                eliminar_equipo(i)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.button("＋ Añadir equipo", on_click=añadir_equipo, key="btn_eq")

    st.markdown("<hr>", unsafe_allow_html=True)

    # ── SECCIÓN 4: Financiación ───────────────────────────────────────────────
    st.markdown('<div class="section-label">04 · Financiación Externa</div>', unsafe_allow_html=True)

    pct_financiacion = st.slider(
        "Porcentaje del coste total financiado externamente",
        min_value=0, max_value=100, value=40, step=5,
        format="%d%%"
    )

    coste_total = coste_total_equipos() + coste_total_servicios()
    capital_externo  = coste_total * (pct_financiacion / 100)
    capital_propio   = coste_total - capital_externo

    c_fin1, c_fin2, c_fin3 = st.columns(3)
    with c_fin1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value">{pct_financiacion}%</div>
            <div class="label">Financiación externa</div>
        </div>""", unsafe_allow_html=True)
    with c_fin2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color:#f0883e">{formato_eur(capital_externo)}</div>
            <div class="label">Capital externo</div>
        </div>""", unsafe_allow_html=True)
    with c_fin3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color:#3fb950">{formato_eur(capital_propio)}</div>
            <div class="label">Capital propio</div>
        </div>""", unsafe_allow_html=True)


# ── COLUMNA RESUMEN ───────────────────────────────────────────────────────────
with col_summary:
    st.markdown('<div class="section-label">Resumen del Proyecto</div>', unsafe_allow_html=True)

    # Datos clave
    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-title">Duración</div>
        <div class="summary-value">{años_proyecto} <span style="font-size:0.9rem">años</span></div>
    </div>
    <div class="summary-box">
        <div class="summary-title">Buques / Año</div>
        <div class="summary-value">{num_buques:,}</div>
    </div>
    <div class="summary-box">
        <div class="summary-title">Toneladas / Año</div>
        <div class="summary-value">{toneladas_anuales:,}</div>
        <div class="summary-label">{tipo_carga}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Estructura de Costes</div>', unsafe_allow_html=True)

    coste_servicios = coste_total_servicios()
    coste_equipos   = coste_total_equipos()
    coste_total_val = coste_servicios + coste_equipos

    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-title">Servicios ({len(st.session_state.servicios)} items)</div>
        <div class="summary-value" style="font-size:1.1rem; color:#58a6ff">{formato_eur(coste_servicios)}</div>
    </div>
    <div class="summary-box">
        <div class="summary-title">Equipos ({len(st.session_state.equipos)} items)</div>
        <div class="summary-value" style="font-size:1.1rem; color:#58a6ff">{formato_eur(coste_equipos)}</div>
    </div>
    <div class="summary-box" style="border-color: #58a6ff44;">
        <div class="summary-title">Inversión Total</div>
        <div class="summary-value">{formato_eur(coste_total_val)}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Financiación</div>', unsafe_allow_html=True)

    pct_propio = 100 - pct_financiacion
    st.markdown(f"""
    <div class="summary-box">
        <div class="summary-title">Capital propio · {pct_propio}%</div>
        <div class="summary-value" style="font-size:1.1rem; color:#3fb950">{formato_eur(capital_propio)}</div>
    </div>
    <div class="summary-box">
        <div class="summary-title">Capital externo · {pct_financiacion}%</div>
        <div class="summary-value" style="font-size:1.1rem; color:#f0883e">{formato_eur(capital_externo)}</div>
    </div>
    """, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ANÁLISIS FINANCIERO PORTUARIO · v0.1 · Módulo de introducción de datos
</div>
""", unsafe_allow_html=True)
