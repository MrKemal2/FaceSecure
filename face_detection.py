import cv2
import os
import numpy as np
from deepface import DeepFace
import mediapipe as mp
import time

from keras_facenet import FaceNet


facenet_model = FaceNet()
# MediaPipe Yüz Algılama modelini başlat
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection()






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
        # Yüz kırpma işlemi
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = img_rgb.shape
        x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height *  ih)
        x, y, w, h = max(0, x), max(0, y), min(iw - x, w), min(ih - y, h)

        face_img = img_rgb[y:y + h, x:x + w]
        face_resized = cv2.resize(face_img, (160, 160))

        # FaceNet modelinin beklediği formata getir (1, 160, 160, 3)
        face_resized = np.expand_dims(face_resized, axis=0)

        # Embedding'i hesapla
        embedding = facenet_model.embeddings(images=face_resized)

        if embedding is None or len(embedding) == 0:
            return {"status": "error", "message": "Embedding oluşturulamadı."}

        # (1, 128) olan embedding'i (128,) formatına getir ve liste olarak döndür
        embedding_obj = embedding[0].tolist()
        return {"status": "success", "embedding": embedding_obj}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    



