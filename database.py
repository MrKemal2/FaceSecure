import pymongo.errors
from pymongo import MongoClient
from datetime import datetime,timezone
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

try:
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "denemeFaceSecure")
    
    client = MongoClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db.user_collection
    logs_collection = db.logs
    admin_collection = db.admin_collection
except pymongo.errors.ConnectionFailure:
    print("MongoDB sunucusuna bağlanılamadı")

def get_user(username: str):
    
    admin_user = admin_collection.find_one({"username": username})
    if admin_user:
        # Admin kullanıcısı için is_admin bayrağını ayarla
        admin_user["is_admin"] = True
        return admin_user

    
    user = collection.find_one({"username": username})
    if user:
        user.setdefault("is_admin", False)
        return user

    return None

def get_admin():
    admin_user = collection.find_one({"is_admin": True})
    return admin_user is not None

def add_user(full_name: str, username: str, hashed_embeddings: bytes):
    """Normal kullanıcıyı tam ad, kullanıcı adı ve yüz verisiyle ekler."""
    collection.insert_one({
        "full_name": full_name,
        "username": username,
        "face_embedding": hashed_embeddings,
        "is_admin": False  # Her normal kullanıcı admin değildir
    })

def get_all_users():
    return collection.find()

def delete_user(username):
    result  = collection.delete_one({"username": username})

    if result.deleted_count > 0 :
        return {"status": "success"}
    else:
        return {"status": "error", "message": "Kullanıcı bulunamadı"}

def log_failed_attempt(ip_address: str, reason: str):
    """Başarısız giriş denemelerini loglar."""
    log_data = {
        "ip_address": ip_address,
        "timestamp": datetime.now(timezone.utc),
        "status": "failed_login",
        "reason": reason
    }
    logs_collection.insert_one(log_data)

def admin_login(username: str, password: str):
    """Admin giriş işlemi. Bu fonksiyon zaten doğru koleksiyonu kullanıyor."""
    admin_user = admin_collection.find_one({"username": username})
    # ÖNEMLİ: Gerçek bir projede şifreler her zaman hash'lenerek saklanmalıdır!
    # Bu sadece bir örnek.
    if admin_user and admin_user.get("password") == password:
        return {"status": "success", "user": admin_user}
    return {"status": "error", "message": "Geçersiz admin kimlik bilgileri"}