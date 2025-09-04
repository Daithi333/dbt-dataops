{{ config(schema='silver') }}
-- trim and uppercase city
-- remove '*'
-- remove rows where city is empty
-- remove rows where city is in specified list
SELECT DISTINCT
    trim(upper(
        replace(city, '*', '')
    )) AS city
FROM {{ ref('cities_bronze') }}
WHERE
    city IS NOT null
    AND NOT city IN ('England', 'Scotland', 'Wales', 'Northern Ireland')
