"""
Q3 - Top 10 most mentioned users (MEMORY optimized)

Strategy:
- Read file line by line (streaming).
- Extract mentions with regex @(\\w+) from the content field.
- Accumulate in a single Counter (low memory usage).

Assumptions:
- Mentions follow the @username format in the tweet content.
- Regex is used on content for maximum efficiency.
"""

from typing import List, Tuple
from collections import Counter
import json
import re
from logger_config import get_logger

logger = get_logger(__name__)


def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    logger.info("Starting q3_memory -- streaming read")
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

    logger.info(f"Processed {line_count} tweets -- {len(mention_counter)} unique users")
    return mention_counter.most_common(10)
