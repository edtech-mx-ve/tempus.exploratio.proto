"""TEMPUS EXPLORATIO PROTO · Práctica 1: cinco series temporales financieras."""
from __future__ import annotations

import logging
from datetime import date, timedelta
import io
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from tempus.assets import ASSETS
from tempus.core import enrich_prices, normalize_prices, summarize
from tempus.dataset import SYMBOLS, load_official_data, describe_quality, comparison_base100, export_bundle
from tempus.io import download_ticker
from tempus.academic_report import build_academic_pdf
from tempus.info_pages import render_information_page
from tempus.temporal import diagnose_time_series
from tempus.descriptive import describe_closing_prices, closing_interpretation

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
LOG = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parent
SECTIONS = ("Análisis financiero", "Acerca de", "Dataset", "Fundamentos",
            "Trivia", "Ayuda", "Institucional", "Tecnologías")
QUIZ = (
    ("¿Qué tipo de variable se analiza en estas series bursátiles?",
     ("Cuantitativa", "Exclusivamente cualitativa", "Sin unidad de medida"), 0,
     "Los precios y volúmenes son mediciones numéricas."),
    ("¿Qué representa Close en OHLCV?",
     ("Volumen", "Precio de cierre", "Precio mínimo"), 1,
     "Close es el precio de cierre de la sesión."),
    ("¿Qué representa una gráfica de precio frente a fecha?",
     ("Evolución histórica", "Ganancia garantizada", "Pronóstico futuro"), 0,
     "La gráfica de la Práctica 1 es una representación descriptiva."),
    ("¿Qué criterio permite comparar sesiones consecutivas?",
     ("Orden alfabético", "Orden cronológico", "Orden por precio"), 1,
     "Las observaciones deben respetar el orden del tiempo."),
    ("¿Cómo se interpreta la regularidad en el histórico bursátil?",
     ("Días naturales sin excepción", "Sesiones del mercado", "Solo lunes"), 1,
     "Los fines de semana y feriados sin negociación no son sesiones faltantes."),
    ("¿Qué significa volumen bursátil?",
     ("Precio máximo", "Número de acciones negociadas", "Tasa de interés"), 1,
     "Volume refleja la actividad negociada durante cada sesión."),
    ("¿Para qué sirve una comparación base 100?",
     ("Igualar el precio real de cada acción", "Comparar evoluciones relativas", "Predecir mañana"), 1,
     "Cada serie inicia en 100 y permite comparar variaciones relativas."),
)


@st.cache_data(show_spinner="Verificando históricos oficiales…")
def official_frames() -> dict[str, pd.DataFrame]:
    """Carga los snapshots oficiales con verificación SHA-256."""
    return load_official_data()


def line_chart(frame: pd.DataFrame, ticker: str, column: str,
               show_ma: bool = False) -> go.Figure:
    """Representa la variable financiera sobre un eje cronológico."""
    enriched = enrich_prices(frame)
    if column not in ("Open", "High", "Low", "Close", "Volume"):
        raise ValueError("Variable no admitida")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=enriched.index, y=enriched[column], name=column,
                             mode="lines", line={"width": 2}))
    if show_ma and column == "Close":
        for field, label in (("sma_20", "MA20"), ("sma_50", "MA50")):
            fig.add_trace(go.Scatter(x=enriched.index, y=enriched[field],
                                     mode="lines", name=label))
    fig.update_layout(title=f"{ticker} — {column} por sesión bursátil",
                      xaxis_title="Fecha bursátil",
                      yaxis_title="Volumen (acciones)" if column == "Volume" else "Precio (USD/acción; ajuste según fuente)",
                      height=420, hovermode="x unified", margin={"t": 60, "b": 35})
    return fig


def navigation() -> tuple[str, str]:
    """Dibuja las siete secciones oficiales de navegación."""
    with st.sidebar:
        logo = ROOT / "assets" / "tempus-logo.png"
        if logo.exists():
            st.image(str(logo), width=155)
        st.markdown("### TEMPUS EXPLORATIO PROTO")
        st.caption("TEMPUS DECISIO PROTO · Módulo I")
        st.write("Exploración y análisis de acciones bursátiles como series temporales cuantitativas.")
        st.divider()
        st.caption("INFORMACIÓN DEL PROYECTO")
        page = st.radio("Navegación", SECTIONS, label_visibility="collapsed")
        st.divider()
        ticker = st.selectbox("Serie financiera", SYMBOLS, format_func=lambda x: f"{x} · {ASSETS[x].company}")
        st.caption("Práctica 1 · Solo análisis histórico")
    return page, ticker


