# Cau hinh Global: API Keys, Font, Mau, DNA cua Modules


import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Config:
    # 1. Cấu hình AI Provider
    DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "Groq")
    
    # 2. Chi tiết từng AI
    AI_CONFIG = {
        "Groq": {
            "api_key": os.getenv("GROQ_API_KEY"),
            "model": os.getenv("GROQ_MODEL")
        },
        "Gemini": {
            "api_key": os.getenv("GOOGLE_API_KEY"),
            "model": os.getenv("GEMINI_MODEL")
        },
        "Ollama": {
            "base_url": os.getenv("OLLAMA_BASE_URL"),
            "model": os.getenv("OLLAMA_MODEL")
        }
    }

    # 3. Quản lý đường dẫn (Paths)
    STORAGE_DIR = os.getenv("STORAGE_PATH", "storage/")
    CATALOG_JSON = os.getenv("CATALOG_FILE", "storage/catalog.json")
    COURSES_DIR = os.getenv("COURSE_DATA_PATH", "storage/courses/")
    WORKSPACE_DIR = os.getenv("WORKSPACE_PATH", "workspace/")
    OUTPUT_DIR = os.getenv("OUTPUT_PATH", "outputs/")
    
    # 4. "ADN" của Modules (Để Classifier nhận diện)
    MODULE_DNA = {
        "excel_expert": "hàm vlookup, bảng tính, định dạng ô, biểu đồ, excel, sheet",
        "code_vsc": "lập trình python, hàm, class, terminal, debug, mã nguồn",
        "logic_engine": "giải thích quy trình, sơ đồ luồng, tại sao, mối liên hệ, logic",
        "intro_outro": "chào mừng, kết thúc, hẹn gặp lại, tổng kết bài học"
    }

    # 5. Cấu hình Branding mặc định (Có thể ghi đè bởi course_meta.json)
    DEFAULT_BRANDING = {
        "primary_color": "#1E90FF",
        "font_family": "Be Vietnam Pro",
        "voice_provider": "Edge-TTS"
    }

    # 6. Voice
    VOICE_SETTINGS = {
        "default_voice": "vi-VN-HoaiMyNeural", # Giọng nữ miền Nam
        "alt_voice": "vi-VN-NamMinhNeural",     # Giọng nam miền Bắc
        "music_volume": -20                     # Độ nhỏ của nhạc nền
    }

config = Config()