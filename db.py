import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host = os.environ.get("DB_HOST", "localhost"),
        user = "root",
        password = os.environ.get("DB_PASSWORD"),
        database = "web_data",
    )

def insert_events(events: list[dict]):
    sql = """
        INSERT INTO events (created_at, user_id, event_type, page_name, purchase, error_code)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    rows = [
        (
            e["created_at"],
            e["user_id"],
            e["event_type"],
            e.get("page"),
            e.get("purchase"),
            e.get("code"),
        )
        for e in events
    ]

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(sql, rows)
        conn.commit()
    print(f"DB에 {len(rows)}개의 이벤트 저장 완료!")
