with risk_index_fct as (
      select * from {{ ref('risk_index_fct') }}
),

pays_dim as (
      select * from {{ ref('pays_dim') }}
),

risk_index as (
    select
        code_iso3,
        annee,
        type_indicateur,
        id_indicateur,
        nom_indicateur,
        score_indicateur,
        nom_zone_geo,
        parent_zone_geo
    from risk_index_fct
    join pays_dim using (code_iso3)
)
select * from risk_index
