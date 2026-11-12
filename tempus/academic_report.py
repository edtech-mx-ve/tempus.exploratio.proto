"""Informe académico de las cinco series financieras; solo evidencia histórica."""
from __future__ import annotations

from datetime import datetime, timezone
import io
from typing import Mapping
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
    Spacer, Table, TableStyle,
)

from tempus.assets import ASSETS
from tempus.core import normalize_prices
from tempus.dataset import SYMBOLS
from tempus.descriptive import DescriptiveSummary, describe_closing_prices, closing_interpretation
from tempus.temporal import diagnose_time_series


def _money(number: float) -> str:
    return f"USD {number:,.2f}"


def _chart_png(frame: pd.DataFrame, title: str) -> io.BytesIO:
    """Construye la gráfica histórica sin recorte de títulos ni unidades."""
    data = normalize_prices(frame)
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    ax.plot(data.index, data["Close"], color="#1764a6", linewidth=1.35)
    ax.set_title(title, fontsize=10, pad=9)
    ax.set_xlabel("Fecha bursátil", fontsize=9)
    ax.set_ylabel("USD por acción", fontsize=9)
    ax.tick_params(axis="both", labelsize=8)
    ax.grid(alpha=0.23)
    fig.autofmt_xdate(rotation=25)
    fig.tight_layout(pad=2.4)
    bio = io.BytesIO()
    fig.savefig(bio, format="png", dpi=140, bbox_inches="tight", pad_inches=.17)
    plt.close(fig)
    bio.seek(0)
    return bio


def _page_number(canvas, doc) -> None:
    """Pie de página uniforme sin modificar contenido del documento."""
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#667181"))
    canvas.drawString(40, 24, "TEMPUS EXPLORATIO PROTO | Práctica 1 | Uso académico")
    canvas.drawRightString(A4[0] - 40, 24, f"Página {doc.page}")
    canvas.restoreState()


