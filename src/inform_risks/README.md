# INFORM dbt project

This project uses dbt to transform data coming from [INFORM Risk](https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk).

The data is stored in a **PostgreSQL** Data Warehouse.

## Contents
* [Workflow](#workflow)
* [Loading the data](#loading-the-data)
* [Visualise Data stored in the DataWarehouse](#visualise-data-stored-in-the-datawarehouse)
* [DataWarehouse layers](#datawarehouse-layers)
* [Develop with dbt](#develop-with-dbt)
    + [Sources in `raw`](#sources-in--raw-)
    + [Staging tables in `stg`](#staging-tables-in--stg-)
    + [Dimensions & Facts tables in `ods`](#dimensions---facts-tables-in--ods-)
    + [Wide tables in `prs`](#wide-tables-in--prs-)
* [Manage the dbt project](#manage-the-dbt-project)
    + [dbt settings](#dbt-settings)
    + [dbt dependencies](#dbt-dependencies)
    + [Generate Sources descriptions `.yaml`](#generate-sources-descriptions-yaml)
    + [(Optional) Describe dbt tables with `.yml` files](#optional-describe-dbt-tables-with-yml-files)
    + [Access Data Catalog](#access-data-catalog)
    
* [Useful Resources:](#useful-resources-)

## Workflow
```mermaid
graph LR

subgraph workflow
    direction LR
    subgraph EL[Extract & Load]
        elscript[extract_load.py]
    end

    subgraph TRANS[Transform]
        dbt[dbt]
    end

    subgraph Ana[Analyze]
        DV[a Data Viz tool]
    end

end

EL --> TRANS --> Ana

subgraph tools
datasource[(Data Source)]
DWH[(DataWarehouse)]
dashboard[Dashbaord]
end

datasource --extract --> EL -- load --> DWH
DWH <--transform--> dbt
DWH --analyze --> dashboard
```

## Loading the data
The data is located in the `source_data` folder. It contains : 
- `inform_trends.parquet` : [Inform Trend 2013-2022](https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk/Results-and-data/moduleId/1782/id/453/controller/Admin/action/Results) converted to `.parquet` format.
- `inform_countries.parquet` [INFORM `/Countries/Index` API endpoint](https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Countries/Index) converted to `.parquet` format.
- `inform_indicators.parquet` [INFORM `/Indicators/Index` API endpoint](https://drmkc.jrc.ec.europa.eu/inform-index/API/InformAPI/Indicators/Index) converted to `.parquet` format.

The data is loaded using a Python script :[`extract_load.py`](/src/extract_load.py). This script will load in the DataWarehouse all `.parqet` & `.csv` files located in the `/source_data` folder.

Once the data is loaded in the DataWarehouse, it is persisted in a volume, so you only need to Extract/Load data when you first initialize this project.

To run the **Extract/Load** script, run
```
python3 /AE_demo/src/extract_load.py
```

## Visualise Data stored in the DataWarehouse
We are using the [PostgreSQL VSCode extension](https://marketplace.visualstudio.com/items?itemName=ckolkman.vscode-postgres) to see tables in the DataWarehouse. To use it you must connect the extension to the database.

The extension will ask you for the following information
- **the hostname of the database** : `postgres`
- **the PostgreSQL user to authenticate as** : `exampleuser`
- **the password of the PostgreSQL user** : `Examplepassword`
- **the port number to connect to** : `5432`
- Use `Standard Connection`
- **database** : `dwh_db`
- Finally, write a display name for this DataWarehouse connection (for example `DWH`)

## DataWarehouse layers

In **dbt** :
- we define raw data in sources `.yml` files 
- we write queries in `.sql` files

When we run dbt, it creates tables in the **DataWarehouse**.

The DataWarehouse is composed of several schemas, mapped to the subfolder structure of the `models` folder.
The schemas/subfolders represent the steps in the transformation workflow :

```mermaid
graph LR
subgraph DataWarehouse
    direction TB
    rawdb[(raw)]
    stgdb[(stg)]
    odsdb[(ods)]
    subgraph prs 
        direction LR
        generaldb[(general)]
        hedb[(hazard_exposure)]
    end
    
end

subgraph dbt
    direction LR
    subgraph sources
    end
    subgraph models
    direction LR
    stg[stg]
    ods[ods]
    prs[prs]
    stg --> ods --> prs
    end
    
    sources --> stg
end 

```

1. **raw** : Where raw data is located. dbt use *raw* tables as *dbt sources* to create *stg* dbt models. See [Sources in `raw`](#sources-in-raw).
2. **stg** : Where data is **st**a**g**ed. We rename and recast sources columns. See [Staging tables in `stg`](#staging-tables-in-stg)
3. **ods** : Where data is transformed into entities (dimensions & facts). See [Dimensions & Facts tables in `ods`](#dimensions--facts-tables-in-ods)
4. **prs** : Where data is unified & ready for analysis. See [Wide tables in `prs`](#wide-tables-in-prs). In fact, there is no `prs` schema in the DataWarehouse but rather multiple ones, dividing data into multiple logical groups :
    - **general**
    - **hazard_exposure**
    - **vulnerability**
    - **lack_of_coping_capacity**


## Develop with dbt

### Sources in `raw`
A `.yml` file must be created in the `/models/raw` folder. It contains a `source` definition, describing a source table in the `raw` schema of the DataWarehouse.

You don't have to write its content, you can  [Generate Sources descriptions `.yaml`](#generate-sources-descriptions-yaml)

### Staging tables in `stg`
Once you defined [Sources in `raw`](#sources-in-raw) :
1. Create a `.sql` file in the `/models/stg` folder. In this file, write a SQL query on a source table in order to **Rename** & **Recast** columns.
2. Run the dbt model to create the table in the Data Warehouse.
3. [(Optional) Describe dbt tables with `.yml` files](#optional-describe-dbt-tables-with-yml-files)

### Dimensions & Facts tables in `ods`
Once you [Staged tables in `stg`](#staging-tables-in-stg) :
1. Create a `.sql` file in the `/models/ods` folder. In this file, write a SQL query on `stg` tables in order to create a functional entity.
2. Run the dbt model to create the table in the Data Warehouse.
3. [(Optional) Describe dbt tables with `.yml` files](#optional-describe-dbt-tables-with-yml-files)

### Wide tables in `prs`
Once you created [Dimensions & Facts tables in `ods`](#dimensions--facts-tables-in-ods) :
1. Create a `.sql` file in the `/models/prs/...` folder (see the 4th points in [DataWarehouse Layers](#datawarehouse-layers)). In this file, write a SQL query on `ods` tables in order to create a Wide table with all information you need from Dimension & Fact tables.
2. Run the dbt model to create the table in the DataWarehouse.
3. [(Optional) Describe dbt tables with `.yml` files](#optional-describe-dbt-tables-with-yml-files)

## Manage the dbt project

### dbt settings
All settings are described in the [`dbt_project.yml`](dbt_project.yml).
A lot of them are set automatically by dbt, except the `Models configuration` section which defines the Materialization (`table`,`view`,...) and the schema (`stg`, `ods`, `prs`) for dbt models depending on their location the `/models` folder.

See [dbt documentation on `dbt_project.yml`](https://docs.getdbt.com/reference/dbt_project.yml)

### dbt dependencies
dbt relies on packages to work (for instance `dbt-codegen` to generate code).
The packages are defined in [`packages.yml`](packages.yml).

To install dbt dependencies, run
```
dbt deps
```

### Generate Sources descriptions `.yaml`
For this to work :
- Make sure the table exists in the Data Warehouse, in the `raw` schema
- Make sure you install [dbt dependencies](#dbt-dependencies)

Run the following code to generate the dbt Source definition of a table *(replace `SOURCE_NAME` by the name of your source table)*
```
dbt run-operation generate_source --args '{"schema_name": "raw", "generate_columns": "true", "include_descriptions":"true", "table_names":["SOURCE__TABLE_NAME"], "name":"inform"}'
```

If you need to merge what has been generated with an existing file, make sure you don't repeat the fields like `version:` and `sources:`

See [dbt documentation on sources](https://docs.getdbt.com/docs/build/sources).

### (Optional) Describe dbt tables with `.yml` files
Run the following code in the terminal to generate the content of the `.yml` file for a table *(replace `TABLE_NAME` by the name of your model)*
```
dbt run-operation generate_model_yaml --args '{"model_names": ["TABLE_NAME"], "upstream_descriptions":"true"}'
```

If you need to merge what has been generated with an existing file, make sure you don't repeat the fields like `version:` and `models:`

See [dbt documentation on Model properties](https://docs.getdbt.com/reference/model-properties)


### Access Data Catalog
1. Generate assets for the website :
```
dbt docs generate
```
2. Run the website server :
```
dbt docs serve
```
3. Access the website with the VSCode pop-up

## Useful Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
