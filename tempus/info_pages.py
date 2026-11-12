"""Páginas informativas de TEMPUS EXPLORATIO PROTO.

Adaptación del módulo original tempus/info_pages.py, centrada en la
Práctica 1: adquisición, descripción, visualización y prueba de cinco series.
No entrena modelos ni genera pronósticos.
"""
from __future__ import annotations

import streamlit as st


def render_information_page(page: str) -> None:
    """Renderiza contenido académico e institucional correspondiente a una sección.

    Args:
        page: Nombre validado de la sección informativa.

    Raises:
        ValueError: Cuando la sección no existe.
    """
    if page == "Acerca de":
        st.header("Acerca de TEMPUS EXPLORATIO PROTO")
        st.caption("TEMPUS DECISIO PROTO · Módulo I · Práctica 1")
        st.markdown("""
**TEMPUS EXPLORATIO PROTO** es una aplicación académica desarrollada en
**Python y Streamlit** para explorar cinco series financieras obtenidas de la web:
**JNJ, MSFT, JPM, WMT y XOM**.

**Cobertura histórica incluida:** diez años, desde el **31 de octubre de 2016**
hasta el **30 de octubre de 2026**, con **2.514 sesiones por empresa**
y **12.570 observaciones en total**, según los snapshots de esta versión.
La cobertura indicada corresponde al conjunto validado suministrado;
las consultas web opcionales pueden utilizar otros períodos.

Su finalidad es **explorar y analizar cinco series temporales financieras**
mediante la adquisición, validación y representación gráfica de datos históricos.
Permite examinar el comportamiento de variables cuantitativas, identificar
tendencias y fluctuaciones, calcular indicadores estadísticos descriptivos
y verificar la consistencia de los resultados obtenidos.

**Relación con la plataforma:** TEMPUS DECISIO PROTO integra este módulo
con TEMPUS PREDICTIO PROTO. Exploratio entrega datos históricos validados,
metadatos e indicadores descriptivos; Predictio se encargará después del
modelado y la evaluación predictiva.
""")
        a, b, c = st.columns(3)
        a.metric("Series históricas", "5")
        b.metric("Práctica", "1")
        c.metric("Modelos predictivos", "0")
        st.subheader("Metodología")
        st.markdown(
            "**Fuente web → adquisición / snapshot → validación → "
            "análisis descriptivo → gráficas → pruebas → exportación e informe PDF.**"
        )
        st.subheader("Alcance y limitaciones")
        st.markdown("""
- Se analizan **observaciones históricas**, no cotizaciones garantizadas en tiempo real.
- Cinco históricos bursátiles no constituyen, por sí solos, una infraestructura Big Data distribuida.
- La aplicación no emite recomendaciones de inversión ni proyecta precios futuros.
- La fecha y el número de registros dependen de la versión validada de los datos.
""")

    elif page == "Fundamentos":
        st.header("Fundamentos de series temporales financieras")
        st.caption("Conceptos utilizados en el análisis e implementación de la Práctica 1")
        st.subheader("1. ¿Qué es una serie de tiempo?")
        st.markdown("""
Es una sucesión de observaciones de una **variable cuantitativa** ordenadas
en el tiempo. Para analizarla correctamente se identifican sus fechas,
la frecuencia de observación y la unidad de medida.
En los datos oficiales incluidos, la ventana histórica comprende
**2016-10-31 a 2026-10-30 (10 años)**.
Las cotizaciones bursátiles se registran por **sesión de negociación**:
los días sin mercado no representan observaciones faltantes automáticas.
""")
        st.subheader("2. Condiciones fundamentales")
        st.markdown("""
1. **Cuantitativa:** la variable se registra mediante valores numéricos medibles.
2. **Orden cronológico:** los datos tienen fechas válidas, ordenadas y sin duplicados.
3. **Regularidad temporal:** se establece una frecuencia de observación.
   Aquí se comprueba cada **sesión bursátil XNYS** dentro del período disponible.

Los días de cierre de la bolsa no son valores faltantes. Las sesiones efectivamente
ausentes se identifican por separado; los períodos regulares son útiles para
varios métodos, aunque también existen series temporales con muestreo irregular.
""")
        st.subheader("3. Variables financieras OHLCV")
        st.markdown("""
- **Open (apertura):** precio al inicio de la sesión.
- **High (máximo):** precio máximo observado durante la sesión.
- **Low (mínimo):** precio mínimo observado.
- **Close (cierre):** precio al cierre de la sesión.
- **Volume (volumen):** acciones negociadas, no un precio.

El conjunto puede contener valores ajustados por eventos corporativos;
la interpretación de cada variable depende de la convención de ajuste declarada.
""")
        st.subheader("4. Lectura de las gráficas")
        st.markdown("""
El eje horizontal representa fechas de negociación; el vertical muestra
**USD por acción** para precios o **número de acciones** para volumen.
Las gráficas históricas sirven para identificar oscilaciones, máximos,
mínimos y tendencias descriptivas; no garantizan el comportamiento futuro.
""")
        st.subheader("5. Indicadores descriptivos")
        st.markdown("""
- **Rendimiento por sesión:** cambio relativo entre dos cierres consecutivos.
- **MA20 y MA50:** promedios móviles sobre 20 y 50 sesiones anteriores, respectivamente.
- **Volatilidad histórica:** medida de dispersión de rendimientos, no de dirección.
- **Índice base 100:** transforma cada serie para comparar variaciones relativas,
  sin equiparar precios nominales.
- **Máximos, mínimos, media y desviación estándar:** resumen del histórico observado.
""")
        st.subheader("6. Calidad, interpretación y límites")
        st.markdown("""
Se revisan duplicados, orden de fechas, tipos numéricos, valores faltantes
y consistencia entre apertura, máximos, mínimos y cierre. Los cambios bruscos
pueden reflejar eventos reales; no se deben borrar sin investigar.

**Continuidad académica:** normalidad, descomposición, periodicidad y técnicas
de inteligencia artificial se estudiarán en profundidad en
**TEMPUS PREDICTIO PROTO**, después de validar las series.
""")

    elif page == "Ayuda":
        st.header("Ayuda · TEMPUS EXPLORATIO PROTO")
        st.caption("Guía práctica de uso y solución de incidencias")
        st.subheader("Recorrido recomendado")
        st.markdown("""
1. En el menú lateral, selecciona una de las empresas: **JNJ, MSFT, JPM, WMT o XOM**.
2. En **Análisis financiero → Serie individual**, selecciona apertura, máximo,
   mínimo, cierre o volumen y observa la evolución cronológica.
3. En **Cinco series**, verifica la gráfica y la descripción de cada empresa.
4. En **Comparación**, consulta las series base 100 y los estadísticos.
5. En **Calidad y resultados**, revisa OHLCV y las tres condiciones temporales, descarga los
   insumos para Predictio o genera el borrador PDF de la Práctica 1.
6. En **Dataset**, verifica fechas, cobertura, procedencia, tabla OHLCV y sesiones XNYS faltantes.
7. En **Fundamentos**, consulta las definiciones; en **Trivia** realiza la autoevaluación.
""")
        st.subheader("Ejemplo de comprobación · Exxon Mobil (XOM)")
        st.markdown("""
- Selecciona **XOM** y visualiza **Close**. Comprueba que el eje vertical
  represente el precio y el eje horizontal las fechas bursátiles.
- Activa las medias móviles MA20/MA50 y verifica que sean curvas históricas
  descriptivas.
- Cambia a **Volume**: las unidades deben ser acciones negociadas.
- Abre **Cinco series** y verifica que estén presentes también JNJ, MSFT, JPM y WMT.
- Consulta **Calidad y resultados**: una validación correcta significa que
  los archivos satisfacen las reglas implementadas, no que sus cotizaciones
  puedan predecirse con certeza.
""")
        st.subheader("Problemas habituales")
        st.markdown("""
- **Faltan datos oficiales:** verifica la carpeta `data/snapshots` y los manifiestos.
- **Falla una validación:** revisa el detalle de la condición cuantitativa,
  cronológica o de regularidad. No sustituyas registros sin documentar el motivo.
- **Sesiones faltantes:** se detectan comparando con el calendario XNYS;
  los fines de semana y cierres programados no son incidencias.
- **No se actualiza Yahoo Finance:** comprueba conectividad; los snapshots
  validados se conservan como respaldo y no son reemplazados automáticamente.
- **No se genera el PDF:** revisa las dependencias y el mensaje de error;
  el borrador requiere completar portada, interpretación y referencias finales.
- **No aparece un cambio:** vuelve a cargar la pestaña del navegador.
""")
        st.code(".\\.venv\\Scripts\\python.exe -m pytest tests -v", language="powershell")
        st.code(".\\.venv\\Scripts\\python.exe -m streamlit run app.py", language="powershell")
        st.caption("URL local habitual: http://localhost:8501 (si el puerto está disponible).")

    elif page == "Institucional":
        st.header("Institucional")
        st.caption("Identificación académica y propósito institucional")
        st.markdown("""
**Proyecto principal:** TEMPUS DECISIO PROTO

**Aplicación:** TEMPUS EXPLORATIO PROTO

**Módulo:** I — Análisis, implementación y prueba de cinco series financieras

**Institución:** Instituto Internacional de Aguascalientes

**Programa:** Maestría en Inteligencia Artificial para la Transformación Digital

**Asignatura:** Tópicos de IA para la Transformación Digital · Unidad 4

**Tutor:** Dr. Francisco Javier Luna Rosas

**Alumno:** Antonio Nicolás Toro González
""")
        st.subheader("Descripción académica")
        st.markdown(
            "Aplicación web educativa para analizar series financieras de cinco empresas, "
            "representarlas gráficamente, verificar sus datos y generar evidencias "
            "reproducibles de la Práctica 1. El pronóstico pertenece a la Práctica 2."
        )
        st.subheader("Fuente y uso responsable")
        st.markdown(
            "Cotizaciones históricas consultables en "
            "[Yahoo Finance](https://finance.yahoo.com/) mediante "
            "[yfinance](https://github.com/ranaroussi/yfinance). "
            "Los datos de respaldo tienen fecha y procedencia propias. "
            "Los contenidos son educativos y no constituyen asesoramiento financiero."
        )
    elif page == "Tecnologías":
        st.header("Tecnologías")
        st.caption("Herramientas y evidencia de implementación de las cinco series temporales")
        st.markdown(
            "El proyecto aplica una secuencia reproducible de **adquisición → "
            "validación → verificación temporal → descripción → visualización → "
            "pruebas → informe y exportación** sobre cinco históricos de "
            "**10 años (2016-10-31 a 2026-10-30)**."
        )
        st.subheader("Bibliotecas y funciones utilizadas")
        st.dataframe([
            {"Biblioteca": "yfinance", "Función o recurso": "Ticker().history() / consulta de cotizaciones",
             "Aplicación": "Adquisición web opcional de OHLCV; sin reemplazo automático de snapshots"},
            {"Biblioteca": "pandas", "Función o recurso": "DatetimeIndex, sort_index(), to_numeric()",
             "Aplicación": "Organización cronológica y comprobación numérica"},
            {"Biblioteca": "pandas", "Función o recurso": "pct_change(), rolling().mean()",
             "Aplicación": "Rendimientos por sesión y medias móviles MA20 / MA50"},
            {"Biblioteca": "pandas", "Función o recurso": "mean(), median(), std(), min(), max(), cummax()",
             "Aplicación": "Cierre inicial/final, dispersión, extremos y caída histórica"},
            {"Biblioteca": "NumPy", "Función o recurso": "isfinite(), sqrt()",
             "Aplicación": "Valores válidos y volatilidad anualizada"},
            {"Biblioteca": "exchange_calendars", "Función o recurso": "get_calendar('XNYS'), sessions_in_range()",
             "Aplicación": "Identificar sesiones bursátiles esperadas y faltantes"},
            {"Biblioteca": "Plotly", "Función o recurso": "graph_objects.Scatter()",
             "Aplicación": "Gráficas cronológicas interactivas"},
            {"Biblioteca": "Matplotlib", "Función o recurso": "plot(), savefig()",
             "Aplicación": "Gráficas de las cinco empresas en el PDF"},
            {"Biblioteca": "Streamlit", "Función o recurso": "tabs(), dataframes, métricas y download_button()",
             "Aplicación": "Interfaz, indicadores y descarga"},
            {"Biblioteca": "ReportLab", "Función o recurso": "SimpleDocTemplate, Paragraph, Table, Image",
             "Aplicación": "Informe académico reproducible"},
            {"Biblioteca": "pytest", "Función o recurso": "Pruebas de validación y exportación",
             "Aplicación": "Verificación de las funciones del proyecto"},
        ], hide_index=True, use_container_width=True)
        st.subheader("Cómo se cumple cada etapa")
        st.dataframe([
            {"Etapa": "1. Adquisición", "Implementación": "tempus/io.py y snapshots Parquet con manifiestos",
             "Evidencia": "Cinco series: JNJ, MSFT, JPM, WMT y XOM"},
            {"Etapa": "2. Validación OHLCV", "Implementación": "tempus/core.py: normalize_prices()",
             "Evidencia": "Tipos, duplicados, fechas, rango y coherencia de precios"},
            {"Etapa": "3. Condiciones temporales", "Implementación": "tempus/temporal.py: diagnose_time_series()",
             "Evidencia": "Cuantitativa, cronológica y regularidad de sesiones XNYS"},
            {"Etapa": "4. Estadística descriptiva", "Implementación": "tempus/descriptive.py y tempus/core.py",
             "Evidencia": "Cierres inicial/final, extremos, promedios, variación y volatilidad"},
            {"Etapa": "5. Gráficas", "Implementación": "app.py / Plotly y academic_report.py / Matplotlib",
             "Evidencia": "Una gráfica de cierre para cada empresa y comparación base 100"},
            {"Etapa": "6. Verificación", "Implementación": "tests/ con pytest",
             "Evidencia": "Resultados comprobables al ejecutar la suite en el equipo"},
            {"Etapa": "7. Reporte", "Implementación": "tempus/academic_report.py",
             "Evidencia": "PDF con cinco fichas individuales, gráficas y tabla comparativa"},
            {"Etapa": "8. Exportación", "Implementación": "tempus/dataset.py",
             "Evidencia": "CSV, manifiesto SHA-256 e indicadores para Predictio"},
        ], hide_index=True, use_container_width=True)
        st.subheader("Organización del proyecto")
        st.markdown("""
- **`app.py`:** navegación y gráficas interactivas en Streamlit.
- **`tempus/io.py` y `tempus/dataset.py`:** carga, versiones y exportación de datos.
- **`tempus/core.py`:** validación OHLCV e indicadores históricos.
- **`tempus/temporal.py`:** comprobación de sesiones bursátiles.
- **`tempus/descriptive.py`:** estadísticos e interpretación por empresa.
- **`tempus/academic_report.py`:** informe PDF con cifras y gráficos.
- **`tests/`:** pruebas automatizadas.

El análisis es **descriptivo**. No se aplican ARIMA, redes neuronales ni
pronósticos futuros, reservados para TEMPUS PREDICTIO PROTO.
""")
    else:
        raise ValueError(f"Página informativa no reconocida: {page}")
