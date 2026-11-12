"""Diagnóstico verificable de condiciones temporales para cotizaciones OHLCV.

Las sesiones bursátiles se contrastan con el calendario XNYS.
No rellena huecos, no reordena el original y no modifica observaciones.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import logging

import numpy as np
import pandas as pd
import exchange_calendars as xcals

from tempus.core import REQUIRED, normalize_prices

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class TemporalDiagnosis:
    """Estado y evidencias observables de las tres condiciones fundamentales."""

    cuantitativa: str
    cronologica: str
    regularidad: str
    calendario: str
    registros: int
    fechas_duplicadas: int
    fechas_invalidas: int
    valores_no_numericos: int
    valores_no_finitos: int
    sesiones_esperadas: int
    sesiones_faltantes: int
    fechas_fuera_sesion: int
    primeras_faltantes: str
    primeras_fuera_sesion: str

    def to_dict(self) -> dict[str, str | int]:
        """Devuelve un diccionario serializable para interfaces y exportaciones."""
        return asdict(self)


def _sample_dates(index: pd.DatetimeIndex, limit: int = 5) -> str:
    """Construye una muestra breve y reproducible de incidencias."""
    return ", ".join(pd.Timestamp(d).date().isoformat() for d in index[:limit]) or "—"


def diagnose_time_series(frame: pd.DataFrame, calendar_name: str = "XNYS") -> TemporalDiagnosis:
    """Evalúa los datos sin reparar ni ocultar fallos de calidad.

    'APROBADA' implica que la comprobación correspondiente se cumplió.
    'REVISAR' identifica incidencias; no significa imposibilidad matemática
    de representar observaciones temporales irregulares.

    Raises:
        TypeError: si el objeto o su índice no tienen estructura temporal.
        ValueError: si la serie está vacía o el calendario no existe.
        RuntimeError: si el calendario no permite calcular el intervalo.
    """
    if not isinstance(frame, pd.DataFrame):
        raise TypeError("Se requiere un DataFrame")
    if frame.empty:
        raise ValueError("No se puede diagnosticar una serie vacía")
    if not isinstance(frame.index, pd.DatetimeIndex):
        raise TypeError("Se requiere un DatetimeIndex")
    if not all(key in frame.columns for key in REQUIRED):
        raise ValueError("Faltan variables OHLCV")

    fechas_invalidas = int(frame.index.isna().sum())
    duplicadas = int(frame.index.duplicated().sum())
    ordenada = bool(frame.index.is_monotonic_increasing)
    cronologica = "APROBADA" if not (fechas_invalidas or duplicadas) and ordenada else "REVISAR"

    values = frame[list(REQUIRED)].apply(pd.to_numeric, errors="coerce")
    no_numericos = int(values.isna().sum().sum())
    no_finitos = int((~np.isfinite(values.to_numpy(dtype="float64"))).sum())
    try:
        normalize_prices(frame)
        cuantitativa = "APROBADA"
    except (ValueError, TypeError) as exc:
        LOG.info("Incidencia de calidad financiera (%s)", type(exc).__name__)
        cuantitativa = "REVISAR"
    if no_numericos or no_finitos:
        cuantitativa = "REVISAR"

    if fechas_invalidas:
        return TemporalDiagnosis(
            cuantitativa, cronologica, "REVISAR", calendar_name, len(frame),
            duplicadas, fechas_invalidas, no_numericos, no_finitos,
            0, 0, 0, "No evaluable: fechas inválidas", "No evaluable: fechas inválidas"
        )

    fechas = frame.index
    if fechas.tz is not None:
        fechas = fechas.tz_localize(None)
    fechas = fechas.normalize().unique().sort_values()
    try:
        cal = xcals.get_calendar(calendar_name)
        esperadas = cal.sessions_in_range(fechas.min(), fechas.max())
    except (ValueError, KeyError, TypeError, OverflowError) as exc:
        raise RuntimeError(f"No se pudo evaluar el calendario {calendar_name}") from exc
    faltantes = esperadas.difference(fechas)
    extras = fechas.difference(esperadas)
    regularidad = "APROBADA" if not len(faltantes) and not len(extras) else "REVISAR"
    return TemporalDiagnosis(
        cuantitativa=cuantitativa,
        cronologica=cronologica,
        regularidad=regularidad,
        calendario=calendar_name,
        registros=len(frame),
        fechas_duplicadas=duplicadas,
        fechas_invalidas=fechas_invalidas,
        valores_no_numericos=no_numericos,
        valores_no_finitos=no_finitos,
        sesiones_esperadas=len(esperadas),
        sesiones_faltantes=len(faltantes),
        fechas_fuera_sesion=len(extras),
        primeras_faltantes=_sample_dates(faltantes),
        primeras_fuera_sesion=_sample_dates(extras),
    )
