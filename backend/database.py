# backend/database.py
import sqlite3
from datetime import datetime
from typing import Optional

DB_PATH = "crop_reco.db"   # file created inside backend/ folder

def init_db() -> None:
    """Create DB and farm_data table if not exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS farm_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lat REAL,
        lon REAL,
        district TEXT,
        state TEXT,
        n REAL,
        p REAL,
        k REAL,
        humidity REAL,
        soil_moisture REAL,
        rainfall REAL,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def insert_farm_data(
    lat: float,
    lon: float,
    district: Optional[str],
    state: Optional[str],
    n: Optional[float],
    p: Optional[float],
    k: Optional[float],
    humidity: Optional[float],
    soil_moisture: Optional[float],
    rainfall: Optional[float]
) -> int:
    """Insert a farm record. Returns the new row id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO farm_data
        (lat, lon, district, state, n, p, k, humidity, soil_moisture, rainfall, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lat, lon, district, state,
        n, p, k, humidity, soil_moisture, rainfall,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    rowid = c.lastrowid
    conn.close()
    return rowid

def fetch_farm_data(record_id: int):
    """Return single row as tuple or None."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM farm_data WHERE id=?", (record_id,))
    row = c.fetchone()
    conn.close()
    return row

def fetch_recent(n: int = 10):
    """Return up to n most recent records."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM farm_data ORDER BY created_at DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return rows