with inform_countries_stg as (
      select * from {{ ref('inform_countries_stg') }}
),


pays_dim as (
    select
        code_iso3,
        nom_zone_geo,
        parent_zone_geo
    from inform_countries_stg
    where type_zone_geo = 'ADMIN0'
)
select * from pays_dim
