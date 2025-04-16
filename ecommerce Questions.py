import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQL Server using Windows Authentication
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=NITYAM;"  # Your server name
    "DATABASE=ecommerce;"  # Your database name
    "Trusted_Connection=yes;"  # Windows Authentication
)

# Create a cursor object
cur = conn.cursor()

# ### **1. Fetch All Table Names in the Database**
query_tables = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
tables_df = pd.read_sql(query_tables, conn)
print("Tables in 'ecommerce' database:")
print(tables_df)

### **2. Get Unique Customer Cities**
query_cities = "SELECT DISTINCT customer_city FROM customers"
cur.execute(query_cities)
data_cities = cur.fetchall()
print("\nUnique customer cities:")
for row in data_cities:
    print(row[0])  # Access first column of each row

# ### **3. Count the Number of Orders Placed in 2017**
query_orders = """
    SELECT COUNT(order_id)
    FROM orders
    WHERE YEAR(order_purchase_timestamp) = 2017
"""
cur.execute(query_orders)
data_orders = cur.fetchone()  # Using `fetchone()` instead of `fetchall()` (since it's a single value)
print("\nNumber of orders placed in 2017:", data_orders[0])

# ### **4. Find Total Sales Per Category**
query_sales = """
SELECT p.[product category], SUM(pay.payment_value) AS total_sales
FROM dbo.product p  
JOIN dbo.order_items oi ON p.product_id = oi.product_id  
JOIN dbo.payments pay ON pay.order_id = oi.order_id  
GROUP BY p.[product category]  -- We use GROUP BY because we did SUM
"""
cur.execute(query_sales)
data_sales = cur.fetchall()
print("\nTotal Sales Per Category:")
for row in data_sales:
    print(f"Category: {row[0]}, Total Sales: {row[1]}")

# ### **5. Calculate the Percentage of Orders Paid in Installments**
query_percentage = """
SELECT (SUM(CASE WHEN payment_installments > 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*)
FROM payments;
"""
cur.execute(query_percentage)
percentage_paid_installments = cur.fetchone()[0]  # Fetch single value
print(f"\nPercentage of orders paid in installments: {percentage_paid_installments:.2f}%")

\




# import pyodbc
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Connect to SQL Server using Windows Authentication
# conn = pyodbc.connect(
#     "DRIVER={SQL Server};"
#     "SERVER=NITYAM;"  # Your server name
#     "DATABASE=ecommerce;"  # Your database name
#     "Trusted_Connection=yes;"  # Windows Authentication
# )

# # Create a cursor object
# cur = conn.cursor()

# ### **1. Fetch All Table Names in the Database**
# query_tables = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
# tables_df = pd.read_sql(query_tables, conn)
# print("Tables in 'ecommerce' database:")
# print(tables_df)

# ### **2. Get Unique Customer Cities**
# query_cities = "SELECT DISTINCT customer_city FROM customers"
# cur.execute(query_cities)
# data_cities = cur.fetchall()
# print("\nUnique customer cities:")
# for row in data_cities:
#     print(row[0])  # Access first column of each row

# # ### **3. Count the Number of Orders Placed in 2017**
# query_orders = """
#     SELECT COUNT(order_id)
#     FROM orders
#     WHERE YEAR(order_purchase_timestamp) = 2017
# """
# cur.execute(query_orders)
# data_orders = cur.fetchone()  # Using `fetchone()` instead of `fetchall()` (since it's a single value)
# print("\nNumber of orders placed in 2017:", data_orders[0])

# # ### **4. Find Total Sales Per Category**
# query_sales = """
# SELECT p.[product category], SUM(pay.payment_value) AS total_sales
# FROM dbo.product p  
# JOIN dbo.order_items oi ON p.product_id = oi.product_id  
# JOIN dbo.payments pay ON pay.order_id = oi.order_id  
# GROUP BY p.[product category]  -- We use GROUP BY because we did SUM
# """
# cur.execute(query_sales)
# data_sales = cur.fetchall()
# print("\nTotal Sales Per Category:")
# for row in data_sales:
#     print(f"Category: {row[0]}, Total Sales: {row[1]}")

# # ### **5. Calculate the Percentage of Orders Paid in Installments**
# query_percentage = """
# SELECT (SUM(CASE WHEN payment_installments > 1 THEN 1 ELSE 0 END) * 100.0) / COUNT(*)
# FROM payments;
# """
# cur.execute(query_percentage)
# percentage_paid_installments = cur.fetchone()[0]  # Fetch single value
# print(f"\nPercentage of orders paid in installments: {percentage_paid_installments:.2f}%")




import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQL Server using Windows Authentication
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=NITYAM;"  # Replace with your actual server name
    "DATABASE=ecommerce;"  # Replace with your actual database name
    "Trusted_Connection=yes;"  # Windows Authentication
)

# Create a cursor object
cur = conn.cursor()

# Query to count the number of customers from each state
query = """
    SELECT customer_state, COUNT(customer_id) AS customer_count
    FROM customers
    GROUP BY customer_state;
"""

# Execute the query
cur.execute(query)

# Fetch the results
data = cur.fetchall()

# Print the fetched data to inspect its structure
print(data)

# Check if data has been returned
if data:
    # Reshaping the data into a list of tuples and ensuring proper format
    data = [tuple(row) for row in data]
    
    # Create DataFrame from the data
    df = pd.DataFrame(data, columns=["state", "customer_count"])

    # Plot the data using matplotlib
    plt.figure(figsize=(10, 6))  # Set figure size for better readability
    plt.bar(df["state"], df["customer_count"], color='skyblue')
    plt.xlabel("State", fontsize=12)  # Label for X-axis
    plt.ylabel("Number of Customers", fontsize=12)  # Label for Y-axis
    plt.title("Customer Count per State", fontsize=14)  # Chart title
    plt.xticks(rotation=45)  # Rotate X-axis labels for better readability
    plt.tight_layout()  # Ensure labels don't get cut off
    plt.show()  # Display the chart
