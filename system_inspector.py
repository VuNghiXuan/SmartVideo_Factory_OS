import os
import importlib.util
from dotenv import load_dotenv

def check_file(path, description):
    if os.path.exists(path):
        print(f"✅ {description}: Đã tìm thấy ({path})")
        return True
    else:
        print(f"❌ {description}: THIẾU! (Cần tạo: {path})")
        return False

def check_library(lib_name):
    if importlib.util.find_spec(lib_name):
        print(f"✅ Library '{lib_name}': Đã cài đặt")
        return True
    else:
        print(f"❌ Library '{lib_name}': CHƯA CÀI! (Hãy chạy: pip install {lib_name})")
        return False

def inspect_system():
    print("="*50)
    print("🔍 SMARTVIDEO FACTORY - HỆ THỐNG KIỂM TRA TỰ ĐỘNG")
    print("="*50)

    # 1. Kiểm tra cấu trúc thư mục & File quan trọng
    files_to_check = {
        "app.py": "File chạy chính (Main App)",
        "config.py": "File cấu hình hệ thống",
        ".env": "File bảo mật API Keys",
        "core/llm_factory.py": "Bộ não AI",
        "core/course_manager.py": "Quản lý khóa học",
        "core/memory.py": "Bộ nhớ ChromaDB",
        "interfaces/editor_ui.py": "Giao diện biên tập",
        "interfaces/render_ui.py": "Giao diện Render",
        "main_orchestrator.py": "Bộ điều phối tổng",
        "engines/voice_engine.py": "Lõi thu âm",
        "engines/video_engine.py": "Lõi dựng video"
    }
    
    missing_files = 0
    for path, desc in files_to_check.items():
        if not check_file(path, desc):
            missing_files += 1

    print("\n" + "-"*30)
    # 2. Kiểm tra Thư viện (Dependencies)
    libs_to_check = [
        "streamlit", "dotenv", "groq", "google.genai", 
        "chromadb", "moviepy", "edge_tts"
    ]
    for lib in libs_to_check:
        check_library(lib)

    print("\n" + "-"*30)
    # 3. Kiểm tra API Keys trong .env
    load_dotenv()
    keys = ["GROQ_API_KEY", "GEMINI_API_KEY"]
    for key in keys:
        if os.getenv(key):
            print(f"🔑 {key}: Đã cấu hình")
        else:
            print(f"⚠️ {key}: Trống (AI sẽ không hoạt động nếu thiếu)")

    print("\n" + "="*50)
    if missing_files == 0:
        print("🚀 HỆ THỐNG SẴN SÀNG CHIẾN ĐẤU!")
    else:
        print(f"⚠️ BẠN CÒN THIẾU {missing_files} FILE. HÃY HOÀN THIỆN TRƯỚC KHI CHẠY.")
    print("="*50)

if __name__ == "__main__":
    inspect_system()