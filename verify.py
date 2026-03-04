"""Quick verification script for all 6 functions."""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from logger_config import get_logger

logger = get_logger(__name__)

FILE_PATH = os.path.join(
    os.path.dirname(__file__), "farmers-protest-tweets-2021-2-4.json"
)


def verify(label, func, file_path):
    logger.info(f"{'=' * 50}")
    logger.info(f"Running: {label}")
    logger.info(f"{'=' * 50}")
    start = time.time()
    result = func(file_path)
    elapsed = time.time() - start
    logger.info(f"Time: {elapsed:.2f}s")
    logger.info(f"Length: {len(result)}")
    for i, item in enumerate(result):
        logger.info(f"  {i + 1}. {item}")
    assert len(result) == 10, f"Expected 10 results, got {len(result)}"
    return result


if __name__ == "__main__":
    logger.info("TESTING MEMORY-OPTIMIZED FUNCTIONS")

    from q1_memory import q1_memory

    r1m = verify("q1_memory", q1_memory, FILE_PATH)

    from q2_memory import q2_memory

    r2m = verify("q2_memory", q2_memory, FILE_PATH)

    from q3_memory import q3_memory

    r3m = verify("q3_memory", q3_memory, FILE_PATH)

    logger.info("TESTING TIME-OPTIMIZED FUNCTIONS")

    from q1_time import q1_time

    r1t = verify("q1_time", q1_time, FILE_PATH)

    from q2_time import q2_time

    r2t = verify("q2_time", q2_time, FILE_PATH)

    from q3_time import q3_time

    r3t = verify("q3_time", q3_time, FILE_PATH)

    # Compare results
    logger.info("COMPARING RESULTS")

    q1_match = set(r1m) == set(r1t)
    logger.info(f"Q1 match: {q1_match}")
    if not q1_match:
        logger.warning(f"  Memory: {r1m}")
        logger.warning(f"  Time:   {r1t}")

    q2_match = set(r2m) == set(r2t)
    logger.info(f"Q2 match: {q2_match}")
    if not q2_match:
        logger.warning(f"  Memory: {r2m}")
        logger.warning(f"  Time:   {r2t}")

    q3_match = set(r3m) == set(r3t)
    logger.info(f"Q3 match: {q3_match}")
    if not q3_match:
        logger.warning(f"  Memory: {r3m}")
        logger.warning(f"  Time:   {r3t}")

    logger.info("ALL VERIFICATIONS COMPLETE")
