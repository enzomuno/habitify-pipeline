-- Importando dados raw
WITH raw_areas AS (
    SELECT
        raw AS raw
    FROM {{ source('raw', 'areas') }}
),

-- Processando os dados
processed AS (
    SELECT 
        raw:id::string AS area_id,
        raw:name::string AS name,
        raw:color::string AS color,
        raw:priority::string AS priority,
        raw:createdAt::timestamp AS created_at
    FROM raw_areas
)

-- Seleção final
SELECT 
    *
FROM processed
