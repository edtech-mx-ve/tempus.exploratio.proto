"""Acceso controlado al conjunto oficial de TEMPUS EXPLORATIO PROTO."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import io
import json
import logging
import zipfile

import pandas as pd

from tempus.assets import ASSETS
from tempus.core import enrich_prices, normalize_prices, summarize
from tempus.io import list_snapshots, load_snapshot
from tempus.temporal import diagnose_time_series

LOG = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_DIR = ROOT / "data" / "snapshots"
SYMBOLS = tuple(ASSETS)


def load_official_data(directory: Path = SNAPSHOT_DIR) -> dict[str, pd.DataFrame]:
    """Carga y valida un snapshot verificado de cada acción, sin modificar originales.

    Raises:
        FileNotFoundError: falta una acción o una versión de datos.
        RuntimeError: archivo inválido o incompatibilidad de dependencias.
    """
    frames: dict[str, pd.DataFrame] = {}
    for ticker in SYMBOLS:
        snapshots = list_snapshots(ticker, directory)
        if not snapshots:
            raise FileNotFoundError(f"Sin históricos para {ticker} en {directory}")
        try:
            frames[ticker] = load_snapshot(snapshots[0], directory, ticker)
        except (OSError, ValueError, ImportError, KeyError, json.JSONDecodeError) as exc:
            LOG.exception("Histórico rechazado para %s", ticker)
            raise RuntimeError(f"No se pudo verificar el histórico de {ticker}") from exc
    return frames


def describe_quality(frame: pd.DataFrame) -> dict[str, object]:
    """Valida OHLCV y entrega información de cobertura."""
    clean = normalize_prices(frame)
    return {
        "filas": len(clean),
        "inicio": clean.index.min().date().isoformat(),
        "fin": clean.index.max().date().isoformat(),
        "duplicados": int(clean.index.duplicated().sum()),
        "faltantes_ohlcv": int(clean[list(("Open", "High", "Low", "Close", "Volume"))].isna().sum().sum()),
        "validacion": "APROBADA",
    }


def comparison_base100(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Alinea cierres por fecha compartida y normaliza a base 100."""
    if set(frames) != set(SYMBOLS):
        raise ValueError("Se requieren exactamente las cinco series aprobadas")
    closes = pd.concat(
        {ticker: normalize_prices(frame)["Close"] for ticker, frame in frames.items()},
        axis=1,
    ).dropna(how="any").sort_index()
    if closes.empty:
        raise ValueError("No existe intersección cronológica entre las series")
    return closes.div(closes.iloc[0]).mul(100)


def dataset_export(frames: dict[str, pd.DataFrame]) -> tuple[bytes, bytes]:
    """Construye CSV y manifiesto de exportación sin incluir valores sintéticos."""
    if set(frames) != set(SYMBOLS):
        raise ValueError("Falta al menos una de las cinco series")
    pieces: list[pd.DataFrame] = []
    for symbol in SYMBOLS:
        valid = normalize_prices(frames[symbol]).reset_index()
        valid.insert(0, "Ticker", symbol)
        pieces.append(valid[["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]])
    union = pd.concat(pieces, ignore_index=True).sort_values(["Ticker", "Date"])
    csv_content = union.to_csv(index=False, date_format="%Y-%m-%d").encode("utf-8")
    manifest = {
        "product": "TEMPUS EXPLORATIO PROTO",
        "contract": "tempus-financial-ohlcv/1.0",
        "dataset_type": "historical_ohlcv",
        "date_frequency": "daily_trading_sessions",
        "symbols": list(SYMBOLS),
        "rows": {s: len(frames[s]) for s in SYMBOLS},
        "data_start": union["Date"].min().date().isoformat(),
        "data_end": union["Date"].max().date().isoformat(),
        "csv_sha256": hashlib.sha256(csv_content).hexdigest(),
        "exported_utc": datetime.now(timezone.utc).isoformat(),
        "adjustment": "Los snapshots originales indican OHLC ajustado si se descargaron con auto_adjust=True; no interpretar como precios no ajustados.",
        "provenance": "Snapshots aportados con el proyecto original; ver JSON individuales; confirmar términos de redistribución antes de publicar.",
    }
    return csv_content, json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")


def export_bundle(frames: dict[str, pd.DataFrame]) -> bytes:
    """Empaqueta CSV, manifiesto y estadísticas sin sobrescribir archivos locales."""
    csv_content, manifest = dataset_export(frames)
    stats = pd.DataFrame([{"ticker": s, **summarize(frames[s])} for s in SYMBOLS])
    temporal = pd.DataFrame([
        {"ticker": ticker, **diagnose_time_series(frames[ticker]).to_dict()}
        for ticker in SYMBOLS
    ])
    memory = io.BytesIO()
    with zipfile.ZipFile(memory, mode="w", compression=zipfile.ZIP_DEFLATED) as bundle:
        bundle.writestr("tempus_exploratio_proto_series.csv", csv_content)
        bundle.writestr("tempus_exploratio_proto_manifest.json", manifest)
        bundle.writestr("tempus_exploratio_proto_indicadores.csv", stats.to_csv(index=False).encode("utf-8"))
        bundle.writestr("tempus_exploratio_proto_diagnostico_temporal.csv",
                        temporal.to_csv(index=False).encode("utf-8"))
    return memory.getvalue()
