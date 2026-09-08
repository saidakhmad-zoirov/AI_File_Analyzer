import json
import time
import requests
from typing import Optional


class KimiAIClient:
    """
    Kimi K2P6 API bilan bog'lanish uchun client.
    .env faylidan API kalitini o'qiydi.
    """
    
    def __init__(self, api_key: str):
        """
        Args:
            api_key: KIMI_API_KEY qiymati
        """
        self.api_key = api_key
        self.base_url = "https://api.kimi.com/v1"  # Asl URL ni o'zingizga o'zgartiring
        self.model = "kimi-k2p6"
        self.max_retries = 3
        self.timeout = 60
    
    def analyze(self, prompt: str, system_message: Optional[str] = None) -> str:
        """
        AI modeliga prompt yuborish, javobni olish.
        
        Args:
            prompt: Tahlil uchun prompt matni
            system_message: System message (optional)
            
        Returns:
            AI javobi (string)
        """
        if not self.api_key:
            raise ValueError("API kaliti yo'q!")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        messages = []
        
        # System message
        if system_message:
            messages.append({"role": "system", "content": system_message})
        
        # User prompt
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4000,
            "temperature": 0.3,
            "stream": False,
        }
        
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"]
                    else:
                        raise ValueError(f"Nozoki API javobi: {data}")
                
                elif response.status_code == 429:
                    # Rate limit - kutish
                    wait_time = 2 ** attempt
                    print(f"Rate limit! {wait_time} s kutamiz...")
                    time.sleep(wait_time)
                    last_error = "Rate limit"
                    continue
                
                elif response.status_code == 401:
                    raise ValueError("API kaliti noto'g'ri yoki yaroqsiz!")
                
                else:
                    raise ValueError(f"API xatosi ({response.status_code}): {response.text}")
                
            except requests.Timeout:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError("API javobi ketmadi (timeout)")
            
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise ValueError(f"Network xatosi: {str(e)}")
        
        # Biznes holatlari - oxirgi urinish xatosi
        if last_error:
            raise ValueError(f"API bilan bog'lanishda xatolik yuz berdi (oxirgi xato: {last_error})")
        
        raise ValueError("AI bilan bog'lanishda xatolik yuz berdi")
    
    def is_configured(self) -> bool:
        """API kaliti to'g'ri sozlanmaganligini tekshirish."""
        return bool(self.api_key and len(self.api_key) > 10)
