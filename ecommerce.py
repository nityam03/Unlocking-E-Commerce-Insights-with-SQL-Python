import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQL Server using Windows Authentication
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=NITYAM;"  # Replace with your SQL Server name
    "DATABASE=ecommerce;"
    "Trusted_Connection=yes;"
)

# Create a cursor to interact with the database
cursor = conn.cursor()

# Monthly Order Count Section
# ============================
# Define the SQL query to fetch order counts by month
monthly_query = """
SELECT 
    DATENAME(MONTH, order_purchase_timestamp) AS Month,
    MONTH(order_purchase_timestamp) AS Month_Number,
    COUNT(order_id) AS Order_Count
FROM orders
GROUP BY 
    DATENAME(MONTH, order_purchase_timestamp), 
    MONTH(order_purchase_timestamp)
ORDER BY Month_Number;
"""

# Execute the query for monthly order count
cursor.execute(monthly_query)
monthly_data = cursor.fetchall()

processed_monthly_data = [[row[0], row[1], row[2]] for row in monthly_data]
monthly_df = pd.DataFrame(processed_monthly_data, columns=['Month', 'Month_Number', 'Order_Count'])

print("\nMonthly Order Count:")
print(monthly_df)

total_orders = monthly_df['Order_Count'].sum()
print(f"\nTotal Orders: {total_orders}")

# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(monthly_df['Month'], monthly_df['Order_Count'], color='skyblue')
plt.title('Monthly Order Count')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
for i, count in enumerate(monthly_df['Order_Count']):
    plt.text(i, count + 200, str(count), ha='center')
plt.savefig('monthly_orders.png')
plt.show()

# Average Products Per Order By Customer City Section
# ==========================
average_query = """
WITH count_per_order AS (
    SELECT top 10
        o.order_id, 
        o.customer_id, 
        COUNT(oi.order_item_id) AS oc
    FROM dbo.order_items oi
    JOIN dbo.orders o ON oi.order_id = o.order_id
    GROUP BY o.order_id, o.customer_id
)
SELECT 
    c.customer_city,
    ROUND(AVG(cpo.oc), 2) AS average_orders
FROM dbo.customers c
JOIN count_per_order cpo ON c.customer_id = cpo.customer_id
GROUP BY c.customer_city;
"""

# Execute the query for average products per order by city
cursor.execute(average_query)

# Fetch the data
top_10_data = cursor.fetchall()

# Print the results
print("\nTop 10 Cities with Average Products Per Order:")
for row in top_10_data:
    print(row)

# Close the cursor and connection when done
cursor.close()
conn.close()
