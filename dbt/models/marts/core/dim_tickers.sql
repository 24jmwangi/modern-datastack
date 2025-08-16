{{ config(
    materialized='incremental',
    unique_key='ticker',
    incremental_strategy='merge'
) }}

select
    ticker,
    last_trade_time,
    last_price,
    prev_day_price,
    change_value,
    change_pct,
    volume,
    volume_avg,
    shares
from {{ ref('stg_ticker') }}
