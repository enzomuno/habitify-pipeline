-- Importando dados raw
WITH source AS (
    SELECT
        raw AS raw
    FROM {{ source('raw', 'notes') }}
),

-- Processando os dados
processed AS (
    SELECT 
        raw:id::string AS note_id,
        raw:content::string AS content,
        raw:created_date::timestamp AS created_date,
        raw:note_type::int AS note_type,
        raw:habit_id::string AS habit_id
    FROM source
)

-- Seleção final
SELECT 
    *
FROM processed
