"""Modelos compartidos para los flujos de dominios.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class ConsultaDominio:
    dominio_consulta: str
    dominio_salida: str
    fecha_registro: date | None = None


@dataclass(slots=True)
class ResultadoDominio:
    dominio_salida: str
    fecha_expiracion: date | None
    dias_restantes: int | None
    estado: str
    detalle: str | None = None
