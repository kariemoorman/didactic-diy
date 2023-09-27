-- Calculate 90th Percentile Trimmed Mean
WITH trimmed_data AS (
  SELECT
    value
  FROM
    dataset
  WHERE
    value >= PERCENTILE_CONT(0.05) WITHIN GROUP (ORDER BY value)
      AND value <= PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY value)
)
SELECT
  AVG(value) AS trimmed_mean
FROM
  trimmed_data;

-- Calculate 95th Percentile Trimmed Mean
WITH trimmed_data AS (
  SELECT
    value
  FROM
    dataset
  WHERE
    value >= PERCENTILE_CONT(0.025) WITHIN GROUP (ORDER BY value)
      AND value <= PERCENTILE_CONT(0.975) WITHIN GROUP (ORDER BY value)
)
SELECT
  AVG(value) AS trimmed_mean
FROM
  trimmed_data;


-- Calculate 99th Percentile Trimmed Mean
WITH trimmed_data AS (
  SELECT
    value
  FROM
    dataset
  WHERE
    value >= PERCENTILE_CONT(0.005) WITHIN GROUP (ORDER BY value)
      AND value <= PERCENTILE_CONT(0.995) WITHIN GROUP (ORDER BY value)
)
SELECT
  AVG(value) AS trimmed_mean
FROM
  trimmed_data;




