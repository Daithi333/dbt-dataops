{{ config(schema='silver') }}

select * from {{ ref('trip_data_bronze') }}
