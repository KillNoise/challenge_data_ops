"""
Q2 - Top 10 most used emojis (MEMORY optimized)

Strategy:
- Read file line by line (streaming).
- Extract emojis from each content with emoji.emoji_list().
- Accumulate in a single Counter (low memory usage).

Assumptions:
- Standard Unicode emojis are used.
- Each emoji occurrence counts individually.
"""

from typing import List, Tuple
from collections import Counter
import json
import emoji
from logger_config import get_logger

logger = get_logger(__name__)


def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Starting q2_memory -- streaming read")
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

    logger.info(f"Processed {line_count} tweets -- {len(emoji_counter)} unique emojis")
    return emoji_counter.most_common(10)
