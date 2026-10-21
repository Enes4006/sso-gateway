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

## 📐 Sistem Mimarisi
