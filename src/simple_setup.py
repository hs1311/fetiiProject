"""
Simple database setup without pandas dependency
"""
import sqlite3
import csv
import os
from pathlib import Path

def create_database():
    """Create SQLite database from CSV files"""
    
    # Create database directory if it doesn't exist
    db_dir = Path("data/database")
    db_dir.mkdir(exist_ok=True)
    
    # Database path
    db_path = db_dir / "fetiipro.db"
    
    # Remove existing database if it exists
    if db_path.exists():
        os.remove(db_path)
    
    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Load demographics data
        print("Loading demographics data...")
        with open("data/csv_xlsx/clean_demographics.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            # Create table
            cursor.execute(f'''
                CREATE TABLE demographics (
                    {headers[0]} INTEGER,
                    {headers[1]} REAL
                )
            ''')
            
            # Insert data
            for row in csv_reader:
                cursor.execute(f'''
                    INSERT INTO demographics ({headers[0]}, {headers[1]})
                    VALUES (?, ?)
                ''', row)
        
        print("Demographics data loaded successfully")
        
        # Load riders data
        print("Loading riders data...")
        with open("data/csv_xlsx/clean_riders.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            # Create table
            cursor.execute(f'''
                CREATE TABLE riders (
                    {headers[0]} INTEGER,
                    {headers[1]} INTEGER,
                    {headers[2]} REAL
                )
            ''')
            
            # Insert data
            for row in csv_reader:
                cursor.execute(f'''
                    INSERT INTO riders ({headers[0]}, {headers[1]}, {headers[2]})
                    VALUES (?, ?, ?)
                ''', row)
        
        print("Riders data loaded successfully")
        
        # Load trips data
        print("Loading trips data...")
        with open("data/csv_xlsx/clean_trips.csv", 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)
            
            # Create table with all columns
            create_sql = f'''
                CREATE TABLE trips (
                    {headers[0]} INTEGER,
                    {headers[1]} INTEGER,
                    {headers[2]} REAL,
                    {headers[3]} REAL,
                    {headers[4]} REAL,
                    {headers[5]} REAL,
                    {headers[6]} TEXT,
                    {headers[7]} TEXT,
                    {headers[8]} TEXT,
                    {headers[9]} INTEGER,
                    {headers[10]} TEXT,
                    {headers[11]} INTEGER,
                    {headers[12]} TEXT,
                    {headers[13]} TEXT,
                    {headers[14]} TEXT,
                    {headers[15]} TEXT,
                    {headers[16]} INTEGER
                )
            '''
            cursor.execute(create_sql)
            
            # Insert data
            for row in csv_reader:
                cursor.execute(f'''
                    INSERT INTO trips ({', '.join(headers)})
                    VALUES ({', '.join(['?' for _ in headers])})
                ''', row)
        
        print("Trips data loaded successfully")
        
        # Create indexes for better performance
        print("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_demographics_user_id ON demographics(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_riders_user_id ON riders(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_riders_trip_id ON riders(trip_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_booking_user_id ON trips(booking_user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_date ON trips(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_trips_hour ON trips(hour)")
        
        # Commit changes
        conn.commit()
        print("Database setup completed successfully!")
        
    except Exception as e:
        print(f"Error creating database: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
    
    return db_path

if __name__ == "__main__":
    db_path = create_database()
    print(f"Database created at: {db_path}")
