"""Resumen financiero descriptivo y explicaciones basadas en datos observados.

Las funciones no modifican los históricos de entrada y no producen predicciones.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import numpy as np
import pandas as pd

from tempus.core import normalize_prices


@dataclass(frozen=True)
class DescriptiveSummary:
    """Indicadores calculados sobre una serie OHLCV validada."""
    fecha_inicial: str
    fecha_final: str
    sesiones: int
    cierre_inicial: float
    cierre_final: float
    cambio_absoluto: float
    cambio_porcentual: float
    cierre_minimo: float
    fecha_minimo: str
    cierre_maximo: float
    fecha_maximo: str
    media_cierre: float
    mediana_cierre: float
    desv_estandar_cierre: float
    volatilidad_anual_pct: float
    volumen_promedio: float
    max_caida_pct: float

    def to_dict(self) -> dict[str, str | int | float]:
        """Convierte el resumen inmutable en campos serializables."""
        return asdict(self)


def describe_closing_prices(frame: pd.DataFrame) -> DescriptiveSummary:
    """Calcula indicadores sin alterar precios ni inferir causalidad."""
    data = normalize_prices(frame)
    close = data["Close"]
    returns = close.pct_change(fill_method=None).dropna()
    peak = close.cummax()
    drawdown = close / peak - 1
    initial = float(close.iloc[0])
    final = float(close.iloc[-1])
    annual_vol = float(returns.std(ddof=1) * np.sqrt(252) * 100) if len(returns) >= 2 else float("nan")
    return DescriptiveSummary(
        fecha_inicial=close.index[0].date().isoformat(),
        fecha_final=close.index[-1].date().isoformat(),
        sesiones=len(close),
        cierre_inicial=initial,
        cierre_final=final,
        cambio_absoluto=final-initial,
        cambio_porcentual=(final / initial-1.0)*100.0,
        cierre_minimo=float(close.min()),
        fecha_minimo=close.idxmin().date().isoformat(),
        cierre_maximo=float(close.max()),
        fecha_maximo=close.idxmax().date().isoformat(),
        media_cierre=float(close.mean()),
        mediana_cierre=float(close.median()),
        desv_estandar_cierre=float(close.std(ddof=1)) if len(close)>1 else 0.0,
        volatilidad_anual_pct=annual_vol,
        volumen_promedio=float(data["Volume"].mean()),
        max_caida_pct=float(drawdown.min()*100.0),
    )


def closing_interpretation(summary: DescriptiveSummary, company: str) -> str:
    """Redacta una interpretación exclusivamente descriptiva, sin causalidad."""
    if not isinstance(company,str) or not company.strip():
        raise ValueError("El nombre de la empresa no puede estar vacío")
    movement = ("aumentó" if summary.cambio_absoluto > 0
                else "disminuyó" if summary.cambio_absoluto < 0 else "permaneció igual")
    return (
        f"Entre {summary.fecha_inicial} y {summary.fecha_final}, el precio de cierre "
        f"registrado de {company} {movement} desde USD {summary.cierre_inicial:,.2f} "
        f"hasta USD {summary.cierre_final:,.2f} por acción "
        f"(variación de {summary.cambio_porcentual:+.2f}% en el período). "
        f"El cierre mínimo fue USD {summary.cierre_minimo:,.2f} "
        f"({summary.fecha_minimo}) y el máximo USD {summary.cierre_maximo:,.2f} "
        f"({summary.fecha_maximo}). La media observada fue USD "
        f"{summary.media_cierre:,.2f}, la volatilidad histórica anualizada "
        f"{summary.volatilidad_anual_pct:.2f}% y la caída máxima respecto "
        f"al máximo previo {summary.max_caida_pct:.2f}%. Estas cifras "
        "describen únicamente el histórico analizado; no explican por sí solas "
        "sus causas ni permiten asegurar rendimientos futuros."
    )
