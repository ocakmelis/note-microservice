import requests
from fastapi import HTTPException

class SummaryService:
    """Not özetleme servisi"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
    
    def summarize_text(self, text: str) -> str:
        """Metni özetler"""
        
        # Eğer API key yoksa basit özet döndür
        if not self.api_key or self.api_key == "your-api-key-here":
            return self._simple_summary(text)
        
        try:
            # OpenRouter API'ye istek gönder
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"Aşağıdaki notu 3 cümleyle özetle:\n\n{text}"
            
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
                summary = result["choices"][0]["message"]["content"]
                return summary.strip()
            else:
                raise HTTPException(status_code=500, detail="Özet oluşturulamadı")
                
        except Exception as e:
            # Hata olursa basit özet döndür
            return self._simple_summary(text)
    
    def _simple_summary(self, text: str) -> str:
        """API olmadan basit özet oluşturur"""
        words = text.split()
        if len(words) <= 30:
            return text
        
        # İlk 30 kelimeyi al
        summary = " ".join(words[:30]) + "..."
        return summary