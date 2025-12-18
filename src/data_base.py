import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def get_engine(user, password, server, database, driver='ODBC Driver 18 for SQL Server'):
    
    password = quote_plus(password)
    driver = quote_plus(driver)

    sql = (
        f'mssql+pyodbc://{user}:{password}@{server}/{database}'
        f'?driver={driver}&Encrypt=yes&TrustServerCertificate=yes'
    )
    return create_engine(sql)

def q(engine, sql):
    return pd.read_sql(sql, engine)

