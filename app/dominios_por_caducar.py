#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
dominios_por_caducar.py
Version: v2.3
Agente/LLM: Codex (GPT-5)

Orquestacion para revisar dominios .CL y detectar cuales estan por caducar.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Iterator

from app.checkpoint_dominios import (
    borrar_checkpoint,
    construir_metadata_checkpoint,
    cargar_checkpoint,
    guardar_checkpoint,
    resolver_checkpoint,
)
from app.comun_nic import (
    eliminar_tildes,
    es_dominio_cl_valido,
    fecha_santiago_hoy,
    limpiar_texto,
    obtener_texto,
)
from app.configuracion import (
    ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA,
    ARCHIVO_DOMINIOS_POR_CADUCAR,
    VERSION_PROYECTO,
)
from app.entrada_dominios import (
    ConsultaDominio,
    leer_registros_desde_fuente,
    parsear_fecha_entrada,
    resolver_entrada,
)
from app.modelos_dominios import ResultadoDominio
from app.progreso_dominios import mostrar_progreso
from app.salida_dominios import asegurar_formato_csv_por_caducar, escribir_resultado

VERSION_SCRIPT = VERSION_PROYECTO
# Seguimiento de version y autoria del cambio: v2.3 | Codex (GPT-5)

URL_RENOVAR = "https://clientes.nic.cl/registrar/renovar.do?d={dominio}"

REGEX_FECHA_ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
REGEX_FECHA_LATAM = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
REGEX_ETIQUETA_FECHA = re.compile(r"fecha de expiracion del dominio", flags=re.IGNORECASE)


def parsear_fecha_expiracion(texto: str) -> date | None:
    normalizado = limpiar_texto(texto)
    texto_sin_tildes = eliminar_tildes(normalizado).lower()

    fragmento = normalizado
    coincidencia_etiqueta = REGEX_ETIQUETA_FECHA.search(texto_sin_tildes)
    if coincidencia_etiqueta:
        inicio = coincidencia_etiqueta.end()
        fragmento = normalizado[inicio : inicio + 160]

    for patron, formato in ((REGEX_FECHA_ISO, "%Y-%m-%d"), (REGEX_FECHA_LATAM, "%d/%m/%Y")):
        coincidencia = patron.search(fragmento)
        if coincidencia:
            try:
                return datetime.strptime(coincidencia.group(1), formato).date()
            except ValueError:
                pass

    for patron, formato in ((REGEX_FECHA_ISO, "%Y-%m-%d"), (REGEX_FECHA_LATAM, "%d/%m/%Y")):
        coincidencia = patron.search(normalizado)
        if coincidencia:
            try:
                return datetime.strptime(coincidencia.group(1), formato).date()
            except ValueError:
                pass

    return None


def consultar_dominio(dominio: ConsultaDominio, umbral_dias: int) -> ResultadoDominio:
    url = URL_RENOVAR.format(dominio=dominio.dominio_consulta)
    fecha_hoy = fecha_santiago_hoy()

    try:
        texto = obtener_texto(url)
    except Exception as error:
        return ResultadoDominio(
            dominio_salida=dominio.dominio_salida,
            fecha_expiracion=None,
            dias_restantes=None,
            estado="error",
            detalle=str(error),
        )

    texto_normalizado = limpiar_texto(texto)
    texto_sin_tildes = eliminar_tildes(texto_normalizado).lower()

    if "no es posible renovar el dominio" in texto_sin_tildes or "consulte informacion en whois" in texto_sin_tildes:
        return ResultadoDominio(
            dominio_salida=dominio.dominio_salida,
            fecha_expiracion=None,
            dias_restantes=None,
            estado="no_renovable",
        )

    fecha_expiracion = parsear_fecha_expiracion(texto_normalizado)
    if fecha_expiracion is None:
        return ResultadoDominio(
            dominio_salida=dominio.dominio_salida,
            fecha_expiracion=None,
            dias_restantes=None,
            estado="sin_fecha",
        )

    dias_restantes = (fecha_expiracion - fecha_hoy).days
    if dias_restantes < 0:
        estado = "caducado"
    elif dias_restantes == 0:
        estado = "vence_hoy"
    elif dias_restantes <= umbral_dias:
        estado = "por_vencer"
    else:
        estado = "fuera_de_umbral"

    return ResultadoDominio(
        dominio_salida=dominio.dominio_salida,
        fecha_expiracion=fecha_expiracion,
        dias_restantes=dias_restantes,
        estado=estado,
    )


