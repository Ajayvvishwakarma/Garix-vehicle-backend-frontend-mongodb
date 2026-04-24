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
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# Collections
appointments = db["appointments"]
contacts = db["contacts"]
subscriptions = db["subscriptions"]
comments = db["comments"]
pricing_requests = db["pricing_requests"]

os.makedirs("static", exist_ok=True)

@app.get("/")
def home():
    return FileResponse("static/index.html") if os.path.exists("static/index.html") else {"message": "API is running"}

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

@app.post("/api/contact")
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = contacts.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/subscribe")
async def subscribe(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = subscriptions.insert_one({"name": name, "email": email, "date": date, "time": "time", "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/plan-request")
async def plan_request(
    name: str = Form(...),
    email: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    subject: str = Form(...),
    message: str = Form(None),
):
    result = pricing_requests.insert_one({"name": name, "email": email, "date": date, "time": time, "subject": subject, "message": message})
    return {"status": "success", "id": str(result.inserted_id)}

@app.post("/api/comment")
async def post_comment(
    name: str = Form(...),
    email: str = Form(...),
    comment: str = Form(...),
):
    result = comments.insert_one({"name": name, "email": email, "comment": comment, "date": datetime.now().strftime("%Y-%m-%d")})
    return {"status": "success", "id": str(result.inserted_id)}

# GET Requests
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

@app.get("/api/plan-requests")
def get_plan_requests():
    data = []
    for item in pricing_requests.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

@app.get("/api/comments")
def get_comments():
    data = []
    for item in comments.find():
        item["_id"] = str(item["_id"])
        data.append(item)
    return data

# DELETE Requests
@app.delete("/api/appointment/{id}")
def delete_appointment(id: str):
    from bson import ObjectId
    result = appointments.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"} if result.deleted_count == 1 else {"message": "Not found"}

@app.delete("/api/contact/{id}")
def delete_contact(id: str):
    from bson import ObjectId
    result = contacts.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"} if result.deleted_count == 1 else {"message": "Not found"}

@app.delete("/api/subscribe/{id}")
def delete_subscribe(id: str):
    from bson import ObjectId
    result = subscriptions.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"} if result.deleted_count == 1 else {"message": "Not found"}

@app.delete("/api/plan-request/{id}")
def delete_plan_request(id: str):
    from bson import ObjectId
    result = pricing_requests.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"} if result.deleted_count == 1 else {"message": "Not found"}

@app.delete("/api/comment/{id}")
def delete_comment(id: str):
    from bson import ObjectId
    result = comments.delete_one({"_id": ObjectId(id)})
    return {"message": "Deleted"} if result.deleted_count == 1 else {"message": "Not found"}

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

