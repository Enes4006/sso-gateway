# 🔐 AuthTake SSO Gateway Demo

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-JSON_Web_Token-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Security](https://img.shields.io/badge/Security-OAuth2_%7C_Zero_Trust-red?style=for-the-badge)

Bu proje, **Sıfır Güven (Zero Trust)** prensipleri ve **Merkezi Kimlik ve Erişim Yönetimi (IAM)** mimarisi baz alınarak geliştirilmiş prototip bir **Tekli Oturum Açma (Single Sign-On - SSO) Gateway** uygulamasıdır.

Kullanıcının tek bir merkezi identity provider (SSO Gateway) üzerinden doğrulanmasını ve üretilen imzalı **JWT (JSON Web Token)** yetki belgesi ile bağımsız mikroservislere tekrar şifre girmeden güvenli bir şekilde erişebilmesini sağlar.

---

## 🚀 Öne Çıkan Özellikler

* **Merkezi Kimlik Doğrulama (Identity Provider):** Kullanıcı oturumlarının tek bir güvenli noktadan yönetilmesi.
* **Stateless (Durumsuz) JWT Oturum Yönetimi:** Sunucu tarafında session tutmadan `HS256` şifrelemeli jeton mekanizması.
* **Güvenli Parola Saklama:** Açık metin şifreler yerine `bcrypt` algoritması ile hash'lenmiş veri koruması.
* **Çoklu Mikroservis Desteği:** Bağımsız mikroservislerin (örn: İK Servisi) kendi veritabanlarında şifre tutmadan merkezi SSO token'ı doğrulaması.
* **Risk Tabanlı Güvenlik (Risk-Based Check):** İstek yapılan IP adresi ve istemci ortamına göre dinamik risk skoru üretimi.

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.11+
* **Web Framework:** FastAPI & Uvicorn
* **Güvenlik & Şifreleme:** `python-jose` (JWT), `passlib[bcrypt]` (Hashing)
* **Dokümantasyon:** Swagger UI / ReDoc (FastAPI dahili)

---

## ⚙️ Kurulum ve Çalıştırma

### 1. Depoyu Kopyalayın ve Bağımlılıkları Yükleyin

```bash
# Projeyi klonlayın
git clone [https://github.com/KULLANICI_ADI/sso-gateway-demo.git](https://github.com/KULLANICI_ADI/sso-gateway-demo.git)
cd sso-gateway-demo

# Sanal ortam oluşturun ve aktif edin
python -m venv venv
# Windows için:
venv\Scripts\activate
# Linux/macOS için:
source venv/bin/activate

# Gerekli paketleri yükleyin
pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart


---
Sistemi tam olarak deneyimlemek için iki ayrı terminal pencerisinde iki servisi de başlatın:

1. Terminal - SSO Gateway (Port 8000):

uvicorn main:app --port 8000 --reload

2. Terminal - İK Mikroservisi (Port 8001):

uvicorn client_app:app --port 8001 --reload
---



🧪 Test Adımları
SSO Gateway Dokümantasyonuna Gidin: http://127.0.0.1:8000/docs

Giriş Yapın: /auth/login uç noktası üzerinden test kullanıcısı ile istek atın:

Username: enes

Password: secret123

Token'ı Alın: Dönen yanıt içerisindeki access_token değerini kopyalayın.

İK Servisine Erişin: http://127.0.0.1:8001/docs adresine gidin.

Yetkilendirme Yapın: Sağ üstteki Authorize butonuna tıklayıp kopyaladığınız token'ı yapıştırın.

Korumalı Kaynağı Çağırın: /hr/reports uç noktasını çalıştırarak ikinci bir şifre girmeden verilerin başarıyla çekildiğini doğrulayın.

---
