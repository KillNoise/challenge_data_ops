-- Q3: Top 10 most mentioned users (@username)
--
-- Strategy:
-- 1. Extract all @mentions from tweet content using regex
-- 2. UNNEST to get individual mentions
-- 3. Count and rank

WITH extracted_mentions AS (
  SELECT
    mention
  FROM `{PROJECT_ID}.challenge_data_ops.tweets`,
  UNNEST(
    REGEXP_EXTRACT_ALL(content, r'@(\w+)')
  ) AS mention
)

SELECT
  mention AS username,
  COUNT(*) AS count
FROM extracted_mentions
GROUP BY mention
ORDER BY count DESC
LIMIT 10;
