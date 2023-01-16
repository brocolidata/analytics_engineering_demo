with source as (
      select * from {{ source('inform', 'inform_countries') }}
),
renamed as (
    select
        cast("CategoryType" as {{ dbt.type_string() }}) as type_zone_geographique,
        cast("Iso3" as {{ dbt.type_string() }}) as code_iso3,
        cast("CountryName" as {{ dbt.type_string() }}) as nom_zone_geo,
        cast("IsoGroup" as {{ dbt.type_string() }}) as parent_zone_geo

    from source
)
select * from renamed
