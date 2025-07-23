from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from typing import Annotated, Optional
from schemas import UserCreate, UserPublic, UserInDB
from security import get_current_admin_user, encrypt_embedding
import database as Db
import numpy as np
import face_detection

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/get_users")
async def get_users(admin: Annotated[UserPublic, Depends(get_current_admin_user)]) -> list[UserPublic]:
    users = Db.get_all_users()
    return list(users)

@router.post("/generate-embedding")
async def generate_embedding_endpoint(image_file: UploadFile = File(...)):
    """Yüz kayıt (enrollment) sırasında tek bir pozdan embedding üretir."""
    image_bytes = await image_file.read()
    result = face_detection.get_face_embedding(image_bytes)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    return {"embedding": result["embedding"]}


@router.post("/create_user")
async def create_user(user_data: UserCreate, admin: Annotated[UserPublic, Depends(get_current_admin_user)]):
    

    if len(user_data.embeddings) == 0:
        raise HTTPException(status_code=400, detail="Kaydedilecek embedding bulunamadı.")
    
    # Kullanıcı adının zaten var olup olmadığını kontrol et
    if Db.get_user(user_data.username):
        raise HTTPException(status_code=400, detail=f"'{user_data.username}' kullanıcı adı zaten mevcut.")

    mean_embedding = np.mean(user_data.embeddings, axis=0).tolist()
    encrypted_embedding = encrypt_embedding(mean_embedding)
    try:
        Db.add_user(
            full_name=user_data.full_name, 
            username=user_data.username, 
            hashed_embeddings=encrypted_embedding
        )
        return {"status": "success", "message": "Kullanıcı başarıyla oluşturuldu"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_user/{username}")
async def delete_user(username: str, admin: Annotated[UserPublic, Depends(get_current_admin_user)]) -> dict:
    if username == admin['username']:
        raise HTTPException(status_code=400, detail="Admin kendi kendini silemez.")
    delete_result = Db.delete_user(username)
    if delete_result.get("status") == "success":
        return {"message": f"{username} kullanıcısı başarıyla silindi."}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{username} adlı kullanıcı bulunamadı")

@router.post("/admin_check")
async def admin_check() -> UserPublic:
    admin_user = Db.get_admin()
    return admin_user