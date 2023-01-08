with inform_trends_stg as (
      select * from {{ ref('inform_trends_stg') }}
),


risk_index_fct as (
    select
        code_iso3,
        annee,
        type_indicateur,
        id_indicateur,
        nom_indicateur,
        score_indicateur
    from inform_trends_stg
    where id_indicateur = 'INFORM'
)
select * from risk_index_fct
