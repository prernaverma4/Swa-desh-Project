import requests
from bs4 import BeautifulSoup
import sys

# Configuration
BASE_URL = "http://127.0.0.1:5002"
LOGIN_URL = f"{BASE_URL}/login"
PRODUCTS_LIST_URL = f"{BASE_URL}/Products2" # Using Products2 as per previous context it seems to be the main one, or /products
USERNAME = "testuser"
PASSWORD = "password123"

def main():
    session = requests.Session()

    # 1. Login
    print(f"Attempting to login to {LOGIN_URL}...")
    try:
        res = session.post(LOGIN_URL, data={'username': USERNAME, 'password': PASSWORD})
        res.raise_for_status()
    except requests.exceptions.ConnectionError:
        print(f"ERROR: Could not connect to {BASE_URL}. Is the server running?")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Login request failed: {e}")
        sys.exit(1)

    # Verify Login 
    # Check if we were redirected or if login page content is no longer present
    if "/login" in res.url and "Log In" in res.text:
         print("ERROR: Login failed. Still on login page.")
         sys.exit(1)
    print("SUCCESS: Logged in.")

    # 2. Find a Product ID dynamically
    # We'll try to fetch the product list to get a valid ID. 
    # If that fails or is empty, we'll fallback to ID 1.
    print(f"Fetching product list from {PRODUCTS_LIST_URL}...")
    try:
        res = session.get(PRODUCTS_LIST_URL)
        if res.status_code != 200:
             # Try fallback URL if Products2 fails
             print(f"WARN: {PRODUCTS_LIST_URL} returned {res.status_code}. Trying /products...")
             res = session.get(f"{BASE_URL}/products")
    except Exception as e:
        print(f"WARN: Failed to fetch product list: {e}")
        res = None

    product_detail_url = f"{BASE_URL}/product/1" # Default fallback
    
    if res and res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
        # Find any link that looks like /product/<id>
        # Excluding /product/add, /product/edit, etc.
        for a in soup.find_all('a', href=True):
            href = a['href']
            # We want /product/123, not /product/add or /product/delete
            if '/product/' in href:
                parts = href.split('/')
                # Check if the last part is a number
                if parts[-1].isdigit():
                    product_detail_url = f"{BASE_URL}{href}" if href.startswith('/') else href
                    if not product_detail_url.startswith('http'):
                        product_detail_url = f"{BASE_URL}/{product_detail_url.lstrip('/')}"
                    print(f"Found dynamic product URL: {product_detail_url}")
                    break

    # 3. Verify Detail Page
    print(f"Verifying detail page: {product_detail_url}")
    res = session.get(product_detail_url)
    
    if res.status_code == 404:
        print("ERROR: Product detail page not found (404).")
        sys.exit(1)
    elif res.status_code != 200:
        print(f"ERROR: Failed to load detail page. Status: {res.status_code}")
        # print(res.text) 
        sys.exit(1)
        
    soup = BeautifulSoup(res.text, 'html.parser')

    # Look for "Delete Product"
    # It might be in a button, or a modal trigger. 
    # We search for the text "Delete Product" generally, or specific elements.
    
    # Check for the button/link text
    element_by_text = soup.find(string=lambda text: text and "Delete Product" in text)
    
    # Check for form action containing delete
    form_with_delete = soup.find('form', action=lambda x: x and '/delete/' in x)
    
    import webbrowser
    if element_by_text:
        print(f"SUCCESS: Found text 'Delete Product' in: <{element_by_text.parent.name}>")
        print("Opening page in browser...")
        webbrowser.open(product_detail_url)
    elif form_with_delete:
         print(f"SUCCESS: Found form with delete action: {form_with_delete.get('action')}")
         print("Opening page in browser...")
         webbrowser.open(product_detail_url)
    else:
        print("FAILURE: 'Delete Product' button implementation NOT found.")
        # Debugging aid
        print("--- Page Text Snippet (first 500 chars) ---")
        print(soup.get_text()[:500])
        print("-------------------------------------------")

    # Extra check for Manufacturer permissions
    # If we are logged in as a normal user, we naturally won't see it.
    # The test user created earlier has role='manufacturer', let's verify that assumption if needed.

if __name__ == "__main__":
    main()
