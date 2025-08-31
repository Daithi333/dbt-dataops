{{ config(schema='silver')}}
select * FROM {{ ref('trip_data_bronze') }}
