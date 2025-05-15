from dotenv import load_dotenv
import os
import time
import psycopg2
from psycopg2 import OperationalError
import pandas as pd

# cargar variables de entorno
load_dotenv()

# access VE
dbname = os.getenv("DBNAME")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")


def connect_db_with_retry(retries=5, delay=5):

    # Se eligio una base de datos Relacional en este caso Postgresql ya que en este ejercicio se proporciono datos de compañias para facturacion
    # La mayoria de esta data es fija entonces no cambia tanto es una base de datos mas estructurada ya que contiene id relacionales, ademas de que podemos hacer consultas mas complejas
    # Las peticiones a estas bases de datos tambien es mas intermitente y para bases de bigdata o no relacionales las cosultas son mas constantes

    attempt = 0
    while attempt < retries:
        try:
            print(f"Intentando conectar a la DB (intento {attempt + 1}/{retries})...")
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host="db",
                port=port,
            )
            print("✅ Conexión exitosa a la base de datos.")
            return conn
        except OperationalError as e:
            print(f"❌ Error de conexión: {e}")
            attempt += 1
            time.sleep(delay)

    raise Exception(
        "🚫 No se pudo conectar a la base de datos después de varios intentos."
    )


def insert_data(df):

    df = df.where(pd.notnull(df), None)

    con = connect_db_with_retry()
    cursor = con.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO companies (id, name) VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING
            """,
            (row["company_id"], row["name"]),
        )

        cursor.execute(
            """
            INSERT INTO charges (id, company_id, amount, status, created_at, paid_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                row["id"],
                row["company_id"],
                row["amount"],
                row["status"],
                row["created_at"],
                row["paid_at"],
            ),
        )

    con.commit()
    cursor.close()
    con.close()


def main():
    df = pd.read_csv("data/transformado.csv")
    insert_data(df)


if __name__ == "__main__":
    main()
