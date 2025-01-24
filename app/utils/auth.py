from bcrypt import hashpw, gensalt, checkpw # type: ignore
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta

# Configuration
SECRET_KEY = "671df52ff4762004db68f6b0aff77fb4cf0752103d80555472109826b60dfa8569"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# JWT Token Handling
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def hash_password(password: str) -> str:
    """Hashes a plain-text password."""
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
#     return get_context.verify(plain_password, hashed_password)
