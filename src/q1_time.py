"""
Q1 - Top 10 fechas con mas tweets (Optimizado por TIEMPO)

Estrategia:
- Leer todo el archivo de una vez en memoria (I/O rapido).
- Parsear cada linea con orjson (parser en Rust, ~5x mas rapido que json stdlib).
- Usar Counter para conteo rapido.
- Prioriza velocidad sobre uso de memoria.

Diferencia vs q1_memory:
- orjson vs json stdlib (parser mas rapido)
- Lectura bulk vs streaming (I/O mas rapido)
"""

from typing import List, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import orjson
from logger_config import get_logger

logger = get_logger(__name__)


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    logger.info("Iniciando q1_time -- lectura bulk + orjson")

    # Leer todo el archivo de una vez (mas rapido que linea a linea)
    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Leidas {len(raw_lines)} lineas en bulk")

    date_counts: Counter = Counter()
    date_user_counts: dict[str, Counter] = defaultdict(Counter)

    for line in raw_lines:
        if not line.strip():
            continue
        tweet = orjson.loads(line)
        date_str = tweet["date"][:10]
        username = tweet["user"]["username"]

        date_counts[date_str] += 1
        date_user_counts[date_str][username] += 1

    # Top 10 fechas
    top_dates = date_counts.most_common(10)

    result = []
    for date_str, _ in top_dates:
        top_user = date_user_counts[date_str].most_common(1)[0][0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        result.append((date_obj, top_user))

    logger.info(f"q1_time completado -- {len(result)} resultados")
    return result
