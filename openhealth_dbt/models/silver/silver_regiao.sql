SELECT
    id AS cod_municipio,
    nome AS nome_municipio,
    "microrregiao.mesorregiao.UF.sigla" AS uf,
    "microrregiao.mesorregiao.UF.nome" AS nome_estado,
    LOWER("microrregiao.mesorregiao.UF.regiao.nome") AS regiao
FROM {{ ref('stg_raw_regiao') }}