def seleccionar_registros(
    registros: list[ConsultaDominio],
    orden: str,
    desde_fecha: date | None,
) -> list[ConsultaDominio]:
    iterable = reversed(registros) if orden == "inverso" else registros
    seleccionados: list[ConsultaDominio] = []
    vistos: set[str] = set()
    usar_corte_rapido = orden == "inverso" and desde_fecha is not None and all(
        registro.fecha_registro is not None for registro in registros
    )

    for registro in iterable:
        if desde_fecha is not None and registro.fecha_registro is not None:
            if usar_corte_rapido and registro.fecha_registro < desde_fecha:
                break
            if registro.fecha_registro < desde_fecha:
                continue

        if registro.dominio_consulta in vistos:
            continue

        vistos.add(registro.dominio_consulta)
        seleccionados.append(registro)

    return seleccionados


def resolver_orden(
    orden_argumentado: str,
    modo: str,
    ruta_entrada: Path | None,
    hay_fechas_en_entrada: bool,
    desde_fecha: date | None,
) -> str:
    if orden_argumentado != "auto":
        return orden_argumentado

    if modo == "descubrir" and (
        ruta_entrada == ARCHIVO_DOMINIOS_ELIMINADOS_SEMANA
        or hay_fechas_en_entrada
        or desde_fecha is not None
    ):
        return "inverso"

    return "normal"


def obtener_firma_entrada(ruta_entrada: Path | None) -> dict[str, object]:
    if ruta_entrada is None:
        return {"tipo": "stdin"}

    informacion = ruta_entrada.resolve()
    estadisticas = ruta_entrada.stat()
    return {
        "tipo": "archivo",
        "ruta": str(informacion),
        "tamano": estadisticas.st_size,
        "mtime_ns": estadisticas.st_mtime_ns,
    }


def inferir_fuente(ruta_entrada: Path | None, modo: str) -> str:
    if ruta_entrada is None:
        return "stdin"
    nombre = ruta_entrada.name.lower()
    if "registrado" in nombre:
        return "registrados"
    if "eliminado" in nombre:
        return "eliminados"
    if modo == "vigilar":
        return "candidatos"
    return ruta_entrada.stem


