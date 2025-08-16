with all_stocks as (

    select 'aapl' as ticker, * from {{ source('silver','aapl') }}
    union all
    select 'amzn', * from {{ source('silver','amzn') }}
    union all
    select 'snow', * from {{ source('silver','snow') }}
    union all
    select 'tsla', * from {{ source('silver','tsla') }}
    union all
    select 'meta', * from {{ source('silver','meta') }}
    union all
    select 'msft', * from {{ source('silver','msft') }}
    union all
    select 'goog', * from {{ source('silver','goog') }}
    union all
    select 'nvda', * from {{ source('silver','nvda') }}

)

select distinct      -- remove accidental duplicates
    ticker,
    cast(date as date) as trade_date,
    safe_cast(open as float64) as open_price,
    safe_cast(high as float64) as high_price,
    safe_cast(low as float64) as low_price,
    safe_cast(close as float64) as close_price,
    safe_cast(volume as int64) as volume
from all_stocks
where date is not null
