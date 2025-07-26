import time
from datetime import timedelta
import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# Session state başlatma
if 'token' not in st.session_state:
    st.session_state['token'] = None
if 'admin_token' not in st.session_state:
    st.session_state['admin_token'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = "login"  # admin, member

def navigate_to(page_name):
    """Sayfa değiştirmek için kullanılır."""
    st.session_state.page = page_name
    st.rerun()




def admin_login(username, password):

    try:
        response = requests.post(f"{API_URL}/users/admin_token", data={"username": username, "password": password})


        if response.status_code == 200:
            st.session_state.admin_token=response.json()['admin_access_token']
            headers = {"Authorization": f"Bearer {st.session_state.admin_token}"}
            
            user_response = requests.get(f"{API_URL}/users/me", headers=headers)
            if user_response.status_code == 200:
                st.session_state.user = user_response.json()
                st.session_state.username = user_response.json()['username']
                st.session_state.role = user_response.json()['is_admin']
                st.session_state.logged_in = True
                # Role göre sayfa belirle
                if st.session_state.role:
                    navigate_to("admin")
                return True

        elif response.status_code == 401:
            st.sidebar.write("Token alma başarısız - 401 hatası")
            st.error("Giriş başarısız. Lütfen girdiğiniz bilgileri kontrol edin.")
        else:
            st.sidebar.write(f"Beklenmeyen token response: {response.status_code}")
        return False
    except requests.exceptions.ConnectionError:
        st.sidebar.write("API bağlantı hatası")
        st.error("API Sunucusuna bağlanılamıyor")
        return False
    except Exception as e:
        st.sidebar.write(f"Genel hata: {e}")
        st.error(f"Bir hata oluştu: {e}")
        return False


def get_all_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response= requests.get(f"{API_URL}/admin/get_users", headers=headers)
        if response.status_code==200:
            return response.json()
        else:
            try:
                error_detail = response.json().get('detail', 'Bilinmeyen hata')
            except:
                error_detail = response.text or f"HTTP {response.status_code} hatası"
            st.error(f"Kullanıcıları getirirken bir hata oluştu: {error_detail}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("API Sunucusuna bağlanılamıyor")
        return None

def add_user(token, data:dict):
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.post(f"{API_URL}/admin/create_user", headers=headers, json=data)
            if response.status_code==200:
                st.success(f"{data.get('full_name')} adlı kullanıcı başarıyla eklendi!")

        except requests.exceptions.ConnectionError:
            st.error("API sunucusuna bağlanılamıyor")

def delete_user(token, username):
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(f"{API_URL}/admin/delete_user/{username}", headers=headers)
        if response.status_code==200:
            st.success( f"{username} adlı kullanıcı başarıyla silindi!")
        else:
            st.error("Kullanıcı silinemedi")
    except requests.exceptions.ConnectionError:
        st.error("API sunucusuna bağlanılamadı")



def show_login_page():
    tab1, tab2 = st.tabs(["👤 Kullanıcı Girişi (Yüz Tanıma)", "🔑 Admin Girişi"])

    with tab1:
        st.header("Yüz Tanıma ile Giriş")
        st.write("Giriş yapmak için kameradan bir fotoğrafınızı çekin.")
        img_file_buffer = st.camera_input("Kamerayı kullanarak yüzünüzü ortalayın", key="face_login_cam")
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            st.image(img_file_buffer, caption="Yakalanan Görüntü", width=320)
            if st.button("Giriş Yap", key="face_login_button"):
                with st.spinner("Yüzünüz doğrulanıyor... Lütfen bekleyin."):
                    files = {'image_file': ('capture.jpg', bytes_data, 'image/jpeg')}
                    try:
                        response = requests.post(f"{API_URL}/users/verify_face", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            # Oturum bilgilerini ayarla
                            st.session_state.token = data['access_token']
                            st.session_state.username = data['username']
                            st.session_state.role = data['is_admin']
                            st.session_state.logged_in = True
                            st.session_state.page = "member"
                            st.success("Giriş başarılı!")

                            time.sleep(1)
                            st.rerun()
                        else:
                            try:
                                error_detail = response.json().get('detail', 'Bilinmeyen hata')
                            except:
                                error_detail = response.text or f"HTTP {response.status_code} hatası"
                            st.error(f"Giriş başarısız: {error_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("API sunucusuna bağlanılamıyor.")
                    except requests.exceptions.JSONDecodeError:
                        st.error("API'den geçersiz yanıt alındı.")
                    except Exception as e:
                        st.error(f"Beklenmeyen hata: {str(e)}")
    with tab2:
        st.header("Admin Giriş Paneli")
        with st.form("admin_login_form", clear_on_submit=True):
            username = st.text_input("Kullanıcı Adı")
            password = st.text_input("Şifre", type= "password")
            submitted = st.form_submit_button("Giriş Yap")
            if submitted:
                admin_login(username, password)


def logout():
    # Session state'i temizle
    st.session_state.logged_in = False
    st.session_state.token = None
    st.session_state.username = None
    st.session_state.role = False
    st.session_state.page = "login"
    
    
    st.success("Başarıyla çıkış yapıldı!")
    
    
    st.rerun()

def admin_panel():
    st.header("🛠️Admin Paneli")
    st.sidebar.header("Admin Paneli")
    if 'embeddings' not in st.session_state:
        st.session_state.embeddings = []

    MAX_POSES = 10
    
    

    st.subheader("📸Yeni Kullanıcı Ekle")
    st.progress(len(st.session_state.embeddings) / MAX_POSES)
    st.write(f"Kaydedilen Poz Sayısı: {len(st.session_state.embeddings)} / {MAX_POSES}")

    if len(st.session_state.embeddings) < MAX_POSES:
        st.write("Farklı açılardan yüzünüzün fotoğrafını çekin (örn: hafif sağa, sola, yukarı, aşağı).")
        img_file_buffer = st.camera_input("Poz yakalamak için kamerayı kullanın",
                                          key=f"enroll_cam_{len(st.session_state.embeddings)}")

        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            files = {'image_file': ('enroll_capture.jpg', bytes_data, 'image/jpeg')}
            headers = {"Authorization": f"Bearer {st.session_state.admin_token}"}
            try:
                response = requests.post(f"{API_URL}/admin/generate-embedding", files=files, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.embeddings.append(data['embedding'])
                    st.success(f"{len(st.session_state.embeddings)}. poz başarıyla eklendi!")
                    time.sleep(1)
                    st.rerun()
                else:
                    try:
                        error_detail = response.json().get('detail', 'Bilinmeyen hata')
                    except:
                        error_detail = response.text or f"HTTP {response.status_code} hatası"
                    st.error(f"Poz kaydedilemedi: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("API sunucusuna bağlanılamıyor.")
            except requests.exceptions.JSONDecodeError:
                st.error("API'den geçersiz yanıt alındı.")
            except Exception as e:
                st.error(f"Beklenmeyen hata: {str(e)}")
    else:
        st.success(f"{MAX_POSES} farklı poz başarıyla toplandı!")
    
        full_name = st.text_input("Ad Soyad")
        username = st.text_input("Kullanıcı Adı")  # <-- YENİ EKLENDİ

        if st.button("Yüz Kaydını Tamamla"):
            # Gerekli alanların boş olup olmadığını kontrol et
            if not full_name or not username:
                st.warning("Lütfen Ad Soyad ve Kullanıcı Adı alanlarını doldurun.")
            else:
                with st.spinner("Yüz verileriniz işleniyor ve kaydediliyor..."):
                    payload = {
                        "full_name": full_name,
                        "username": username,  # <-- YENİ EKLENDİ
                        "embeddings": st.session_state.embeddings
                    }
                headers = {"Authorization": f"Bearer {st.session_state.admin_token}"}
                try:
                    response = requests.post(f"{API_URL}/admin/create_user", json=payload, headers=headers)
                    if response.status_code == 200:
                        st.success("Yüz kaydınız başarıyla tamamlandı! Artık sisteme giriş yapabilirsiniz.")
                        # Kayıt sonrası state'i temizle
                        del st.session_state.embeddings
                        time.sleep(3)
                        st.rerun() # Sayfayı yenileyerek girdi alanlarını temizle

                    else:
                        try:
                            error_detail = response.json().get('detail', 'Bilinmeyen hata')
                        except:
                            error_detail = response.text or f"HTTP {response.status_code} hatası"
                        st.error(f"Kayıt tamamlanamadı: {error_detail}")
                except requests.exceptions.ConnectionError:
                        st.error("API sunucusuna bağlanılamıyor.")




   
    st.subheader("🪪 Kullanıcı Listesi")

    st.markdown("---")
    header_col1, header_col2, header_col3, header_col4 = st.columns([2, 1, 2, 1])
    with header_col1:
        st.markdown("<h4 style='text-align: left; color: #4682B4;'>Kullanıcı Adı</h4>", unsafe_allow_html=True)
    with header_col2:
        st.markdown("<h4 style='text-align: left; color: #4682B4;'>Tam Adı</h4>", unsafe_allow_html=True)
    with header_col3:
        st.markdown("<h4 style='text-align: left; color: #4682B4;'>Admin Yetkisi</h4>", unsafe_allow_html=True)
    with header_col4:
        st.markdown("<h4 style='text-align: left; color: #4682B4;'>İşlemler</h4>", unsafe_allow_html=True)
    st.markdown("---")


    try:
        users=get_all_users(st.session_state.admin_token)
        if users:
            for user in users:
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                with col1:
                    st.write(user.get('username', 'N/A')) # .get() ile anahtar hatasını önle
                with col2:
                    st.write(user.get('full_name', 'N/A'))
                with col3:
                    if user.get('is_admin', False):
                        st.write("Admin")
                    else:
                        st.write("Üye")
                with col4:
                    if not user.get('is_admin', False):  # Admin kendini silemesin
                        if st.button("Sil", key=f"delete_{user.get('username')}"):
                            delete_user(st.session_state.admin_token, user.get('username'))
                            st.rerun()

    except requests.exceptions.ConnectionError:
        st.error("API sunucusuna bağlanılamıyor.")

    if st.sidebar.button("Çıkış Yap", key="logout_button"):
        logout()
        return  # Fonksiyondan çık


def member_panel():
    st.header("Üye Paneli")
    response = requests.get(f"{API_URL}/users/me", headers={"Authorization": f"Bearer {st.session_state.token}"})
    user_data = response.json()
    st.write("Hoşgeldin ", user_data.get("full_name"))
    if st.button("Çıkış Yap", key="user_logout_button"):
        logout()
        return  # Fonksiyondan çık



st.set_page_config(page_title="FaceSecure")
st.title("FaceSecure")

# Ana uygulama akışı
def main():
    # Session state kontrolü
    if not st.session_state.logged_in or st.session_state.page == "login":
        show_login_page()
    else:
        # Oturum açıksa, doğru sayfayı göster
        if st.session_state.page == "member":
            member_panel()
        elif st.session_state.page == "admin":
            admin_panel()

# Ana fonksiyonu çağır
main()