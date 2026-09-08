import os
import psycopg2
from psycopg2.extras import Json

PG_CONFIG = {
    # "host": os.getenv("PG_HOST", "mcpmvp-postgres"),
    "host": os.getenv("PG_HOST", "localhost"),
    "port": os.getenv("PG_PORT", "5432"),
    "dbname": os.getenv("PG_DB", "mcpmvp_logs"),
    "user": os.getenv("PG_USER", "postgres"),
    "password": os.getenv("PG_PASSWORD", "postgres"),
}


def get_conn():
    return psycopg2.connect(**PG_CONFIG)


def insert_failure_log(payload: dict) -> int:
    """실패 이벤트 raw log 저장, 생성된 row id 반환"""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO failure_logs
                    (dag_id, task_id, run_id, try_number, exception, log_url, execution_date, raw_payload)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    payload["dag_id"],
                    payload["task_id"],
                    payload["run_id"],
                    payload["try_number"],
                    payload["exception"],
                    payload["log_url"],
                    payload["execution_date"],
                    Json(payload),
                ),
            )
            row_id = cur.fetchone()[0]
        conn.commit()
        return row_id
    finally:
        conn.close()