select
    habit_id,
    habit_name,
    is_archived,
    CONVERT_TIMEZONE('UTC', 'America/Sao_Paulo', start_date) AS start_date_brt,
    area_id,
    goal_unit_type,
    goal_value,
    goal_periodicity,
from {{ ref('stg_habits') }}