def iterar_consultas_en_flujo(
    registros: list[ConsultaDominio],
    umbral_dias: int,
    hilos: int,
) -> Iterator[tuple[ConsultaDominio, ResultadoDominio]]:
    if not registros:
        return

    limite_en_vuelo = max(2, hilos * 4)
    iterador = iter(registros)
    futuros: dict[concurrent.futures.Future[ResultadoDominio], ConsultaDominio] = {}

    def rellenar_cola(executor: concurrent.futures.ThreadPoolExecutor) -> None:
        while len(futuros) < limite_en_vuelo:
            try:
                registro = next(iterador)
            except StopIteration:
                return
            futuro = executor.submit(consultar_dominio, registro, umbral_dias)
            futuros[futuro] = registro

    with concurrent.futures.ThreadPoolExecutor(max_workers=hilos) as executor:
        rellenar_cola(executor)
        while futuros:
            terminados, _ = concurrent.futures.wait(
                set(futuros),
                return_when=concurrent.futures.FIRST_COMPLETED,
            )
            for futuro in terminados:
                registro = futuros.pop(futuro)
                try:
                    resultado = futuro.result()
                except Exception as error:
                    resultado = ResultadoDominio(
                        dominio_salida=registro.dominio_salida,
                        fecha_expiracion=None,
                        dias_restantes=None,
                        estado="error",
                        detalle=str(error),
                    )
                yield registro, resultado
            rellenar_cola(executor)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Revisa dominios .CL en NIC Chile y detecta si estan por caducar."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION_SCRIPT}")
    parser.add_argument(
        "--modo",
        choices=("vigilar", "descubrir"),
        required=True,
        help="vigilar usa una lista conocida; descubrir puede tomar eliminados para la prueba de humo.",
    )
    parser.add_argument(
        "--entrada",
        default=None,
        help="Archivo con dominios o lista por stdin. Si no se indica, se usa un archivo por defecto segun el modo.",
    )
    parser.add_argument(
        "--salida",
        default=None,
        help="Archivo CSV de salida. Si no se indica, usa el historico dominios-por-caducar.csv.",
    )
    parser.add_argument(
        "--umbral-dias",
        type=int,
        default=90,
        help="Cantidad de dias para considerar un dominio como por vencer. Default: 90.",
    )
    parser.add_argument(
        "--hilos",
        type=int,
        default=4,
        help="Cantidad de consultas concurrentes. Default: 4.",
    )
    parser.add_argument(
        "--sin-punycode",
        action="store_true",
        help="Conserva el dominio de salida tal como se entrego, en vez de escribirlo en punycode.",
    )
    parser.add_argument(
        "--incluir-todos",
        action="store_true",
        default=None,
        help="Escribe tambien sin_fecha, no_renovable y fuera_de_umbral.",
    )
    parser.add_argument(
        "--progreso",
        choices=("auto", "si", "no"),
        default="auto",
        help="Controla el indicador de avance en stderr. Default: auto.",
    )
    parser.add_argument(
        "--progreso-cada",
        type=int,
        default=100,
        help="Frecuencia del avance visible. Default: 100.",
    )
    parser.add_argument(
        "--orden",
        choices=("auto", "normal", "inverso"),
        default="auto",
        help="Orden de procesamiento. auto usa inverso cuando revisas historicos con fecha.",
    )
    parser.add_argument(
        "--desde-fecha",
        default=None,
        help="Filtra historicos por fecha de registro minima en formato YYYY-MM-DD.",
    )
    parser.add_argument(
        "--limite",
        type=int,
        default=None,
        help="Maximo de dominios a procesar en esta corrida. Default: sin limite.",
    )
    parser.add_argument(
        "--checkpoint",
        default=None,
        help="Archivo JSON para reanudar una corrida interrumpida. Default: checkpoint local automatico.",
    )
    return parser


