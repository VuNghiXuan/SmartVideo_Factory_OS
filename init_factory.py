import os
import json

def create_factory_structure():
    base_dir = "SmartVideo_Factory_OS"
    
    # 1. Danh sách các thư mục cần tạo
    folders = [
        "core",
        "interfaces",
        "engines",
        "storage/courses",
        "assets/branding",
        "assets/lottie",
        "assets/music",
        "assets/templates",
        "workspace",
        "outputs"
    ]

    # 2. Danh sách các file Python và nội dung sơ khởi
    files = {
        "app.py": "# Entry point: Khoi tao Streamlit & Dieu huong Class-based UI",
        "main_orchestrator.py": "# Dispatcher: Nhan kich ban -> Goi Engine -> Noi Video",
        "config.py": "# Cau hinh Global: API Keys, Font, Mau, DNA cua Modules",
        # ".env": "GEMINI_API_KEY=\nELEVENLABS_API_KEY=\nAZURE_SPEECH_KEY=",
        
        # Core
        "core/classifier.py": "# Phung su MiniLM: Nhan dien Module & Logic Type",
        "core/memory.py": "# ChromaDB/FAISS: Luu/Tra cuu kien thuc tu bai cu",
        "core/course_manager.py": "# Quan ly cau truc Phan cap: Catalog -> Course -> Chapter -> Lesson",
        "core/checkpoint.py": "# State manager: Luu tien do render",
        "core/logger.py": "# Ghi log chi tiet loi render",
        
        # Interfaces
        "interfaces/base_ui.py": "class BaseInterface:\n    def display(self): pass",
        "interfaces/dashboard_ui.py": "from .base_ui import BaseInterface\nclass DashboardUI(BaseInterface):\n    def display(self): pass",
        "interfaces/editor_ui.py": "from .base_ui import BaseInterface\nclass EditorUI(BaseInterface):\n    def display(self): pass",
        "interfaces/render_ui.py": "from .base_ui import BaseInterface\nclass RenderUI(BaseInterface):\n    def display(self): pass",
        "interfaces/assets_ui.py": "from .base_ui import BaseInterface\nclass AssetsUI(BaseInterface):\n    def display(self): pass",
        
        # Engines
        "engines/voice_engine.py": "# ElevenLabs/Azure/Edge-TTS + Pydub",
        "engines/logic_engine.py": "# Manim/Graphviz: Render so do luong",
        "engines/code_engine.py": "# Render VSC: Highlight ma nguon",
        "engines/office_engine.py": "# Render Excel/Word: Thao tac o cot",
        "engines/video_engine.py": "# MoviePy Core: Mix layers & Export",
    }

    # 3. Khoi tao các file JSON mẫu
    json_files = {
        "storage/catalog.json": {"total_courses": 0, "courses": []},
    }

    print(f"🚀 Dang khoi tao nha may: {base_dir}...")

    # Tao thu muc
    for folder in folders:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f"  [+] Created folder: {path}")

    # Tao file Python
    for file_path, content in files.items():
        full_path = os.path.join(base_dir, file_path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  [f] Created file: {full_path}")

    # Tao file JSON
    for json_path, data in json_files.items():
        full_path = os.path.join(base_dir, json_path)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"  [j] Created JSON: {full_path}")

    print("\n✅ Da xong! Nha may SmartVideo_Factory_OS da san sang.")
    print("Mày có thể bắt đầu bằng cách mở app.py hoặc config.py.")

if __name__ == "__main__":
    create_factory_structure()