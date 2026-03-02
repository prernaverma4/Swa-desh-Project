import urllib.request
import urllib.parse
import http.cookiejar
import re

login_url = "http://127.0.0.1:5002/login"
products_url = "http://127.0.0.1:5002/Products2?state=Maharashtra"
username = "testuser"
password = "password123"

# Setup cookie jar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)

# Login
login_data = urllib.parse.urlencode({'username': username, 'password': password}).encode()
try:
    with opener.open(login_url, data=login_data) as response:
        print(f"Login Response Code: {response.getcode()}")
        login_content = response.read().decode('utf-8')
        if "Login" in login_content and "Invalid" in login_content:
             print("Login Failed - Invalid credentials or error on page")
             exit(1)
except Exception as e:
    print(f"Login Failed: {e}")
    exit(1)

# Fetch Products
try:
    with opener.open(products_url) as response:
        print(f"Products Response Code: {response.getcode()}")
        content = response.read().decode('utf-8')
        
        products = ["Kolhapuri Chappals", "Warli Painting", "Solapuri Chaddar", "Nashik Grapes"]
        missing = []
        for product in products:
            if product in content:
                print(f"Found: {product}")
            else:
                print(f"MISSING: {product}")
                missing.append(product)
        
        if missing:
             # Extract title
             page_title = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
             if page_title:
                 print(f"Page Title: {page_title.group(1).strip()}")
             
             # Check for specific failure messages
             if "Invalid username or password" in content:
                 print("Login failed: Invalid credentials message found on page.")
             
             if "No products found" in content:
                 print("Page loaded but no products found.")
             
             print(f"Content Preview: {content[:500]}...")
             
             # Extract h6 titles just in case
             titles = re.findall(r'<h6[^>]*>(.*?)</h6>', content, re.DOTALL)
             clean_titles = [t.strip() for t in titles]
             print(f"Visible Product Titles: {clean_titles}")

except Exception as e:
    print(f"Fetch Failed: {e}")
    exit(1)
