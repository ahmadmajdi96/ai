import os
import psycopg2
import psycopg2.extras

def get_conn():
    url = os.getenv("DATABASE_URL", "postgres://aiops:aiops_pass@postgres:5432/aiops_main")
    return psycopg2.connect(url)

def fetch_all(q, params=None):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(q, params or [])
            return cur.fetchall()

def fetch_one(q, params=None):
    rows = fetch_all(q, params)
    return rows[0] if rows else None

def execute(q, params=None):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(q, params or [])
        conn.commit()
