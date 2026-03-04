"""
Q3 - Top 10 usuarios más mencionados (Optimizado por MEMORIA)

Estrategia:
- Leer línea a línea (streaming).
- Extraer menciones con regex @(\w+) del campo content.
- Acumular en Counter (bajo uso de memoria).

Supuestos:
- Las menciones siguen el formato @username en el contenido del tweet.
- Se usa regex sobre content para máxima eficiencia.
"""

from typing import List, Tuple
from collections import Counter
import json
import re
from logger_config import get_logger

logger = get_logger(__name__)


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Iniciando q3_memory — lectura streaming")
    mention_counter: Counter = Counter()
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
            mentions = re.findall(r"@(\w+)", content)
            mention_counter.update(mentions)
            line_count += 1

    logger.info(
        f"Procesados {line_count} tweets — {len(mention_counter)} usuarios únicos"
    )
    return mention_counter.most_common(10)
