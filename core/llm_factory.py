import os
import requests
from groq import Groq
from google import genai # Thư viện mới nhất của Google
from dotenv import load_dotenv
from config import config

# Nạp biến từ .env
load_dotenv()

class LLMProvider:
    def __init__(self, provider_name=None):
        # Lấy provider từ UI hoặc mặc định
        self.provider = provider_name or config.DEFAULT_PROVIDER
        
    def _get_config(self):
        """Lấy API Key và Model từ .env, nếu thiếu thì lấy từ config.py"""
        prefix = self.provider.upper() # Ví dụ: GEMINI hoặc GROQ
        
        api_key = os.getenv(f"{prefix}_API_KEY")
        model_name = os.getenv(f"{prefix}_MODEL")
        base_url = os.getenv(f"{prefix}_BASE_URL")

        # Fallback về config nếu .env trống
        conf_fallback = config.AI_CONFIG.get(self.provider, {})
        
        return {
            "api_key": api_key or conf_fallback.get("api_key"),
            "model": model_name or conf_fallback.get("model"),
            "base_url": base_url or conf_fallback.get("base_url", "http://localhost:11434")
        }

    def ask(self, prompt, temperature=0):
        conf = self._get_config()
        
        try:
            # --- Nhánh GROQ ---
            if self.provider == "Groq":
                if not conf["api_key"]: return "❌ Thiếu GROQ_API_KEY trong .env"
                client = Groq(api_key=conf["api_key"])
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=conf["model"],
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()

            # --- Nhánh GEMINI (SDK v2.0) ---
            elif self.provider == "Gemini":
                if not conf["api_key"]: return "❌ Thiếu GEMINI_API_KEY trong .env"
                client = genai.Client(api_key=conf["api_key"])
                response = client.models.generate_content(
                    model=conf["model"],
                    contents=prompt
                )
                return response.text.strip()

            # --- Nhánh OLLAMA ---
            elif self.provider == "Ollama":
                url = f"{conf['base_url']}/api/generate"
                payload = {
                    "model": conf["model"], 
                    "prompt": prompt, 
                    "stream": False
                }
                response = requests.post(url, json=payload, timeout=30)
                return response.json().get("response", "").strip()

        except Exception as e:
            return f"❌ Lỗi kết nối {self.provider}: {str(e)}"