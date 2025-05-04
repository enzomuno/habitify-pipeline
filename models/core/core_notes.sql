select
    note_id,
    content,
    created_date,
    habit_id
from {{ ref('stg_notes') }}