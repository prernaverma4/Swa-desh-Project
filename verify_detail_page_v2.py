import requests

session = requests.Session()
login_url = "http://127.0.0.1:5002/login"
product_detail_url = "http://127.0.0.1:5002/product/1"
username = "testuser"
password = "password123"

# Login
res = session.post(login_url, data={'username': username, 'password': password})
print(f"Login Response URL: {res.url}")

if "login" in res.url:
    print("Login FAILED (Still on login page)")
    exit(1)

# Fetch Detail Page
res = session.get(product_detail_url)
print(f"Detail Page URL: {res.url}")

if "Delete Product" in res.text:
    print("SUCCESS: Delete Button found.")
else:
    print("FAILURE: Delete Button NOT found.")
    # Print the relevant section of HTML
    start_index = res.text.find("Artisan Details")
    print("--- HTML Snippet ---")
    print(res.text[start_index:start_index+1000])
