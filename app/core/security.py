from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token", auto_error=False)
security = HTTPBearer()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_refresh_hash(refresh_token):
    return password_hash.hash(refresh_token)