def render_financial(frames: dict[str, pd.DataFrame], ticker: str) -> None:
    """Análisis descriptivo principal y comprobación de cinco series."""
    st.header("Análisis financiero")
    st.caption("Cinco series históricas · Análisis, implementación y prueba")
    st.info("Cobertura oficial: **10 años (2016-10-31 a 2026-10-30)** · "
            "**2.514 sesiones por empresa** · **12.570 registros históricos en total**.")
    tabs = st.tabs(["Serie individual", "Cinco series", "Comparación", "Calidad y resultados"])
    with tabs[0]:
        frame = frames[ticker]
        summary = summarize(frame)
        a,b,c,d = st.columns(4)
        a.metric("Registros", f"{summary['observaciones']:,}")
        b.metric("Fecha inicial", summary["inicio"])
        c.metric("Fecha final", summary["fin"])
        d.metric("Último cierre", f"${summary['cierre_final']:,.2f}")
        st.write(f"**{ASSETS[ticker].company} — {ASSETS[ticker].sector}.** "
                 "Se representa la evolución histórica de una variable cuantitativa por sesión bursátil.")
        individual = describe_closing_prices(frame)
        st.markdown("**Resumen histórico del cierre**")
        st.write(closing_interpretation(individual, ASSETS[ticker].company))
        column = st.selectbox("Variable temporal", ("Close", "Open", "High", "Low", "Volume"),
                              format_func=lambda x: {"Close":"Cierre","Open":"Apertura",
                              "High":"Máximo","Low":"Mínimo","Volume":"Volumen"}[x])
        show_ma = st.checkbox("Mostrar medias móviles históricas MA20 y MA50", value=True,
                              disabled=column != "Close")
        st.plotly_chart(line_chart(frame,ticker,column,show_ma), use_container_width=True)
        unidad = "acciones negociadas" if column == "Volume" else "USD por acción (ajuste según la fuente)"
        st.caption(
            f"Variable: {column} · Unidad: {unidad} · "
            f"Frecuencia: sesión bursátil · Finalidad: observar cambios históricos de {ASSETS[ticker].company}."
        )
        st.info("La serie representa hechos históricos. No constituye una predicción ni una recomendación de inversión.")
        st.dataframe(frame.tail(20), use_container_width=True)
    with tabs[1]:
        st.subheader("Implementación y comprobación de las cinco series exigidas")
        for sym in SYMBOLS:
            with st.expander(f"{sym} · {ASSETS[sym].company}", expanded=sym == ticker):
                st.write(f"**Finalidad:** observar cómo cambia el precio de cierre de {ASSETS[sym].company} a lo largo del tiempo.")
                st.write(closing_interpretation(describe_closing_prices(frames[sym]), ASSETS[sym].company))
                st.plotly_chart(line_chart(frames[sym],sym,"Close"), use_container_width=True,
                                key=f"chart-{sym}")
                q = describe_quality(frames[sym])
                st.success(f"Prueba OHLCV: {q['validacion']} · {q['filas']:,} observaciones · {q['inicio']} a {q['fin']}")
    with tabs[2]:
        st.subheader("Comparación relativa: base 100")
        compare = comparison_base100(frames)
        st.line_chart(compare, height=410)
        st.caption("Base 100 permite comparar variaciones relativas; no representa rentabilidad futura.")
        st.subheader("Cierres y variación acumulada de las cinco empresas")
        details = pd.DataFrame([
            {
                "Empresa": sym,
                "Cierre inicial (USD)": round((d := describe_closing_prices(frames[sym])).cierre_inicial, 2),
                "Cierre final (USD)": round(d.cierre_final, 2),
                "Variación (%)": round(d.cambio_porcentual, 2),
                "Volatilidad anualizada (%)": round(d.volatilidad_anual_pct, 2),
            } for sym in SYMBOLS
        ])
        st.dataframe(details, hide_index=True, use_container_width=True)
        st.subheader("Estadísticos descriptivos")
        summary_table = pd.DataFrame([{"Empresa":s, **summarize(frames[s])} for s in SYMBOLS])
        st.dataframe(summary_table, hide_index=True, use_container_width=True)
    with tabs[3]:
        st.subheader("Condiciones de las series temporales · XNYS")
        temporal = pd.DataFrame([
            {"Empresa": sym, **diagnose_time_series(frames[sym]).to_dict()}
            for sym in SYMBOLS
        ])
        st.dataframe(temporal, hide_index=True, use_container_width=True)
        if (temporal[["cuantitativa", "cronologica", "regularidad"]] == "APROBADA").all().all():
            st.success("Las tres condiciones temporales se verificaron en las cinco series.")
        else:
            st.warning("Se detectaron incidencias temporales. Revisa las sesiones faltantes o fuera de calendario.")
        st.caption("Regularidad: calendario bursátil XNYS; los cierres programados no se cuentan como faltantes.")
        quality = pd.DataFrame([{"Empresa":s, **describe_quality(frames[s])} for s in SYMBOLS])
        st.dataframe(quality, hide_index=True, use_container_width=True)
        st.info("Los datos disponibles se verificaron con las reglas OHLCV; consulta también el diagnóstico temporal.")
        st.caption("Prueba automatizada de datos: no sustituye la inspección manual de la interfaz.")
        st.subheader("Entregables")
        st.download_button("Descargar insumos para TEMPUS PREDICTIO PROTO (ZIP)",
                           export_bundle(frames), file_name="tempus_exploratio_proto_datos.zip",
                           mime="application/zip", key="zip-financial")
        if st.button("Generar informe académico descriptivo (PDF)", type="primary"):
            try:
                st.session_state["report_pdf"] = build_academic_pdf(frames)
            except (ValueError, OSError, RuntimeError) as exc:
                LOG.exception("Falló el informe académico")
                st.error(f"No fue posible generar el informe: {exc}")
        if "report_pdf" in st.session_state:
            st.download_button("Descargar informe PDF de Práctica 1",
                               st.session_state["report_pdf"],
                               file_name="TEMPUS_EXPLORATIO_PROTO_Practica_1.pdf",
                               mime="application/pdf")
            st.caption("El informe se genera a partir de los históricos verificados; revisa las interpretaciones y las referencias antes de su entrega académica.")


