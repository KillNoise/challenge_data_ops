-- Q1: Top 10 dates with most tweets and most active user per date
--
-- Strategy:
-- 1. Extract date and username from each tweet
-- 2. Count tweets per (date, user)
-- 3. Use window functions to get date totals and rank users
-- 4. Pick the top user per date

WITH base AS (
  SELECT
    DATE(date) AS tweet_date,
    user.username AS username
  FROM `{PROJECT_ID}.challenge_data_ops.tweets`
),

date_user AS (
  SELECT
    tweet_date,
    username,
    COUNT(*) AS user_cnt
  FROM base
  GROUP BY tweet_date, username
),

ranked AS (
  SELECT
    tweet_date,
    username,
    user_cnt,
    SUM(user_cnt) OVER (PARTITION BY tweet_date) AS date_total,
    ROW_NUMBER() OVER (PARTITION BY tweet_date ORDER BY user_cnt DESC) AS rn
  FROM date_user
)

SELECT
  tweet_date,
  username,
  date_total
FROM ranked
WHERE rn = 1
ORDER BY date_total DESC
LIMIT 10;
