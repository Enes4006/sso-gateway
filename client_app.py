
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from security import decode_access_token


# İK mikroservisi: 8001 portunda çalışacak
app = FastAPI(
    title="AuthTake Client App (İK Servisi)",
    description="SSO Gateway ile entegre çalışan bağımsız mikroservis",
    version="1.0.0"
)

# HTTP Bearer token doğrulaması
security = HTTPBearer(auto_error=False)


def verify_sso_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Gelen Bearer Token'ı alır ve doğrular.
    """

    # Authorization başlığı veya Bearer token yoksa
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer Token eksik. Lütfen önce SSO Gateway üzerinden giriş yapın.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Token'ı security.py içindeki fonksiyonla doğrula
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz veya süresi dolmuş SSO Token!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


@app.get("/")
def read_root():
    return {
        "service": "İK Yönetim Servisi",
        "status": "Aktif"
    }


@app.get("/hr/reports")
def get_hr_reports(
    current_user: dict = Depends(verify_sso_token)
):
    """
    Geçerli SSO Token'ına sahip kullanıcılar erişebilir.
    """

    return {
        "service_name": "İK Raporlama Servisi",
        "accessed_by": current_user.get("sub"),
        "user_email": current_user.get("email"),
        "user_role": current_user.get("role"),
        "reports": [
            {
                "id": 101,
                "title": "2026 Q3 Performans Raporu",
                "status": "Onaylandı"
            },
            {
                "id": 102,
                "title": "Ekim Ayı Personel İzin Listesi",
                "status": "Beklemede"
            }
        ],
        "message": (
            "SSO doğrulaması başarılı! "
            "İkinci bir şifre girmeden bu servise eriştiniz."
        )
    }