else:
    print("No data returned from the query.")

# Close the cursor and connection after everything is done
cur.close()
conn.close()


# calculate the number of orders per month in 2018

import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Connect to SQL Server using Windows Authentication
conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=NITYAM;"
    "DATABASE=ecommerce;"
    "Trusted_Connection=yes;"
)

# Create a cursor to interact with the database
cursor = conn.cursor()

# Define the SQL query to fetch order counts by month
query = """
SELECT DATENAME(MONTH, order_purchase_timestamp) AS Month,
       MONTH(order_purchase_timestamp) AS Month_Number,
       COUNT(order_id) AS Order_Count
FROM orders
GROUP BY DATENAME(MONTH, order_purchase_timestamp), MONTH(order_purchase_timestamp)
ORDER BY Month_Number;
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
data = cursor.fetchall()

# Convert the pyodbc Row objects to a proper list of lists
processed_data = []
for row in data:
    processed_data.append([row[0], row[1], row[2]])

# Create a DataFrame from the processed data
df = pd.DataFrame(processed_data, columns=['Month', 'Month_Number', 'Order_Count'])

# Display the DataFrame
print("\nMonthly Order Count:")
print(df)

# Create a total row at the bottom
total_orders = df['Order_Count'].sum()
print(f"\nTotal Orders: {total_orders}")

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.bar(df['Month'], df['Order_Count'], color='skyblue')
plt.title('Monthly Order Count')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of each bar
for i, count in enumerate(df['Order_Count']):
    plt.text(i, count + 200, str(count), ha='center')

# Save the chart to a file
plt.savefig('monthly_orders.png')

# Display the chart (comment this out if running in an environment without display)
plt.show()

# Close the cursor and connection
cursor.close()
conn.close()

# Average Products Per Order By Customer City Section
# ==========================
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


#identify the correlation between product price and number of times a product has been purchsed

query = """
SELECT 
    CAST(dbo.product.[product category] AS VARCHAR(255)) AS product_category,
    COUNT(dbo.order_items.product_id) AS order_count,
    ROUND(AVG(dbo.order_items.price), 2) AS avg_price
FROM 
    dbo.product
JOIN 
    dbo.order_items
    ON dbo.product.product_id = dbo.order_items.product_id
JOIN 
    dbo.payments
    ON dbo.order_items.order_id = dbo.payments.order_id
GROUP BY 
    dbo.product.[product category]
"""

cursor.execute(query)
raw_data = cursor.fetchall()

# Cleaned data
cleaned_data = []

for row in raw_data:
    # Handle NULL product categories
    category = row[0].strip() if row[0] is not None else "Unknown"
    order_count = int(row[1])
    avg_price = float(row[2])
    cleaned_data.append((category, order_count, avg_price))

# Create DataFrame
df = pd.DataFrame(cleaned_data, columns=["product_category", "order_count", "avg_price"])

# Display
print(df.head())

# Correlation
correlation = np.corrcoef(df["order_count"], df["avg_price"])[0, 1]
print("\nCorrelation between Order Count and Average Price:", round(correlation, 2))

#Calculate the moving average of order values for each customer over their order history.

# SQL Query
query = """
SELECT 
    customer_id, 
    order_purchase_timestamp, 
    payment,
    AVG(payment) OVER (
        PARTITION BY customer_id 
        ORDER BY order_purchase_timestamp
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS mov_avg
FROM (
    SELECT 
        o.customer_id, 
        o.order_purchase_timestamp,
        p.payment_value AS payment
    FROM dbo.payments p
    JOIN dbo.orders o ON p.order_id = o.order_id
    WHERE p.payment_value IS NOT NULL AND o.order_purchase_timestamp IS NOT NULL
) AS sub;
"""

# Run and display
df = pd.read_sql_query(query, conn)
print(df.head())

#Calculate the moving average of order values for each customer over their order history.


# SQL Query
query = """
SELECT 
    customer_id, 
    order_purchase_timestamp, 
    payment,
    AVG(payment) OVER (
        PARTITION BY customer_id 
        ORDER BY order_purchase_timestamp
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS mov_avg
FROM (
    SELECT 
        o.customer_id, 
        o.order_purchase_timestamp,
        p.payment_value AS payment
    FROM dbo.payments p
    JOIN dbo.orders o ON p.order_id = o.order_id
    WHERE p.payment_value IS NOT NULL AND o.order_purchase_timestamp IS NOT NULL
) AS sub;
"""

# Run and display
df = pd.read_sql_query(query, conn)
print(df.head())

#Identify the top 3 customers who spent the most money in each year


# SQL Query
query = """
WITH RankedCustomers AS (
    SELECT 
        YEAR(o.order_purchase_timestamp) AS years,
        o.customer_id,
        SUM(p.payment_value) AS payment,
        DENSE_RANK() OVER (
            PARTITION BY YEAR(o.order_purchase_timestamp)
            ORDER BY SUM(p.payment_value) DESC
        ) AS drank
    FROM dbo.orders o
    JOIN dbo.payments p ON o.order_id = p.order_id
    GROUP BY 
        YEAR(o.order_purchase_timestamp),
        o.customer_id
)
SELECT years, customer_id, payment, drank
FROM RankedCustomers
WHERE drank <= 3
ORDER BY years, drank;
"""

# Run and display
df = pd.read_sql_query(query, conn)
print(df.head())
