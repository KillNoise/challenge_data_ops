"""
Q2 - Top 10 most used emojis (TIME optimized)

Strategy:
- Read entire file at once into memory (fast bulk I/O).
- Parse each line with orjson (Rust-based parser, ~5x faster than json stdlib).
- Extract emojis using emoji.emoji_list().
- Prioritizes speed over memory usage.

Difference vs q2_memory:
- orjson vs json stdlib (faster parser)
- Bulk read vs streaming (faster I/O)
"""

from typing import List, Tuple
from collections import Counter
import orjson
import emoji
from logger_config import get_logger

logger = get_logger(__name__)


def q2_time(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Starting q2_time -- bulk read + orjson")

    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Read {len(raw_lines)} lines in bulk")

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

    logger.info(f"q2_time completed -- {len(emoji_counter)} unique emojis found")
    return emoji_counter.most_common(10)
