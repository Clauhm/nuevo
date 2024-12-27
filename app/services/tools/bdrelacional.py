from pandasai.connectors import PostgreSQLConnector
from pandasai import SmartDataframe
from langchain_core.tools import tool
from config.settings import settings
import os

os.environ["PANDASAI_API_KEY"] = settings.pandasai_api_key
#os.environ["PANDASAI_API_KEY"] = "$2a$10$KdISWjGwmCdSlk/3DngSx.x828Gl/VkunVziuYdu/fVFzVSuF.mOu"

postgres_connector_bd = PostgreSQLConnector(
    config={
        "host": "db",
        "port": 5432,
        "database": "data_bank",
        "username": "postgres",
        "password": "12345678",
        "table": "accounts"
        }
)

df = SmartDataframe(postgres_connector_bd)

@tool
def get_query_database(consulta: str) -> int:
    """Use this tool to query bank transactions, withdrawals, deposits, and balances in a DataFrame.
           The query is processed using Pandas AI to analyze the data and return an answer based on 
           the available information."""
    try: 
            result = df.chat(consulta) # Procesa la consulta utilizando el SmartDataframe
            return result
    except Exception as e:
            print(f"Error al ejecutar la consulta: {e}") # Manejo de errores
            return None

#response = get_query_database.invoke("Cuánto se depositó en junio de 2017 en el numero de cuenta 409000611074")
#print(response)
