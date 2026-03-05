# Data Engineering Challenge

## Descripcion

Solucion al desafio de ingenieria de datos. Se procesan **~398MB** de tweets (~117K registros en formato JSON Lines) para resolver 3 problemas:

| Problema | Descripcion |
|----------|------------|
| **Q1** | Top 10 fechas con mas tweets y el usuario mas activo en cada fecha |
| **Q2** | Top 10 emojis mas usados en todos los tweets |
| **Q3** | Top 10 usuarios mas mencionados (@username) |

## Enfoques

### Solucion Local (`src/`)

Cada problema se implemento con **2 enfoques**:

- **`*_time`**: Optimizado por velocidad -- `orjson` (parser Rust) + lectura bulk en RAM
- **`*_memory`**: Optimizado por memoria -- `json` stdlib + streaming linea a linea

#### Resultados

| Function | Time (s) | Memory (MiB) | Approach |
|----------|----------|--------------|----------|
| q1_time | 2.96 | 494.3 | orjson + bulk |
| q1_memory | 6.97 | 86.3 | streaming |
| q2_time | 48.23 | 495.3 | orjson + bulk |
| q2_memory | 52.04 | 86.4 | streaming |
| q3_time | 2.80 | 496.0 | orjson + bulk |
| q3_memory | 6.68 | 73.4 | streaming |

> Tiempos medidos con `cProfile` (Python Profilers). Memoria medida con `memory_profiler`. Ambas herramientas recomendadas por el challenge.

### Solucion Cloud (`cloud/`)

Implementacion en **GCP con BigQuery + Terraform**:

- Infraestructura como codigo (Terraform): GCS bucket, BigQuery dataset/tabla, Service Account
- Script de carga: JSON → GCS → BigQuery
- Queries SQL para los 3 problemas

> En BigQuery el tradeoff tiempo vs memoria no aplica -- es serverless y una sola query SQL resuelve cada problema.

Ver [cloud/README.md](cloud/README.md) para el paso a paso completo.

## Estructura del proyecto

```
.
├── README.md
├── requirements.txt
├── verify.py
├── src/
│   ├── challenge.ipynb
│   ├── analisis.md
│   ├── logger_config.py
│   ├── q1_time.py
│   ├── q1_memory.py
│   ├── q2_time.py
│   ├── q2_memory.py
│   ├── q3_time.py
│   └── q3_memory.py
└── cloud/
    ├── README.md
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    ├── load_data.sh
    └── queries/
        ├── q1_top_dates.sql
        ├── q2_top_emojis.sql
        └── q3_top_mentions.sql
```

## Como ejecutar (Local)

### Prerequisitos

- Python 3.9+
- pip

### Instalacion

```bash
pip install -r requirements.txt
```

### Ejecucion

1. Colocar el archivo `farmers-protest-tweets-2021-2-4.json` en la raiz del proyecto
2. Abrir y ejecutar `src/challenge.ipynb`

O ejecutar la verificacion rapida:

```bash
python verify.py
```

## Tecnologias utilizadas

### Local
- **Python**: Lenguaje principal
- **orjson**: Parser JSON basado en Rust (~5x mas rapido que json stdlib)
- **memory_profiler**: Medicion de uso de memoria (recomendado por el challenge)
- **cProfile**: Medicion de tiempo de ejecucion (Python Profilers, recomendado por el challenge)
- **emoji**: Deteccion de emojis Unicode

### Cloud
- **BigQuery**: Procesamiento de datos serverless
- **GCS**: Almacenamiento de datos raw
- **Terraform**: Infraestructura como codigo (IaC)
