# INFORM dbt project

This project uses dbt to transform data coming from [INFORM Risk](https://drmkc.jrc.ec.europa.eu/inform-index/INFORM-Risk).

The data is stored in a **Postgres** Data Warehouse.


## Loading the data
The data is located in the `inform_trends.parquet` file. The data in this file is loaded using a Python script. 

The data in the DataWarehouse is persisted in a volume, so you only need to Extract/Load data when you first initialize this project.

To run the **Extract/Load** script, run
```
python3 /scripts/extract_load.py
```

## DataWarehouse layers

The DataWarehouse is composed of several schemas :
- **raw** : Where the raw data is located. dbt use *raw* tables as *dbt sources* to create *stg* dbt models.
- **stg** : Where the data is **st**a**g**ed. We rename and recast sources columns.
- **ods** : Where the data is transformed into entities (dimensions & facts).
- Finally we create multiple schemas for analysis purposes : 
    - **general**
    - **hazard_exposure**
    - **vulnerability**
    - **lack_of_coping_capacity**


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)