# -*- coding: utf-8 -*-
"""
Clase 8 - Procesamiento de Lenguaje Natural
Generación de figuras para el informe de evidencias (Actividad 8).

Autor del script de apoyo: Víctor Manuel Santos Martínez
Docente: M.C. Pablo Ricardo Sánchez Gómez

Este módulo NO reemplaza al análisis del profesor. Toma las salidas .csv
producidas por `analisis_ambiguedad_clase8.py` y las resume en gráficos .png
que se incrustan en el informe redactado en Obsidian. Se mantiene una única
responsabilidad por función (principio SRP) y rutas parametrizadas para
favorecer la reproducibilidad.
"""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: permite exportar en entornos headless
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------- #
# Configuración global
# --------------------------------------------------------------------------- #
BASE = Path(__file__).resolve().parent
SALIDAS = BASE / "salidas_clase8"
FIGURAS = BASE / "figuras"
FIGURAS.mkdir(exist_ok=True)

# Paleta coherente con el material de clase (azules institucionales)
COLOR_LEX, COLOR_SINT, COLOR_SEM = "#174666", "#2b6cb0", "#63b3ed"
PALETA_TIPO = {"lexica": COLOR_LEX, "sintactica": COLOR_SINT, "semantica": COLOR_SEM}

plt.rcParams.update(
    {
        "figure.dpi": 130,
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def leer_csv(nombre: str) -> list[dict]:
    """Lee un CSV de salida (codificación utf-8-sig) y devuelve lista de dicts."""
    with open(SALIDAS / nombre, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def _etiquetar_barras(ax, valores) -> None:
    """Coloca el valor numérico encima de cada barra."""
    for barra, valor in zip(ax.patches, valores):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + max(valores) * 0.01,
            str(valor),
            ha="center",
            va="bottom",
            fontweight="bold",
        )


def fig_distribucion_dataset() -> None:
    """Fig. 1 - Distribución del dataset por tipo de ambigüedad."""
    resumen = {r["tipo_ambiguedad"]: int(r["total"]) for r in leer_csv("05_resumen_por_tipo.csv")}
    orden = ["lexica", "sintactica", "semantica"]
    valores = [resumen[k] for k in orden]
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.bar([k.capitalize() for k in orden], valores, color=[PALETA_TIPO[k] for k in orden])
    _etiquetar_barras(ax, valores)
    ax.set_ylabel("Número de oraciones")
    ax.set_title("Distribución del dataset por tipo de ambigüedad")
    ax.set_ylim(0, max(valores) * 1.18)
    fig.tight_layout()
    fig.savefig(FIGURAS / "a8_fig1_distribucion_dataset.png")
    plt.close(fig)


def fig_indicios_por_categoria() -> None:
    """Fig. 2 - Cantidad de oraciones marcadas por cada detector de señales."""
    conteos = {
        "Indicios\nléxicos": len(leer_csv("02_indicios_lexicos.csv")),
        "Indicios\nsintácticos": len(leer_csv("03_indicios_sintacticos.csv")),
        "Indicios\nsemánticos": len(leer_csv("04_indicios_semanticos.csv")),
    }
    valores = list(conteos.values())
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.bar(list(conteos.keys()), valores, color=[COLOR_LEX, COLOR_SINT, COLOR_SEM])
    _etiquetar_barras(ax, valores)
    ax.set_ylabel("Oraciones con al menos una señal")
    ax.set_title("Señales de ambigüedad detectadas por el sistema")
    ax.set_ylim(0, max(valores) * 1.18)
    fig.tight_layout()
    fig.savefig(FIGURAS / "a8_fig2_indicios_por_categoria.png")
    plt.close(fig)


def fig_palabras_ambiguas() -> None:
    """Fig. 3 - Frecuencia de palabras ambiguas detectadas (señal léxica)."""
    conteo = Counter(r["palabra_ambigua"] for r in leer_csv("02_indicios_lexicos.csv"))
    items = conteo.most_common()
    etiquetas = [w for w, _ in items]
    valores = [c for _, c in items]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.barh(etiquetas[::-1], valores[::-1], color=COLOR_LEX)
    for i, v in enumerate(valores[::-1]):
        ax.text(v + 0.03, i, str(v), va="center", fontweight="bold")
    ax.set_xlabel("Frecuencia en el dataset")
    ax.set_title("Palabras ambiguas detectadas (indicios léxicos)")
    fig.tight_layout()
    fig.savefig(FIGURAS / "a8_fig3_palabras_ambiguas.png")
    plt.close(fig)


def fig_dominios() -> None:
    """Fig. 4 - Distribución de oraciones por dominio temático."""
    conteo = Counter(r["dominio"] for r in leer_csv("01_dataset_validado.csv"))
    items = conteo.most_common()
    etiquetas = [w for w, _ in items]
    valores = [c for _, c in items]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(etiquetas[::-1], valores[::-1], color="#2b6cb0")
    for i, v in enumerate(valores[::-1]):
        ax.text(v + 0.03, i, str(v), va="center", fontweight="bold")
    ax.set_xlabel("Número de oraciones")
    ax.set_title("Cobertura temática del dataset (dominios)")
    fig.tight_layout()
    fig.savefig(FIGURAS / "a8_fig4_dominios.png")
    plt.close(fig)


def fig_puntaje_revision() -> None:
    """Fig. 5 - Puntaje de revisión sugerido por el sistema, por tipo."""
    filas = leer_csv("06_muestra_sugerida.csv")
    # Puntaje medio por tipo de ambigüedad
    acum: dict[str, list[int]] = {}
    for r in filas:
        acum.setdefault(r["tipo_ambiguedad"], []).append(int(r["puntaje_revision"]))
    orden = ["lexica", "sintactica", "semantica"]
    medias = [sum(acum[k]) / len(acum[k]) for k in orden]
    fig, ax = plt.subplots(figsize=(7, 4.3))
    ax.bar([k.capitalize() for k in orden], medias, color=[PALETA_TIPO[k] for k in orden])
    for barra, valor in zip(ax.patches, medias):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 0.03,
            f"{valor:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    ax.set_ylabel("Puntaje de revisión promedio")
    ax.set_title("Prioridad de revisión humana sugerida por tipo")
    ax.set_ylim(0, max(medias) * 1.18)
    fig.tight_layout()
    fig.savefig(FIGURAS / "a8_fig5_puntaje_revision.png")
    plt.close(fig)


def main() -> None:
    fig_distribucion_dataset()
    fig_indicios_por_categoria()
    fig_palabras_ambiguas()
    fig_dominios()
    fig_puntaje_revision()
    print("Figuras generadas en:", FIGURAS.resolve())
    for p in sorted(FIGURAS.glob("*.png")):
        print(" -", p.name)


if __name__ == "__main__":
    main()
