import requests
import mysql.connector
import os

FRED_API_KEY = os.environ.get("FRED_API_KEY")
API_BASE = "https://api.stlouisfed.org/fred/series/observations"

INDICATORS = {
        "GDP" : "GDP",
        "CPI" : "CPIAUCESL",
        "UNRATE" : "UNRATE"
}

def fetchData(series_id):

def insertIntoDB(indicator, observations):

def main():
    for label, series_id in INDICATORS.items():
        print("Fetching data for: {label}")
        try:
            observations = fetchData(series_id)
            insertIntoDB(label, observations)
            print("Inserted {len(observations)} recrods for {label}")
        execpt Exception as e:
            print("Error fetching or inserting data for {label}")

if __name__ == "__main__":
    main()
