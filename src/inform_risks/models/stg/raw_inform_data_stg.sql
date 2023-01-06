with source as (
      select * from {{ source('inform', 'raw_inform_data') }}
),
renamed as (
    select
        cast("Iso3" as {{ dbt.type_string() }}) as code_pays_iso3,
        cast("INFORMYear" as {{ dbt.type_int() }}) as annee,
        cast("Indicator Type" as {{ dbt.type_string() }}) as type_indicateur,
        cast("IndicatorId" as {{ dbt.type_string() }} ) as id_indicateur,
        cast("IndicatorName" as {{ dbt.type_string() }}) as nom_indicateur,
        cast("IndicatorScore" as {{ dbt.type_numeric() }}) as score_indicateur

    from source
)
select * from renamed