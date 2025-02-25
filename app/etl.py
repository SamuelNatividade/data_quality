import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

import os 

def load_settings():
    """Carrega as configurações a partir de variáveis de ambiente."""
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }
    return settings


def extrair_do_sql(query: str) -> pd.DataFrame:
    """Extrai os dados de um banco de dados SQL."""
    settings = load_settings()
    ## criar string de conexao do banco 
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
        df = pd.read_sql(query, conn)

    return pd.read_sql(query, engine)
