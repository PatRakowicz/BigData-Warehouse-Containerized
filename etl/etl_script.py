import requests
import mysql.connector
import os

FRED_API_KEY = os.environ.get("FRED_API_KEY")
API_BASE = "https://api.stlouisfed.org/fred/series/observations"

INDICATORS = {
    "GDP": "GDP",
    "CPI": "CPIAUCESL",
    "UNRATE": "UNRATE"
}

def fetch_indicator_data(series_id):
    res = requests.get(API_BASE, params={
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    })
    res.raise_for_status()
    return res.json()["observations"]

def insert_into_mysql(indicator, observations):
    conn = mysql.connector.connect(
        host="mysql",
        user="freduser",
        password="fredpass",
        database="fred_data"
    )
    cursor = conn.cursor()

    for obs in observations:
        date = obs["date"]
        value = obs["value"]
        if value == ".":
            continue

        cursor.execute("""
            INSERT INTO fred_data (indicator, date, value)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE value = VALUES(value)
        """, (indicator, date, value))

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    for label, series_id in INDICATORS.items():
        print(f"Fetching {label}...")
        data = fetch_indicator_data(series_id)
        insert_into_mysql(label, data)
        print(f"Inserted {len(data)} records for {label}")