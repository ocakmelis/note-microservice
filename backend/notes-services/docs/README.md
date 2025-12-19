# Note Service

Bu proje FastAPI kullanılarak geliştirilmiştir.

## Özellikler
- Kullanıcı yönetimi
- Not yönetimi
- SQL yazmadan ORM kullanımı
- Docker ile çalıştırılabilir

## Kullanılan Teknolojiler
- FastAPI
- SQLAlchemy
- Docker

## Çalıştırma

```bash
docker build -t note-service .
docker run -p 8000:8000 note-service
