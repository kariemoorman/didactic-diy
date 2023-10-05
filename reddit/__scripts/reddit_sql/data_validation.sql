/* Check for Duplicates in a SQL Table */

SELECT duplicate_column, COUNT(*) AS duplicate_column_count
FROM table_name
GROUP BY duplicate_column
HAVING COUNT(*) > 1;

/* Check for Missing Values */

SELECT *
FROM table_name
WHERE column_name IS NULL;

/* Check for Non-Missing Values */

SELECT *
FROM table_name
WHERE column_name IS NOT NULL;

/* Check for Invalid Data Types */

SELECT *
FROM table_name
WHERE ISNUMERIC(column_name) = 0;

/* Check if Column can be CAST to a Data Type */
/* If there are any rows that fail the conversion, 
   the count will be greater than zero, indicating 
   potential data type issues. */

SELECT COUNT(*)
FROM table_name
WHERE TRY_CAST(column_name AS NUMERIC) IS NULL;

/* Check if Column can be CONVERTed to a Data Type */
/* If there are any rows that fail the conversion, 
   the count will be greater than zero, indicating 
   potential data type issues. */

SELECT COUNT(*)
FROM table_name
WHERE TRY_CONVERT(NUMERIC, column_name) IS NULL;
