
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sample sales dataset
data = {
    "Product": [
        "Laptop", "Mobile", "Tablet", "Laptop", "Mobile",
        "Tablet", "Laptop", "Mobile", "Tablet", "Laptop"
    ],
    "Category": ["Electronics"] * 10,
    "Quantity": [2, 5, 3, 1, 4, 6, 2, 3, 4, 1],
    "Price": [
        50000, 15000, 20000, 50000, 15000,
        20000, 50000, 15000, 20000, 50000
    ],
    "City": [
        "Delhi", "Mumbai", "Chandigarh", "Delhi", "Mumbai",
        "Chandigarh", "Delhi", "Mumbai", "Chandigarh", "Delhi"
    ]
}

df = pd.DataFrame(data)
df["Sales"] = df["Quantity"] * df["Price"]

# Dashboard title
st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive retail sales analysis using Python and Streamlit")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

selected_cities = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=sorted(df["Product"].unique()),
    default=sorted(df["Product"].unique())
)

filtered_df = df[
    df["City"].isin(selected_cities)
    & df["Product"].isin(selected_products)
]

# KPI metrics
total_revenue = filtered_df["Sales"].sum()
total_quantity = filtered_df["Quantity"].sum()
total_orders = len(filtered_df)
average_sale = (
    total_revenue / total_orders if total_orders else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_quantity:,}")
col3.metric("Sales Records", f"{total_orders:,}")
col4.metric("Average Sale", f"₹{average_sale:,.0f}")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Revenue by Product")
    product_sales = filtered_df.groupby("Product")["Sales"].sum()

    fig1, ax1 = plt.subplots(figsize=(7, 4))
    product_sales.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Product")
    ax1.set_ylabel("Revenue (INR)")
    ax1.tick_params(axis="x", rotation=0)
    fig1.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

with right:
    st.subheader("Revenue by City")
    city_sales = filtered_df.groupby("City")["Sales"].sum()

    fig2, ax2 = plt.subplots(figsize=(7, 4))
    city_sales.plot(kind="bar", ax=ax2)
    ax2.set_xlabel("City")
    ax2.set_ylabel("Revenue (INR)")
    ax2.tick_params(axis="x", rotation=0)
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

# Data table
st.subheader("Sales Data")
st.dataframe(filtered_df, use_container_width=True)

# CSV download
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Sales Data",
    data=csv_data,
    file_name="sales_analysis_results.csv",
    mime="text/csv"
)
