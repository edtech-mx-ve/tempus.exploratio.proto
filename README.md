<div align="center">

<img src="assets/tempus-logo.png" width="150" alt="Logotipo TEMPUS DECISIO PROTO">

# TEMPUS EXPLORATIO PROTO

### TEMPUS DECISIO PROTO · Módulo I

**Exploración y análisis de acciones bursátiles como series temporales cuantitativas.**

**Python 3.12 · Streamlit · 5 empresas · 10 años de históricos · Práctica 1**

[Aplicación Streamlit](https://tempus-exploratio-proto.streamlit.app/) ·
[Repositorio GitHub](https://github.com/edtech-mx-ve/tempus.exploratio.proto)

</div>

## 1. Presentación y alcance

**TEMPUS EXPLORATIO PROTO** es una aplicación académica para adquirir o consultar, validar, explorar, representar gráficamente y documentar cinco series temporales financieras. Pertenece al proyecto **TEMPUS DECISIO PROTO** y corresponde a la **Práctica 1 de la Unidad 4** de *Tópicos de IA para la Transformación Digital*.

La aplicación realiza **análisis histórico descriptivo**. No entrena modelos de inteligencia artificial, no proyecta cotizaciones futuras y no ofrece asesoramiento financiero. El modelado predictivo corresponde al módulo posterior **TEMPUS PREDICTIO PROTO**.

**Institución:** Instituto Internacional de Aguascalientes.  
**Programa:** Maestría en Inteligencia Artificial para la Transformación Digital.  
**Alumno:** Antonio Nicolás Toro González.  
**Tutor:** Dr. Francisco Javier Luna Rosas.

## 2. Datos oficiales de la aplicación

Los snapshots históricos incluidos en la distribución actual declaran:

| Empresa | Símbolo | Sector | Observaciones |
|---|---|---|---:|
| Johnson & Johnson | JNJ | Salud | 2.514 |
| Microsoft | MSFT | Tecnología | 2.514 |
| JPMorgan Chase | JPM | Financiero | 2.514 |
| Walmart | WMT | Comercio minorista | 2.514 |
| ExxonMobil | XOM | Energía | 2.514 |
| **Total** | | | **12.570** |

- **Período documentado:** 31 de octubre de 2016 al 30 de octubre de 2026 (**10 años**).
- **Frecuencia:** sesiones bursátiles diarias, no todos los días naturales.
- **Variables OHLCV:** `Open`, `High`, `Low`, `Close` (USD por acción, según el ajuste de la fuente) y `Volume` (acciones negociadas).
- **Origen declarado:** cotizaciones históricas de Yahoo Finance, con datos locales Parquet y manifiestos JSON que registran cobertura e integridad.
- **Calendario de control:** XNYS mediante `exchange_calendars`, para detectar posibles sesiones faltantes sin confundir fines de semana o días de cierre con errores.
- **Actualización web:** consulta opcional de un activo; **no reemplaza los snapshots oficiales**.

El hash SHA-256 verifica que un archivo coincide con su referencia registrada; por sí solo no certifica autenticidad ni derechos de redistribución.

## 3. Navegación actual: dos áreas en la barra lateral

La interfaz organiza sus contenidos en **dos áreas**, seleccionables bajo **SECCIONES**:

### 3.1. Análisis financiero

Al seleccionar **Análisis financiero**, aparece el control **Serie financiera** para elegir JNJ, MSFT, JPM, WMT o XOM. El panel principal presenta cuatro pestañas:

| Pestaña | Función |
|---|---|
| **Serie individual** | Resumen del cierre, gráfica histórica de OHLCV, medias móviles MA20/MA50 cuando se consulta `Close` y últimos registros |
| **Cinco series** | Explicación, gráfica de cierre y estado OHLCV de las cinco empresas |
| **Comparación** | Índice base 100, cierres iniciales/finales, variación acumulada y estadísticos descriptivos |
| **Calidad y resultados** | Diagnóstico temporal y OHLCV, descarga del dataset y generación/descarga del informe académico PDF |

### 3.2. Información del proyecto

Al seleccionar **Información del proyecto**, se muestran **siete páginas**:

1. **Acerca de:** objetivo, alcance y metodología del Módulo I.
2. **Dataset:** fuente, diez años de cobertura, OHLCV, condiciones temporales, consulta y exportación.
3. **Fundamentos:** definiciones e interpretación de series e indicadores.
4. **Trivia:** identidad de TEMPUS y preguntas con evaluación y retroalimentación.
5. **Ayuda:** guía de navegación y resolución de problemas.
6. **Institucional:** información académica.
7. **Tecnologías:** bibliotecas, funciones Python, arquitectura y etapas del proceso.

**Persistencia de selección:** la última empresa elegida en **Análisis financiero → Serie financiera** se conserva al cambiar de área. En **Información del proyecto** no aparece dicho selector; la página **Dataset** utiliza la última empresa seleccionada.

## 4. Metodología implementada

La Práctica 1 sigue el procedimiento:

**Problema → fuentes → datos → validación → estadística descriptiva → representación gráfica → comprobación → informe y exportación.**

| Paso | Implementación |
|---|---|
| Adquisición y snapshots | `tempus/io.py`; consulta opcional mediante `yfinance` y almacenamiento versionado |
| Integridad financiera | `tempus/core.py`; fechas, datos numéricos, faltantes, rangos y coherencia OHLCV |
| Condiciones temporales | `tempus/temporal.py`; cuantitativa, cronológica y regularidad según sesiones XNYS |
| Indicadores | `tempus/core.py` y `tempus/descriptive.py`; rendimientos, promedios móviles, cierres, volatilidad, máximos/mínimos y variaciones |
| Gráficas | `app.py` con Plotly; figuras del informe con Matplotlib |
| Interfaz | `app.py`, `tempus/info_pages.py` y Streamlit |
| Informe | `tempus/academic_report.py` con ReportLab |
| Exportación | `tempus/dataset.py`; CSV y manifiesto de trazabilidad |
| Pruebas | `tests/` con `pytest`, si la suite de desarrollo está disponible localmente |

Se trabaja con el histórico observado, sin ajustes predictivos ni eliminación automática de valores extremos.

## 5. Estructura del proyecto

Solo los archivos esenciales se requieren para ejecutar la app en Streamlit:

```text
TEMPUS EXPLORATIO PROTO/
├── app.py
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml
├── assets/
│   └── tempus-logo.png
├── tempus/
│   ├── __init__.py
│   ├── academic_report.py
│   ├── assets.py
│   ├── core.py
│   ├── dataset.py
│   ├── descriptive.py
│   ├── info_pages.py
│   ├── io.py
│   └── temporal.py
└── data/
    └── snapshots/
        ├── JNJ/    # Parquet + JSON
        ├── MSFT/   # Parquet + JSON
        ├── JPM/    # Parquet + JSON
        ├── WMT/    # Parquet + JSON
        └── XOM/    # Parquet + JSON
```

El entorno virtual `.venv/`, los respaldos, los informes generados y los archivos temporales **no forman parte del despliegue**. La suite `tests/` y `requirements-dev.txt` pueden permanecer solo en la instalación de desarrollo; no son necesarios para ejecutar la app publicada.

## 6. Instalación y prueba en la carpeta local existente

No hace falta crear otra carpeta del proyecto. Desde la **carpeta local actual**:

```powershell
# Si el entorno .venv ya existe, no volver a crearlo.
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check

# Si tests/ y pytest están instalados:
.\.venv\Scripts\python.exe -m pytest tests -v

# Ejecutar aplicación local:
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**URL local habitual:** http://localhost:8501.

Si aún no existe el entorno virtual, se puede crear en esa misma carpeta con `py -3.12 -m venv .venv`. Los cambios de código deben validarse **primero en local**, antes de enviarlos a GitHub.

### Comprobación manual mínima

1. Comprobar ambas áreas de la barra lateral.
2. Seleccionar MSFT en **Análisis financiero → Serie financiera**; cambiar a **Información del proyecto → Dataset** y comprobar que sigue siendo MSFT.
3. Visualizar las cuatro pestañas de análisis y comprobar las gráficas de las cinco empresas.
4. Consultar regularidad y calidad OHLCV.
5. Completar Trivia y comprobar su retroalimentación.
6. Generar el PDF y verificar sus resultados, unidades y referencias.
7. Descargar el ZIP de datos y comprobar los archivos exportados.

Las pruebas de Python no equivalen a una auditoría visual automática de Streamlit.

## 7. Informe académico y exportación

En **Análisis financiero → Calidad y resultados**:

- **Generar informe académico descriptivo (PDF):** crea un nuevo informe de la Práctica 1 a partir de los históricos validados. Incluye comparación, valores de cierre, análisis individual, figuras, metodología, comprobaciones y referencias.
- **Descargar informe PDF de Práctica 1:** permite guardar el documento generado.
- **Descargar insumos para TEMPUS PREDICTIO PROTO (ZIP):** conserva el contrato del dataset.

El ZIP de datos incluye:

```text
tempus_exploratio_proto_series.csv
tempus_exploratio_proto_manifest.json
tempus_exploratio_proto_indicadores.csv
tempus_exploratio_proto_diagnostico_temporal.csv
```

El manifiesto documenta la procedencia declarada, cobertura, frecuencia y SHA-256 del CSV. El archivo de diagnóstico temporal es complementario y no modifica las columnas del CSV OHLCV.

**Importante:** un PDF descargado con anterioridad no se actualiza automáticamente; debe generarse de nuevo desde la aplicación después de un cambio de código o datos.

## 8. Publicación y actualizaciones

**Repositorio:** https://github.com/edtech-mx-ve/tempus.exploratio.proto  
**Aplicación:** https://tempus-exploratio-proto.streamlit.app/

El repositorio utiliza **`app.py`** como archivo principal, la rama **`main`** y las dependencias de `requirements.txt`. Python **3.12** es la versión local recomendada.

Para registrar una actualización aprobada, ejecutar desde la **misma carpeta local**:

```powershell
git status
git add app.py tempus/info_pages.py README.md
git diff --cached --name-only
git commit -m "Actualizar navegacion y documentacion de Exploratio"
git push origin main
```

Ajustar `git add` a los archivos realmente modificados. No ejecutar `git add .` si el objetivo es publicar solo componentes específicos. Antes de cada publicación, revisar licencias y permisos de redistribución de los snapshots.

## 9. Alcance y limitaciones

- Los datos históricos terminan el **2026-10-30**; la app no asegura cotizaciones en tiempo real.
- Las series se describen y comparan; no se emiten pronósticos ni recomendaciones de inversión.
- Las tasas de variación históricas no indican rendimiento futuro ni equivalencia de riesgo entre empresas.
- Los precios pueden estar ajustados por eventos corporativos según el proveedor; consultar metadatos.
- Las cinco series locales no demuestran, por sí solas, procesamiento Big Data distribuido.
- La verificación automatizada y el despliegue público deben complementarse con revisión funcional y académica.
