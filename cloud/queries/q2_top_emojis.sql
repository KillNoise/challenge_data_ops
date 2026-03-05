-- Q2: Top 10 most used emojis
--
-- Strategy:
-- 1. Extract emoji characters from tweet content using Unicode regex ranges
-- 2. UNNEST the array to get individual emojis
-- 3. Count and rank top 10
--
-- Note: Covers most common emoji Unicode blocks (emoticons, symbols,
-- transport, flags, supplemental). Some compound emojis (e.g. skin
-- tone modifiers, ZWJ sequences) may be split into individual codepoints.

WITH extracted_emojis AS (
  SELECT
    emoji
  FROM `{PROJECT_ID}.challenge_data_ops.tweets`,
  UNNEST(
    REGEXP_EXTRACT_ALL(
      content,
      r'[\x{1F600}-\x{1F64F}]|[\x{1F300}-\x{1F5FF}]|[\x{1F680}-\x{1F6FF}]|[\x{1F1E0}-\x{1F1FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F900}-\x{1F9FF}]|[\x{1FA00}-\x{1FA6F}]|[\x{1FA70}-\x{1FAFF}]|[\x{2B50}]|[\x{2B55}]|[\x{23F0}-\x{23FA}]|[\x{25AA}-\x{25FE}]'
    )
  ) AS emoji
)

SELECT
  emoji,
  COUNT(*) AS count
FROM extracted_emojis
GROUP BY emoji
ORDER BY count DESC
LIMIT 10;
