import os
import pandas as pd
import sqlalchemy
import pathlib
from tqdm import tqdm

def get_database_engine():
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@postgres:5432/{db_name}"
    engine = sqlalchemy.create_engine(database_url)
    return engine

def create_schema(engine, schema="raw"):
    query = sqlalchemy.text(f'CREATE SCHEMA IF NOT EXISTS {schema}')
    with engine.begin() as con:
        rs = con.execute(query)


def extract_load(engine, file_to_load):
    if file_to_load.suffix.endswith('.parquet'):
        df = pd.read_parquet(file_to_load)
    elif file_to_load.suffix.endswith('.csv'):
        df = pd.read_csv(file_to_load)
    else:
        raise ValueError('This script only supports .csv and .parquet files')
    table_name = pathlib.Path(file_to_load).stem
    df.to_sql(
        name=table_name,
        con=engine,
        schema="raw",
        index=0,
        if_exists="replace"
    )


def get_files_to_EL(data_folder="/source_data"):
    ls_files = []
    for data_file in os.listdir('/source_data'):
        file_path = pathlib.Path(data_folder, data_file)
        ls_files.append(file_path)
    return ls_files
    



if __name__ == '__main__':
    engine = get_database_engine()
    create_schema(engine)
    files_to_load = get_files_to_EL()
    files_iterator = tqdm(files_to_load)
    for file_to_load in files_iterator:
        files_iterator.set_description(f'Loading {file_to_load.stem} ..')
        extract_load(engine, file_to_load)