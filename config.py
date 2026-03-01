# Cau hinh Global: API Keys, Font, Mau, DNA cua Modules

import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Config:
    # --- 0. ĐƯỜNG DẪN GỐC (ROOT) ---
    # Lấy đường dẫn tuyệt đối của thư mục chứa file config.py này
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # --- 1. Cấu hình AI Provider ---
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

    # --- 3. QUẢN LÝ ĐƯỜNG DẪN (PATHS) ---
    
    # Dữ liệu biến đổi (Storage)
    STORAGE_DIR = os.path.join(BASE_DIR, "storage")
    CATALOG_JSON = os.path.join(STORAGE_DIR, "catalog.json")
    COURSES_DIR = os.path.join(STORAGE_DIR, "courses")
    WORKSPACE_DIR = os.path.join(STORAGE_DIR, "workspace")
    OUTPUT_FOLDER_NAME = "outputs"

    # --- 4. KHO TEMPLATES DÙNG CHUNG (NẰM Ở GỐC - CÙNG CẤP APP.PY) ---
    # Sửa từ STORAGE_DIR sang BASE_DIR để đưa ra ngoài gốc
    TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
    
    # Đảm bảo các thư mục quan trọng luôn tồn tại
    os.makedirs(STORAGE_DIR, exist_ok=True)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "assets"), exist_ok=True)

    # 5. "ADN" của Modules (Để Classifier nhận diện)
    MODULE_DNA = {
        "excel_expert": "hàm vlookup, bảng tính, định dạng ô, biểu đồ, excel, sheet",
        "code_vsc": "lập trình python, hàm, class, terminal, debug, mã nguồn",
        "logic_engine": "giải thích quy trình, sơ đồ luồng, tại sao, mối liên hệ, logic",
        "intro_outro": "chào mừng, kết thúc, hẹn gặp lại, tổng kết bài học"
    }

    # 6. Cấu hình Branding mặc định
    DEFAULT_BRANDING = {
        "primary_color": "#1E90FF",
        "font_family": "Be Vietnam Pro",
        "voice_provider": "Edge-TTS"
    }

    # 7. Voice
    VOICE_SETTINGS = {
        "default_voice": "vi-VN-HoaiMyNeural", # Giọng nữ miền Nam
        "alt_voice": "vi-VN-NamMinhNeural",     # Giọng nam miền Bắc
        "music_volume": -20 
    }

    # 8. Danh sách các module giao diện hỗ trợ render HTML
    SUPPORTED_HTML_MODULES = ["excel", "vsc", "chrome", "word", "txt"]
    REFERENCE_LABELS = ["excel", "vsc", "chrome", "word", "txt"]
    # Cập nhật trong config.py
    REFERENCE_TEXTS = [
        "ghi vào ô tính toán bảng tính hàng cột hàm công thức vlookup sum excel format sheet dữ liệu pivot biểu đồ", # EXCEL
        "viết mã lập trình python script terminal vsc code biên dịch biến class def import mã nguồn thực thi",    # VSC
        "mở trang web trình duyệt tìm kiếm google download tải link url chrome website truy cập tham khảo tra cứu", # CHROME
        "soạn thảo văn bản trình bày word văn thư đoạn văn font chữ in ấn tài liệu trang giấy ký tên",            # WORD
        "ghi chú nhanh nội dung thô notepad đơn giản txt lưu trữ note log văn bản không định dạng"                # TXT
    ]

    # Ngưỡng tin cậy
    NLP_THRESHOLD_ACTION = 0.1
    NLP_THRESHOLD_LESSON = 0.2

    # --- 9. FIX LỖI "NO ATTRIBUTE" VÀ ASSETS ---
    DEFAULT_VOICE = VOICE_SETTINGS["default_voice"]
    MUSIC_VOLUME = VOICE_SETTINGS["music_volume"]

    # Đường dẫn ảnh nền mặc định (Ưu tiên file ở gốc, sau đó đến assets)
    DEFAULT_BG_PATH = os.path.join(BASE_DIR, "background.jpg")
    if not os.path.exists(DEFAULT_BG_PATH):
        DEFAULT_BG_PATH = os.path.join(BASE_DIR, "assets", "default_bg.png")

# Khởi tạo đối tượng config
config = Config()

# Kiểm tra nhanh khi khởi động
if __name__ == "__main__":
    print(f"✅ Config Loaded từ: {config.BASE_DIR}")
    print(f"📁 Templates Dir : {config.TEMPLATES_DIR}")
    print(f"📁 Storage Dir: {config.STORAGE_DIR}")
    print(f"🖼️ Default BG Path: {config.DEFAULT_BG_PATH}")

    
