"""Persistencia de checkpoint para el flujo de dominios.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import time
from datetime import datetime, date
from pathlib import Path

from app.configuracion import ARCHIVO_CHECKPOINT_POR_CADUCAR

_CHECKPOINTS_ADVERTIDOS: set[Path] = set()


def ruta_checkpoint_por_defecto() -> Path:
    return ARCHIVO_CHECKPOINT_POR_CADUCAR


def resolver_checkpoint(argumento: str | None) -> Path | None:
    if argumento is None:
        return ruta_checkpoint_por_defecto()
    if argumento.strip() in {"", "-"}:
        return None
    return Path(argumento)


def construir_metadata_checkpoint(
    version: str,
    modo: str,
    orden: str,
    desde_fecha: date | None,
    limite: int | None,
    umbral_dias: int,
    firma_entrada: dict[str, object],
) -> dict[str, object]:
    return {
        "version": version,
        "modo": modo,
        "orden": orden,
        "desde_fecha": desde_fecha.isoformat() if desde_fecha else None,
        "limite": limite,
        "umbral_dias": umbral_dias,
        "entrada": firma_entrada,
    }


def cargar_checkpoint(ruta_checkpoint: Path | None, metadata_esperada: dict[str, object]) -> tuple[int, dict[str, object] | None]:
    if ruta_checkpoint is None or not ruta_checkpoint.exists():
        return 0, None

    try:
        with ruta_checkpoint.open("r", encoding="utf-8") as archivo:
            payload = json.load(archivo)
    except Exception as error:
        print(f"[warn] No se pudo leer el checkpoint: {error}", file=sys.stderr)
        return 0, None

    metadata_guardada = payload.get("metadata")
    if metadata_guardada != metadata_esperada:
        print("[warn] El checkpoint existente no coincide con la configuracion actual; se ignora.", file=sys.stderr)
        return 0, None

    try:
        procesados = int(payload.get("procesados", 0))
    except Exception:
        procesados = 0

    return max(procesados, 0), payload


def guardar_checkpoint(
    ruta_checkpoint: Path | None,
    metadata: dict[str, object],
    procesados: int,
    escritos: int,
    omitidos: int,
    ultimo_dominio: str,
    completado: bool,
) -> None:
    if ruta_checkpoint is None:
        return

    payload = {
        "metadata": metadata,
        "procesados": procesados,
        "escritos": escritos,
        "omitidos": omitidos,
        "ultimo_dominio": ultimo_dominio,
        "completado": completado,
        "actualizado_en": datetime.now().isoformat(timespec="seconds"),
    }

    ruta_checkpoint.parent.mkdir(parents=True, exist_ok=True)
    ultimo_error: PermissionError | None = None

    for intento in range(8):
        descriptor: int | None = None
        ruta_temporal: Path | None = None
        try:
            descriptor, nombre_temporal = tempfile.mkstemp(
                prefix=f"{ruta_checkpoint.name}.",
                suffix=".tmp",
                dir=ruta_checkpoint.parent,
                text=True,
            )
            ruta_temporal = Path(nombre_temporal)

            with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
                descriptor = None
                json.dump(payload, archivo, ensure_ascii=False, indent=2)
                archivo.write("\n")

            ruta_temporal.replace(ruta_checkpoint)
            return
        except PermissionError as error:
            ultimo_error = error
            if intento < 7:
                time.sleep(0.05 * (intento + 1))
        finally:
            if descriptor is not None:
                try:
                    os.close(descriptor)
                except OSError:
                    pass
            if ruta_temporal is not None:
                try:
                    ruta_temporal.unlink(missing_ok=True)
                except Exception:
                    pass

    if ultimo_error is not None:
        ruta_resuelta = ruta_checkpoint.resolve()
        if ruta_resuelta not in _CHECKPOINTS_ADVERTIDOS:
            print(
                f"[warn] No se pudo guardar el checkpoint; la corrida continua sin reanudacion garantizada: {ultimo_error}",
                file=sys.stderr,
            )
            _CHECKPOINTS_ADVERTIDOS.add(ruta_resuelta)


def borrar_checkpoint(ruta_checkpoint: Path | None) -> None:
    if ruta_checkpoint is None:
        return
    try:
        ruta_checkpoint.unlink(missing_ok=True)
    except Exception as error:
        print(f"[warn] No se pudo borrar el checkpoint: {error}", file=sys.stderr)
