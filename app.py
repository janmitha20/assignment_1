import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 🔗 Connect to TiDB Cloud
db_url = "mysql+pymysql://kdkYFd9i4JYockp.root:vVcWE4VLsvjKf5hs@gateway01.us-west-2.prod.aws.tidbcloud.com:4000/retail_orders?ssl_ca=<CA_PATH>&ssl_verify_cert=true&ssl_verify_identity=true"
engine = create_engine(db_url)

# 🎯 Function to Execute SQL Queries
def run_query(query):
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

# 🎯 Streamlit App Title
st.title("📊 Retail Order Data Analysis Dashboard")

# 📌 Sidebar for selecting analysis type
option = st.sidebar.selectbox("Choose Analysis", [
    "View Raw Data",
    "Top-Selling Products",
    "Monthly Sales Analysis",
    "Product Performance",
    "Regional Sales Analysis",
    "Discount Analysis",
    "Top 10 Revenue-Generating Products",
    "Find Top 5 Cities with Highest Profit Margins",
    "Total Discount by Category",
    "Average Sale Price per Category",
    "Region with Highest Average Sale Price",
    "Total Profit per Category",
    "Top 3 Segments with Most Orders",
    "Average Discount Percentage per Region",
    "Product Category with Highest Total Profit",
    "Total Revenue Per Year",
    "Best-Selling Product in Each Category",
    "Month with Highest Revenue",
    "Top 3 Categories with Most Sales",
    "Total Orders Per Region",
    "Category with Lowest Profit Margin",
    "Customers with Most Orders",
    "Revenue Per Shipping Mode",
    "Percentage Revenue by Region",
    "Most Common Discount Percentage",
    "find the total number of orders ",
    "Highlight Subcategories with Highest Profit Margins"
])

