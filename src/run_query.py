"""
Script to run SQL queries and save results to CSV files in the output folder.
"""
import sqlite3
import pandas as pd
import os
from pathlib import Path


def run_query_and_save(query_file, db_path, output_file):
    """
    Execute a SQL query and save results to a CSV file.
    
    Args:
        query_file (str): Path to SQL query file
        db_path (str): Path to SQLite database
        output_file (str): Path to output CSV file
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Read SQL query from file
        with open(query_file, 'r') as f:
            # Filter out comments and get only SQL statements
            lines = []
            for line in f:
                # Skip comment lines (lines starting with --)
                if line.strip() and not line.strip().startswith('--'):
                    lines.append(line)
            query = ''.join(lines)
        
        # Connect to database and execute query
        conn = sqlite3.connect(db_path)
        
        try:
            # Execute query and load results into DataFrame
            df = pd.read_sql_query(query, conn)
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            
            print(f"[OK] Query executed successfully")
            print(f"[OK] Results saved to: {output_file}")
            print(f"[OK] Rows returned: {len(df)}")
            
            # Display first few rows
            print(f"\nFirst 5 rows:")
            print(df.head().to_string(index=False))
            
            return df
            
        finally:
            conn.close()
            
    except FileNotFoundError as e:
        print(f"[ERROR] File not found: {e}")
        return None
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function to run the customer analytics query and save results."""
    # File paths
    query_file = 'customer_analytics.sql'
    db_path = 'ecommerce.db'
    output_file = 'output/customer_analytics_results.csv'
    
    print("="*70)
    print("Running Customer Analytics Query")
    print("="*70)
    print(f"Query file: {query_file}")
    print(f"Database: {db_path}")
    print(f"Output file: {output_file}")
    print("-"*70)
    
    # Check if files exist
    if not os.path.exists(query_file):
        print(f"[ERROR] Query file not found: {query_file}")
        return
    
    if not os.path.exists(db_path):
        print(f"[ERROR] Database file not found: {db_path}")
        print(f"[INFO] Please run 'python src/db_ingest.py' first to create the database")
        return
    
    # Run query and save results
    run_query_and_save(query_file, db_path, output_file)
    
    print("\n" + "="*70)
    print("Query execution completed!")
    print("="*70)


if __name__ == "__main__":
    main()

