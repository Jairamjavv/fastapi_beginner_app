import psycopg2
from psycopg2.extras import RealDictCursor
from db_secrets import DbCredentials


def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DbCredentials.HOST.value,
            database=DbCredentials.DATABASE.value,
            user=DbCredentials.USERNAME.value,
            password=DbCredentials.PASSWORD.value,
            cursor_factory=RealDictCursor,  # uses python like dictionary to retrieve values instead of tuples
        )
        yield conn
    except Exception as error:
        print("Database connection Failed." + str(error))
