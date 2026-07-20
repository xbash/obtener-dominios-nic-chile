"""Funciones comunes para consulta y analisis de dominios NIC Chile.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import re
import socket
import time
import urllib.error
import urllib.request
from datetime import datetime

CARACTERES_FINAL = ".,;:!?)]}Â»â€œâ€\"'"
CARACTERES_PROHIBIDOS = set("@?=&%#,:")
AGENTE_USUARIO = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0 Safari/537.36"
)


def obtener_texto(url: str, timeout: int = 30) -> str:
    peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE_USUARIO})
    for intento in range(3):
        try:
            with urllib.request.urlopen(peticion, timeout=timeout) as respuesta:
                bytes_crudos = respuesta.read()
                codificacion = respuesta.headers.get_content_charset() or "utf-8"
                try:
                    return bytes_crudos.decode(codificacion, errors="replace")
                except LookupError:
                    return bytes_crudos.decode("utf-8", errors="replace")
        except (urllib.error.URLError, socket.timeout, TimeoutError):
            if intento < 2:
                time.sleep(2**intento)
            else:
                raise


def quitar_envoltorios(texto: str) -> str:
    return texto.strip().strip(CARACTERES_FINAL)


def extraer_parametro_d(token: str) -> str:
    texto = token.replace("&amp;", "&")
    texto_minusculas = texto.lower()
    if "whois.do" in texto_minusculas and ("?d=" in texto_minusculas or "&d=" in texto_minusculas):
        posicion = texto_minusculas.find("?d=")
        if posicion == -1:
            posicion = texto_minusculas.find("&d=")
        if posicion != -1:
            valor = texto[posicion + 3 :]
            valor = re.split(r"[&#\?\'\"<>\s]", valor, maxsplit=1)[0]
            return quitar_envoltorios(valor)
    return quitar_envoltorios(texto)


def es_dominio_cl_valido(dominio: str) -> bool:
    if not dominio:
        return False
    dominio_minusculas = dominio.lower()
    if not dominio_minusculas.endswith(".cl"):
        return False
    if "/" in dominio_minusculas or " " in dominio_minusculas or ".." in dominio_minusculas:
        return False
    if any(caracter in dominio_minusculas for caracter in CARACTERES_PROHIBIDOS):
        return False
    return len(dominio_minusculas[:-3]) > 0


def limpiar_texto(texto: str) -> str:
    import html
    import unicodedata

    texto = html.unescape(texto)
    texto = unicodedata.normalize("NFKC", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def eliminar_tildes(texto: str) -> str:
    import unicodedata

    normalizado = unicodedata.normalize("NFD", texto)
    return "".join(caracter for caracter in normalizado if unicodedata.category(caracter) != "Mn")


def a_punycode(dominio: str) -> str:
    try:
        return dominio.encode("idna").decode("ascii")
    except Exception:
        return dominio


def canonizar_dominio(dominio: str) -> str:
    return a_punycode(dominio.lower())


def fecha_santiago_iso() -> str:
    try:
        from zoneinfo import ZoneInfo

        zona_horaria = ZoneInfo("America/Santiago")
        return datetime.now(zona_horaria).date().isoformat()
    except Exception:
        return datetime.now().date().isoformat()


def fecha_santiago_hoy():
    try:
        from zoneinfo import ZoneInfo

        return datetime.now(ZoneInfo("America/Santiago")).date()
    except Exception:
        return datetime.now().date()
