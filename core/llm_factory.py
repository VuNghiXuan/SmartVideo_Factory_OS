import os
import re
import json
import requests
import unicodedata
from groq import Groq
from google import genai
from dotenv import load_dotenv
from config import config

load_dotenv()

class LLMProvider:
    def __init__(self, provider_name=None):
        self.provider = provider_name or config.DEFAULT_PROVIDER
        
    def _sanitize_id(self, text):
        """Khắc phục lỗi Validation: Biến 'lớp_học_ai' -> 'lop_hoc_ai'"""
        if not text: return "default_id"
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^a-zA-Z0-9._-]', '_', text)
        return text.strip('_.-')

    def _get_config(self):
        prefix = self.provider.upper()
        api_key = os.getenv(f"{prefix}_API_KEY")
        model_name = os.getenv(f"{prefix}_MODEL")
        conf_fallback = config.AI_CONFIG.get(self.provider, {})
        return {
            "api_key": api_key or conf_fallback.get("api_key"),
            "model": model_name or conf_fallback.get("model")
        }

    def _extract_json(self, text):
        """Gọt vỏ văn bản để lấy đúng JSON bên trong, né lỗi 'Unexpected token D'"""
        try:
            # Tìm đoạn nằm giữa [ ] hoặc { }
            match = re.search(r'(\[.*\]|\{.*\})', text, re.DOTALL)
            if match:
                return match.group(1)
            return text
        except Exception:
            return text

    def ask(self, prompt, temperature=0, context_name=None):
        conf = self._get_config()
        safe_context_name = self._sanitize_id(context_name) if context_name else None
        
        try:
            raw_content = ""
            # --- Nhánh GROQ ---
            if self.provider == "Groq":
                if not conf["api_key"]: return "❌ Thiếu GROQ_API_KEY"
                client = Groq(api_key=conf["api_key"])
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=conf["model"],
                    temperature=temperature
                )
                raw_content = response.choices[0].message.content.strip()

            # --- Nhánh GEMINI ---
            elif self.provider == "Gemini":
                if not conf["api_key"]: return "❌ Thiếu GEMINI_API_KEY"
                client = genai.Client(api_key=conf["api_key"])
                response = client.models.generate_content(
                    model=conf["model"],
                    contents=prompt
                )
                raw_content = response.text.strip()

            # --- BỘ LỌC THẦN THÁNH ---
            # Nếu prompt yêu cầu JSON (thường có chữ JSON hoặc dấu [ trong prompt)
            # thì mình gọt vỏ luôn trước khi trả về
            if "JSON" in prompt.upper() or "[" in prompt:
                return self._extract_json(raw_content)
            
            return raw_content

        except Exception as e:
            if "Validation error" in str(e):
                return f"❌ Lỗi định dạng: Tên '{context_name}' không hợp lệ."
            return f"❌ Lỗi kết nối {self.provider}: {str(e)}"