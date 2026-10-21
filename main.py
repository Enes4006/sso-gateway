from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from security import verify_password, hash_password, create_access_token, decode_access_token
from fastapi import Request

app = FastAPI(
    title="AuthTake SSO Gateway",
    description="Parolasız / Merkezi Kimlik Doğrulama Gateway Simülasyonu",
    version="1.0.0"
)

# OAuth2 şeması: Token'ın nereden alınacağını belirtir
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Simüle edilmiş kullanıcı veritabanı (Gerçek uygulamada PostgreSQL/OpenLDAP olur)
# Not: Parola 'secret123' ifadesinin bcrypt hash'idir.
FAKE_USERS_DB = {
    "enes": {
        "username": "enes",
        "full_name": "Muhammed Enes Baysal",
        "email": "enes@authtake.com",
        "hashed_password": hash_password("secret123"),
        "role": "admin"
    }
}

# --- GÜVENLİK VE TOKEN DOĞRULAMA DEPENDENCY ---
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Gelen isteklerdeki Bearer Token'ı doğrular.
    Her korumalı endpoint bu fonksiyonu çağırarak kimlik denetimi yapar.
    """
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş token (SSO Doğrulama Başarısız)",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    user = FAKE_USERS_DB.get(username)
    if user is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    return user


# --- SSO GATEWAY ENDPOINT'LERİ ---

@app.get("/")
def read_root():
    return {"message": "AuthTake SSO Gateway Çalışıyor!"}


@app.post("/auth/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    user = FAKE_USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Kullanıcı adı veya şifre hatalı",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # --- RİSK TABANLI GÜVENLİK DENETİMİ (Risk-Based Check) ---
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Risk Puanı Hesaplama Simülasyonu
    risk_score = 0
    if client_ip not in ["127.0.0.1", "localhost"]:
        risk_score += 50  # Farklı bir ağdan geliyorsa risk yükselir
        
    print(f"[SECURITY LOG] İstenen Giriş - Kullanıcı: {user['username']} | IP: {client_ip} | Risk Skor: {risk_score}")

    # JWT içine güvenlik metadatalarını ekleme
    token_payload = {
        "sub": user["username"],
        "email": user["email"],
        "role": user["role"],
        "client_ip": client_ip,
        "risk_score": risk_score
    }
    
    access_token = create_access_token(data=token_payload)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "sso_status": "authenticated",
        "security_context": {
            "ip": client_ip,
            "risk_score": risk_score
        }
    }


@app.get("/dashboard")
def get_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Korumalı bir servisin simülasyonu.
    Yalnızca geçerli bir SSO Token'ına sahip kullanıcılar erişebilir.
    """
    return {
        "message": f"Hoş geldin {current_user['full_name']}!",
        "user_info": {
            "email": current_user["email"],
            "role": current_user["role"]
        },
        "system_status": "SSO Doğrulaması Başarılı, Güvenli Alandayken Çalışıyor."
    }