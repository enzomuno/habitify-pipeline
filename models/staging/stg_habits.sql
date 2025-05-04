-- Importando dados raw
with source as (
    select
        raw AS raw
    from {{ source('raw', 'habits') }}
),

-- Processando os dados
processed AS (
    select
        raw:"id"::string as habit_id,
        raw:"name"::string as habit_name,
        raw:"is_archived"::boolean as is_archived,
        raw:"start_date"::timestamp as start_date,
        raw:"created_date"::timestamp as created_date,
        raw:"log_method"::string as log_method,
        raw:"recurrence"::string as recurrence,
        raw:"priority"::float as priority,
        raw:"area":"id"::string as area_id,
        raw:"time_of_day" AS time_of_day,
        raw:"remind" AS remind,
        -- goal fields
        raw:"goal":"unit_type"::string as goal_unit_type,
        raw:"goal":"value"::float as goal_value,
        raw:"goal":"periodicity"::string as goal_periodicity

    from source
)



-- Seleção final
select
    *
from processed
