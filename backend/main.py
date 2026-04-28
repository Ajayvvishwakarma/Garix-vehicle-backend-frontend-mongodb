from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
import razorpay
from datetime import datetime

load_dotenv()

app = FastAPI()

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# DB Setup
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017") # Default fallback
DB_NAME = os.getenv("DB_NAME", "garix")
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
appointments = db["appointments"]
contacts = db["contacts"]
subscriptions = db["subscriptions"]
comments = db["comments"]
pricing_requests = db["pricing_requests"]
cart = db["cart"]
wishlist = db["wishlist"]
orders = db["orders"]

# Razorpay Setup
client_razorpay = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID", "rzp_test_default"), os.getenv("RAZORPAY_KEY_SECRET", "default_secret")))

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html") if os.path.exists("static/index.html") else {"message": "API is running"}

# ================= ADMIN PANEL ROUTES =================

@app.post("/admin/login")
async def admin_login(username: str = Form(...), password: str = Form(...)):
    if username == "soni@gmail.com" and password == "12345678":
        return {"status": "success", "message": "Login successful"}
    return {"status": "error", "message": "Invalid credentials"}

@app.get("/admin/stats")
async def get_admin_stats():
    total_orders = orders.count_documents({})
    total_appointments = appointments.count_documents({})
    total_contacts = contacts.count_documents({})
    total_cart = cart.count_documents({})
    total_wishlist = wishlist.count_documents({})
    
    rev_pipe = [{"$match": {"payment_status": "paid"}}, {"$group": {"_id": None, "total": {"$sum": "$total"}}}]
    rev_data = list(orders.aggregate(rev_pipe))
    total_revenue = rev_data[0]["total"] if rev_data else 0

    return {
        "total_orders": total_orders, "total_appointments": total_appointments,
        "total_contacts": total_contacts, "total_cart": total_cart,
        "total_wishlist": total_wishlist, "total_revenue": total_revenue
    }

@app.get("/admin/orders")
async def get_admin_orders():
    data = []
    for item in orders.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/appointments")
async def get_admin_appointments():
    data = []
    for item in appointments.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/contacts")
async def get_admin_contacts():
    data = []
    for item in contacts.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/cart")
async def get_admin_cart():
    data = []
    for item in cart.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/wishlist")
async def get_admin_wishlist():
    data = []
    for item in wishlist.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/comments")
async def get_admin_comments():
    data = []
    for item in comments.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/subscriptions")
async def get_admin_subscriptions():
    data = []
    for item in subscriptions.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/admin/pricing")
async def get_admin_pricing():
    data = []
    for item in pricing_requests.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.delete("/admin/{collection}/{id}")
async def delete_item(collection: str, id: str):
    col_map = {
        "orders": orders, "appointments": appointments, "contacts": contacts,
        "cart": cart, "wishlist": wishlist, "comments": comments,
        "subscriptions": subscriptions, "pricing": pricing_requests
    }
    if collection in col_map:
        res = col_map[collection].delete_one({"_id": ObjectId(id)})
        if res.deleted_count == 1:
            return {"status": "success", "message": "Deleted"}
    return {"status": "error", "message": "Not found"}

# ================= USER / FRONTEND ROUTES =================

@app.post("/api/appointment")
async def book_appointment(name: str = Form(...), email: str = Form(...), date: str = Form(...), time: str = Form(...), subject: str = Form(...), message: str = Form(None)):
    result = appointments.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/contact")
async def contact(name: str = Form(...), email: str = Form(...), date: str = Form(...), time: str = Form(...), subject: str = Form(...), message: str = Form(None)):
    result = contacts.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/subscribe")
async def subscribe(name: str = Form(...), email: str = Form(...), date: str = Form(...), time: str = Form(...), subject: str = Form(...), message: str = Form(None)):
    result = subscriptions.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/cart")
async def add_to_cart(product_name: str = Form(...), product_price: str = Form(...), product_img: str = Form(...), quantity: int = Form(1)):
    result = cart.insert_one({"product_name": product_name, "product_price": product_price, "product_img": product_img, "quantity": quantity})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/wishlist")
async def add_to_wishlist(product_name: str = Form(...), product_price: str = Form(...), product_img: str = Form(...)):
    result = wishlist.insert_one({"product_name": product_name, "product_price": product_price, "product_img": product_img})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/create-razorpay-order")
async def create_order(amount: int = Form(...)):
    try:
        data = {"amount": amount * 100, "currency": "INR", "receipt": "receipt_" + str(os.urandom(5).hex())}
        payment = client_razorpay.order.create(data=data)
        return {"id": payment['id'], "amount": payment['amount'], "currency": payment['currency']}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/order-save")
async def save_order(billing_first_name: str = Form(...), billing_last_name: str = Form(...), billing_email: str = Form(...), billing_phone: str = Form(...), billing_address_1: str = Form(...), billing_city: str = Form(...), billing_country: str = Form(...), billing_postcode: str = Form(...), payment_method: str = Form("razorpay"), order_notes: str = Form(""), razorpay_payment_id: str = Form(None), razorpay_order_id: str = Form(None), razorpay_signature: str = Form(None)):
    order_id = "ORD-" + datetime.now().strftime("%Y%m%d%H%M%S")
    import random
    order_data = {
        "order_id": order_id + str(random.randint(100,999)),
        "customer": {"first_name": billing_first_name, "last_name": billing_last_name, "email": billing_email, "phone": billing_phone, "address": billing_address_1, "city": billing_city, "country": billing_country, "postcode": billing_postcode},
        "total": 308, "payment_method": payment_method,
        "razorpay_payment_id": razorpay_payment_id, "razorpay_order_id": razorpay_order_id, "razorpay_signature": razorpay_signature,
        "payment_status": "paid" if razorpay_payment_id else "pending",
        "status": "pending", "notes": order_notes, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = orders.insert_one(order_data)
    return {"status": "success", "id": str(result.inserted_id)}

# Wildcard handler for serving HTML
@app.get("/{filename:path}")
def serve_html(filename: str):
    filepath = os.path.join("static", filename)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return FileResponse(filepath)
    if not filename.endswith(".html"):
        html_path = os.path.join("static", filename + ".html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
