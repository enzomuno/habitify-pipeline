SELECT
    area_id,
    name,
    CONVERT_TIMEZONE('UTC', 'America/Sao_Paulo', created_at) AS created_at_brt
FROM {{ ref('stg_areas') }}
