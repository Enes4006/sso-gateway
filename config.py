import os

# JWT için gizli anahtar (Gerçek prodüksiyon sistemlerinde rastgele karmaşık bir string olmalıdır)
SECRET_KEY = "authtake-sso-secret-key-super-secure-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60