import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
from scraper import scrape_amazon
import base64

# Set page config FIRST
st.set_page_config(
    page_title="QuantAI Amazon Scraper",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Now add your logo and company name
col_logo, col_title = st.columns([0.3, 8])
with col_logo:
    st.image("images/quantai_logo.png", width=300)
with col_title:
    st.markdown(
        "<span style='font-size: 2rem; font-weight: bold; color: #1a73e8; letter-spacing: 2px; position: relative; top: -8px;'>QuantAI</span>",
        unsafe_allow_html=True
    )

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF9900;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #E88A00;
    }
    .dataframe {
        font-size: 14px;
    }
    .dataframe th {
        background-color: #232F3E;
        color: white;
    }
    .dataframe td {
        padding: 8px;
    }
    .dataframe th, .dataframe td {
        font-size: 20px !important;
    }
    .dataframe a {
        font-size: 20px !important;
    }
    .dataframe td:nth-child(2) a {
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state for caching results
if 'products' not in st.session_state:
    st.session_state.products = []

# Header
st.title("🛍️ Product Search")
st.markdown("Search for products on Amazon and compare prices!")

# Create two columns for search and sort
col1, col2 = st.columns([2, 1])

with col1:
    # Search input with custom styling
    search_term = st.text_input("🔍 Search for products", placeholder="Enter product name...")

with col2:
    # Sorting dropdown
    sort_by = st.selectbox("📊 Sort by", ["-- Select --", "Name (A-Z)", "Price (Low to High)", "Rating (High to Low)"])

# Search button
if st.button("Search Products") and search_term.strip():
    with st.spinner("🔍 Searching Amazon..."):
        st.session_state.products = scrape_amazon(search_term)

# Sorting logic
def price_to_int(p):
    try:
        return int(p.replace(",", "").split()[0])
    except:
        return float("inf")

def rating_to_float(r):
    try:
        return float(r.split()[0])
    except:
        return 0

products = st.session_state.products

if sort_by == "Name (A-Z)":
    products = sorted(products, key=lambda x: x['name'].lower())
elif sort_by == "Price (Low to High)":
    products = sorted(products, key=lambda x: price_to_int(x['price']))
elif sort_by == "Rating (High to Low)":
    products = sorted(products, key=lambda x: rating_to_float(x['rating']), reverse=True)

# Display results in a table
if products:
    st.markdown("### 📦 Search Results")
    
    # Convert products to DataFrame
    df = pd.DataFrame(products)
    
    # Convert image URLs to HTML <img> tags
    df['image'] = df['image'].apply(lambda url: f'<img src="{url}" width="250">')
    
    # Create clickable links for product names
    df['name'] = df.apply(lambda x: f'<a href="{x["link"]}" target="_blank">{x["name"]}</a>', axis=1)
    
    # Reorder columns and rename them
    df = df[['image', 'name', 'price', 'rating']]
    df.columns = ['Image', 'Product Name', 'Price (₹)', 'Rating']
    
    # Display the table
    st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    
    # Add download button for the data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name='amazon_products.csv',
        mime='text/csv',
    )
else:
    st.info("👆 Enter a search term and click Search to find products.")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
