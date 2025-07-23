import cv2
import os
import numpy as np
from deepface import DeepFace
import mediapipe as mp
import time
from dotenv import load_dotenv

load_dotenv()

# Yüz tanıma için kullanılacak model (TensorFlow tabanlı)
# Diğer seçenekler: 'Facenet', 'ArcFace', 'OpenFace' vb.
MODEL_NAME = "Facenet"


# MediaPipe Yüz Algılama modelini başlat
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()





def cosine_similarity(embedding1, embedding2):
    """İki embedding vektörü arasındaki kosinüs benzerliğini hesaplar."""
    # Vektörleri düzleştir (eğer çok boyutluysa)
    embedding1 = np.asarray(embedding1).flatten()
    embedding2 = np.asarray(embedding2).flatten()

    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)

    # Sıfıra bölünmeyi önle
    if norm1 == 0 or norm2 == 0:
        return 0.0

    similarity = dot_product / (norm1 * norm2)
    return similarity


# --- Ana Fonksiyonlar ---
def get_face_embedding(image_bytes :bytes):
    """
    Verilen bir görüntüden (bytes formatında) yüzü tespit eder ve
    128 boyutlu bir embedding vektörü döndürür.
    """
    try: 
        #Görüntü bytelarını numpy dizisine çevir
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # MediaPipe ile yüz tespiti yap
        results = face_detection.process(img_rgb)

        if not results.detections:
            return {"status": "error", "message": "Yüz tespit edilemedi."}
        if len(results.detections) > 1:
            return {"status": "error", "message": "Birden fazla yüz tespit edildi. Lütfen tek bir yüz ile deneyin."}
        detection = results.detections[0]
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = img_rgb.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height *  ih)
        x, y, w, h = max(0, x), max(0, y), min(iw - x, w), min(ih - y, h)

        face_img = img_rgb[y:y + h, x:x + w]



        #deepface ile embedding oluştur
        embedding_obj = DeepFace.represent(img_path = face_img , model_name=MODEL_NAME, enforce_detection=False)

        if not embedding_obj:
            return {"status": "error", "message": "Embedding oluşturulamadı."}

        embedding = embedding_obj[0]["embedding"]
        return {"status": "success", "embedding": embedding}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    



