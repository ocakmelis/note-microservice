import requests
from fastapi import HTTPException

class CategoryService:
    """Not kategorilendirme"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def generate_tags(self, text: str) -> list[str]:
        """Metin için etiketler oluşturur"""
        
        # Eğer API key yoksa basit etiketler döndür
        if not self.api_key or self.api_key == "your-api-key-here":
            return self._simple_tags(text)
        
        try:
            # OpenRouter API'ye istek gönder
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"Bu not için uygun 3 anahtar kelime/etiket üret. Yanıtın sadece kelimeler olsun, virgülle ayrılmış:\n\n{text}"
            
            data = {
                "model": "meta-llama/llama-3.2-3b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                tags_text = result["choices"][0]["message"]["content"]
                
                # Virgülle ayrılmış etiketleri ayır
                tags = [tag.strip() for tag in tags_text.split(",")]
                return tags[:3]  # İlk 3 etiketi al
            else:
                raise HTTPException(status_code=500, detail="Etiketler oluşturulamadı")
                
        except Exception as e:
            # Hata olursa basit etiketler döndür
            return self._simple_tags(text)
    
    def _simple_tags(self, text: str) -> list[str]:
        """API olmadan basit etiketler oluşturur"""
        # En sık kullanılan kelimeleri bul
        words = text.lower().split()
        
        # Çok kısa kelimeleri çıkar
        words = [w for w in words if len(w) > 3]
        
        if not words:
            return ["genel"]
        
        # İlk 3 kelimeyi etiket olarak döndür
        unique_words = []
        for word in words:
            if word not in unique_words:
                unique_words.append(word)
            if len(unique_words) == 3:
                break
        
        return unique_words if unique_words else ["genel"]
