# Digital Catalyst - API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
Most API endpoints are open and do not require authentication. However, the web interface requires login for CRUD operations.

---

## Endpoints

### 1. Heritage Sites API

#### Get All Heritage Sites
**Endpoint:** `GET /api/heritage`

**Description:** Retrieve all heritage sites in the database

**Authentication:** Not required

**Response:**
```json
[
  {
    "id": 1,
    "name": "Taj Mahal",
    "state": "Uttar Pradesh",
    "category": "Monument",
    "description": "Iconic white marble mausoleum",
    "annual_visitors": 7000000,
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  },
  {
    "id": 2,
    "name": "Red Fort",
    "state": "Delhi",
    "category": "Fort",
    "description": "Historic fortified palace",
    "annual_visitors": 2500000,
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

**Example cURL:**
```bash
curl http://localhost:5000/api/heritage
```

---

### 2. Artisans API

#### Get All Artisans
**Endpoint:** `GET /api/artisans`

**Description:** Retrieve all artisans in the database

**Authentication:** Not required

**Response:**
```json
[
  {
    "id": 1,
    "name": "Ramesh Kumar",
    "craft": "Pottery",
    "state": "Rajasthan",
    "product_price": 1500.0,
    "contact": "9876543210",
    "description": "Traditional blue pottery artisan",
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  },
  {
    "id": 2,
    "name": "Lakshmi Devi",
    "craft": "Weaving",
    "state": "West Bengal",
    "product_price": 3500.0,
    "contact": "9876543211",
    "description": "Handloom saree weaver",
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

**Example cURL:**
```bash
curl http://localhost:5000/api/artisans
```

---

### 3. Recommendations API

#### Get Heritage Site Recommendations
**Endpoint:** `GET /api/recommendations`

**Description:** Get AI-powered recommendations for heritage sites or artisans

**Authentication:** Not required

**Query Parameters:**
- `type` (required): 'heritage' or 'artisans'
- `top_n` (optional): Number of recommendations (default: 5, max: 10)
- `state` (optional): State filter for artisan recommendations

**Example 1: Heritage Site Recommendations**
```bash
curl "http://localhost:5000/api/recommendations?type=heritage&top_n=5"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Taj Mahal",
    "state": "Uttar Pradesh",
    "category": "Monument",
    "description": "Iconic white marble mausoleum",
    "annual_visitors": 7000000,
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

**Example 2: Artisan Recommendations by State**
```bash
curl "http://localhost:5000/api/recommendations?type=artisans&state=Rajasthan&top_n=3"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Ramesh Kumar",
    "craft": "Pottery",
    "state": "Rajasthan",
    "product_price": 1500.0,
    "contact": "9876543210",
    "description": "Traditional blue pottery artisan",
    "created_at": "2026-02-14T10:30:00",
    "updated_at": "2026-02-14T10:30:00"
  }
]
```

---

### 4. Analytics API

#### Get Analytics Data
**Endpoint:** `GET /api/analytics`

**Description:** Retrieve comprehensive analytics including economic impact, visitor trends, and state distribution

**Authentication:** Not required

**Response:**
```json
{
  "economic_impact": {
    "total_visitors": 13800000,
    "tourism_revenue": 6900000000,
    "artisan_revenue": 850000,
    "total_economic_impact": 6900850000,
    "avg_product_price": 2125.0
  },
  "visitor_trends": {
    "labels": ["Taj Mahal", "Mysore Palace", "Red Fort"],
    "values": [7000000, 2800000, 2500000]
  },
  "state_distribution": {
    "Rajasthan": 2,
    "West Bengal": 1,
    "Uttar Pradesh": 1,
    "Gujarat": 1,
    "Kerala": 1,
    "Madhya Pradesh": 1,
    "Assam": 1
  }
}
```

**Example cURL:**
```bash
curl http://localhost:5000/api/analytics
```

---

## Web Routes (Require Login)

### Authentication Routes

#### Login
**Endpoint:** `POST /login`
**Method:** POST
**Form Data:**
- `username`: User's username
- `password`: User's password

#### Register
**Endpoint:** `POST /register`
**Method:** POST
**Form Data:**
- `username`: New username
- `email`: Email address
- `password`: Password

#### Logout
**Endpoint:** `GET /logout`
**Method:** GET
**Authentication:** Required

---

### Heritage Site Routes

#### List Heritage Sites
**Endpoint:** `GET /heritage`
**Query Parameters:**
- `search`: Search by name
- `state`: Filter by state
- `category`: Filter by category

#### Add Heritage Site
**Endpoint:** `POST /heritage/add`
**Form Data:**
- `name`: Site name
- `state`: State
- `category`: Category
- `description`: Description
- `annual_visitors`: Number of annual visitors

#### Edit Heritage Site
**Endpoint:** `POST /heritage/edit/<id>`
**Form Data:** Same as add

#### Delete Heritage Site
**Endpoint:** `POST /heritage/delete/<id>`

---

### Artisan Routes

#### List Artisans
**Endpoint:** `GET /artisans`
**Query Parameters:**
- `search`: Search by name
- `state`: Filter by state
- `craft`: Filter by craft type

#### Add Artisan
**Endpoint:** `POST /artisans/add`
**Form Data:**
- `name`: Artisan name
- `craft`: Craft type
- `state`: State
- `product_price`: Product price
- `contact`: Contact number
- `description`: Description

#### Edit Artisan
**Endpoint:** `POST /artisans/edit/<id>`
**Form Data:** Same as add

#### Delete Artisan
**Endpoint:** `POST /artisans/delete/<id>`

---

### Export Routes

#### Export Heritage Sites to CSV
**Endpoint:** `GET /export/heritage`
**Response:** CSV file download

#### Export Artisans to CSV
**Endpoint:** `GET /export/artisans`
**Response:** CSV file download

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid recommendation type"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 401 Unauthorized
Redirects to login page for web routes

---

## Rate Limiting
Currently, there are no rate limits on API endpoints.

## Data Types

### Heritage Site Object
```typescript
{
  id: number,
  name: string,
  state: string,
  category: string,
  description: string | null,
  annual_visitors: number,
  created_at: string (ISO 8601),
  updated_at: string (ISO 8601)
}
```

### Artisan Object
```typescript
{
  id: number,
  name: string,
  craft: string,
  state: string,
  product_price: number,
  contact: string | null,
  description: string | null,
  created_at: string (ISO 8601),
  updated_at: string (ISO 8601)
}
```

---

## Testing with Python

### Example: Get Heritage Sites
```python
import requests

response = requests.get('http://localhost:5000/api/heritage')
data = response.json()

for site in data:
    print(f"{site['name']} - {site['state']}")
```

### Example: Get Recommendations
```python
import requests

params = {
    'type': 'heritage',
    'top_n': 5
}

response = requests.get('http://localhost:5000/api/recommendations', params=params)
recommendations = response.json()

for site in recommendations:
    print(f"{site['name']}: {site['annual_visitors']:,} visitors")
```

### Example: Get Analytics
```python
import requests

response = requests.get('http://localhost:5000/api/analytics')
analytics = response.json()

print(f"Total Economic Impact: ₹{analytics['economic_impact']['total_economic_impact']:,.0f}")
```

---

## Notes

1. All timestamps are in ISO 8601 format (UTC)
2. Currency values are in Indian Rupees (₹)
3. The API returns JSON by default
4. CORS is not enabled by default
5. All successful GET requests return 200 status code
6. All successful POST requests return 302 (redirect) for web forms

---

**Last Updated:** February 14, 2026
**API Version:** 1.0.0
