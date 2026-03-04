"""
Q2 - Top 10 emojis más usados (Optimizado por MEMORIA)

Estrategia:
- Leer línea a línea (streaming).
- Extraer emojis de cada content con emoji.emoji_list().
- Acumular en un Counter (bajo uso de memoria).

Supuestos:
- Se usan emojis Unicode estándar.
- Cada aparición de un emoji cuenta individualmente.
"""

from typing import List, Tuple
from collections import Counter
import json
import emoji
from logger_config import get_logger

logger = get_logger(__name__)


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Iniciando q2_memory — lectura streaming")
    emoji_counter: Counter = Counter()
    line_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tweet = json.loads(line)
            content = tweet.get("content", "")
            if not content:
                continue
            emojis = emoji.emoji_list(content)
            for e in emojis:
                emoji_counter[e["emoji"]] += 1
            line_count += 1

    logger.info(f"Procesados {line_count} tweets — {len(emoji_counter)} emojis únicos")
    return emoji_counter.most_common(10)
