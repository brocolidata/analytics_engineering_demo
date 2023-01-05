import os
import pandas as pd
import sqlalchemy

def get_database_engine():
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    database_url = f"postgresql+psycopg2://{db_user}:{db_password}@postgres:5432/{db_name}"
    engine = sqlalchemy.create_engine(database_url)
    return engine

def create_schema(schema="raw"):
    engine = get_database_engine()
    with engine.connect() as con:
        rs = con.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')


def extract_load():

    df = pd.read_parquet('/source_data/inform_trends.parquet')
    df = df[df.columns.difference(["surveyyear"])]
    engine = get_database_engine()
    df.to_sql(
        name="raw_inform_data",
        con=engine,
        schema="raw",
        index=0
    )
    print('successfully loaded INFORM data in DWH')


if __name__ == '__main__':
    create_schema()
    print('"raw" schema created or already existing')
    extract_load()