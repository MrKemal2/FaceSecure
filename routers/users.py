from datetime import timedelta
import numpy as np
import face_detection
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import database as Db
from security import create_access_token, get_current_user, decrypt_embedding,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import UserPublic
from bson import Binary
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity




router = APIRouter(prefix="/users", tags=["users"])

@router.post("/verify_face")
async def verify_face(request: Request, image_file: UploadFile = File(...)):
    image_bytes = await image_file.read()

    result = face_detection.get_face_embedding(image_bytes)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
    login_embedding = np.array(result["embedding"])

    # Sadece yüz verisi olan kullanıcıları filtrele
    users = list(filter(lambda user: user.get("face_embedding") is not None, Db.get_all_users()))
    
    if not users:
        raise HTTPException(
            status_code=400, 
            detail="Veritabanında yüz verisi olan kullanıcı bulunamadı. Lütfen önce kullanıcı kaydı yapın."
        )

    best_match_user = None
    highest_similarity = 0.0
    
    SIMILARITY_THRESHOLD = 0.75

    

    for user in users:
        encrypted_embedding = user.get("face_embedding")
        
        
        
            
        # MongoDB'den gelen veriyi bytes'a çevir
        try:
            if isinstance(encrypted_embedding, Binary):
                encrypted_embedding = bytes(encrypted_embedding)
            elif not isinstance(encrypted_embedding, bytes):
                print(f"Beklenmeyen veri tipi: {type(encrypted_embedding)} - Kullanıcı: {user.get('username')}")
                continue
                
            decrypted_embedding_list = decrypt_embedding(encrypted_embedding)
            stored_embedding = np.array(decrypted_embedding_list)
        except Exception as e:
            print(f"Hata: {user.get('username')} kullanıcısının yüz verisi çözülemedi: {str(e)}")
            continue
            

        # Embeddings'leri 2D array formatına çevir (cosine_similarity için gerekli)
        login_embedding_2d = login_embedding.reshape(1, -1)
        stored_embedding_2d = stored_embedding.reshape(1, -1)
        similarity = cosine_similarity(login_embedding_2d, stored_embedding_2d)[0][0]

       

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match_user = user
    

    if best_match_user and highest_similarity >= SIMILARITY_THRESHOLD:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": best_match_user["username"]},
            expires_delta=access_token_expires
        )
        return {
            "message": "Kimlik doğrulandı.",
            "username": best_match_user["username"],
            "is_admin": best_match_user.get("is_admin", False),
            "similarity": f"{highest_similarity:.2f}",
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
        
        Db.log_failed_attempt(ip_address=request.client.host,reason= f"Düşük benzerlik skoru: {highest_similarity:.2f}")
        detail_message = (
            "Kimlik doğrulanamadı. Yüz eşleşmedi. "
            f"(Benzerlik: {highest_similarity:.2f}, Gereken: {SIMILARITY_THRESHOLD})"
        )
        raise HTTPException(status_code=401, detail=detail_message)






#------------Admin  giriş kontrolü-------------
@router.post("/admin_token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    
    login_result = Db.admin_login(form_data.username, form_data.password)

    if login_result.get("status") != "success":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz admin kimlik bilgileri",
            headers={"WWW-Authenticate": "Bearer"},
        )

    admin_user = login_result["user"]
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": admin_user["username"]}, expires_delta=access_token_expires
    )
    return {"admin_access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[UserPublic, Depends(get_current_user)]):
    return current_user