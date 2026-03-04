"""
Q2 - Top 10 emojis mas usados (Optimizado por TIEMPO)

Estrategia:
- Leer todo el archivo de una vez en memoria (I/O rapido).
- Parsear cada linea con orjson (parser en Rust, ~5x mas rapido que json stdlib).
- Extraer emojis con emoji.emoji_list().
- Prioriza velocidad sobre uso de memoria.

Diferencia vs q2_memory:
- orjson vs json stdlib (parser mas rapido)
- Lectura bulk vs streaming (I/O mas rapido)
"""

from typing import List, Tuple
from collections import Counter
import orjson
import emoji
from logger_config import get_logger

logger = get_logger(__name__)


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Iniciando q2_time -- lectura bulk + orjson")

    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Leidas {len(raw_lines)} lineas en bulk")

    emoji_counter: Counter = Counter()

    for line in raw_lines:
        if not line.strip():
            continue
        tweet = orjson.loads(line)
        content = tweet.get("content", "")
        if not content:
            continue
        emojis = emoji.emoji_list(content)
        for e in emojis:
            emoji_counter[e["emoji"]] += 1

    logger.info(f"q2_time completado -- {len(emoji_counter)} emojis unicos encontrados")
    return emoji_counter.most_common(10)
