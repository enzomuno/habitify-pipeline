select
    habit_id,
    unit_type,
    periodicity,
    target_value,
    current_value,
    status,
    CONVERT_TIMEZONE('UTC', 'America/Sao_Paulo', reference_date) AS reference_date_brt
from {{ ref('stg_journal') }}