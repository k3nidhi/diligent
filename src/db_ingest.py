import sqlite3
import pandas as pd
import os
from pathlib import Path


def create_database_schema(conn):
    """Create all tables with proper schema, primary keys, and foreign keys."""
    cursor = conn.cursor()
    
    # Drop existing tables if they exist (for re-running the script)
    cursor.execute("DROP TABLE IF EXISTS reviews")
    cursor.execute("DROP TABLE IF EXISTS transactions")
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")
    
    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            signup_date DATE NOT NULL,
            country TEXT NOT NULL
        )
    """)
    
    # Create products table
    cursor.execute("""
        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE transactions (
            transaction_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        )
    """)
    
    # Create reviews table
    cursor.execute("""
        CREATE TABLE reviews (
            review_id TEXT PRIMARY KEY,
            product_id TEXT NOT NULL,
            customer_id TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            review_text TEXT NOT NULL,
            review_date DATE NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        )
    """)
    
    conn.commit()
    print("[OK] Database schema created successfully")


def ingest_csv_to_table(conn, csv_path, table_name):
    """Ingest a CSV file into a SQLite table."""
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Insert data into the table
        df.to_sql(table_name, conn, if_exists='append', index=False)
        
        # Get row count
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        print(f"[OK] Ingested {table_name}.csv: {row_count} rows inserted")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to ingest {table_name}.csv: {str(e)}")
        return False


def main():
    """Main function to run the database ingestion."""
    # Database file path
    db_path = 'ecommerce.db'
    
    # Remove existing database if it exists (for re-running)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[INFO] Removed existing database: {db_path}")
    
    # Connect to SQLite database (creates if doesn't exist)
    conn = sqlite3.connect(db_path)
    print(f"[INFO] Connected to database: {db_path}")
    
    try:
        # Create database schema
        create_database_schema(conn)
        
        # Base directory for CSV files
        data_dir = Path('data')
        
        # List of CSV files and their corresponding table names
        csv_files = [
            ('customers.csv', 'customers'),
            ('products.csv', 'products'),
            ('orders.csv', 'orders'),
            ('transactions.csv', 'transactions'),
            ('reviews.csv', 'reviews')
        ]
        
        print("\n" + "="*50)
        print("Starting CSV ingestion...")
        print("="*50 + "\n")
        
        # Ingest each CSV file
        for csv_file, table_name in csv_files:
            csv_path = data_dir / csv_file
            
            if not csv_path.exists():
                print(f"[ERROR] File not found: {csv_path}")
                continue
            
            ingest_csv_to_table(conn, csv_path, table_name)
        
        print("\n" + "="*50)
        print("Database ingestion completed successfully!")
        print("="*50)
        
        # Verify the ingestion by showing table counts
        print("\nTable row counts:")
        cursor = conn.cursor()
        tables = ['customers', 'products', 'orders', 'transactions', 'reviews']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  - {table}: {count} rows")
        
    except Exception as e:
        print(f"\n[ERROR] An error occurred during ingestion: {str(e)}")
        conn.rollback()
        raise
    
    finally:
        # Close database connection
        conn.close()
        print(f"\n[INFO] Database connection closed")


if __name__ == "__main__":
    main()

