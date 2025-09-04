{{ config(schema='silver') }}
-- upper case address
-- cast total_spend to decimal
-- match the address to a city from the cities table
-- remove rows with no address
-- use OTHER when no match for city
SELECT
    company_id,
    cast(total_spend AS decimal) AS total_spend,
    upper(address) AS address,
    coalesce(
        (
            SELECT city FROM {{ ref('cities_silver') }}
            WHERE upper(address) LIKE '%' || chr(10) || city || ',%'
            ORDER BY city DESC LIMIT 1
        ),
        'OTHER'
    ) AS city
FROM {{ ref('addresses_bronze') }}
WHERE address IS NOT null
