"""Despachador central de los programas del proyecto.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import sys
from pathlib import Path

from app.consulta_dominios import principal as principal_consulta
from app.dominios_por_caducar import principal as principal_caducar


PROGRAMAS_CONSULTA = {"dominios-nic", "consulta-dominios", "consulta_dominios"}
PROGRAMAS_CADUCAR = {"dominios-por-caducar", "dominios_por_caducar"}
PROGRAMAS_VALIDOS = PROGRAMAS_CONSULTA | PROGRAMAS_CADUCAR


def ejecutar(programa: str | None = None) -> int:
    nombre_programa = (programa or Path(sys.argv[0]).stem).lower()

    if nombre_programa in PROGRAMAS_CONSULTA:
        return principal_consulta()
    if nombre_programa in PROGRAMAS_CADUCAR:
        return principal_caducar()

    print(
        "[error] No se pudo determinar el programa a ejecutar. "
        "Use un wrapper o ejecute: python -m app.main <programa> [opciones].",
        file=sys.stderr,
    )
    return 2


def principal() -> int:
    if len(sys.argv) > 1 and sys.argv[1].lower() in PROGRAMAS_VALIDOS:
        programa = sys.argv[1].lower()
        sys.argv = [programa, *sys.argv[2:]]
        return ejecutar(programa)

    return ejecutar()


if __name__ == "__main__":
    raise SystemExit(principal())
