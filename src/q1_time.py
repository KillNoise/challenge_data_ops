"""
Q1 - Top 10 dates with most tweets (TIME optimized)

Strategy:
- Read entire file at once into memory (fast bulk I/O).
- Parse each line with orjson (Rust-based parser, ~5x faster than json stdlib).
- Use Counter for fast aggregation.
- Prioritizes speed over memory usage.

Difference vs q1_memory:
- orjson vs json stdlib (faster parser)
- Bulk read vs streaming (faster I/O)
"""

from typing import List, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import orjson
from logger_config import get_logger

logger = get_logger(__name__)


def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    logger.info("Starting q1_time -- bulk read + orjson")

    # Read entire file at once (faster than line-by-line)
    with open(file_path, "rb") as f:
        raw_lines = f.readlines()

    logger.info(f"Read {len(raw_lines)} lines in bulk")

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

    # Top 10 dates
    top_dates = date_counts.most_common(10)

    result = []
    for date_str, _ in top_dates:
        top_user = date_user_counts[date_str].most_common(1)[0][0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        result.append((date_obj, top_user))

    logger.info(f"q1_time completed -- {len(result)} results")
    return result
