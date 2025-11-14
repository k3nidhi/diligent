-- Customer Analytics Query
-- This query joins multiple tables to produce a comprehensive customer analytics report
-- Includes: customer name, number of orders, total spent, most purchased category, and average rating

WITH customer_orders AS (
    -- Aggregate order data per customer
    -- This CTE calculates number of orders and total spent for each customer
    SELECT 
        customer_id,
        COUNT(order_id) AS num_orders,
        SUM(total_amount) AS total_spent
    FROM orders
    GROUP BY customer_id
),
customer_category_counts AS (
    -- Count reviews per customer and category
    -- This helps identify the most reviewed (purchased) category for each customer
    SELECT 
        r.customer_id,
        p.category,
        COUNT(*) AS category_count
    FROM reviews r
    JOIN products p ON r.product_id = p.product_id
    GROUP BY r.customer_id, p.category
),
customer_top_categories AS (
    -- Find the most reviewed category for each customer
    -- Uses a window function approach with ROW_NUMBER for efficiency
    SELECT 
        customer_id,
        category AS most_purchased_category,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY category_count DESC, category) AS rn
    FROM customer_category_counts
),
customer_reviews AS (
    -- Aggregate review data per customer
    -- This CTE calculates average rating per customer
    SELECT 
        customer_id,
        AVG(rating) AS avg_rating
    FROM reviews
    GROUP BY customer_id
),
customer_most_category AS (
    -- Get the most reviewed category for each customer
    SELECT 
        customer_id,
        most_purchased_category
    FROM customer_top_categories
    WHERE rn = 1
)

-- Main query joining customers with their order and review analytics
SELECT 
    -- Customer name from customers table
    c.name AS customer_name,
    
    -- Number of orders from customer_orders CTE
    -- COALESCE handles customers who haven't made orders yet
    COALESCE(co.num_orders, 0) AS number_of_orders,
    
    -- Total amount spent from customer_orders CTE
    -- COALESCE handles customers who haven't made orders yet
    COALESCE(co.total_spent, 0) AS total_spent,
    
    -- Most purchased category from customer_most_category CTE
    -- Note: Since there's no order_items table, we use the most reviewed category
    -- as a proxy for the most purchased category
    COALESCE(cmc.most_purchased_category, 'N/A') AS most_purchased_category,
    
    -- Average rating given by the customer from customer_reviews CTE
    -- ROUND to 2 decimal places for readability
    -- COALESCE handles customers who haven't given any reviews yet
    ROUND(COALESCE(cr.avg_rating, 0), 2) AS average_rating

-- Start with customers table (LEFT JOIN ensures all customers are included)
FROM customers c

-- LEFT JOIN with customer_orders to get order statistics
-- LEFT JOIN ensures customers without orders are still included (will show 0 orders, 0 spent)
LEFT JOIN customer_orders co ON c.customer_id = co.customer_id

-- LEFT JOIN with customer_reviews to get review statistics
-- LEFT JOIN ensures customers without reviews are still included (will show 0 avg rating)
LEFT JOIN customer_reviews cr ON c.customer_id = cr.customer_id
-- LEFT JOIN with customer_most_category to get most purchased category
LEFT JOIN customer_most_category cmc ON c.customer_id = cmc.customer_id

-- Order results by total spent (descending) to show top customers first
ORDER BY total_spent DESC;

