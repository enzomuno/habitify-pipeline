-- Importando dados raw
with source as (
    select
        raw AS raw
    from {{ source('raw', 'journal') }}
),

-- Processando os dados
processed AS (
    select
        raw:"id"::string as habit_id,
        raw:"progress"::variant:"unit_type"::VARCHAR(15)           AS unit_type,
        raw:"progress"::variant:"periodicity"::VARCHAR(15)         AS periodicity,
        (raw:"progress"::variant:"target_value")::numeric          AS target_value,
        (raw:"progress"::variant:"current_value")::numeric         AS current_value,
        raw:"progress"::variant:"reference_date"                   AS reference_date
    from source
)

-- Seleção final
select
    *
from processed
