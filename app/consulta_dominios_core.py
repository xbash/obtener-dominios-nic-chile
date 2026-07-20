"""Nucleo de consulta y persistencia de dominios NIC Chile.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import csv
import io
import re
import sys
from datetime import datetime
from typing import TypedDict

from app.comun_nic import (
    canonizar_dominio,
    fecha_santiago_iso,
    obtener_texto,
    extraer_parametro_d,
    es_dominio_cl_valido,
)
from app.configuracion import (
    DIRECTORIO_ARCHIVO,
    ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA,
    ARCHIVO_DOMINIOS_REGISTRADOS_MES,
    VERSION_PROYECTO,
)

REGEX_WHOIS = re.compile(r"whois\.do\?d=([^\s<>'\"/,&]+\.cl)", flags=re.IGNORECASE)
REGEX_TOKEN = re.compile(r"([^\s<>'\"/,]+\.cl)\b", flags=re.IGNORECASE)
ENCABEZADO_REGISTRADOS = ("fecha_consulta", "dominio", "fecha_registro")
ENCABEZADO_FECHA_DOMINIO = ("fecha", "dominio")
ENCABEZADO_CONSULTA_DOMINIO = ("fecha_consulta", "dominio")


class ConfiguracionTarea(TypedDict):
    url_txt: str
    url_html: str
    base_salida: str
    periodo_defecto: str
    periodos: tuple[str, ...]
    sufijos: dict[str, str]


CONFIG_TAREAS: dict[str, ConfiguracionTarea] = {
    "registrados": {
        "url_txt": "https://www.nic.cl/registry/Ultimos.do?f=csv&t={periodo}",
        "url_html": "https://www.nic.cl/registry/Ultimos.do?t={periodo}",
        "base_salida": ARCHIVO_DOMINIOS_REGISTRADOS_MES.stem.rsplit("-", 1)[0],
        "periodo_defecto": "1d",
        "periodos": ("1h", "1d", "1w", "1m"),
        "sufijos": {"1h": "hora", "1d": "dia", "1w": "semana", "1m": "mes"},
    },
    "eliminados": {
        "url_txt": "https://nic.cl/registry/Eliminados.do?f=txt&t={periodo}",
        "url_html": "https://nic.cl/registry/Eliminados.do?t={periodo}",
        "base_salida": ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA.stem.rsplit("-", 1)[0],
        "periodo_defecto": "1s",
        "periodos": ("1d", "1s"),
        "sufijos": {"1d": "dia", "1s": "semana"},
    },
}


def extraer_dominios(texto: str) -> set[str]:
    encontrados: set[str] = set()

    for coincidencia in REGEX_WHOIS.finditer(texto):
        dominio = extraer_parametro_d(coincidencia.group(0))
        if es_dominio_cl_valido(dominio):
            encontrados.add(dominio.lower())

    for coincidencia in REGEX_TOKEN.finditer(texto):
        crudo = coincidencia.group(1)
        limpio = extraer_parametro_d(crudo)
        for prefijo in ("http://", "https://", "www."):
            if limpio.lower().startswith(prefijo):
                limpio = limpio[len(prefijo) :]
        if es_dominio_cl_valido(limpio):
            encontrados.add(limpio.lower())

    encontrados.discard("nic.cl")
    return encontrados


def parsear_fecha_inscripcion(valor: str) -> str | None:
    valor_limpio = valor.strip()
    if not valor_limpio:
        return None
    for formato in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(valor_limpio, formato).date().isoformat()
        except ValueError:
            pass
    coincidencia = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", valor_limpio)
    if coincidencia:
        return coincidencia.group(1)
    return None


def extraer_registros_inscritos_csv(texto: str) -> dict[str, str]:
    registros: dict[str, str] = {}
    lector = csv.DictReader(io.StringIO(texto))
    for fila in lector:
        dominio = (fila.get("Nombre Dominio") or fila.get("dominio") or "").strip()
        fecha = parsear_fecha_inscripcion(fila.get("Fecha Inscripción") or fila.get("fecha_registro") or "")
        if dominio and fecha and es_dominio_cl_valido(dominio):
            registros[canonizar_dominio(dominio)] = fecha
    return registros


def cargar_dominios_existentes(ruta: str) -> set[str]:
    existentes: set[str] = set()
    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:
            muestra = archivo.readline()
            archivo.seek(0)
            if muestra.lower().startswith(("fecha,", "fecha_consulta,")):
                lector = csv.DictReader(archivo)
                for fila in lector:
                    dominio = (fila.get("dominio") or "").strip()
                    if es_dominio_cl_valido(dominio):
                        existentes.add(canonizar_dominio(dominio))
                return existentes
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                encontrados = extraer_dominios(linea)
                if encontrados:
                    existentes.update(canonizar_dominio(dominio) for dominio in encontrados)
                else:
                    partes = re.split(r"[\s,;]+", linea)
                    if partes:
                        candidato = extraer_parametro_d(partes[-1].lower())
                        if es_dominio_cl_valido(candidato):
                            existentes.add(canonizar_dominio(candidato))
    except FileNotFoundError:
        pass
    return existentes


def cargar_filas_csv(ruta: str) -> tuple[tuple[str, ...], list[list[str]]]:
    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.reader(archivo)
            encabezado = tuple(next(lector, ()))
            filas = list(lector)
    except FileNotFoundError:
        return (), []
    return encabezado, filas


def asegurar_formato_registrados(ruta: str) -> None:
    encabezado, filas = cargar_filas_csv(ruta)
    if not encabezado:
        return

    if encabezado == ENCABEZADO_REGISTRADOS:
        return
    if encabezado != ENCABEZADO_FECHA_DOMINIO:
        return

    respaldo = f"{ruta}.bak"
    with open(respaldo, "w", encoding="utf-8", newline="") as archivo_respaldo:
        escritor_respaldo = csv.writer(archivo_respaldo, lineterminator="\n")
        escritor_respaldo.writerow(encabezado)
        escritor_respaldo.writerows(filas)

    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        escritor.writerow(ENCABEZADO_REGISTRADOS)
        for fila in filas:
            if len(fila) < 2:
                continue
            fecha = fila[0].strip()
            dominio = fila[1].strip()
            if fecha and dominio:
                escritor.writerow((fecha, dominio, fecha))


def actualizar_fechas_registro(ruta: str, fechas_registro: dict[str, str]) -> int:
    if not fechas_registro:
        return 0

    encabezado, filas = cargar_filas_csv(ruta)
    if encabezado != ENCABEZADO_REGISTRADOS:
        return 0

    actualizadas = 0
    filas_actualizadas: list[list[str]] = []
    for fila in filas:
        if len(fila) < 3:
            filas_actualizadas.append(fila)
            continue
        clave = canonizar_dominio(fila[1])
        fecha_nic = fechas_registro.get(clave)
        if fecha_nic and fila[2] != fecha_nic:
            fila = [*fila]
            fila[2] = fecha_nic
            actualizadas += 1
        filas_actualizadas.append(fila)

    if actualizadas:
        with open(ruta, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, lineterminator="\n")
            escritor.writerow(ENCABEZADO_REGISTRADOS)
            escritor.writerows(filas_actualizadas)

    return actualizadas


def agregar_con_fecha(
    ruta: str,
    fecha_consulta: str,
    dominios: list[str],
    modo: str,
    fechas_registro: dict[str, str] | None = None,
) -> None:
    if not dominios:
        return
    fechas_registro = fechas_registro or {}
    with open(ruta, "a", encoding="utf-8", newline="") as archivo:
        escritor = csv.writer(archivo, lineterminator="\n")
        if archivo.tell() == 0:
            if modo == "registrados":
                escritor.writerow(ENCABEZADO_REGISTRADOS)
            else:
                escritor.writerow(ENCABEZADO_CONSULTA_DOMINIO)
        for dominio in dominios:
            if modo == "registrados":
                fecha_registro = fechas_registro.get(canonizar_dominio(dominio), fecha_consulta)
                escritor.writerow((fecha_consulta, dominio, fecha_registro))
            else:
                escritor.writerow((fecha_consulta, dominio))


def archivo_salida_por_defecto(modo: str, periodo: str) -> str:
    configuracion = CONFIG_TAREAS[modo]
    sufijo = configuracion["sufijos"].get(periodo, periodo)
    return str(DIRECTORIO_ARCHIVO / f'{configuracion["base_salida"]}-{sufijo}.csv')


def ejecutar_tarea(modo: str, periodo: str, ruta_salida: str, sin_punycode: bool) -> int:
    configuracion = CONFIG_TAREAS[modo]
    url_txt = configuracion["url_txt"].format(periodo=periodo)
    url_html = configuracion["url_html"].format(periodo=periodo)

    fechas_registro: dict[str, str] = {}
    try:
        texto_txt = obtener_texto(url_txt)
        if modo == "registrados":
            fechas_registro = extraer_registros_inscritos_csv(texto_txt)
            dominios_encontrados = set(fechas_registro)
            fuente = f"CSV ({periodo})"
        else:
            dominios_encontrados = extraer_dominios(texto_txt)
            fuente = f"TXT ({periodo})"
    except Exception as error_txt:
        print(f"[warn] Fallo TXT {periodo}: {error_txt}. Intentando HTML...", file=sys.stderr)
        try:
            texto_html = obtener_texto(url_html)
            dominios_encontrados = extraer_dominios(texto_html)
            fuente = f"HTML ({periodo})"
            if modo == "registrados":
                fechas_registro = {canonizar_dominio(dominio): fecha_santiago_iso() for dominio in dominios_encontrados}
        except Exception as error_html:
            print(f"[error] Fallo HTML {periodo}: {error_html}", file=sys.stderr)
            return 2

    if not dominios_encontrados:
        print("[info] No se encontraron dominios en la fuente.", file=sys.stderr)

    claves_obtenidas = {canonizar_dominio(dominio) for dominio in dominios_encontrados}
    dominio_mostrado = {
        canonizar_dominio(dominio): (dominio.lower() if sin_punycode else canonizar_dominio(dominio))
        for dominio in dominios_encontrados
    }

    if modo == "registrados":
        asegurar_formato_registrados(ruta_salida)
        actualizados = actualizar_fechas_registro(ruta_salida, fechas_registro)
    else:
        actualizados = 0

    dominios_existentes = cargar_dominios_existentes(ruta_salida)
    claves_existentes = {canonizar_dominio(dominio) for dominio in dominios_existentes}

    claves_nuevas = sorted(claves_obtenidas - claves_existentes)
    dominios_nuevos = [dominio_mostrado[clave] for clave in claves_nuevas]

    fecha = fecha_santiago_iso()
    agregar_con_fecha(ruta_salida, fecha, dominios_nuevos, modo, fechas_registro)

    print(
        f"[ok] Version: {obtener_version()} | Modo: {modo} | Periodo: {periodo} | "
        f"Fuente: {fuente} | obtenidos={len(claves_obtenidas)} | "
        f"existentes={len(claves_existentes)} | nuevos={len(dominios_nuevos)} | "
        f"fechas_registro_actualizadas={actualizados}"
    )
    print(f"[ok] Archivo: {ruta_salida}")
    if dominios_nuevos:
        print(f"[ok] {len(dominios_nuevos)} dominios agregados (fecha {fecha}).")
    else:
        print("[ok] No habia dominios nuevos para agregar.")

    return 0


def obtener_version() -> str:
    return VERSION_PROYECTO
