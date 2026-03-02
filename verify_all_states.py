import requests
from bs4 import BeautifulSoup

login_url = "http://127.0.0.1:5002/login"
username = "testuser"
password = "password123"

session = requests.Session()

# Login
response = session.post(login_url, data={'username': username, 'password': password})
if "Login" in response.text and "Invalid" in response.text:
    print("Login Failed!")
    exit(1)

for state in ['Maharashtra', 'Bihar', 'Uttarakhand']:
    products_url = f"http://127.0.0.1:5002/Products2?state={state}"
    res = session.get(products_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = [t.get_text().strip() for t in soup.find_all(['h5', 'h6'], class_='card-title')]
    print(f"--- State: {state} ---")
    print(f"Found {len(titles)} products: {titles}")
