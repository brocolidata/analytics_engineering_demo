with source as (
      select * from {{ source('inform', 'raw_inform_data') }}
),
renamed as (
    select
        "Iso3" as code_pays_iso3,
        "INFORMYear" as annee,
        "Indicator Type" as type_indicateur,
        "IndicatorId" as id_indicateur,
        "IndicatorName" as nom_indicateur,
        "IndicatorScore" as score_indicateur

    from source
)
select * from renamed