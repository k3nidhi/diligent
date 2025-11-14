import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# Initialize Faker for realistic data
fake = Faker()

# Set random seed for reproducibility
random.seed(42)
Faker.seed(42)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Generate date range (last 2 years)
start_date = datetime.now() - timedelta(days=730)
end_date = datetime.now()

# 1. Generate Customers (50-100 rows)
num_customers = random.randint(50, 100)
print(f"Generating {num_customers} customers...")

customers = []
countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'India', 'Japan', 'Brazil', 'Mexico']

for i in range(1, num_customers + 1):
    signup_date = fake.date_between(start_date=start_date - timedelta(days=365), end_date=end_date)
    customers.append({
        'customer_id': f'CUST{i:04d}',
        'name': fake.name(),
        'email': fake.email(),
        'signup_date': signup_date.strftime('%Y-%m-%d'),
        'country': random.choice(countries)
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv('data/customers.csv', index=False)
print(f"[OK] Created customers.csv with {len(customers_df)} rows")

# 2. Generate Products (50-100 rows)
num_products = random.randint(50, 100)
print(f"Generating {num_products} products...")

products = []
categories = [
    'Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports & Outdoors',
    'Beauty & Personal Care', 'Toys & Games', 'Food & Beverages', 'Automotive', 'Health & Wellness'
]

product_names = {
    'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smart Watch', 'Tablet', 'Camera', 'Speaker'],
    'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers', 'Hat', 'Scarf'],
    'Books': ['Novel', 'Biography', 'Cookbook', 'Mystery', 'Science Fiction', 'History Book'],
    'Home & Garden': ['Lamp', 'Cushion', 'Plant Pot', 'Mirror', 'Vase', 'Curtains'],
    'Sports & Outdoors': ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Bicycle', 'Tent'],
    'Beauty & Personal Care': ['Shampoo', 'Moisturizer', 'Lipstick', 'Perfume', 'Sunscreen'],
    'Toys & Games': ['Board Game', 'Action Figure', 'Puzzle', 'Building Blocks', 'Doll'],
    'Food & Beverages': ['Coffee', 'Tea', 'Chocolate', 'Snacks', 'Wine', 'Honey'],
    'Automotive': ['Car Mat', 'Phone Mount', 'Air Freshener', 'Car Cover', 'Tire Gauge'],
    'Health & Wellness': ['Vitamins', 'Protein Powder', 'First Aid Kit', 'Thermometer', 'Blood Pressure Monitor']
}

for i in range(1, num_products + 1):
    category = random.choice(categories)
    product_name_base = random.choice(product_names[category])
    product_name = f"{product_name_base} - {fake.word().capitalize()}"
    price = round(random.uniform(10, 500), 2)
    stock = random.randint(0, 500)
    
    products.append({
        'product_id': f'PROD{i:04d}',
        'product_name': product_name,
        'category': category,
        'price': price,
        'stock': stock
    })

products_df = pd.DataFrame(products)
products_df.to_csv('data/products.csv', index=False)
print(f"[OK] Created products.csv with {len(products_df)} rows")

# 3. Generate Orders (50-100 rows)
num_orders = random.randint(50, 100)
print(f"Generating {num_orders} orders...")

orders = []
customer_ids = customers_df['customer_id'].tolist()

for i in range(1, num_orders + 1):
    customer_id = random.choice(customer_ids)
    # Get customer signup date to ensure order_date is after signup
    customer_signup = pd.to_datetime(customers_df[customers_df['customer_id'] == customer_id]['signup_date'].values[0])
    order_date = fake.date_between(start_date=customer_signup, end_date=end_date)
    total_amount = round(random.uniform(20, 1000), 2)
    
    orders.append({
        'order_id': f'ORD{i:05d}',
        'customer_id': customer_id,
        'order_date': order_date.strftime('%Y-%m-%d'),
        'total_amount': total_amount
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv('data/orders.csv', index=False)
print(f"[OK] Created orders.csv with {len(orders_df)} rows")

# 4. Generate Transactions (50-100 rows)
num_transactions = random.randint(50, 100)
print(f"Generating {num_transactions} transactions...")

transactions = []
order_ids = orders_df['order_id'].tolist()
payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']
payment_statuses = ['Completed', 'Pending', 'Failed', 'Refunded']
# Weight the statuses: mostly completed
status_weights = [0.85, 0.10, 0.04, 0.01]

for i in range(1, num_transactions + 1):
    order_id = random.choice(order_ids)
    payment_method = random.choice(payment_methods)
    payment_status = random.choices(payment_statuses, weights=status_weights)[0]
    
    transactions.append({
        'transaction_id': f'TXN{i:05d}',
        'order_id': order_id,
        'payment_method': payment_method,
        'payment_status': payment_status
    })

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv('data/transactions.csv', index=False)
print(f"[OK] Created transactions.csv with {len(transactions_df)} rows")

# 5. Generate Reviews (50-100 rows)
num_reviews = random.randint(50, 100)
print(f"Generating {num_reviews} reviews...")

reviews = []
product_ids = products_df['product_id'].tolist()
review_texts_positive = [
    "Great product! Highly recommended.",
    "Excellent quality and fast shipping.",
    "Love it! Exactly as described.",
    "Perfect for my needs. Very satisfied.",
    "Amazing product, will buy again!",
    "Outstanding quality and value.",
    "Better than expected. Great purchase!",
]

review_texts_negative = [
    "Not what I expected. Disappointed.",
    "Quality could be better for the price.",
    "Had some issues with this product.",
    "Could use some improvements.",
    "Average product, nothing special.",
]

review_texts_neutral = [
    "It's okay, does the job.",
    "Decent product for the price.",
    "As expected, nothing more.",
    "Average quality, works fine.",
]

for i in range(1, num_reviews + 1):
    product_id = random.choice(product_ids)
    customer_id = random.choice(customer_ids)
    rating = random.randint(1, 5)
    
    # Generate review text based on rating
    if rating >= 4:
        review_text = random.choice(review_texts_positive)
    elif rating <= 2:
        review_text = random.choice(review_texts_negative)
    else:
        review_text = random.choice(review_texts_neutral)
    
    # Get customer signup date to ensure review_date is after signup
    customer_signup = pd.to_datetime(customers_df[customers_df['customer_id'] == customer_id]['signup_date'].values[0])
    review_date = fake.date_between(start_date=customer_signup, end_date=end_date)
    
    reviews.append({
        'review_id': f'REV{i:05d}',
        'product_id': product_id,
        'customer_id': customer_id,
        'rating': rating,
        'review_text': review_text,
        'review_date': review_date.strftime('%Y-%m-%d')
    })

reviews_df = pd.DataFrame(reviews)
reviews_df.to_csv('data/reviews.csv', index=False)
print(f"[OK] Created reviews.csv with {len(reviews_df)} rows")

print("\n" + "="*50)
print("All datasets generated successfully!")
print("="*50)
print(f"Files created in 'data/' directory:")
print(f"   - customers.csv ({len(customers_df)} rows)")
print(f"   - products.csv ({len(products_df)} rows)")
print(f"   - orders.csv ({len(orders_df)} rows)")
print(f"   - transactions.csv ({len(transactions_df)} rows)")
print(f"   - reviews.csv ({len(reviews_df)} rows)")

