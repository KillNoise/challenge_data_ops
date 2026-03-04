"""
Q1 - Top 10 fechas con más tweets (Optimizado por MEMORIA)

Estrategia:
- Leer el archivo línea a línea (streaming) para evitar cargar todo en RAM.
- Usar Counter para contar tweets por fecha.
- Usar defaultdict(Counter) para contar tweets por (fecha, usuario).
- Solo mantener en memoria los contadores, no los tweets completos.

Supuestos:
- El archivo es un JSON lines (un JSON por línea).
- El campo "date" contiene un string ISO 8601 del cual tomamos los primeros 10 chars.
- El campo "user" es un dict con key "username".
"""

from typing import List, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import json
from logger_config import get_logger

logger = get_logger(__name__)


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    logger.info("Iniciando q1_memory — lectura streaming")
    date_counts: Counter = Counter()
    date_user_counts: dict[str, Counter] = defaultdict(Counter)
    line_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tweet = json.loads(line)
            date_str = tweet["date"][:10]
            username = tweet["user"]["username"]

            date_counts[date_str] += 1
            date_user_counts[date_str][username] += 1
            line_count += 1

    logger.info(f"Procesados {line_count} tweets en streaming")

    # Top 10 fechas
    top_dates = date_counts.most_common(10)

    result = []
    for date_str, _ in top_dates:
        top_user = date_user_counts[date_str].most_common(1)[0][0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        result.append((date_obj, top_user))

    logger.info(f"q1_memory completado — {len(result)} resultados")
    return result
