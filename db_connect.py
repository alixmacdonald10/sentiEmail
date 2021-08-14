import os
import psycopg2
import urllib.parse as urlparse
from sqlalchemy import create_engine
import pandas as pd


def read_vars():
    # # load in the dotenv file LOCAL ONLY
    # dotenv_file = dotenv.find_dotenv()
    # dotenv.load_dotenv(dotenv_file)

    env_var = os.environ
    # get data from a .env file thats in .gitignore (for privacy - this hides the personal access token and path)
    USER = env_var['USER']
    # USER = os.getenv("USER")
    # access to token generated from github
    # PASSWORD = os.getenv("PASSWORD")
    PASSWORD = env_var['PASSWORD']
    # database name
    # DB_NAME = os.getenv("DBNAME")
    DB_NAME = env_var['DBNAME']
    # port
    # PORT = os.getenv("PORT")
    PORT = env_var['PORT']
    # host
    # HOST = os.getenv("HOST")
    HOST = env_var['HOST']
    # DATABASE URL
    DATABASE_URL = env_var['DATABASE_URL']
    return USER, PASSWORD, DB_NAME, PORT, HOST, DATABASE_URL


def connect(table_name):
    
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
            )
    # establish connection
    sql = f"SELECT * FROM {table_name};"
    df = pd.read_sql_query(sql, conn)
    conn.close()
    
    return df


def append_email(table_name, df):
    
    URL = urlparse.urlparse(os.environ['DATABASE_URL'])
    DBNAME = URL.path[1:]
    USER = URL.username
    PASSWORD = URL.password
    HOST = URL.hostname
    PORT = URL.port
    # establish connection
    DATABASE_URL = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
    conn = create_engine(DATABASE_URL)
    pd.DataFrame.to_sql(self=df, name=table_name, con=conn, if_exists='append', index=False)
    # connection.close() FIGURE OUT HOW TO CLOSE
