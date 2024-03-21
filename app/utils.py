from passlib.context import CryptContext

## declare hashing algorithm
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_content.hash(password)

## take raw password and compare to hash in database
def verify(plain_password, hashed_password):
    return pwd_content.verify(plain_password, hashed_password)