SELECT
    LPAD(CAST(CAST("COD. UF" AS INT) AS TEXT), 2, '0') ||
    LPAD(CAST("COD. MUNIC" AS TEXT), 5, '0') AS cod_municipio,

    "UF" AS uf,
    "NOME DO MUNICÍPIO" AS nome_municipio,
    CAST("POPULAÇÃO ESTIMADA" AS INTEGER) AS populacao

FROM {{ ref('stg_raw_populacao') }}

WHERE
    "COD. UF" IS NOT NULL
    AND "COD. MUNIC" IS NOT NULL
    AND "POPULAÇÃO ESTIMADA" IS NOT NULL