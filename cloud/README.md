# Solucion Cloud: BigQuery + Terraform

## Arquitectura

```
JSON file --> GCS Bucket --[Cloud Function]--> BigQuery Table --> SQL Queries (Q1, Q2, Q3)
```

Toda la infraestructura se provisiona con **Terraform** (IaC). No se almacenan credenciales en el codigo.

### Pipeline Event-Driven

Al subir un archivo JSON al bucket GCS, una **Cloud Function (Gen2)** se dispara automaticamente via **Eventarc** y:
1. Valida que el archivo este en el prefijo `raw/` y sea `.json`
2. Carga los datos en BigQuery con schema auto-detectado
3. Loguea el resultado (filas cargadas)

Esto elimina la necesidad de ejecutar `load_data.sh` manualmente — el pipeline es completamente automatizado.

## Prerequisitos

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (CLI `gcloud`)
- [Terraform](https://developer.hashicorp.com/terraform/downloads) (>= 1.0)
- Un proyecto de GCP con facturacion habilitada
- APIs habilitadas: BigQuery, Cloud Storage

## Paso a paso

### 1. Autenticarse con GCP

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Habilitar APIs necesarias

```bash
gcloud services enable bigquery.googleapis.com storage.googleapis.com
```

### 3. Provisionar infraestructura con Terraform

```bash
cd cloud/
terraform init
terraform plan -var="project_id=YOUR_PROJECT_ID"
terraform apply -var="project_id=YOUR_PROJECT_ID"
```

Esto crea:
- Bucket GCS: `YOUR_PROJECT_ID-challenge-raw-data`
- Dataset BigQuery: `challenge_data_ops`
- Tabla BigQuery: `tweets`
- Service Account: `challenge-data-ops@YOUR_PROJECT_ID.iam.gserviceaccount.com`

### 4. Subir datos y cargar en BigQuery

```bash
chmod +x load_data.sh
./load_data.sh YOUR_PROJECT_ID
```

El script:
1. Sube el archivo JSON a GCS
2. Lo carga en BigQuery con schema auto-detectado
3. Verifica el conteo de filas

### 5. Ejecutar queries SQL

Ejecutar las queries en `queries/` via consola de BigQuery o CLI:

```bash
# Q1: Top 10 fechas con mas tweets
bq query --use_legacy_sql=false < queries/q1_top_dates.sql

# Q2: Top 10 emojis mas usados
bq query --use_legacy_sql=false < queries/q2_top_emojis.sql

# Q3: Top 10 usuarios mas mencionados
bq query --use_legacy_sql=false < queries/q3_top_mentions.sql
```

> **Nota**: Reemplazar `{PROJECT_ID}` en los archivos SQL con el ID real del proyecto antes de ejecutar.

### 6. Limpieza

```bash
terraform destroy -var="project_id=YOUR_PROJECT_ID"
```

## Por que BigQuery?

- **Serverless**: Sin infraestructura que administrar, sin dimensionar clusters
- **Economico**: Para ~400MB de datos, las queries cuestan fracciones de centavo
- **Soporte nativo JSON**: Auto-detecta schema desde NDJSON, maneja campos nested
- **SQL**: Los 3 problemas se traducen directamente a SQL, sin codigo custom
- **Escalable**: Las mismas queries funcionan en GB/TB/PB sin cambios de codigo

## Comparacion: Local vs Cloud

En la solucion local se implementaron **2 versiones** por problema:
- `*_time`: Optimizado por velocidad (orjson + lectura bulk en RAM)
- `*_memory`: Optimizado por uso de memoria (streaming linea a linea)

Este tradeoff tiempo vs memoria **no aplica en BigQuery** porque:
1. **BigQuery es serverless** -- no se controla la RAM ni el CPU. Google administra los recursos internamente
2. **Una sola query SQL** resuelve cada problema -- no es necesario elegir entre "cargar todo en RAM" vs "streaming"
3. **El costo** se mide en bytes procesados, no en tiempo de ejecucion o memoria

Esto demuestra que la herramienta correcta (BigQuery) elimina la complejidad de optimizacion manual que fue necesaria en la solucion local.

## Resultados obtenidos

Datos cargados: **117,405 filas** (2 omitidas por nesting extremo en `quotedTweet.quotedTweet.quotedTweet`)

### Q1 - Top 10 fechas con mas tweets

| Fecha | Usuario mas activo | Total tweets |
|-------|-------------------|-------------|
| 2021-02-12 | RanbirS00614606 | 12,347 |
| 2021-02-13 | MaanDee08215437 | 11,296 |
| 2021-02-17 | RaaJVinderkaur | 11,086 |
| 2021-02-16 | jot__b | 10,443 |
| 2021-02-14 | rebelpacifist | 10,249 |
| 2021-02-18 | neetuanjle_nitu | 9,625 |
| 2021-02-15 | jot__b | 9,197 |
| 2021-02-20 | MangalJ23056160 | 8,502 |
| 2021-02-23 | Surrypuria | 8,417 |
| 2021-02-19 | Preetm91 | 8,204 |

### Q3 - Top 10 usuarios mas mencionados

| Usuario | Menciones |
|---------|----------|
| narendramodi | 2,261 |
| Kisanektamorcha | 1,836 |
| RakeshTikaitBKU | 1,641 |
| PMOIndia | 1,422 |
| RahulGandhi | 1,125 |
| GretaThunberg | 1,046 |
| RaviSinghKA | 1,015 |
| rihanna | 972 |
| UNHumanRights | 962 |
| meenaharris | 925 |

> **Nota**: Los resultados de Q1 y Q3 coinciden exactamente con la solucion local. Q2 (emojis) funciona correctamente pero la consola CLI muestra Unicode escapes en vez de los caracteres emoji.