# 📈 SQL Queries
queries = {
    "View Raw Data": "SELECT * FROM orders_details LIMIT 10;",
    "Top-Selling Products": """
        SELECT product_id, SUM(sale_price * quantity) AS total_revenue
        FROM orders_details
        GROUP BY product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "Monthly Sales Analysis": """
        SELECT MONTH(order_date) AS month, YEAR(order_date) AS year, SUM(sale_price * quantity) AS revenue
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY YEAR(order_date), MONTH(order_date)
        ORDER BY year, month;
    """,
    "Product Performance": """
        WITH
  `ProductRanks` AS (
    SELECT
      `product_id`,
      SUM(`sale_price`) AS `revenue`,
      SUM(`profit`) AS `profit_margin`,
      ROW_NUMBER() OVER (
        ORDER BY
          SUM(`sale_price`) DESC
      ) AS `revenue_rank`,
      ROW_NUMBER() OVER (
        ORDER BY
          SUM(`profit`) DESC
      ) AS `profit_rank`
    FROM
      `orders_details`
    GROUP BY
      `product_id`
  )
SELECT
  *
FROM
  `ProductRanks`;
    """,
    "Regional Sales Analysis": """
        SELECT m.region, SUM(d.sale_price * d.quantity) AS total_revenue
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY m.region;
    """,
    "Discount Analysis": """
        SELECT DISTINCT discount_percent 
        FROM orders_details 
        ORDER BY discount_percent DESC;
    """,
    "Top 10 Revenue-Generating Products": """
        SELECT product_id, SUM(sale_price * quantity) AS total_revenue
        FROM orders_details
        GROUP BY product_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "Find Top 5 Cities with Highest Profit Margins": """
        SELECT city, SUM(profit) AS total_profit
        FROM orders_details
        JOIN orders_main ON orders_details.order_id = orders_main.order_id
        GROUP BY city
        ORDER BY total_profit DESC
        LIMIT 5;
    """,
    "Total Discount by Category": """
        SELECT category, SUM(discount) AS total_discount
        FROM orders_details
        GROUP BY category;
    """,
    "Average Sale Price per Category": """
        SELECT category, AVG(sale_price) AS avg_sale_price
        FROM orders_details
        GROUP BY category;
    """,
    "Region with Highest Average Sale Price": """
        SELECT m.region, AVG(d.sale_price) AS avg_sale_price
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY m.region
        ORDER BY avg_sale_price DESC
       
    """,
    "Total Profit per Category": """
        SELECT category, SUM(profit) AS total_profit
        FROM orders_details
        GROUP BY category;
    """,
    "Top 3 Segments with Most Orders": """
        SELECT segment, COUNT(order_id) AS order_count
        FROM orders_main
        GROUP BY segment
        ORDER BY order_count DESC
        LIMIT 3;
    """,
    "Average Discount Percentage per Region": """
        SELECT m.region, AVG(d.discount_percent) AS avg_discount
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY m.region;
    """,
    "Product Category with Highest Total Profit": """
        SELECT category, SUM(profit) AS total_profit
        FROM orders_details
        GROUP BY category
        ORDER BY total_profit DESC
        LIMIT 1;
    """,
    "Total Revenue Per Year": """
        SELECT YEAR(order_date) AS year, SUM(sale_price * quantity) AS total_revenue
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY YEAR(order_date)
        ORDER BY year;
    """,
    "Best-Selling Product in Each Category": """
        SELECT d.category, d.product_id, SUM(d.quantity) AS total_sold
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY d.category, d.product_id
        ORDER BY total_sold DESC;
    """,
    "Month with Highest Revenue": """
        SELECT MONTH(m.order_date) AS month, SUM(d.sale_price * d.quantity) AS revenue
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY MONTH(m.order_date)
        ORDER BY revenue DESC
        LIMIT 1;
    """,
    "Top 3 Categories with Most Sales": """
        SELECT category, SUM(quantity) AS total_quantity
        FROM orders_details
        GROUP BY category
        ORDER BY total_quantity DESC
        LIMIT 3;
    """,
    "Total Orders Per Region": """
        SELECT m.region, COUNT(m.order_id) AS total_orders
        FROM orders_main m
        GROUP BY m.region;
    """,
    "Category with Lowest Profit Margin": """
        SELECT category, SUM(profit) AS total_profit
        FROM orders_details
        GROUP BY category
        ORDER BY total_profit ASC
        LIMIT 1;
    """,
    "Customers with Most Orders": """
        SELECT m.customer_name, COUNT(m.order_id) AS order_count
        FROM orders_main m
        GROUP BY m.customer_name
        ORDER BY order_count DESC
        LIMIT 5;
    """,
    "Revenue Per Shipping Mode": """
        SELECT m.ship_mode, SUM(d.sale_price * d.quantity) AS revenue
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY m.ship_mode;
    """,
    "Percentage Revenue by Region": """
        SELECT m.region, 
            (SUM(d.sale_price * d.quantity) / (SELECT SUM(sale_price * quantity) FROM orders_details)) * 100 AS revenue_percentage
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY m.region;
    """,
    "Most Common Discount Percentage": """
        SELECT discount_percent, COUNT(*) AS discount_count
        FROM orders_details
        GROUP BY discount_percent
        ORDER BY discount_count DESC
        LIMIT 1;
    """,
    
    "find the total number of orders ": """
        SELECT COUNT(order_id) AS total_orders
        FROM orders_main;
    """,
    "Highlight Subcategories with Highest Profit Margins": """
        SELECT 
        d.sub_category, 
        SUM(d.sale_price * d.quantity) AS total_revenue, 
        SUM(d.profit) AS total_profit, 
        (SUM(d.profit) / NULLIF(SUM(d.sale_price * d.quantity), 0)) * 100 AS profit_margin
        FROM orders_details d
        JOIN orders_main m ON d.order_id = m.order_id
        GROUP BY d.sub_category
        ORDER BY profit_margin DESC
        LIMIT 10;
    """
    

}


# 🎯 Show the SQL Query Executed in Streamlit
st.sidebar.subheader("SQL Query Executed")

st.sidebar.code(queries[option], language="sql")



# 🎯 Run the Selected Query

df = run_query(queries[option])


# 📊 Display Results in Streamlit
st.subheader(option)
st.dataframe(df)

# 📉 Show a Chart for Numeric Data
if "total_revenue" in df.columns or "avg_sale_price" in df.columns:
    st.bar_chart(df.set_index(df.columns[0]))
