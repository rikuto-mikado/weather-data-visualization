import requests
import selectorlib
import psycopg2
import os
from datetime import datetime

# Setting of connecting databases
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:password@localhost:5432/weather_db"
)

URL = "http://programmer100.pythonanywhere.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}


def get_db_connection():
    """Obtain a PostgreSQL connection"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Error of database connection: {e}")
        return None


def create_table_if_not_exists():
    """Create table if it doesn't exist"""
    conn = get_db_connection()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS temperatures (
                id SERIAL PRIMARY KEY,
                date VARCHAR(50) NOT NULL,
                temperature FLOAT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Table check/creation completed")
    except Exception as e:
        print(f"Table creation error: {e}")
        conn.close()


def scope(url):
    """Scraping data from web pages"""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Scraping error: {e}")
        return None


def extract(source):
    """Extracting temperature data from HTML"""
    try:
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return float(value) if value else None
    except Exception as e:
        print(f"data extraction error: {e}")
        return None


def store(temperature):
    """Store data to PostgreSQL"""
    if temperature is None:
        print("Skipping save due to null temperature data")
        return

    conn = get_db_connection()
    if conn is None:
        return

    try:
        now = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO temperatures (date, temperature) VALUES (%s, %s)",
            (now, temperature),
        )

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Data saved successfully: {now}, {temperature}°C")

    except Exception as e:
        print(f"Data save error: {e}")
        conn.close()


def main():
    """Main processing"""
    print("Weather Data Scraper (PostgreSQL version)")
    print("=" * 40)

    # Create table
    create_table_if_not_exists()

    # Data scraping
    print("Retrieving data from website...")
    scraped = scope(URL)

    if scraped is None:
        print("Scraping failed")
        return

    # Data extraction
    extracted = extract(scraped)

    if extracted is None:
        print("Data extraction failed")
        return

    print(f"Extracted temperature: {extracted}°C")

    # Data storage
    store(extracted)
    print("Processing completed")


if __name__ == "__main__":
    main()
