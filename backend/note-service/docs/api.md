# Note Service API

## Teknolojiler
- FastAPI
- SQLAlchemy ORM
- Docker

## Endpointler

### 1. Authentication (Auth Service)

#### POST /auth/register
Yeni kullanıcı kaydı oluşturur.

**Request:**

POST /auth/register
Content-Type: application/json
```
{
  "username": "melis",
  "password": "SecurePass123!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "melis"
}
```

**Hata Durumları:**
- 400: Kullanıcı adı zaten kullanılıyor
- 422: Geçersiz veri formatı

---

### POST /users
```json
{
  "username": "melis",
  "password": "123456"
}
