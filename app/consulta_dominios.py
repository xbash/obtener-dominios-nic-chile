#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
consulta_dominios.py
Version: v2.3
Agente/LLM: Codex (GPT-5)

Interfaz de linea de comandos para consultar dominios NIC Chile.
"""

from __future__ import annotations

import argparse

from app.configuracion import VERSION_PROYECTO
from app.consulta_dominios_core import CONFIG_TAREAS, archivo_salida_por_defecto, ejecutar_tarea

VERSION_SCRIPT = VERSION_PROYECTO


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Consulta dominios .CL en NIC Chile y agrega solo los nuevos a un CSV."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION_SCRIPT}")
    parser.add_argument(
        "--modo",
        choices=tuple(CONFIG_TAREAS.keys()),
        required=True,
        help="Modo de consulta: registrados o eliminados.",
    )
    parser.add_argument(
        "--periodo",
        default=None,
        help="Periodo segun el modo: registrados usa 1h, 1d, 1w o 1m; eliminados usa 1d o 1s.",
    )
    parser.add_argument("--salida", default=None, help="Archivo CSV de salida.")
    parser.add_argument(
        "--sin-punycode",
        action="store_true",
        help="No convertir a punycode; guardar tal como aparece (Unicode).",
    )
    return parser


def principal() -> int:
    parser = construir_parser()
    argumentos = parser.parse_args()

    modo = argumentos.modo
    configuracion = CONFIG_TAREAS[modo]
    periodo = argumentos.periodo or configuracion["periodo_defecto"]

    if periodo not in configuracion["periodos"]:
        parser.error(
            f"Periodo invalido para el modo '{modo}': {periodo}. "
            f"Use uno de: {', '.join(configuracion['periodos'])}."
        )

    ruta_salida = argumentos.salida or archivo_salida_por_defecto(modo, periodo)
    return ejecutar_tarea(modo, periodo, ruta_salida, argumentos.sin_punycode)
