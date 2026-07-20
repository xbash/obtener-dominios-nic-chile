"""Escritura y filtrado de resultados para los flujos de dominios.

Version: v2.3
Agente/LLM: Codex (GPT-5)
"""

from __future__ import annotations

import csv
import tempfile
from pathlib import Path

from app.enriquecimiento_dominios import enriquecer_dominio
from app.configuracion import ARCHIVO_DOMINIOS_POR_CADUCAR, DIRECTORIO_ARCHIVO
from app.modelos_dominios import ConsultaDominio, ResultadoDominio

ENCABEZADO_DOMINIOS_POR_CADUCAR = (
    "fecha_consulta",
    "fuente",
    "fecha_registro",
    "dominio",
    "fecha_expiracion",
    "dias_restantes",
    "estado",
    "longitud",
    "contiene_guion",
    "contiene_numero",
    "solo_letras",
    "keyword_principal",
    "sector_probable",
    "riesgo_reventa",
)

ENCABEZADO_ANTERIOR_DOMINIOS_POR_CADUCAR = (
    "fecha_consulta",
    "dominio",
    "fecha_expiracion",
    "dias_restantes",
    "estado",
)


def filtrar_resultado(resultado: ResultadoDominio, incluir_todos: bool) -> bool:
    if incluir_todos:
        return True
    return resultado.estado in {"por_vencer", "vence_hoy", "caducado"}


def escribir_resultado(
    archivo,
    fecha_consulta: str,
    fuente: str,
    registro: ConsultaDominio,
    resultado: ResultadoDominio,
    sin_punycode: bool,
    incluir_todos: bool,
) -> bool:
    if not filtrar_resultado(resultado, incluir_todos):
        return False

    dominio_salida = registro.dominio_salida if sin_punycode else registro.dominio_consulta
    fecha_expiracion = resultado.fecha_expiracion.isoformat() if resultado.fecha_expiracion else ""
    dias_restantes = "" if resultado.dias_restantes is None else str(resultado.dias_restantes)
    fecha_registro = registro.fecha_registro.isoformat() if registro.fecha_registro else ""
    enriquecimiento = enriquecer_dominio(dominio_salida)
    escritor = csv.writer(archivo, lineterminator="\n")
    if archivo.tell() == 0:
        escritor.writerow(ENCABEZADO_DOMINIOS_POR_CADUCAR)
    escritor.writerow(
        (
            fecha_consulta,
            fuente,
            fecha_registro,
            dominio_salida,
            fecha_expiracion,
            dias_restantes,
            resultado.estado,
            enriquecimiento["longitud"],
            enriquecimiento["contiene_guion"],
            enriquecimiento["contiene_numero"],
            enriquecimiento["solo_letras"],
            enriquecimiento["keyword_principal"],
            enriquecimiento["sector_probable"],
            enriquecimiento["riesgo_reventa"],
        )
    )
    archivo.flush()
    return True


def asegurar_formato_csv_por_caducar(ruta_salida: Path) -> None:
    if not ruta_salida.exists() or ruta_salida.stat().st_size == 0:
        return

    with ruta_salida.open("r", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        try:
            encabezado = tuple(next(lector))
        except StopIteration:
            return

    if encabezado == ENCABEZADO_DOMINIOS_POR_CADUCAR:
        return
    if encabezado != ENCABEZADO_ANTERIOR_DOMINIOS_POR_CADUCAR:
        return

    descriptor, nombre_temporal = tempfile.mkstemp(
        prefix=f"{ruta_salida.name}.",
        suffix=".migracion.tmp",
        dir=ruta_salida.parent,
        text=True,
    )
    ruta_temporal = Path(nombre_temporal)

    try:
        with (
            ruta_salida.open("r", encoding="utf-8", newline="") as entrada,
            open(descriptor, "w", encoding="utf-8", newline="") as salida,
        ):
            lector = csv.reader(entrada)
            next(lector, None)
            escritor = csv.writer(salida, lineterminator="\n")
            escritor.writerow(ENCABEZADO_DOMINIOS_POR_CADUCAR)
            for fila in lector:
                if len(fila) < len(ENCABEZADO_ANTERIOR_DOMINIOS_POR_CADUCAR):
                    continue
                fecha_consulta, dominio, fecha_expiracion, dias_restantes, estado = fila[:5]
                enriquecimiento = enriquecer_dominio(dominio)
                escritor.writerow(
                    (
                        fecha_consulta,
                        "historico",
                        "",
                        dominio,
                        fecha_expiracion,
                        dias_restantes,
                        estado,
                        enriquecimiento["longitud"],
                        enriquecimiento["contiene_guion"],
                        enriquecimiento["contiene_numero"],
                        enriquecimiento["solo_letras"],
                        enriquecimiento["keyword_principal"],
                        enriquecimiento["sector_probable"],
                        enriquecimiento["riesgo_reventa"],
                    )
                )
        respaldo = ruta_salida.with_suffix(ruta_salida.suffix + ".bak")
        ruta_salida.replace(respaldo)
        ruta_temporal.replace(ruta_salida)
    finally:
        ruta_temporal.unlink(missing_ok=True)


def archivo_salida_por_defecto(nombre_base: str) -> Path:
    return DIRECTORIO_ARCHIVO / nombre_base
