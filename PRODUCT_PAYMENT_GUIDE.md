# Product & Payment Gateway Guide

## Overview
The Digital Catalyst platform now includes a complete e-commerce system for artisans to sell their products with integrated payment gateway.

## Features Added

### 1. Product Management
- Artisans can upload multiple products
- Each product has: name, description, price, image, and stock quantity
- Products are linked to specific artisans

### 2. Product Browsing
- View all products from all artisans
- View products by specific artisan
- Product detail pages with full information

### 3. Shopping & Checkout
- Add products to cart
- Checkout with shipping information
- Order tracking

### 4. Payment Gateway (Demo)
- Multiple payment methods:
  - UPI / PhonePe / Google Pay
  - Credit / Debit Card
  - Net Banking
  - Cash on Delivery
- Secure payment processing
- Order confirmation

### 5. Order Management
- View order history
- Track payment status
- Order details and receipts

## How to Use

### For Artisans (Adding Products)

1. **Navigate to Artisans Page**
   - Click "Artisans" in the navigation menu

2. **View Artisan Products**
   - Click the green bag icon next to any artisan
   - Or go to: http://localhost:5002/artisan/{artisan_id}/products

3. **Add New Product**
   - Click "Add Product" button
   - Fill in product details:
     - Product Name
     - Description
     - Price (₹)
     - Stock Quantity
     - Image URL (optional)
   - Click "Add Product"

4. **Manage Products**
   - Edit: Update product details
   - Delete: Remove product
   - View: See product details

### For Customers (Buying Products)

1. **Browse Products**
   - Click "Products" in navigation menu
   - Or go to: http://localhost:5002/products

2. **View Product Details**
   - Click "View Details" on any product
   - See full description, price, stock, and artisan info

3. **Purchase Product**
   - Click "Buy Now" button
   - Fill in shipping information:
     - Full Name
     - Email
     - Phone Number
     - Shipping Address
     - Quantity
   - Click "Proceed to Payment"

4. **Complete Payment**
   - Select payment method:
     - UPI
     - Card
     - Net Banking
     - Cash on Delivery
   - Click "Complete Payment"
   - View order confirmation

5. **Track Orders**
   - Click "My Orders" in navigation
   - View all your orders
   - Check payment status
   - View order details

## Database Models

### Product Model
```python
- id: Unique identifier
- name: Product name
- description: Product description
- price: Product price in ₹
- image_url: Product image URL
- stock: Available quantity
- artisan_id: Link to artisan
```

### Order Model
```python
- id: Order number
- user_id: Customer ID
- product_id: Product ID
- quantity: Number of items
- total_amount: Total price
- payment_status: pending/completed/failed
- payment_id: Payment transaction ID
- customer_name: Buyer name
- customer_email: Buyer email
- customer_phone: Buyer phone
- shipping_address: Delivery address
```

## API Endpoints

### Product APIs
- `GET /products` - List all products
- `GET /artisan/<id>/products` - Products by artisan
- `GET /product/<id>` - Product details
- `POST /product/add/<artisan_id>` - Add product
- `POST /product/edit/<id>` - Edit product
- `POST /product/delete/<id>` - Delete product

### Order APIs
- `GET /product/<id>/checkout` - Checkout page
- `POST /product/<id>/checkout` - Create order
- `GET /payment/<order_id>` - Payment page
- `POST /payment/<order_id>/process` - Process payment
- `GET /order/<order_id>/success` - Order confirmation
- `GET /my-orders` - User's orders

## Payment Gateway Integration

### Current Status: DEMO MODE
The payment gateway is currently in demo mode for testing purposes.

### For Production Deployment

To integrate with real payment gateways, replace the demo payment processing with:

#### Option 1: Razorpay (Recommended for India)
```python
import razorpay

client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

# Create order
order = client.order.create({
    'amount': total_amount * 100,  # Amount in paise
    'currency': 'INR',
    'payment_capture': 1
})
```

#### Option 2: Stripe (International)
```python
import stripe

stripe.api_key = "YOUR_SECRET_KEY"

# Create payment intent
intent = stripe.PaymentIntent.create(
    amount=int(total_amount * 100),
    currency='inr'
)
```

#### Option 3: PayPal
```python
import paypalrestsdk

paypalrestsdk.configure({
    "mode": "live",
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})
```

## Navigation Updates

New menu items added:
- **Products**: Browse all products
- **My Orders**: View order history

Artisan page now has:
- **Products button** (green bag icon) next to each artisan

## Security Features

- Login required for all transactions
- Order tracking by user ID
- Secure payment status tracking
- Customer information validation

## Testing the System

### Test Scenario 1: Add Product
1. Login as admin
2. Go to Artisans page
3. Click products icon for "Ramesh Kumar"
4. Add a pottery product
5. Set price: ₹500, stock: 10

### Test Scenario 2: Make Purchase
1. Go to Products page
2. Click on the pottery product
3. Click "Buy Now"
4. Fill shipping details
5. Select UPI payment
6. Complete payment
7. View order confirmation

### Test Scenario 3: View Orders
1. Click "My Orders"
2. See your purchase
3. Click "View" to see details

## Sample Product Data

You can add these sample products:

**For Ramesh Kumar (Pottery)**
- Blue Pottery Vase - ₹1,500
- Decorative Plate Set - ₹2,000
- Ceramic Bowl - ₹800

**For Lakshmi Devi (Weaving)**
- Handloom Silk Saree - ₹5,000
- Cotton Dupatta - ₹1,200
- Woven Table Runner - ₹600

**For Mohammed Ali (Metalwork)**
- Brass Lamp - ₹2,500
- Copper Water Bottle - ₹1,800
- Metal Wall Art - ₹3,500

## Troubleshooting

### Products not showing
- Check if products are added for artisans
- Verify stock quantity > 0

### Payment fails
- Currently in demo mode - all payments auto-complete
- Check order status in "My Orders"

### Images not loading
- Verify image URL is valid
- Use placeholder if no image provided

## Future Enhancements

1. Shopping cart for multiple items
2. Product reviews and ratings
3. Wishlist functionality
4. Product categories and filters
5. Real payment gateway integration
6. Email notifications
7. SMS alerts
8. Invoice generation
9. Shipping tracking
10. Discount coupons

## Access URLs

- Products: http://localhost:5002/products
- My Orders: http://localhost:5002/my-orders
- Artisan Products: http://localhost:5002/artisan/{id}/products
- Add Product: http://localhost:5002/product/add/{artisan_id}

## Support

For issues or questions:
1. Check this guide
2. Review API_DOCUMENTATION.md
3. Check console logs
4. Verify database tables created

---

**Happy Selling! 🛍️**

Last Updated: February 14, 2026
