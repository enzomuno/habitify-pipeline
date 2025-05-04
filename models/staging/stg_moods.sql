-- Importando dados raw
WITH raw_moods AS (
    SELECT
        raw AS raw
    FROM {{ source('raw', 'moods') }}
),

-- Processando os dados
processed AS (
    SELECT 
        raw:id::string AS moods_id,
        raw:created_at::timestamp AS created_at,
        raw:value::int AS value
    FROM raw_moods
)

-- Seleção final
SELECT 
    *
FROM processed
