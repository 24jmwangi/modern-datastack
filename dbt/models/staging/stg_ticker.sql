select distinct
    symbol_name as ticker,
    parse_timestamp('%Y-%m-%d %H:%M:%S', last_trade_time) as last_trade_time,
    safe_cast(last_price as float64) as last_price,
    safe_cast(previous_day_price as float64) as prev_day_price,
    safe_cast(change as float64) as change_value,
    safe_cast(change_pct as float64) as change_pct,
    safe_cast(volume as int64) as volume,
    safe_cast(volume_avg as int64) as volume_avg,
    safe_cast(shares as int64) as shares
from {{ source('silver','ticker') }}
where symbol_name is not null
