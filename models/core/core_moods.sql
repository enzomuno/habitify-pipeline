select
    moods_id,
    CONVERT_TIMEZONE('UTC', 'America/Sao_Paulo', created_at) AS created_at_brt,
    value
from {{ ref('stg_moods') }}