def render_dataset(frames: dict[str, pd.DataFrame], ticker: str) -> None:
    """Muestra fuente, estructura, calidad y exportación del dataset."""
    st.header("Dataset")
    st.caption("Cobertura, calidad y contrato de datos para la Práctica 2")
    st.info("Históricos oficiales: **10 años (2016-10-31 a 2026-10-30)**. "
            "Cada una de las cinco acciones contiene **2.514 registros**; "
            "**12.570 observaciones** en total. "
            "La actualización web opcional no reemplaza estos snapshots.")
    st.markdown("**Fuente de referencia:** históricos financieros del proyecto original, con snapshots "
                "y metadatos de integridad. Se admite la actualización desde Yahoo Finance.")
    st.dataframe(pd.DataFrame([{"Símbolo":s,"Empresa":ASSETS[s].company,
                               "Sector":ASSETS[s].sector,**describe_quality(frames[s])}
                              for s in SYMBOLS]), hide_index=True, use_container_width=True)
    st.subheader("Condiciones fundamentales de las series")
    diag = pd.DataFrame([
        {"Ticker": symbol, **diagnose_time_series(frames[symbol]).to_dict()}
        for symbol in SYMBOLS
    ])
    st.dataframe(diag, hide_index=True, use_container_width=True)
    st.caption(
        "Cuantitativa: valores numéricos válidos; cronológica: fechas únicas y ordenadas; "
        "regularidad: sesiones XNYS esperadas frente a las observadas. "
        "La evaluación preserva los registros originales."
    )
    st.subheader("Contexto de Big Data")
    st.info(
        "Estas cinco series ejemplifican datos de la web con estructura temporal. "
        "El tamaño del conjunto local no demuestra procesamiento masivo distribuido "
        "ni captura en tiempo real."
    )
    st.subheader("Diccionario OHLCV")
    st.markdown(
        "**Open:** apertura · **High:** máximo · **Low:** mínimo · "
        "**Close:** cierre · **Volume:** volumen negociado. "
        "Los ajustes corporativos deben interpretarse conforme a la fuente."
    )
    st.subheader(f"Observaciones OHLCV · {ticker}")
    st.dataframe(frames[ticker].tail(40), use_container_width=True)
    st.caption("Open / High / Low / Close expresados en USD por acción; "
               "Volume en acciones negociadas. Se respeta el calendario de sesiones bursátiles.")
    st.download_button("Descargar conjunto validado y manifiesto (ZIP)",
                       export_bundle(frames), "tempus_exploratio_proto_datos.zip",
                       mime="application/zip", key="zip-dataset")
    with st.expander("Actualizar un ticker desde la web (opcional)"):
        st.write("La actualización se consulta temporalmente y no reemplaza el dataset oficial validado.")
        if st.button(f"Consultar Yahoo Finance: {ticker}"):
            try:
                end = date.today() + timedelta(days=1)
                fresh = download_ticker(ticker, end-timedelta(days=365),end)
                st.success(f"Consulta completada: {len(fresh)} registros.")
                st.dataframe(fresh.tail(10))
                st.download_button("Descargar consulta en CSV",
                                   fresh.to_csv().encode("utf-8"),
                                   f"{ticker}_consulta_actual.csv", "text/csv")
            except (ValueError, RuntimeError, OSError, ImportError) as exc:
                LOG.warning("La actualización no se completó: %s",type(exc).__name__)
                st.error("No se pudo descargar la consulta. Los históricos oficiales permanecen disponibles.")


