"""
Q3 - Top 10 usuarios mas mencionados (Optimizado por TIEMPO)

Estrategia:
- Leer todo el archivo de una vez en memoria (I/O rapido).
- Parsear cada linea con orjson (parser en Rust, ~5x mas rapido que json stdlib).
- Extraer menciones con regex compilado.
- Prioriza velocidad sobre uso de memoria.

Diferencia vs q3_memory:
- orjson vs json stdlib (parser mas rapido)
- Lectura bulk vs streaming (I/O mas rapido)
- Regex pre-compilado para max velocidad
"""

from typing import List, Tuple
from collections import Counter
import re
import orjson
from logger_config import get_logger

logger = get_logger(__name__)

# Pre-compilar regex fuera de la funcion para max performance
MENTION_PATTERN = re.compile(r"@(\w+)")


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Iniciando q3_time -- lectura bulk + orjson")

    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Leidas {len(raw_lines)} lineas en bulk")

    mention_counter: Counter = Counter()

    for line in raw_lines:
        if not line.strip():
            continue
        tweet = orjson.loads(line)
        content = tweet.get("content", "")
        if not content:
            continue
        mentions = MENTION_PATTERN.findall(content)
        mention_counter.update(mentions)

    logger.info(
        f"q3_time completado -- {len(mention_counter)} usuarios unicos mencionados"
    )
    return mention_counter.most_common(10)
