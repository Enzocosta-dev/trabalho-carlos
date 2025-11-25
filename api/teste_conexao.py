from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("bc.env")

DATABASE_URL = os.getenv("DATABASE_URL")
print("Tentando conectar ao banco...")

try:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    print("Conexão bem sucedida!")
    conn.close()
except Exception as e:
    print("Erro ao conectar:", e)
