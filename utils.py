from passlib.context import CryptContext # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(passsword: str):
    return pwd_context.hash(passsword)

def verify(password, hashed_pass):
    return pwd_context.verify(password, hashed_pass)