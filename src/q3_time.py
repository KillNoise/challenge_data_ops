"""
Q3 - Top 10 most mentioned users (TIME optimized)

Strategy:
- Read entire file at once into memory (fast bulk I/O).
- Parse each line with orjson (Rust-based parser, ~5x faster than json stdlib).
- Extract mentions with pre-compiled regex.
- Prioritizes speed over memory usage.

Difference vs q3_memory:
- orjson vs json stdlib (faster parser)
- Bulk read vs streaming (faster I/O)
- Pre-compiled regex for max speed
"""

from typing import List, Tuple
from collections import Counter
import re
import orjson
from logger_config import get_logger

logger = get_logger(__name__)

# Pre-compile regex outside the function for max performance
MENTION_PATTERN = re.compile(r"@(\w+)")


def q3_time(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Starting q3_time -- bulk read + orjson")

    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Read {len(raw_lines)} lines in bulk")

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

    logger.info(f"q3_time completed -- {len(mention_counter)} unique users mentioned")
    return mention_counter.most_common(10)
