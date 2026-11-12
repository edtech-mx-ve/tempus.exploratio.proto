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
        st.caption("Navegación por dos áreas y guía de uso de la Práctica 1")
        st.subheader("1. Seleccionar un área")
        st.markdown("""
En la barra lateral, el bloque **SECCIONES** permite elegir entre dos áreas:

- **Análisis financiero:** muestra el selector **Serie financiera** para elegir
  JNJ, MSFT, JPM, WMT o XOM.
- **Información del proyecto:** muestra las siete páginas **Acerca de, Dataset,
  Fundamentos, Trivia, Ayuda, Institucional y Tecnologías**.

Al cambiar de área se conserva la última empresa seleccionada. En las páginas
informativas, el selector de empresa no aparece; **Dataset** utiliza la empresa
seleccionada previamente en **Análisis financiero**.
""")
        st.subheader("2. Explorar las cinco series financieras")
        st.markdown("""
1. Selecciona **Análisis financiero** en **SECCIONES**.
2. En **Serie financiera**, elige JNJ, MSFT, JPM, WMT o XOM.
3. En **Serie individual**, consulta cierre inicial y final, resumen descriptivo,
   la gráfica y las observaciones OHLCV. Cambia entre apertura, máximo, mínimo,
   cierre y volumen; las medias móviles MA20/MA50 se muestran sobre **Close**.
4. En **Cinco series**, revisa la explicación y la gráfica histórica de cada empresa.
5. En **Comparación**, examina el índice base 100, cierres y variación acumulada
   y la tabla de estadísticos descriptivos.
6. En **Calidad y resultados**, revisa las tres condiciones temporales, los
   controles OHLCV y la exportación del conjunto o el informe académico PDF.
""")
        st.info(
            "Los snapshots incorporados comprenden 10 años: "
            "del 2016-10-31 al 2026-10-30, con 2.514 registros por empresa "
            "y 12.570 observaciones en total."
        )
        st.subheader("3. Consultar información del proyecto")
        st.markdown("""
Selecciona **Información del proyecto** y elige la página:

- **Acerca de:** objetivos, alcance y límites del Módulo I.
- **Dataset:** fuente, cobertura, condiciones temporales, registros OHLCV
  y consulta web opcional del activo previamente seleccionado.
- **Fundamentos:** series temporales, OHLCV, medias móviles e interpretación.
- **Trivia:** identidad TEMPUS y cuestionario interactivo.
- **Ayuda:** esta guía.
- **Institucional:** identificación académica.
- **Tecnologías:** bibliotecas Python, funciones y pasos implementados.
""")
        st.subheader("4. Ejemplo de comprobación · ExxonMobil (XOM)")
        st.markdown("""
1. Selecciona **Análisis financiero** y, en **Serie financiera**, **XOM · ExxonMobil**.
2. Abre **Serie individual** y visualiza **Close** (USD por acción).
3. Activa MA20 y MA50 para observar promedios móviles históricos.
4. Selecciona **Volume** y comprueba la unidad *acciones negociadas*.
5. Abre **Calidad y resultados** y examina el diagnóstico temporal.
6. Cambia a **Información del proyecto → Dataset**. Debe mostrarse XOM
   como último activo seleccionado.
""")
        st.subheader("5. Informe, exportación y consultas")
        st.markdown("""
- En **Análisis financiero → Calidad y resultados**, pulsa
  **Generar informe académico descriptivo (PDF)** y después
  **Descargar informe PDF de Práctica 1**.
- En la misma pestaña puedes descargar el ZIP de datos para
  **TEMPUS PREDICTIO PROTO**.
- En **Información del proyecto → Dataset**, puedes descargar los datos
  validados o consultar cotizaciones web opcionalmente. Esa consulta
  **no reemplaza** los snapshots oficiales incluidos.
""")
        st.subheader("6. Problemas habituales")
        st.markdown("""
- **No aparece Serie financiera:** vuelve a **SECCIONES → Análisis financiero**.
- **No aparecen las siete páginas:** selecciona **Información del proyecto**.
- **No cambia el activo en Dataset:** selecciona primero la empresa en
  **Análisis financiero**; la selección se conserva al volver.
- **Faltan datos oficiales:** comprueba `data/snapshots/` y sus manifiestos.
- **Hay incidencias temporales:** examina los estados cuantitativo,
  cronológico y de regularidad XNYS; los cierres programados no son faltantes.
- **Falla la consulta web:** comprueba la conexión; los datos oficiales no se modifican.
- **No se genera el PDF:** revisa el mensaje de error y las dependencias.
  El archivo ya descargado no se actualiza automáticamente.
- **No ves cambios después de actualizar:** reinicia Streamlit y recarga el navegador.
""")
        st.subheader("7. Verificación local")
        st.code(".\\.venv\\Scripts\\python.exe -m pytest tests -v", language="powershell")
        st.code(".\\.venv\\Scripts\\python.exe -m streamlit run app.py", language="powershell")
        st.caption(
            "Aplicación local: http://localhost:8501 (si el puerto está disponible). "
            "La validación automática no sustituye la revisión visual de Streamlit."
        )

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
        st.markdown("""
| Biblioteca | Función o recurso | Aplicación |
|---|---|---|
| `yfinance` | `Ticker().history()` / consulta de cotizaciones | Adquisición web opcional de OHLCV; sin reemplazo automático de snapshots |
| `pandas` | `DatetimeIndex`, `sort_index()`, `to_numeric()` | Organización cronológica y comprobación numérica |
| `pandas` | `pct_change()`, `rolling().mean()` | Rendimientos por sesión y medias móviles MA20 / MA50 |
| `pandas` | `mean()`, `median()`, `std()`, `min()`, `max()`, `cummax()` | Cierre inicial/final, dispersión, extremos y caída histórica |
| `NumPy` | `isfinite()`, `sqrt()` | Valores válidos y volatilidad anualizada |
| `exchange_calendars` | `get_calendar('XNYS')`, `sessions_in_range()` | Identificar sesiones bursátiles esperadas y faltantes |
| `Plotly` | `graph_objects.Scatter()` | Gráficas cronológicas interactivas |
| `Matplotlib` | `plot()`, `savefig()` | Gráficas de las cinco empresas en el PDF |
| `Streamlit` | `tabs()`, `dataframe()`, `metric()`, `download_button()` | Interfaz, indicadores y descarga |
| `ReportLab` | `SimpleDocTemplate`, `Paragraph`, `Table`, `Image` | Informe académico reproducible |
| `pytest` | Pruebas de validación y exportación | Verificación de las funciones del proyecto |
""")
        st.subheader("Cómo se cumple cada etapa")
        st.markdown("""
| Etapa | Implementación | Evidencia |
|---|---|---|
| 1. Adquisición | `tempus/io.py` y snapshots Parquet con manifiestos | Cinco series: JNJ, MSFT, JPM, WMT y XOM |
| 2. Validación OHLCV | `tempus/core.py`: `normalize_prices()` | Tipos, duplicados, fechas, rango y coherencia de precios |
| 3. Condiciones temporales | `tempus/temporal.py`: `diagnose_time_series()` | Cuantitativa, cronológica y regularidad de sesiones XNYS |
| 4. Estadística descriptiva | `tempus/descriptive.py` y `tempus/core.py` | Cierres inicial/final, extremos, promedios, variación y volatilidad |
| 5. Gráficas | `app.py` / Plotly y `tempus/academic_report.py` / Matplotlib | Una gráfica de cierre para cada empresa y comparación base 100 |
| 6. Verificación | `tests/` con `pytest` | Resultados comprobables al ejecutar la suite en el equipo |
| 7. Reporte | `tempus/academic_report.py` | PDF con cinco fichas individuales, gráficas y tabla comparativa |
| 8. Exportación | `tempus/dataset.py` | CSV, manifiesto SHA-256 e indicadores para Predictio |
""")
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
