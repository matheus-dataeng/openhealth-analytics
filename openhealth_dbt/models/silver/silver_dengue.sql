SELECT 
    CAST("DT_NOTIFIC" AS DATE) as data_notificacao,
    CAST("DT_SIN_PRI" AS DATE) as data_primeiros_sintomas,
CASE
    WHEN "SG_UF" = 11 THEN 'RO'
    WHEN "SG_UF" = 12 THEN 'AC'
    WHEN "SG_UF" = 13 THEN 'AM'
    WHEN "SG_UF" = 14 THEN 'RR'
    WHEN "SG_UF" = 15 THEN 'PA'
    WHEN "SG_UF" = 16 THEN 'AP'
    WHEN "SG_UF" = 17 THEN 'TO'
    WHEN "SG_UF" = 21 THEN 'MA'
    WHEN "SG_UF" = 22 THEN 'PI'
    WHEN "SG_UF" = 23 THEN 'CE'
    WHEN "SG_UF" = 24 THEN 'RN'
    WHEN "SG_UF" = 25 THEN 'PB'
    WHEN "SG_UF" = 26 THEN 'PE'
    WHEN "SG_UF" = 27 THEN 'AL'
    WHEN "SG_UF" = 28 THEN 'SE'
    WHEN "SG_UF" = 29 THEN 'BA'
    WHEN "SG_UF" = 31 THEN 'MG'
    WHEN "SG_UF" = 32 THEN 'ES'
    WHEN "SG_UF" = 33 THEN 'RJ'
    WHEN "SG_UF" = 35 THEN 'SP'
    WHEN "SG_UF" = 41 THEN 'PR'
    WHEN "SG_UF" = 42 THEN 'SC'
    WHEN "SG_UF" = 43 THEN 'RS'
    WHEN "SG_UF" = 50 THEN 'MS'
    WHEN "SG_UF" = 51 THEN 'MT'
    WHEN "SG_UF" = 52 THEN 'GO'
    WHEN "SG_UF" = 53 THEN 'DF'
END AS uf,
"ID_MN_RESI" AS cod_municipio_residencia,
CASE
    WHEN "NU_IDADE_N" BETWEEN 4000 AND 4009 THEN '0-9 anos'
    WHEN "NU_IDADE_N" BETWEEN 4010 AND 4019 THEN '10-19 anos'
    WHEN "NU_IDADE_N" BETWEEN 4020 AND 4039 THEN '20-39 anos'
    WHEN "NU_IDADE_N" BETWEEN 4040 AND 4059 THEN '40-59 anos'
    WHEN "NU_IDADE_N" >= 4060 THEN '60+ anos'
    ELSE 'menor que 1 ano'
END AS faixa_etaria,
CASE
    WHEN "CS_SEXO" = 'F' THEN 'feminino'
    WHEN "CS_SEXO" = 'M' THEN 'masculino'
    WHEN "CS_SEXO" = 'I' THEN 'ignorado'
    ELSE 'sexo_nao_informado'
END AS sexo,
CASE
    WHEN "CS_GESTANT" = 1 THEN '1º trimestre'
    WHEN "CS_GESTANT" = 2 THEN '2º trimestre'
    WHEN "CS_GESTANT" = 3 THEN '3º trimestre'
    WHEN "CS_GESTANT" = 4 THEN 'idade_gestacional_ignorada'
    WHEN "CS_GESTANT" = 5 THEN 'nao'
    WHEN "CS_GESTANT" = 6 THEN 'nao_se_aplica'
    WHEN "CS_GESTANT" = 9 THEN 'ignorado'
    ELSE 'nao_informado'
END AS gestante,
CASE
    WHEN "CS_RACA" = 1 THEN 'branca'
    WHEN "CS_RACA" = 2 THEN 'preta'
    WHEN "CS_RACA" = 3 THEN 'amarela'
    WHEN "CS_RACA" = 4 THEN 'parda'
    WHEN "CS_RACA" = 5 THEN 'indígena'
    WHEN "CS_RACA" = 9 THEN 'ignorado'
    ELSE 'nao_informado'
END AS raca,
CASE
    WHEN "CLASSI_FIN" = 10 THEN 'dengue'
    WHEN "CLASSI_FIN" = 11 THEN 'dengue com sinais de alarme'
    WHEN "CLASSI_FIN" = 12 THEN 'dengue grave'
    WHEN "CLASSI_FIN" = 8 THEN 'descartado'
    WHEN "CLASSI_FIN" = 0 THEN 'ignorado'
    ELSE 'nao informado'
END AS classificacao_final,
CASE
    WHEN "EVOLUCAO" = 1 THEN 'cura'
    WHEN "EVOLUCAO" = 2 THEN 'obito por dengue'
    WHEN "EVOLUCAO" = 3 THEN 'obito por outras causas'
    WHEN "EVOLUCAO" = 4 THEN 'obito em investigação'
    WHEN "EVOLUCAO" = 9 THEN 'ignorado'
    WHEN "EVOLUCAO" = 0 THEN 'em branco'
    ELSE 'nao informado'
END AS evolucao,
CASE
    WHEN "FEBRE" = 1 THEN 'sim'
    WHEN "FEBRE" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS febre,
CASE
    WHEN "MIALGIA" = 1 THEN 'sim'
    WHEN "MIALGIA" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS mialgia,
CASE
    WHEN "EXANTEMA" = 1 THEN 'sim'
    WHEN "EXANTEMA" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS exantema,
CASE
    WHEN "CEFALEIA" = 1 THEN 'sim'
    WHEN "CEFALEIA" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS cefaleia,
CASE
    WHEN "VOMITO" = 1 THEN 'sim'
    WHEN "VOMITO" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS vomito,
CASE
    WHEN "NAUSEA" = 1 THEN 'sim'
    WHEN "NAUSEA" = 2 THEN 'nao'
    ELSE 'nao informado'
END AS nausea
FROM {{ ref('stg_raw_dengue') }}