# E-Commerce Data Pipeline Project

## 1. Project Overview

This project is an end-to-end e-commerce data pipeline that demonstrates data generation, ingestion, and analytics. It includes:

- **Synthetic Data Generation**: Python script to create realistic e-commerce CSV datasets
- **Database Ingestion**: SQLite database setup with proper schema, primary keys, and foreign keys
- **Data Analytics**: SQL queries for customer analytics and insights

The project generates 5 synthetic e-commerce datasets (customers, products, orders, transactions, and reviews), ingests them into a SQLite database, and provides analytical queries to extract meaningful business insights.

## 2. Folder Structure

```
diligent/
│
├── data/                          # Generated CSV datasets
│   ├── customers.csv              # Customer information (customer_id, name, email, signup_date, country)
│   ├── products.csv               # Product catalog (product_id, product_name, category, price, stock)
│   ├── orders.csv                 # Order records (order_id, customer_id, order_date, total_amount)
│   ├── transactions.csv           # Payment transactions (transaction_id, order_id, payment_method, payment_status)
│   └── reviews.csv                # Product reviews (review_id, product_id, customer_id, rating, review_text, review_date)
│
├── src/                           # Source code directory
│   └── db_ingest.py               # Database ingestion script (reads CSVs, creates SQLite database with schema)
│
├── prompts/                       # Project prompts/notes
│   ├── prompt1.txt                # Project prompt 1
│   └── prompt2.txt                # Project prompt 2
│
├── generate_data.py               # Script to generate synthetic e-commerce CSV datasets
├── customer_analytics.sql         # SQL query for customer analytics report
├── requirements.txt               # Python package dependencies
├── ecommerce.db                   # SQLite database (generated after running ingestion script)
└── README.md                      # This file

```

## 3. How to Run Scripts

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- `pandas` - for data manipulation and CSV handling
- `faker` - for generating realistic synthetic data

### Step 2: Generate CSV Datasets

Run the data generation script to create synthetic e-commerce CSV files:

```bash
python generate_data.py
```

**What it does:**
- Creates the `data/` directory if it doesn't exist
- Generates 5 CSV files with 50-100 rows each:
  - `customers.csv` - Customer records with names, emails, signup dates, and countries
  - `products.csv` - Product catalog with categories, prices, and stock levels
  - `orders.csv` - Order records linked to customers
  - `transactions.csv` - Payment transaction records linked to orders
  - `reviews.csv` - Product reviews linked to customers and products

**Output:**
- All CSV files will be saved in the `data/` directory
- Success messages will display the number of rows generated for each dataset

### Step 3: Ingest Data into SQLite Database

Run the database ingestion script to load CSV data into SQLite:

```bash
python src/db_ingest.py
```

**What it does:**
- Creates/overwrites `ecommerce.db` SQLite database
- Creates tables with proper data types and constraints:
  - Primary keys on all ID columns
  - Foreign key relationships:
    - `orders.customer_id` → `customers.customer_id`
    - `transactions.order_id` → `orders.order_id`
    - `reviews.product_id` → `products.product_id`
    - `reviews.customer_id` → `customers.customer_id`
- Loads all CSV data into corresponding tables

**Output:**
- `ecommerce.db` SQLite database file will be created
- Success messages will show the number of rows inserted into each table

### Step 4: Run SQL Query

Execute the customer analytics SQL query using one of the following methods:

#### Option A: Using Python

```bash
python -c "import sqlite3; conn = sqlite3.connect('ecommerce.db'); cursor = conn.cursor(); exec(open('customer_analytics.sql').read().split('--')[0]); print('Query executed successfully'); conn.close()"
```

#### Option B: Using SQLite Command Line

```bash
sqlite3 ecommerce.db < customer_analytics.sql
```

#### Option C: Interactive SQLite Session

```bash
sqlite3 ecommerce.db
```

Then paste the contents of `customer_analytics.sql` or use:

```sql
.read customer_analytics.sql
```

#### Option D: Using a Database GUI Tool

Open `ecommerce.db` with a SQLite database tool (like DB Browser for SQLite, DBeaver, or VS Code SQLite extension) and run the query from `customer_analytics.sql`.

## 4. SQL Query Output

The `customer_analytics.sql` query produces a comprehensive customer analytics report with the following columns:

### Output Columns

1. **customer_name** (TEXT)
   - Full name of the customer from the `customers` table

2. **number_of_orders** (INTEGER)
   - Total count of orders placed by the customer
   - Shows `0` for customers who haven't placed any orders

3. **total_spent** (REAL)
   - Sum of all order amounts for the customer
   - Shows `0` for customers who haven't placed any orders
   - Formatted as currency amount

4. **most_purchased_category** (TEXT)
   - The product category the customer has reviewed most frequently
   - Since there's no `order_items` table linking orders to specific products, this uses the most reviewed category as a proxy for the most purchased category
   - Shows `'N/A'` for customers who haven't reviewed any products

5. **average_rating** (REAL)
   - Average rating (1-5 scale) given by the customer across all their product reviews
   - Rounded to 2 decimal places
   - Shows `0.00` for customers who haven't given any reviews

### Query Features

- **Uses Common Table Expressions (CTEs)** for clarity and performance
- **Implements window functions** (`ROW_NUMBER()`) to rank categories
- **Handles missing data** with `COALESCE()` and `LEFT JOIN` to include all customers
- **Orders results** by total spent in descending order (highest spenders first)

### Example Output

```
customer_name        | number_of_orders | total_spent | most_purchased_category | average_rating
--------------------------------------------------------------------------------------------
Brian Lee            | 5                | 2497.18     | Clothing               | 1.0
Lisa Hensley         | 4                | 1961.12     | N/A                    | 0.0
Grant Watts          | 3                | 1868.05     | N/A                    | 0.0
...
```

---

## Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate CSV datasets
python generate_data.py

# 3. Ingest into SQLite database
python src/db_ingest.py

# 4. Run analytics query (using SQLite CLI)
sqlite3 ecommerce.db < customer_analytics.sql
```

---

## Notes

- The database will be recreated each time you run `src/db_ingest.py` (existing data will be overwritten)
- To regenerate different data, simply run `generate_data.py` again (it uses random seed 42 for reproducibility)
- All dates in the generated data span the last 2 years from the current date
- Customer IDs follow the format: `CUST0001`, `CUST0002`, etc.
- Product IDs follow the format: `PROD0001`, `PROD0002`, etc.
- Order IDs follow the format: `ORD00001`, `ORD00002`, etc.

