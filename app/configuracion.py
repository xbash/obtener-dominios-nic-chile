"""Configuracion compartida para los scripts del proyecto.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

from pathlib import Path

VERSION_PROYECTO = "v2.3"

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]
DIRECTORIO_APP = RAIZ_PROYECTO / "app"
DIRECTORIO_ARCHIVO = RAIZ_PROYECTO / "archivo"
DIRECTORIO_ENTRADA = RAIZ_PROYECTO / "entrada"
DIRECTORIO_LOGS = RAIZ_PROYECTO / "logs"
DIRECTORIO_TOOLS = RAIZ_PROYECTO / "tools"
DIRECTORIO_DESCARGAS = RAIZ_PROYECTO / "descargas"

ARCHIVO_CANDIDATOS = DIRECTORIO_ENTRADA / "candidatos.txt"
ARCHIVO_DOMINIOS_REGISTRADOS_MES = DIRECTORIO_ARCHIVO / "dominios-nic-registrados-mes.csv"
ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA = DIRECTORIO_ARCHIVO / "dominios-nic-eliminados-semana.csv"
ARCHIVO_DOMINIOS_POR_CADUCAR = DIRECTORIO_ARCHIVO / "dominios-por-caducar.csv"
ARCHIVO_CHECKPOINT_POR_CADUCAR = DIRECTORIO_ARCHIVO / "dominios-por-caducar.checkpoint.json"
