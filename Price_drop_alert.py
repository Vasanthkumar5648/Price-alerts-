import streamlit as st
import requests
from bs4 import BeautifulSoup

# Function to extract price
def get_price(url):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko)"
                      " Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        page = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(page.content, 'lxml')
        title = soup.find(id='productTitle').get_text().strip()
        price = soup.find('span', {'class': 'a-price-whole'}).get_text().replace(',', '')
        price = float(price)
        return title, price
    except Exception:
        return None, None

# Streamlit UI
st.title("🔔 Price Drop Alert")

product_url = st.text_input("Enter Product URL (Amazon)", "")
target_price = st.number_input("Target Price (₹)", min_value=0.0, step=100.0)

if st.button("Check Now"):
    if product_url:
        title, price = get_price(product_url)
        if title and price:
            st.success(f"📦 Product: {title}")
            st.info(f"💵 Current Price: ₹{price}")
            if price <= target_price:
                st.balloons()
                st.success("✅ Price has dropped below your target!")
            else:
                st.warning("🔔 Not yet below target.")
        else:
            st.error("⚠️ Could not fetch the product details.")
