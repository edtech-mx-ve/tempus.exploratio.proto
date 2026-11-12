<div align="center">

<img src="assets/tempus-logo.png" width="150" alt="Logotipo de TEMPUS EXPLORATIO PROTO">

# TEMPUS EXPLORATIO PROTO

**TEMPUS DECISIO PROTO · Módulo I · Práctica 1**

**Exploración y análisis de acciones bursátiles como series temporales cuantitativas.**

Python 3.12 · Streamlit · pandas · NumPy · Plotly · Parquet · PDF

[Repositorio de esta aplicación](https://github.com/edtech-mx-ve/tempus.exploratio.proto)

</div>

## 1. Descripción y alcance

**TEMPUS EXPLORATIO PROTO** es una aplicación académica para adquirir, validar, explorar, representar gráficamente y documentar **cinco series temporales financieras**. Permite examinar la evolución histórica de los precios de las acciones, contrastar sus comportamientos, verificar las condiciones de una serie temporal y obtener evidencias descriptivas.

La aplicación corresponde a la **Práctica 1** de la Unidad 4. **No entrena modelos de inteligencia artificial ni genera pronósticos bursátiles.** El modelado y la evaluación predictiva pertenecen al módulo posterior, **TEMPUS PREDICTIO PROTO**, que podrá utilizar los datos validados exportados desde esta aplicación.

El análisis se limita a los datos observados y no constituye una recomendación de inversión.

## 2. Series y cobertura histórica

Los cinco snapshots incluidos en esta edición tienen la misma cobertura de **diez años, del 31 de octubre de 2016 al 30 de octubre de 2026**.

| Símbolo | Empresa | Sector | Observaciones | Período |
|---|---|---|---:|---|
| JNJ | Johnson & Johnson | Salud | 2.514 | 2016-10-31 a 2026-10-30 |
| MSFT | Microsoft | Tecnología | 2.514 | 2016-10-31 a 2026-10-30 |
| JPM | JPMorgan Chase | Financiero | 2.514 | 2016-10-31 a 2026-10-30 |
| WMT | Walmart | Comercio minorista | 2.514 | 2016-10-31 a 2026-10-30 |
| XOM | ExxonMobil | Energía | 2.514 | 2016-10-31 a 2026-10-30 |
| **Total** | **5 empresas** | | **12.570** | |

Las cifras anteriores se obtuvieron de los **metadatos JSON incluidos** en la edición v0.3.4; los archivos Parquet contienen los históricos asociados y se verifican mediante hashes SHA-256 al cargarlos.

La frecuencia corresponde a **sesiones bursátiles diarias**, no a días naturales: fines de semana y cierres oficiales del mercado no implican automáticamente observaciones faltantes. El calendario de referencia es **XNYS (New York Stock Exchange)**.

Los snapshots son datos históricos versionados. La aplicación **no representa un flujo de precios en tiempo real** y la consulta web opcional no sustituye automáticamente los históricos oficiales.

## 3. Variables y condiciones de una serie temporal

Cada empresa dispone de las variables OHLCV:

| Campo | Interpretación | Unidad |
|---|---|---|
| `Open` | Precio de apertura | USD por acción |
| `High` | Precio máximo | USD por acción |
| `Low` | Precio mínimo | USD por acción |
| `Close` | Precio de cierre | USD por acción |
| `Volume` | Volumen negociado | Acciones |

**Nota de interpretación:** la descarga web se realiza con `auto_adjust=True` en `yfinance`. Los ajustes de precios dependen de la fuente y de los metadatos de cada snapshot; no deben confundirse indiscriminadamente con precios nominales sin ajustar.

Se comprueban tres condiciones fundamentales:

1. **Cuantitativa:** valores numéricos válidos, rangos coherentes y consistencia OHLCV.
2. **Cronológica:** fechas válidas, orden temporal y ausencia de duplicados.
3. **Regularidad:** concordancia entre las fechas observadas y las sesiones bursátiles esperadas según XNYS.

Las incidencias se presentan para su revisión; la aplicación **no inventa, interpola ni elimina automáticamente registros** para hacerlos cumplir estas condiciones. Desde un punto de vista general, también existen series temporales con muestreo irregular; la regularidad de sesiones es el criterio operativo adoptado en este estudio.

## 4. Funcionalidades de la aplicación

La navegación contiene **ocho secciones**:

| Sección | Funcionalidad real |
|---|---|
| **Análisis financiero** | Serie individual, cinco gráficas de cierre, comparación base 100, estadísticos, calidad y resultados |
| **Acerca de** | Objetivo, metodología, alcance y relación con TEMPUS DECISIO PROTO |
| **Dataset** | Cobertura, OHLCV, validaciones, registros, consulta web opcional y exportación |
| **Fundamentos** | Series temporales, condiciones, variables, indicadores e interpretación |
| **Trivia** | Identidad de TEMPUS, contenido educativo y cuestionario interactivo con puntuación |
| **Ayuda** | Recorrido de uso y solución de incidencias |
| **Institucional** | Identificación académica del proyecto |
| **Tecnologías** | Bibliotecas Python, funciones utilizadas, arquitectura y etapas implementadas |

Dentro de **Análisis financiero** están disponibles las pestañas **Serie individual**, **Cinco series**, **Comparación** y **Calidad y resultados**. Las gráficas se presentan en el tiempo y no son extrapolaciones.

### Indicadores descriptivos

Se calculan, según el componente, cierres inicial y final, variación absoluta y porcentual, extremos históricos y sus fechas, media, mediana, desviación estándar, rendimiento por sesión, medias móviles **MA20/MA50**, volatilidad histórica anualizada (factor convencional de 252 sesiones), volumen promedio, caída máxima (*drawdown*) y comparación normalizada **base 100**.

Estas medidas describen el período analizado y **no garantizan resultados futuros**. Comparar la variación acumulada de dos acciones no equivale a una comparación ajustada por riesgo.

## 5. Cómo se implementó el proceso

| Etapa | Implementación | Verificación o evidencia |
|---|---|---|
| 1. Adquisición y carga | `tempus/io.py`, `yfinance`, snapshots Parquet/JSON | Cinco históricos disponibles; consulta web opcional |
| 2. Validación OHLCV | `tempus/core.py`: `normalize_prices()` | Tipos, faltantes, duplicados y coherencia de precios |
| 3. Verificación temporal | `tempus/temporal.py`: `diagnose_time_series()` y calendario XNYS | Condiciones cuantitativa, cronológica y regularidad |
| 4. Descripción estadística | `tempus/core.py` y `tempus/descriptive.py` | Resúmenes y análisis individual de cada empresa |
| 5. Visualización | `app.py` con Plotly; `tempus/academic_report.py` con Matplotlib | Cinco gráficas, indicadores y comparación relativa |
| 6. Prueba | Archivos de `tests/` con `pytest` en el entorno de desarrollo | Validaciones y contratos comprobables |
| 7. Informe académico | `tempus/academic_report.py` con ReportLab | PDF con cifras, interpretación y gráficas por empresa |
| 8. Exportación | `tempus/dataset.py` | ZIP con CSV, manifiesto, indicadores y diagnóstico temporal |

El informe PDF se **genera desde la aplicación** en **Análisis financiero → Calidad y resultados → Generar informe académico descriptivo (PDF)**. Incluye cierre inicial/final y un análisis por empresa; requiere revisión académica antes de su entrega.

La exportación destinada a Predictio mantiene el contrato `tempus-financial-ohlcv/1.0` y añade un archivo de diagnóstico temporal. No equivale a ejecutar modelos predictivos.

## 6. Tecnologías utilizadas

| Biblioteca / herramienta | Uso en esta edición |
|---|---|
| **Python 3.12** | Lenguaje de implementación recomendado |
| **Streamlit** | Interfaz interactiva, navegación, métricas y descargas |
| **pandas** | Fechas, organización de tablas, `pct_change()`, `rolling()`, `mean()`, `median()`, `std()` |
| **NumPy** | Comprobación de valores finitos y cálculos numéricos |
| **Plotly** | Gráficas históricas interactivas |
| **Matplotlib** | Gráficas incorporadas en el informe PDF |
| **yfinance** | Consulta opcional de cotizaciones de Yahoo Finance |
| **PyArrow / Parquet** | Lectura de archivos históricos de datos |
| **exchange_calendars** | Calendario XNYS y sesiones de negociación |
| **ReportLab** | Generación del PDF académico |
| **pytest** | Pruebas automatizadas durante el desarrollo |

No se utilizan ARIMA, SES, evaluación *walk-forward* ni pronósticos futuros en esta edición de Exploratio.

## 7. Requisitos y ejecución local

- Python **3.12** recomendado.
- Windows PowerShell para los comandos siguientes.
- Los datos oficiales deben conservarse dentro de `data/snapshots/`, con su archivo `.parquet` y su manifiesto `.json` correspondiente.
- La consulta web opcional requiere internet; la exploración de snapshots incluidos no depende de una descarga nueva.

Desde la **carpeta raíz del proyecto**, donde está `app.py`:

```powershell
# Crear entorno virtual solo si todavía no existe
py -3.12 -m venv .venv

# Instalar las bibliotecas necesarias
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Comprobar dependencias
.\.venv\Scripts\python.exe -m pip check

# Abrir la aplicación
.\.venv\Scripts\python.exe -m streamlit run app.py
```

URL local habitual: **http://localhost:8501**.

Para ejecutar las pruebas en un entorno de desarrollo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest tests -v
```

`requirements-dev.txt` y `tests/` son útiles para validación local, pero **no son necesarios en el repositorio mínimo de despliegue**, siempre que `requirements.txt` incluya todas las dependencias de ejecución.

**Importante:** no utilizar los comandos `refresh_10y.py`, `run_10y_pipeline.py` o `rebuild_comparative_report.py` de ediciones anteriores: **no están incluidos en esta versión**.

## 8. Organización del proyecto

Estructura de los archivos necesarios para ejecutar la aplicación:

```text
TEMPUS EXPLORATIO PROTO/
├── .streamlit/
│   └── config.toml
├── assets/
│   └── tempus-logo.png
├── data/
│   └── snapshots/
│       ├── JNJ/       # 1 archivo .parquet y 1 .json
│       ├── MSFT/      # 1 archivo .parquet y 1 .json
│       ├── JPM/       # 1 archivo .parquet y 1 .json
│       ├── WMT/       # 1 archivo .parquet y 1 .json
│       └── XOM/       # 1 archivo .parquet y 1 .json
├── tempus/
│   ├── __init__.py
│   ├── academic_report.py
│   ├── assets.py
│   ├── core.py
│   ├── dataset.py
│   ├── demo.py
│   ├── descriptive.py
│   ├── info_pages.py
│   ├── io.py
│   └── temporal.py
├── app.py
├── requirements.txt
└── README.md
```

La carpeta local de desarrollo también puede contener `tests/`, `requirements-dev.txt`, registros de cambios y `.venv/`; no forman parte de la estructura mínima indicada.

## 9. Publicación en GitHub y Streamlit Community Cloud

**Repositorio de esta edición:**
[edtech-mx-ve/tempus.exploratio.proto](https://github.com/edtech-mx-ve/tempus.exploratio.proto).

La publicación se realiza desde la **carpeta local existente**; no es necesario duplicar el proyecto ni crear otra carpeta.

Antes de hacer `git push`, revisar `git status` y `git diff --cached --name-only` para comprobar que se subirán únicamente `app.py`, `requirements.txt`, `.streamlit/config.toml`, `assets/tempus-logo.png`, los archivos Python necesarios de `tempus/`, los cinco pares Parquet/JSON y este README. No incluir `.venv`, secretos, cachés, reportes generados o respaldos.

**Configuración prevista para Streamlit Community Cloud:**

| Parámetro | Valor |
|---|---|
| Repositorio | `edtech-mx-ve/tempus.exploratio.proto` |
| Rama | `main` |
| Archivo principal | `app.py` |
| Python | `3.12` |

**La URL pública de Streamlit se incorporará al README una vez confirmado el despliegue.** No se utiliza la URL de la edición anterior como si correspondiera a este repositorio.

Antes de hacer públicos los históricos, revisar si los términos del proveedor permiten su redistribución. La presencia de snapshots en el proyecto local no demuestra, por sí sola, autorización para publicarlos.

## 10. Reproducibilidad, limitaciones y uso académico

- Los resultados se calculan sobre los cinco históricos de la edición indicada, con fecha final **2026-10-30**.
- Los precios pueden incorporar ajustes del proveedor; deben interpretarse junto con los metadatos.
- La verificación del calendario cubre las sesiones comprendidas entre la primera y la última observación.
- No se completan huecos artificialmente ni se sustituyen snapshots sin decisión explícita.
- Cinco series bursátiles históricas no implican por sí solas infraestructura Big Data distribuida.
- Los cálculos automáticos no sustituyen la revisión visual de los controles, gráficas y PDF.
- El informe académico generado debe revisarse antes de entregarse.
- No se producen pronósticos ni recomendaciones financieras.

## 11. Identificación institucional

**Institución:** Instituto Internacional de Aguascalientes  
**Programa:** Maestría en Inteligencia Artificial para la Transformación Digital  
**Asignatura:** Tópicos de IA para la Transformación Digital · Unidad 4  
**Tutor:** Dr. Francisco Javier Luna Rosas  
**Alumno:** Antonio Nicolás Toro González  

**Proyecto:** TEMPUS DECISIO PROTO  
**Aplicación:** TEMPUS EXPLORATIO PROTO · Módulo I · Práctica 1

---

**Fuentes y documentación técnica:**
[Yahoo Finance](https://finance.yahoo.com/) ·
[yfinance](https://github.com/ranaroussi/yfinance) ·
[Streamlit](https://docs.streamlit.io/) ·
[pandas](https://pandas.pydata.org/docs/) ·
[exchange_calendars](https://github.com/gerrymanoim/exchange_calendars)
