import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and Description
st.title("Product Recommendation System")
st.write("This app analyzes product data and provides recommendations based on demand analysis.")

# Sidebar for Dataset Uploads
st.sidebar.header("Upload Datasets")
file1 = st.sidebar.file_uploader("C:/Users/shree/Downloads/PRODUCT_NEW (1).csv", type=["csv"])

file2 = st.sidebar.file_uploader("C:/Users/shree/Downloads/PRODUCT_NEW_RATINGS (1).csv", type=["csv"])

if file1 and file2:
    # Load datasets
    product_details = pd.read_csv(file1)
    product_ratings = pd.read_csv(file2)

    st.subheader("Product Details Preview")
    st.dataframe(product_details.head())

    st.subheader("Product Ratings Preview")
    st.dataframe(product_ratings.head())

    # Data Preprocessing
    st.write("## Data Preprocessing")
    st.write("Splitting product features and merging datasets...")

    feature_cols = ['Color', 'Gender', 'Size', 'Brand', 'Category']
    product_details[feature_cols] = product_details['features'].str.split('|', expand=True)

    merged_data = pd.merge(product_ratings, product_details, on='product-id', how='left')

    st.write("Merged Data Preview:")
    st.dataframe(merged_data.head())

    # Demand Analysis
    st.write("## Demand Analysis")
    product_demand = merged_data.groupby('product-id').agg(
        avg_rating=('rating', 'mean'),
        num_ratings=('rating', 'count'),
        product_name=('product-title', 'first')
    ).reset_index()
    product_demand = product_demand.sort_values(by='num_ratings', ascending=False)

    st.write("Top Products by Demand:")
    st.dataframe(product_demand.head(10))

    # Recommendation System
    def recommend_products(data, num_recommendations=10):
        return data.head(num_recommendations)

    st.sidebar.header("Recommendations")
    num_recommendations = st.sidebar.slider("Number of Products to Recommend", 1, 20, 10)

    recommended_products = recommend_products(product_demand, num_recommendations)
    st.subheader("Recommended Products")
    st.dataframe(recommended_products[['product-id', 'product_name', 'avg_rating', 'num_ratings']])

    # Visualization
    st.write("## Visualization")
    st.write("Demand for Top Products")
    fig, ax = plt.subplots()
    ax.bar(recommended_products['product_name'], recommended_products['num_ratings'], color='skyblue')
    ax.set_xlabel("Product Name")
    ax.set_ylabel("Number of Ratings")
    ax.set_title("Top Recommended Products by Demand")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

else:
    st.info("Please upload both datasets to proceed.")