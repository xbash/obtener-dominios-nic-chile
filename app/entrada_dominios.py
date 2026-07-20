"""Entrada y parseo de listas de dominios.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date
from pathlib import Path
from typing import Iterable

from app.comun_nic import (
    canonizar_dominio,
    es_dominio_cl_valido,
    extraer_parametro_d,
    quitar_envoltorios,
)
from app.configuracion import ARCHIVO_CANDIDATOS, ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA
from app.modelos_dominios import ConsultaDominio

REGEX_DOMINIO = re.compile(r"([^\s<>'\"/]+\.cl)\b", flags=re.IGNORECASE)
REGEX_FECHA_ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
REGEX_FECHA_LATAM = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
REGEX_ETIQUETA_FECHA = re.compile(r"fecha de expiracion del dominio", flags=re.IGNORECASE)
REGEX_ENTRADA_FECHA = re.compile(r"^(?P<fecha>\d{4}-\d{2}-\d{2})[\t,; ]+(?P<resto>.+)$")
ENCABEZADOS_IGNORADOS = {
    ("fecha", "dominio"),
    ("fecha_consulta", "dominio"),
    ("fecha_consulta", "dominio", "fecha_registro"),
}


def parsear_fecha_entrada(valor: str) -> date | None:
    valor = valor.strip()
    if not valor:
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None


def extraer_dominios_desde_texto(texto: str) -> list[str]:
    encontrados: list[str] = []
    vistos: set[str] = set()
    for coincidencia in REGEX_DOMINIO.finditer(texto):
        dominio = quitar_envoltorios(coincidencia.group(1))
        dominio = dominio.replace("&amp;", "&")
        for prefijo in ("http://", "https://", "www."):
            if dominio.lower().startswith(prefijo):
                dominio = dominio[len(prefijo) :]
        if es_dominio_cl_valido(dominio):
            clave = canonizar_dominio(dominio)
            if clave not in vistos:
                vistos.add(clave)
                encontrados.append(dominio)
    return encontrados


def extraer_registros_desde_linea(linea: str) -> list[ConsultaDominio]:
    texto = linea.strip()
    if not texto:
        return []

    columnas_csv = [columna.strip() for columna in next(csv.reader([texto]))]
    columnas_normalizadas = tuple(columna.lower() for columna in columnas_csv)
    if columnas_normalizadas in ENCABEZADOS_IGNORADOS:
        return []
    if len(columnas_csv) == 2:
        fecha_consulta_csv = parsear_fecha_entrada(columnas_csv[0])
        dominio_csv = quitar_envoltorios(columnas_csv[1])
        if fecha_consulta_csv is not None and es_dominio_cl_valido(dominio_csv):
            return [
                ConsultaDominio(
                    dominio_consulta=canonizar_dominio(dominio_csv),
                    dominio_salida=dominio_csv.lower(),
                    fecha_registro=fecha_consulta_csv,
                )
            ]
    if len(columnas_csv) >= 3:
        fecha_registro_csv = parsear_fecha_entrada(columnas_csv[2])
        dominio_csv = quitar_envoltorios(columnas_csv[1])
        if fecha_registro_csv is not None and es_dominio_cl_valido(dominio_csv):
            return [
                ConsultaDominio(
                    dominio_consulta=canonizar_dominio(dominio_csv),
                    dominio_salida=dominio_csv.lower(),
                    fecha_registro=fecha_registro_csv,
                )
            ]

    fecha_registro: date | None = None
    resto = texto
    coincidencia_fecha = REGEX_ENTRADA_FECHA.match(texto)
    if coincidencia_fecha:
        fecha_registro = parsear_fecha_entrada(coincidencia_fecha.group("fecha"))
        resto = coincidencia_fecha.group("resto")

    dominios = extraer_dominios_desde_texto(resto)
    if not dominios:
        partes = re.split(r"[\s,;]+", resto.strip())
        if partes:
            candidato = quitar_envoltorios(partes[-1])
            if es_dominio_cl_valido(candidato):
                dominios = [candidato]

    registros: list[ConsultaDominio] = []
    for dominio in dominios:
        registros.append(
            ConsultaDominio(
                dominio_consulta=canonizar_dominio(dominio),
                dominio_salida=dominio.lower(),
                fecha_registro=fecha_registro,
            )
        )
    return registros


def leer_registros_desde_iterable(lineas: Iterable[str]) -> list[ConsultaDominio]:
    registros: list[ConsultaDominio] = []
    for linea in lineas:
        registros.extend(extraer_registros_desde_linea(linea))
    return registros


def leer_registros_desde_fuente(ruta: Path | None) -> list[ConsultaDominio]:
    if ruta is None:
        if sys.stdin.isatty():
            raise SystemExit("Debe indicar --entrada o entregar dominios por stdin.")
        return leer_registros_desde_iterable(sys.stdin)

    if not ruta.exists():
        raise SystemExit(f"No existe la entrada: {ruta}")

    with ruta.open("r", encoding="utf-8") as archivo:
        return leer_registros_desde_iterable(archivo)


def resolver_entrada(argumento: str | None, modo: str) -> Path | None:
    if argumento:
        if argumento == "-":
            return None
        return Path(argumento)
    if modo == "descubrir" and ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA.exists():
        return ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA
    if modo == "vigilar" and ARCHIVO_CANDIDATOS.exists():
        return ARCHIVO_CANDIDATOS
    return None
