from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import os
from datetime import datetime

load_dotenv()

app = FastAPI()

# CORS Middleware (Corrected spelling)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# Database Connection (Variables fixed)
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections (All collections defined)
appointments = db["appointments"] # Fixed Spelling
contacts = db["contacts"]
subscriptions = db["subscriptions"]
comments = db["comments"]
pricing_requests = db["pricing_requests"]
cart = db["cart"]          # Added for Cart logic
wishlist = db["wishlist"]        # Added for Wishlist logic

os.makedirs("static", exist_ok=True)

@app.get("/")
def home():
    return FileResponse("static/index.html") if os.path.exists("static/index.html") else {"message": "API is running"}

# 1. APPOINTMENT
@app.post("/api/appointment")
async def book_appointment(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = appointments.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

# 2. CONTACT
@app.post("/api/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = contacts.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": "subject", "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

# 3. SUBSCRIBE
@app.post("/api/subscribe")
async def subscribe(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    current_date = datetime.now().strftime("%Y-%m-%d")
    result = subscriptions.insert_one({"name": "Newsletter", "email": email, "date": current_date, "time": "00:00", "subject": "Newsletter Subscription", "message": "Subscribed from Index Page"})
    return {"status": "success", "id": str(result.inserted_id)}

# 4. CART (Shop Page se click ho toh cart page jayega)
@app.post("/api/cart")
async def add_to_cart(
    product_name: str = Form(...),
    product_price: str = Form(...),
    product_img: str = Form(...),
    quantity: int = Form(1),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = cart.insert_one({"product_name": product_name, "product_price": product_price, "product_img": product_img, "quantity": quantity, "date": date, "time": "time", "subject": "Cart Item Added", "message": "Added to Cart from Shop Page"})
    return {"status": "success", "id": str(result.inserted_id)}


# 5. WISHLIST
@app.post("/api/wishlist")
async def add_to_wishlist(
    product_name: str = Form(...),
    product_price: str = Form(...),
    product_img: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = wishlist.insert_one({"product_name": product_name, "product_price": product_price, "product_img": product_img, "date": date, "time": "time", "subject": "Wishlist Item Added", "message": "Added to Wishlist"})
    return {"status": "success", "id": str(result.inserted_id)}

# 6. PLAN REQUEST
@app.post("/api/plan-request")
async def create_plan_request(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = pricing_requests.insert_one({
        "name": name,
        "email": email,
        "date": date,
        "time": time,
        "subject": subject,
        "message": message
    })
    return {"status": "success", "id": str(result.inserted_id)}

# --- GET REQUESTS ---
@app.get("/api/appointments")
def get_appointments():
    data = []
    for item in appointments.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/contacts")
def get_contacts():
    data = []
    for item in contacts.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/subscriptions")
def get_subscriptions():
    data = []
    for item in subscriptions.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/comments")
def get_comments():
    data = []
    for item in comments.find().sort([("_id", -1)]):
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/cart")
def get_cart():
    data = []
    for item in cart.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/wishlist")
def get_wishlist():
    data = []
    for item in wishlist.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

# --- DELETE REQUESTS ---
@app.delete("/api/appointment/{id}")
def delete_appointment(id: str):
    result = appointments.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/contact/{id}")
def delete_contact(id: str):
    result = contacts.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/subscribe/{id}")
def delete_subscribe(id: str):
    result = subscriptions.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/comment/{id}")
def delete_comment(id: str):
    result = comments.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/cart/{id}")
def delete_cart(id: str):
    result = cart.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/wishlist/{id}")
def delete_wishlist(id: str):
    result = wishlist.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

@app.delete("/api/plan-request/{id}")
def delete_plan_request(id: str):
    result = pricing_requests.delete_one({"_id": ObjectId(id)})
    msg = "Deleted" if result.deleted_count == 1 else "Not found"
    return {"message": msg}

# SERVE STATIC FILES
@app.get("/{filename:path}")
def serve_html(filename: str):
    filepath = os.path.join("static", filename)
    if os.path.exists(filepath) and os.path.isfile(filepath):
        return FileResponse(filepath)
    if not filename.endswith(".html"):
        html_path = os.path.join("static", filename + ".html")
        if os.path.exists(html_path):
            return FileResponse(html_path)
    return HTMLResponse(f"<h2>File not found: {filename}</h2>", status_code=404)

# START SERVER
if __name__ == "__main__":
    import uvicorn
    print("Starting Server...")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
