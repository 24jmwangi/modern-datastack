{{ config(
    materialized='incremental',
    unique_key='ticker_trade_date',
    incremental_strategy='merge'
) }}

select
    ticker,
    trade_date,
    concat(ticker, '_', cast(trade_date as string)) as ticker_trade_date, -- surrogate PK
    open_price,
    high_price,
    low_price,
    close_price,
    volume
from {{ ref('stg_stocks') }}

{% if is_incremental() %}
  where trade_date > (select max(trade_date) from {{ this }})
{% endif %}
