import requests
from bs4 import BeautifulSoup

login_url = "http://127.0.0.1:5002/login"
products_url = "http://127.0.0.1:5002/Products2?state=Maharashtra"
username = "testuser"
password = "password123"

session = requests.Session()

# Login
response = session.post(login_url, data={'username': username, 'password': password})
print(f"Login URL: {response.url}")
print(f"Login Status: {response.status_code}")

if "Login" in response.text and "Invalid" in response.text:
    print("Login Failed!")
    exit(1)

# Fetch Products
response = session.get(products_url)
print(f"Products URL: {response.url}")
print(f"Products Status: {response.status_code}")

content = response.text
products = ["Kolhapuri Chappals", "Warli Painting", "Solapuri Chaddar", "Nashik Grapes"]

missing = []
for product in products:
    if product in content:
        print(f"Found: {product}")
    else:
        print(f"MISSING: {product}")
        missing.append(product)

if missing:
    print(f"Failed to find: {', '.join(missing)}")
    # Print a snippet of HTML to see what's there
    soup = BeautifulSoup(content, 'html.parser')
    titles = [t.get_text() for t in soup.find_all('h6', class_='card-title')]
    print(f"Actual Visible Products: {titles}")
else:
    print("All products found!")
