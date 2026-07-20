"""Indicador de progreso para corridas largas.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import sys


def mostrar_progreso(
    actual: int,
    total: int,
    dominio: str,
    habilitado: bool,
    frecuencia: int,
    finalizar: bool = False,
) -> None:
    if not habilitado:
        return
    if actual not in {0, total} and frecuencia > 1 and actual % frecuencia != 0:
        return

    porcentaje = 100 if total == 0 else int((actual / total) * 100)
    if actual == 0:
        mensaje = f"Analizando dominio 0 de {total} (0%)"
    else:
        mensaje = f"Analizando dominio {actual} de {total} ({porcentaje}%)"
        if dominio:
            mensaje += f" - {dominio}"

    sys.stderr.write("\r" + mensaje + ("\n" if finalizar else ""))
    sys.stderr.flush()
