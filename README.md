# MIA_C3_PLN_Corte_02_Bitacora_08 — Análisis de Ambigüedad Lingüística

**Alumno:** Víctor Manuel Santos Martínez
**Matrícula:** 253220020 · **Grupo:** 3.º A
**Materia:** Procesamiento de Lenguaje Natural (Maestría en Inteligencia Artificial — UPMH)
**Docente:** M.C. Pablo Ricardo Sánchez Gómez
**Actividad:** Clase 8 — *Ambigüedad y transición al análisis semántico* (Corte 2, Unidad 3.1)

## Descripción de la actividad

Detección y clasificación automática de **ambigüedad lingüística** en español sobre un dataset
de **72 oraciones** balanceadas (24 léxicas, 24 sintácticas, 24 semánticas). El sistema aplica un
motor de reglas transparente que rastrea tres tipos de señales:

- **Léxicas:** palabras polisémicas/homónimas (p. ej. *banco*, *planta*, *sierra*) y su contexto local.
- **Sintácticas:** preposiciones que pueden producir adjunción ambigua de sintagma preposicional.
- **Semánticas:** cuantificadores, negación, anáfora, causalidad y roles temáticos.

El objetivo pedagógico no es "resolver" la ambigüedad, sino **detectarla y administrarla con
evidencia**, señalando qué casos requieren revisión humana obligatoria.

## Estructura del proyecto

```
codigo_datos_clase8/
├── analisis_ambiguedad_clase8.py     # Script original del docente (motor de reglas, stdlib)
├── analisis_ambiguedad_clase8.ipynb  # Cuaderno documentado (reproduce + visualiza el análisis)
├── generar_figuras.py                # Genera las 5 figuras .png a partir de las salidas .csv
├── datos/
│   └── oraciones_clase8.csv          # Dataset de 72 oraciones etiquetadas
├── salidas_clase8/                   # 6 CSV verificables generados por el análisis
│   ├── 01_dataset_validado.csv
│   ├── 02_indicios_lexicos.csv
│   ├── 03_indicios_sintacticos.csv
│   ├── 04_indicios_semanticos.csv
│   ├── 05_resumen_por_tipo.csv
│   └── 06_muestra_sugerida.csv
├── figuras/                          # Gráficas .png para el informe
├── requirements.txt
└── README.md
```

## Requisitos y ejecución

Entorno probado: **conda `pln311`** (Python 3.11, pandas 3.0, matplotlib 3.10, spacy 3.8).

```bash
conda activate pln311

# 1) Análisis (script del docente) -> genera salidas_clase8/*.csv
python analisis_ambiguedad_clase8.py

# 2) Figuras para el informe -> genera figuras/*.png
python generar_figuras.py

# 3) (Opcional) Cuaderno documentado
jupyter notebook analisis_ambiguedad_clase8.ipynb
```

## Salidas principales

| Archivo | Contenido |
|:--|:--|
| `01_dataset_validado.csv` | Limpieza, tokenización y clasificación inicial |
| `02_indicios_lexicos.csv` | Palabras ambiguas + contexto local (24 casos) |
| `03_indicios_sintacticos.csv` | Preposiciones con posible adjunción ambigua (38 casos) |
| `04_indicios_semanticos.csv` | Negación, cuantificadores, anáfora y roles (52 casos) |
| `05_resumen_por_tipo.csv` | Conteo por tipo de ambigüedad |
| `06_muestra_sugerida.csv` | Oraciones priorizadas para revisión humana |

## Nota metodológica

El motor evita deliberadamente modelos estadísticos (spaCy) para mantener cada marca del sistema
**explicable y auditable**, coherente con la advertencia de la clase sobre *no sobreconfiar en los
modelos*: el programa produce hipótesis con evidencia, y la interpretación final es humana.