def render_trivia() -> None:
    """Trivia de cinco conceptos, con respuesta evaluada y retroalimentación."""
    st.header("Trivia")
    st.caption("Autoevaluación didáctica de series temporales y cotizaciones")
    st.subheader("¿De dónde viene TEMPUS DECISIO PROTO?")
    st.markdown("""
**TEMPUS DECISIO** combina dos términos de origen latino:
- **Tempus:** tiempo.
- **Decisio:** decisión o determinación.

Su interpretación conceptual es **«decisiones fundamentadas en el análisis
del tiempo y la información histórica»**.
**PROTO** identifica el carácter de prototipo académico y tecnológico.
""")
    st.subheader("¿Qué significa TEMPUS EXPLORATIO PROTO?")
    st.write(
        "Es el Módulo I dedicado a explorar, validar, analizar y visualizar "
        "series temporales financieras mediante Python y Streamlit."
    )
    st.subheader("¿Por qué cinco empresas?")
    st.write(
        "JNJ, MSFT, JPM, WMT y XOM permiten estudiar salud, tecnología, "
        "banca, comercio minorista y energía mediante un procedimiento homogéneo."
    )
    st.subheader("¿Qué condiciones caracterizan estas series temporales?")
    st.write(
        "Valores cuantitativos, secuencia cronológica y frecuencia definida "
        "por las sesiones bursátiles correspondientes."
    )
    st.subheader("¿Qué representa el logotipo?")
    logo = ROOT / "assets" / "tempus-logo.png"
    if logo.exists():
        st.image(str(logo), width=180)
    st.write(
        "Identifica visualmente a TEMPUS DECISIO PROTO y sus módulos. "
        "No se atribuyen simbolismos que el diseño no permita verificar."
    )
    st.subheader("¿Cómo se relacionan los módulos?")
    st.write(
        "TEMPUS EXPLORATIO PROTO organiza datos históricos validados e indicadores "
        "descriptivos; TEMPUS PREDICTIO PROTO utilizará estos insumos para "
        "modelado y evaluación posterior."
    )
    st.subheader("Autoevaluación interactiva")
    with st.form("quiz_form"):
        chosen = []
        for idx,(question, answers, _, _) in enumerate(QUIZ, start=1):
            chosen.append(st.radio(f"{idx}. {question}", answers,
                                   index=None, key=f"q{idx}"))
        submitted = st.form_submit_button("Evaluar respuestas", type="primary")
    if submitted:
        score = 0
        for choice,(question, answers, correct, feedback) in zip(chosen, QUIZ):
            if choice is None:
                st.warning(f"Sin responder: {question}")
            elif choice == answers[correct]:
                score += 1
                st.success(f"Correcto. {feedback}")
            else:
                st.error(f"Respuesta correcta: {answers[correct]}. {feedback}")
        st.metric("Resultado de Trivia", f"{score}/{len(QUIZ)}")



def main() -> None:
    """Control secuencial de la aplicación, con errores comunicados al usuario."""
    st.set_page_config(page_title="TEMPUS EXPLORATIO PROTO",
                       page_icon="📈", layout="wide",
                       initial_sidebar_state="expanded")
    page, ticker = navigation()
    st.title("TEMPUS EXPLORATIO PROTO")
    st.caption("Plataforma TEMPUS DECISIO PROTO · Práctica 1")
    st.markdown("**Exploración y análisis de acciones bursátiles como series temporales cuantitativas.**")
    if page in ("Acerca de","Fundamentos","Trivia","Ayuda","Institucional","Tecnologías"):
        if page == "Trivia":
            render_trivia()
        else:
            render_information_page(page)
    else:
        try:
            frames = official_frames()
            if page == "Análisis financiero":
                render_financial(frames,ticker)
            elif page == "Dataset":
                render_dataset(frames,ticker)
        except (FileNotFoundError, ValueError, RuntimeError, ImportError, OSError) as exc:
            LOG.exception("Carga/visualización no disponible")
            st.error(f"No se pudieron validar las cinco series: {exc}")
            st.info("Verifica PyArrow, los snapshots y sus archivos de metadatos.")
    st.divider()
    st.caption("TEMPUS EXPLORATIO PROTO · Uso académico · Datos históricos, no pronósticos")


if __name__ == "__main__":
    main()