def _table(rows: list[list[str]], widths: list[int]) -> Table:
    """Presenta datos compactos con encabezado y unidades explícitas."""
    table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5edf5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8fafc")]),
        ("GRID", (0, 0), (-1, -1), .3, colors.HexColor("#c3ccd8")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def build_academic_pdf(frames: Mapping[str, pd.DataFrame]) -> bytes:
    """Genera un informe con cifras reales calculadas desde los datos recibidos.

    Verifica los cinco históricos sin alterarlos, no inventa precios ni
    interpreta eventos como causas demostradas.
    """
    if set(frames) != set(SYMBOLS):
        raise ValueError("El informe requiere exactamente las cinco series aprobadas")
    cleaned = {symbol: normalize_prices(frames[symbol]) for symbol in SYMBOLS}
    results = {symbol: describe_closing_prices(cleaned[symbol]) for symbol in SYMBOLS}
    diagnoses = {symbol: diagnose_time_series(cleaned[symbol]) for symbol in SYMBOLS}

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CaptionSmall", parent=styles["BodyText"],
        fontSize=8, leading=11, textColor=colors.HexColor("#5b6677"),
        spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="ReportBody", parent=styles["BodyText"],
        fontSize=9, leading=13, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="ReportTitle", parent=styles["Title"],
        fontSize=20, leading=25, alignment=TA_CENTER,
        textColor=colors.HexColor("#183b61"), spaceAfter=15,
    ))

    output = io.BytesIO()
    doc = SimpleDocTemplate(
        output, pagesize=A4,
        leftMargin=42, rightMargin=42, topMargin=43, bottomMargin=43,
        title="TEMPUS EXPLORATIO PROTO | Informe de la Práctica 1",
        author="TEMPUS EXPLORATIO PROTO",
    )
    elements: list[object] = []

    def text(value: str, style: str = "ReportBody") -> None:
        elements.append(Paragraph(escape(value), styles[style]))

    def markup(value: str, style: str = "ReportBody") -> None:
        elements.append(Paragraph(value, styles[style]))

    # Portada
    elements.append(Spacer(1, 100))
    text("TEMPUS EXPLORATIO PROTO", "ReportTitle")
    text("Práctica 1: análisis, implementación y prueba de cinco series temporales financieras", "Heading2")
    text("TEMPUS DECISIO PROTO · Módulo I")
    text("Instituto Internacional de Aguascalientes")
    text("Maestría en Inteligencia Artificial para la Transformación Digital")
    text("Tópicos de IA para la Transformación Digital · Unidad 4")
    text("Tutor: Dr. Francisco Javier Luna Rosas")
    text("Alumno: Antonio Nicolás Toro González")
    text("Cobertura oficial: 2016-10-31 a 2026-10-30 (10 años)")
    text(f"Informe generado (UTC): {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}")
    elements.append(PageBreak())

    text("1. Introducción", "Heading1")
    text("Se estudian cinco series cuantitativas de precios de cierre bursátil "
         "correspondientes a JNJ, MSFT, JPM, WMT y XOM. "
         "El objetivo es describir su comportamiento histórico durante diez años, "
         "representarlo gráficamente y verificar las condiciones y la integridad "
         "de los datos. No se generan pronósticos.")
    text("Las fechas delimitan las sesiones históricas incluidas en los archivos "
         "versionados del proyecto. Los cierres se expresan en USD por acción, "
         "con la convención de ajuste indicada en los metadatos de origen.")
    text("2. Metodología y tecnologías", "Heading1")
    text("Secuencia aplicada: adquisición y conservación de snapshots; validación "
         "OHLCV y fechas; diagnóstico cuantitativo, cronológico y de regularidad "
         "bursátil; cálculo de indicadores; visualización individual y comparativa; "
         "exportación y pruebas reproducibles.")
    text("Python: pandas (DatetimeIndex, sort_index, rolling, pct_change, "
         "mean, std y cummax); NumPy (isfinite y sqrt); "
         "exchange_calendars (calendario XNYS); Matplotlib (gráficas para PDF); "
         "Plotly y Streamlit (interfaz); ReportLab (documentación); "
         "pytest (pruebas).")
    text("3. Resumen comparativo de cierre", "Heading1")
    rows = [["Empresa", "Cierre inicial", "Último cierre", "Cambio %", "Volatil. %"]]
    for symbol in SYMBOLS:
        d = results[symbol]
        rows.append([
            symbol, _money(d.cierre_inicial), _money(d.cierre_final),
            f"{d.cambio_porcentual:+.2f}%", f"{d.volatilidad_anual_pct:.2f}%"
        ])
    elements.append(_table(rows, [85, 115, 120, 95, 95]))
    elements.append(Spacer(1, 9))
    text("La variación porcentual compara exclusivamente el primer y el último cierre "
         "disponibles de cada serie. La volatilidad anualizada se estima sobre "
         "rendimientos diarios, con 252 sesiones como convención anual.", "CaptionSmall")

    # Fichas individuales, cada una en página separada
    for i, symbol in enumerate(SYMBOLS, start=1):
        d = results[symbol]
        elements.append(PageBreak())
        text(f"4.{i}. {ASSETS[symbol].company} ({symbol})", "Heading1")
        text(f"Sector: {ASSETS[symbol].sector}. Variable: precio de cierre "
             f"(USD por acción). Frecuencia: sesiones bursátiles.")
        text(f"Período: {d.fecha_inicial} a {d.fecha_final}. "
             f"Observaciones: {d.sesiones:,}.")
        rows = [
            ["Indicador", "Valor", "Indicador", "Valor"],
            ["Primer cierre", _money(d.cierre_inicial),
             "Último cierre", _money(d.cierre_final)],
            ["Variación absoluta", _money(d.cambio_absoluto),
             "Variación relativa", f"{d.cambio_porcentual:+.2f}%"],
            ["Cierre mínimo", _money(d.cierre_minimo),
             "Fecha mínimo", d.fecha_minimo],
            ["Cierre máximo", _money(d.cierre_maximo),
             "Fecha máximo", d.fecha_maximo],
            ["Media de cierre", _money(d.media_cierre),
             "Mediana de cierre", _money(d.mediana_cierre)],
            ["Desv. estándar", _money(d.desv_estandar_cierre),
             "Volatil. anual", f"{d.volatilidad_anual_pct:.2f}%"],
            ["Volumen promedio", f"{d.volumen_promedio:,.0f} acciones",
             "Caída máxima", f"{d.max_caida_pct:.2f}%"],
        ]
        elements.append(_table(rows, [123, 126, 124, 125]))
        elements.append(Spacer(1, 9))
        text("Análisis descriptivo", "Heading2")
        text(closing_interpretation(d, ASSETS[symbol].company))
        elements.append(Spacer(1, 5))
        image_bytes = _chart_png(cleaned[symbol], f"{symbol} | Precio de cierre histórico")
        elements.append(Image(image_bytes, width=494, height=195))
        text("Eje horizontal: fecha bursátil. Eje vertical: USD por acción. "
             "La serie expresa observaciones históricas, no estimaciones futuras.",
             "CaptionSmall")

    elements.append(PageBreak())
    text("5. Implementación y prueba de las series", "Heading1")
    text("Los cinco snapshots son analizados con las mismas funciones, sin completar "
         "automáticamente fechas faltantes ni sustituir cotizaciones históricas. "
         "Se comprobaron los campos OHLCV y la consistencia matemática entre "
         "precios de apertura, máximo, mínimo y cierre.")
    rows = [["Serie", "Cuantitativa", "Cronológica", "Regularidad", "Faltan", "Extras"]]
    for symbol in SYMBOLS:
        diag = diagnoses[symbol]
        rows.append([symbol, diag.cuantitativa, diag.cronologica,
                     diag.regularidad, str(diag.sesiones_faltantes),
                     str(diag.fechas_fuera_sesion)])
    elements.append(_table(rows, [61, 101, 98, 104, 73, 73]))
    elements.append(Spacer(1, 10))
    text("La frecuencia se evalúa según sesiones bursátiles XNYS, no por días "
         "naturales consecutivos. Los días de cierre programado de la bolsa no "
         "se consideran observaciones ausentes. El diagnóstico se calcula "
         "entre la primera y última fecha de cada serie.")
    text("Las pruebas automatizadas verifican funciones y contratos de datos; "
         "no sustituyen la comprobación visual de todos los controles de Streamlit.")
    text("6. Conclusiones", "Heading1")
    ordered = sorted(SYMBOLS, key=lambda name: results[name].cambio_porcentual, reverse=True)
    best = ordered[0]
    worst = ordered[-1]
    text(f"En la ventana de estudio, {best} presentó la mayor variación relativa "
         f"de cierre ({results[best].cambio_porcentual:+.2f}%) y {worst} la menor "
         f"({results[worst].cambio_porcentual:+.2f}%). Estas diferencias describen "
         "la evolución observada de cada instrumento y no equivalen a una "
         "comparación ajustada por riesgo ni a una predicción.")
    text("Se logró documentar, representar gráficamente y examinar la calidad "
         "de cinco series financieras con una metodología reproducible. "
         "La interpretación permanece limitada al período y los datos disponibles.")
    text("7. Referencias", "Heading1")
    markup("Yahoo Finance. (2026). <i>Yahoo Finance</i>. https://finance.yahoo.com/")
    markup("Aroussi, R. (2026). <i>yfinance</i> [Software]. GitHub. "
           "https://github.com/ranaroussi/yfinance")
    markup("Streamlit. (2026). <i>Documentation</i>. https://docs.streamlit.io/")
    markup("The pandas development team. (2026). <i>pandas documentation</i>. "
           "https://pandas.pydata.org/docs/")
    markup("Matplotlib Development Team. (2026). <i>Matplotlib</i>. "
           "https://matplotlib.org/")

    doc.build(elements, onFirstPage=_page_number, onLaterPages=_page_number)
    return output.getvalue()
