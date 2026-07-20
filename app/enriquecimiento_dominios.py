"""Enriquecimiento local y heuristico de dominios.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import re

from app.comun_nic import eliminar_tildes

TERMINOS_SECTOR: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("legal", ("abogado", "abogados", "juridico", "legal", "notaria")),
    ("salud", ("clinica", "salud", "medico", "medicina", "dental", "dentista", "psicologo", "kine")),
    ("educacion", ("colegio", "escuela", "universidad", "curso", "cursos", "capacitacion", "academia")),
    ("inmobiliario", ("propiedad", "propiedades", "inmobiliaria", "parcela", "parcelas", "arriendo")),
    ("vehiculos", ("auto", "autos", "motor", "motos", "camioneta", "repuesto", "repuestos")),
    ("turismo", ("hotel", "hostal", "turismo", "viaje", "viajes", "cabana", "cabanas")),
    ("comercio", ("tienda", "market", "shop", "venta", "ventas", "delivery", "outlet")),
    ("tecnologia", ("tech", "software", "web", "hosting", "digital", "cloud", "app")),
    ("finanzas", ("credito", "creditos", "seguro", "seguros", "finanzas", "inversion")),
)

TERMINOS_SENSIBLES = (
    "banco",
    "bank",
    "gob",
    "gobierno",
    "municipalidad",
    "minsal",
    "sii",
    "afp",
    "isapre",
    "universidad",
    "farmacia",
    "clinica",
)

TERMINOS_GENERICOS = tuple(
    sorted({termino for _, terminos in TERMINOS_SECTOR for termino in terminos}, key=len, reverse=True)
)


def quitar_tld_cl(dominio: str) -> str:
    dominio_limpio = dominio.strip().lower()
    if dominio_limpio.endswith(".cl"):
        return dominio_limpio[:-3]
    return dominio_limpio


def tokenizar_nombre(nombre: str) -> list[str]:
    tokens = [token for token in re.split(r"[-\W_0-9]+", nombre) if token]
    if tokens:
        return tokens
    return [nombre] if nombre else []


def detectar_keyword_principal(nombre_normalizado: str, tokens: list[str]) -> str:
    for termino in TERMINOS_GENERICOS:
        if termino in nombre_normalizado:
            return termino
    if not tokens:
        return ""
    return max(tokens, key=len)


def detectar_sector(nombre_normalizado: str) -> str:
    sectores: list[str] = []
    for sector, terminos in TERMINOS_SECTOR:
        if any(termino in nombre_normalizado for termino in terminos):
            sectores.append(sector)
    return "|".join(sectores) if sectores else "indeterminado"


def estimar_riesgo_reventa(nombre_normalizado: str, contiene_numero: bool, longitud: int) -> str:
    if any(termino in nombre_normalizado for termino in TERMINOS_SENSIBLES):
        return "alto"
    if contiene_numero or longitud > 28:
        return "medio"
    return "bajo"


def enriquecer_dominio(dominio: str) -> dict[str, object]:
    nombre = quitar_tld_cl(dominio)
    nombre_normalizado = eliminar_tildes(nombre)
    tokens = tokenizar_nombre(nombre_normalizado)
    contiene_numero = any(caracter.isdigit() for caracter in nombre_normalizado)
    solo_letras = nombre_normalizado.isalpha()

    return {
        "longitud": len(nombre),
        "contiene_guion": "-" in nombre,
        "contiene_numero": contiene_numero,
        "solo_letras": solo_letras,
        "keyword_principal": detectar_keyword_principal(nombre_normalizado, tokens),
        "sector_probable": detectar_sector(nombre_normalizado),
        "riesgo_reventa": estimar_riesgo_reventa(nombre_normalizado, contiene_numero, len(nombre)),
    }
