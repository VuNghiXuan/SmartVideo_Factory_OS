# Quan ly cau truc Phan cap: Catalog -> Course -> Chapter -> Lesson

import os
import json
from config import config

class CourseManager:
    def __init__(self):
        self.catalog_path = config.CATALOG_JSON
        self.courses_dir = config.COURSES_DIR
        self._init_catalog()

    def _init_catalog(self):
        """Khởi tạo file catalog nếu chưa có"""
        if not os.path.exists(self.catalog_path):
            with open(self.catalog_path, 'w', encoding='utf-8') as f:
                json.dump({"total_courses": 0, "courses": []}, f, indent=4)

    def create_course(self, course_name, author="Vũ"):
        """Tạo một khóa học mới hoàn toàn"""
        course_id = course_name.lower().replace(" ", "_")
        course_path = os.path.join(self.courses_dir, course_id)
        
        # 1. Tạo thư mục khóa học
        os.makedirs(os.path.join(course_path, "chapters"), exist_ok=True)
        os.makedirs(os.path.join(course_path, "history"), exist_ok=True)

        # 2. Tạo file meta.json (Sổ hộ khẩu riêng)
        meta_data = {
            "course_id": course_id,
            "course_name": course_name,
            "author": author,
            "branding": config.DEFAULT_BRANDING,
            "structure": [] # Chứa chapters và lessons
        }
        with open(os.path.join(course_path, "course_meta.json"), 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=4, ensure_ascii=False)

        # 3. Cập nhật Catalog tổng
        self._update_catalog(course_id, course_name, course_path)
        return course_id

    def _update_catalog(self, course_id, name, path):
        with open(self.catalog_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            # Kiểm tra nếu đã tồn tại thì thôi
            if not any(c['id'] == course_id for c in data['courses']):
                data['courses'].append({"id": course_id, "name": name, "path": path})
                data['total_courses'] = len(data['courses'])
                f.seek(0)
                json.dump(data, f, indent=4, ensure_ascii=False)
                f.truncate()

    def get_catalog(self):
        """Hàm trả về toàn bộ danh mục để hiển thị lên Dashboard"""
        try:
            if not os.path.exists(self.catalog_path):
                self._init_catalog()
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Lỗi đọc catalog: {e}")
            return {"total_courses": 0, "courses": []}

    def add_course(self, course_name, author="Vũ"):
        """Đổi tên từ create_course thành add_course để khớp với nút bấm Dashboard"""
        course_id = course_name.lower().replace(" ", "_")
        course_path = os.path.join(self.courses_dir, course_id)
        
        # 1. Tạo thư mục cấu trúc
        os.makedirs(os.path.join(course_path, "chapters"), exist_ok=True)
        os.makedirs(os.path.join(course_path, "history"), exist_ok=True)

        # 2. Tạo 'hộ khẩu' meta.json
        meta_data = {
            "course_id": course_id,
            "course_name": course_name,
            "author": author,
            "structure": []
        }
        with open(os.path.join(course_path, "course_meta.json"), 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=4, ensure_ascii=False)

        # 3. Cập nhật Catalog tổng
        self._update_catalog(course_id, course_name, course_path)
        return course_id