import streamlit as st
import pandas as pd
from scraper import scrape_amazon
import base64
import streamlit.components.v1 as components

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set page config
st.set_page_config(
    page_title="QuantAI Amazon Scraper",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add global CSS for Lato font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap');
    
    /* Apply Lato font to all elements */
    * {
        font-family: 'Lato', sans-serif !important;
    }
    
    /* Specific styles for different elements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Lato', sans-serif !important;
        font-weight: 700 !important;
    }
    
    p, span, div, button, input, select {
        font-family: 'Lato', sans-serif !important;
    }
    
    .stButton > button {
        font-family: 'Lato', sans-serif !important;
    }
    
    .stTextInput > div > div > input {
        font-family: 'Lato', sans-serif !important;
    }
    
    .stSelectbox > div > div > select {
        font-family: 'Lato', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

logo_base64 = get_base64_image("images/quantai_logo.png")

def show_home():
    # Logo and company name
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 0px; margin-bottom: 1.5rem;'>
            <img src='data:image/png;base64,{logo_base64}' style='width: 80px; height: auto; display: block;'>
            <span style='font-size: 1.7rem; font-weight: bold; color: #ffffff; letter-spacing: 2px;'>QuantAI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Header section with blue-600 background
    st.markdown(
        """
        <div style='background-color: #black; padding: 2rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;'>
            <h1 style='color: #fff; font-size: 3rem; font-weight: bold; margin-bottom: 0.5rem; text-shadow: 2px 2px 8px #1e40af;'>Product Scraper</h1>
            <p style='font-size: 1.3rem; color: #e0e7ff; font-style: italic;'>
                Instantly search, compare, and download product data with ease.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Centered Streamlit Get Started button with blue-700 color and blue-800 hover effect
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Lato', sans-serif !important;
        }
        div.stButton > button {
            background-color: #1d4ed8;
            color: #fff !important;
            border: none;
            border-radius: 10px;
            padding: 1rem 3rem;
            font-size: 1.3rem;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.3s;
            margin-bottom: 2rem;
            display: block;
            margin-left: auto;
            margin-right: auto;
            font-family: 'Lato', sans-serif !important;
        }
        div.stButton > button:hover {
            background-color: #1e40af;
        }
        .feature-box {
            transition: box-shadow 0.3s, transform 0.3s;
        }
        .feature-box:hover {
            box-shadow: 0 8px 32px #1e40af;
            transform: scale(1.04);
        }
        </style>
    """, unsafe_allow_html=True)
    st.write("")  # Spacer
    if st.button("Get Started"):
        st.session_state.page = "scraper"
        st.rerun()

    # Features section
    st.markdown(
        """
        <h2 style='text-align: center; color: white; margin-top: 2rem;'>Discover Our Core Features</h2>
        <p style='text-align: center; color: #666; margin-bottom: 2rem;'>
            Explore the powerful tools designed to simplify your product research and comparison.
        </p>
        """,
        unsafe_allow_html=True
    )

    # Features grid with blue-600 background
    features = [
        {"icon": "🔎", "title": "Fast Product Search", "desc": "Quickly search for any product on Amazon and get instant results."},
        {"icon": "📊", "title": "Product Comparison", "desc": "Easily compare prices, ratings, and features across multiple products."},
        {"icon": "⬇️", "title": "Download Results", "desc": "Export your search results as a CSV file for further analysis."},
        {"icon": "⭐", "title": "Smart Sorting", "desc": "Sort products by name, price, or rating to find the best deals."},
        {"icon": "🖼️", "title": "Image Previews", "desc": "See visual previews of products to quickly identify items."},
        {"icon": "🔒", "title": "Privacy First", "desc": "Your searches are private and never stored. We respect your privacy."}
    ]
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class='feature-box' style='background: #2563eb; border-radius: 16px; padding: 2rem; margin-bottom: 2rem; min-height: 220px; box-shadow: 0 2px 8px #1e40af; text-align: center;'>
                    <div style='font-size: 2.5rem; margin-bottom: 1rem; color: #fff;'>{feature['icon']}</div>
                    <div style='font-size: 1.2rem; font-weight: bold; color: #fff; margin-bottom: 0.5rem;'>{feature['title']}</div>
                    <div style='color: #e0e7ff;'>{feature['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    # Footer
    st.markdown(
        """
        <div style='text-align: center; color: #ffffff; margin-top: 3rem; font-size: 1.1rem;'>
            Powered by QuantAI
        </div>
        """,
        unsafe_allow_html=True
    )

def show_scraper():
    # Logo and company name
    st.markdown(
        f"""
        <div style='display: flex; align-items: center; gap: 0px; margin-bottom: 1.5rem;'>
            <img src='data:image/png;base64,{logo_base64}' style='width: 80px; height: auto; display: block;'>
            <span style='font-size: 1.7rem; font-weight: bold; color: #ffffff; letter-spacing: 2px;'>QuantAI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        /* Style for Back to Home button by targeting its Streamlit container */
        div[data-testid="stButton"] > button {
            /* Ensure this style only applies to the first button in the scraper section, if needed */
        }

        /* Updated style for Back to Home button */
        /* Target the specific button using its test ID container */
        /* This targets the button within the first stButton div in the app structure */
        /* If there are other buttons before it, this might need adjustment */
        /* A more robust approach would involve using the key if possible, but testid is more standard */
        div[data-testid="stButton"]:first-of-type button {
            width: 100%;
            background-color: #1d4ed8 !important; /* Blue-700 */
            color: white !important;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 1.2rem;
            font-weight: bold;
            transition: background 0.3s;
        }
        div[data-testid="stButton"]:first-of-type button:hover {
            background-color: #1e40af !important; /* Blue-800 */
        }

        .stButton>button:not(div[data-testid="stButton"]:first-of-type button) {
            width: 100%;
            background-color: #FF9900;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
        .stButton>button:not(div[data-testid="stButton"]:first-of-type button):hover {
            background-color: #E88A00;
        }

        /* Remove default border, outline, and box-shadow from text input */
        div[data-testid="stTextInput"] input[type="text"] {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }

        /* Remove default border, outline, and box-shadow from selectbox */
        div[data-testid="stSelectbox"] div[role="button"] {
             border: none !important;
             outline: none !important;
             box-shadow: none !important;
        }

        /* Style the container of the text input with a blue-700 border and rounded corners */
        div[data-testid="stTextInput"] > div:first-child {
            border: 2px solid #1d4ed8 !important; /* Blue-700 */
            border-radius: 0.5rem !important; /* Match image */
            padding: 0.3rem !important; /* Add padding inside border */
        }

        /* Style the container of the selectbox with a blue-700 border and rounded corners */
        div[data-testid="stSelectbox"] > div:first-child {
             border: 2px solid #1d4ed8 !important; /* Blue-700 */
             border-radius: 0.5rem !important; /* Match image */
             padding: 0.3rem !important; /* Add padding inside border */
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

    # Back button
    if st.button("Back to Home", key="back_home_btn", help="Go back to home"):
        st.session_state.page = "home"
        st.rerun()
    # Add class to the button using streamlit.components.v1.html
    components.html("""
        <script>
        const btns = window.parent.document.querySelectorAll('button');
        if (btns.length > 0) {
            btns[0].classList.add('back-home-btn');
        }
        </script>
    """, height=0)

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
        sort_by = st.selectbox("📊 Sort by", ["-- Select --", "Name (A-Z)", "Price (Low to High)", "Rating (High to Low)", "Price (High to Low)"])

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
    elif sort_by == "Price (High to Low)":
        products = sorted(products, key=lambda x: -price_to_int(x['price']))

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

if st.session_state.page == "home":
    show_home()
else:
    show_scraper()
