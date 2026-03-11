import psycopg2
import os

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'climate_data',
    'user': 'postgres',
    'password': 'root'
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'climate_files'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("ERROR: Table 'climate_files' does not exist!")
        print("Run: python manage.py makemigrations && python manage.py migrate")
    else:
        print("Table 'climate_files' exists.\n")
        
        # Get all records
        cursor.execute("SELECT variable_name, file_path, file_name FROM climate_files")
        rows = cursor.fetchall()
        
        if not rows:
            print("ERROR: No files in database!")
            print("You need to add climate file paths to the database.")
        else:
            print(f"Found {len(rows)} file(s) in database:\n")
            for row in rows:
                var_name, file_path, file_name = row
                print(f"Variable: {var_name}")
                print(f"File Path: {file_path}")
                print(f"File Name: {file_name}")
                
                # Check if file exists
                if os.path.exists(file_path):
                    print(f"✓ File exists")
                    print(f"  Size: {os.path.getsize(file_path)} bytes")
                else:
                    print(f"✗ FILE DOES NOT EXIST!")
                print("-" * 50)
    
    conn.close()
    
except psycopg2.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