def principal() -> int:
    parser = construir_parser()
    argumentos = parser.parse_args()

    if argumentos.umbral_dias < 0:
        parser.error("--umbral-dias debe ser mayor o igual a 0.")
    if argumentos.hilos < 1:
        parser.error("--hilos debe ser mayor o igual a 1.")
    if argumentos.progreso_cada < 1:
        parser.error("--progreso-cada debe ser mayor o igual a 1.")
    if argumentos.limite is not None and argumentos.limite < 1:
        parser.error("--limite debe ser mayor o igual a 1.")

    modo = argumentos.modo
    ruta_entrada = resolver_entrada(argumentos.entrada, modo)
    ruta_salida = Path(argumentos.salida) if argumentos.salida else ARCHIVO_DOMINIOS_POR_CADUCAR
    ruta_checkpoint = resolver_checkpoint(argumentos.checkpoint)
    desde_fecha = parsear_fecha_entrada(argumentos.desde_fecha) if argumentos.desde_fecha else None

    registros_crudos = leer_registros_desde_fuente(ruta_entrada)
    if not registros_crudos:
        print("[warn] No se encontraron dominios de entrada.", file=sys.stderr)
        return 1

    hay_fechas_en_entrada = all(registro.fecha_registro is not None for registro in registros_crudos)
    orden_final = resolver_orden(
        argumentos.orden,
        modo,
        ruta_entrada,
        hay_fechas_en_entrada,
        desde_fecha,
    )
    incluir_todos = argumentos.incluir_todos
    if incluir_todos is None:
        incluir_todos = modo == "vigilar"

    registros_seleccionados = seleccionar_registros(registros_crudos, orden_final, desde_fecha)
    firma_entrada = obtener_firma_entrada(ruta_entrada)
    metadata_checkpoint = construir_metadata_checkpoint(
        version=VERSION_SCRIPT,
        modo=modo,
        orden=orden_final,
        desde_fecha=desde_fecha,
        limite=argumentos.limite,
        umbral_dias=argumentos.umbral_dias,
        firma_entrada=firma_entrada,
    )

    procesados_checkpoint, checkpoint_previo = cargar_checkpoint(ruta_checkpoint, metadata_checkpoint)
    if procesados_checkpoint > len(registros_seleccionados):
        print("[warn] El checkpoint excede el total actual; se ignorara.", file=sys.stderr)
        procesados_checkpoint = 0
        checkpoint_previo = None

    if procesados_checkpoint:
        registros_seleccionados = registros_seleccionados[procesados_checkpoint:]

    if argumentos.limite is not None:
        registros_seleccionados = registros_seleccionados[: argumentos.limite]

    total_a_procesar = len(registros_seleccionados)
    if total_a_procesar == 0:
        borrar_checkpoint(ruta_checkpoint)
        print(
            f"[ok] Version: {VERSION_SCRIPT} | Modo: {modo} | Orden: {orden_final} | "
            f"Entrada: {ruta_entrada or 'stdin'} | Salida: {ruta_salida} | consultados=0 | escritos=0"
        )
        print("[ok] No habia dominios pendientes para procesar.")
        return 0

    mostrar_barra = argumentos.progreso == "si" or (argumentos.progreso == "auto" and sys.stderr.isatty())
    fecha_consulta = fecha_santiago_hoy().isoformat()
    fuente = inferir_fuente(ruta_entrada, modo)

    if mostrar_barra:
        mostrar_progreso(0, total_a_procesar, "", True, argumentos.progreso_cada)

    procesados = 0
    escritos = 0
    omitidos_salida = 0
    estados: dict[str, int] = {}
    ultimo_dominio = ""
    checkpoint_guardado = procesados_checkpoint

    try:
        asegurar_formato_csv_por_caducar(ruta_salida)
        with ruta_salida.open("a", encoding="utf-8", newline="") as archivo_salida:
            for registro, resultado in iterar_consultas_en_flujo(
                registros_seleccionados,
                argumentos.umbral_dias,
                argumentos.hilos,
            ):
                procesados += 1
                ultimo_dominio = registro.dominio_consulta
                estados[resultado.estado] = estados.get(resultado.estado, 0) + 1

                if escribir_resultado(
                    archivo_salida,
                    fecha_consulta,
                    fuente,
                    registro,
                    resultado,
                    argumentos.sin_punycode,
                    incluir_todos,
                ):
                    escritos += 1
                else:
                    omitidos_salida += 1

                checkpoint_guardado = procesados_checkpoint + procesados
                guardar_checkpoint(
                    ruta_checkpoint,
                    metadata_checkpoint,
                    checkpoint_guardado,
                    escritos,
                    omitidos_salida,
                    ultimo_dominio,
                    completado=False,
                )

                if mostrar_barra:
                    mostrar_progreso(
                        procesados,
                        total_a_procesar,
                        registro.dominio_consulta if not argumentos.sin_punycode else registro.dominio_salida,
                        True,
                        argumentos.progreso_cada,
                        finalizar=procesados == total_a_procesar,
                    )
    except KeyboardInterrupt:
        guardar_checkpoint(
            ruta_checkpoint,
            metadata_checkpoint,
            checkpoint_guardado,
            escritos,
            omitidos_salida,
            ultimo_dominio,
            completado=False,
        )
        print("\n[warn] Corrida interrumpida. El checkpoint quedo guardado para reanudar.", file=sys.stderr)
        return 130

    borrar_checkpoint(ruta_checkpoint)

    resumen_estados = ", ".join(f"{estado}={cantidad}" for estado, cantidad in sorted(estados.items()))
    print(
        f"[ok] Version: {VERSION_SCRIPT} | Modo: {modo} | Orden: {orden_final} | "
        f"Entrada: {ruta_entrada or 'stdin'} | Salida: {ruta_salida} | "
        f"consultados={procesados} | escritos={escritos} | omitidos={omitidos_salida}"
    )
    print(f"[ok] Estados: {resumen_estados}")
    if checkpoint_previo is not None:
        print("[ok] Checkpoint anterior reanudado y eliminado al terminar.")

    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
