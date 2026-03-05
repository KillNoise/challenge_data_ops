"""
Q1 - Top 10 dates with most tweets (MEMORY optimized)

Strategy:
- Read file line by line (streaming) to avoid loading everything into RAM.
- Use Counter to count tweets per date.
- Use defaultdict(Counter) to count tweets per (date, user).
- Only counters are kept in memory, not the full tweets.

Assumptions:
- File is JSON Lines (one JSON object per line).
- The "date" field contains an ISO 8601 string; we take the first 10 chars.
- The "user" field is a dict with a "username" key.
"""

from typing import List, Tuple
from datetime import datetime
from collections import Counter, defaultdict
import json
from logger_config import get_logger

logger = get_logger(__name__)


def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    logger.info("Starting q1_memory -- streaming read")
    date_counts: Counter = Counter()
    date_user_counts: dict[str, Counter] = defaultdict(Counter)
    line_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tweet = json.loads(line)
            # Extract date (YYYY-MM-DD) directly from string to avoid
            # the overhead of parsing the full datetime
            date_str = tweet["date"][:10]
            username = tweet["user"]["username"]

            date_counts[date_str] += 1
            date_user_counts[date_str][username] += 1
            line_count += 1

    logger.info(f"Processed {line_count} tweets via streaming")

    # Top 10 dates
    top_dates = date_counts.most_common(10)

    result = []
    for date_str, _ in top_dates:
        top_user = date_user_counts[date_str].most_common(1)[0][0]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        result.append((date_obj, top_user))

    logger.info(f"q1_memory completed -- {len(result)} results")
    return result
