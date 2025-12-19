# JWT ayarları
SECRET_KEY = "gizli-anahtar-buraya-gelecek"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_config():
    return{
        SECRET_KEY: SECRET_KEY,
        ALGORITHM: ALGORITHM,
        ACCESS_TOKEN_EXPIRE_MINUTES: ACCESS_TOKEN_EXPIRE_MINUTES
    }