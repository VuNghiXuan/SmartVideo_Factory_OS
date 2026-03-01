# Quan ly cau truc Phan cap: Catalog -> Course -> Chapter -> Lesson

import os
import json
from config import config
from core.nlp_processor import NLPProcessor  # Import chuyên gia NLP dùng chung

class CourseManager:
    def __init__(self):
        self.catalog_path = config.CATALOG_JSON
        self.courses_dir = config.COURSES_DIR
        self.nlp = NLPProcessor()  # Khởi tạo công cụ NLP
        self._init_catalog()

    def _init_catalog(self):
        """Khởi tạo file catalog nếu chưa có"""
        if not os.path.exists(self.catalog_path):
            with open(self.catalog_path, 'w', encoding='utf-8') as f:
                json.dump({"total_courses": 0, "courses": []}, f, indent=4)

    def add_course(self, course_name, author="Vũ"):
        """Tạo khóa học mới và cập nhật catalog"""
        course_id = course_name.lower().replace(" ", "_")
        course_path = os.path.join(self.courses_dir, course_id)
        
        # 1. Tạo cấu trúc thư mục
        os.makedirs(os.path.join(course_path, "chapters"), exist_ok=True)
        os.makedirs(os.path.join(course_path, "history"), exist_ok=True)

        # 2. Tạo file meta.json
        meta_data = {
            "course_id": course_id,
            "course_name": course_name,
            "author": author,
            "branding": getattr(config, 'DEFAULT_BRANDING', {}),
            "structure": [] 
        }
        meta_path = os.path.join(course_path, "course_meta.json")
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(meta_data, f, indent=4, ensure_ascii=False)

        # 3. Cập nhật Catalog
        self._update_catalog(course_id, course_name, course_path)
        return course_id

    def _update_catalog(self, course_id, name, path):
        # CÁCH AN TOÀN TUYỆT ĐỐI: 
        # Không quan tâm path tuyệt đối là gì, ta chỉ lưu cấu trúc chuẩn của Project
        relative_path = os.path.join("storage", "courses", course_id)

        with open(self.catalog_path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            # Kiểm tra xem khóa học đã có trong catalog chưa
            idx = next((i for i, c in enumerate(data['courses']) if c['id'] == course_id), -1)
            
            new_course_data = {
                "id": course_id, 
                "name": name, 
                "path": relative_path # Ghi vào JSON: storage/courses/py_basic
            }

            if idx == -1:
                data['courses'].append(new_course_data)
            else:
                # Nếu đã có thì cập nhật lại (để sửa đống đường dẫn tuyệt đối cũ)
                data['courses'][idx] = new_course_data
                
            data['total_courses'] = len(data['courses'])
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()

    def get_catalog(self):
        try:
            if not os.path.exists(self.catalog_path):
                return {"total_courses": 0, "courses": []}
                
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for course in data.get('courses', []):
                p = course['path']
                # Nếu đường dẫn không phải tuyệt đối (không bắt đầu bằng C:\ hoặc D:\)
                if not os.path.isabs(p):
                    # Nối nó với BASE_DIR của config hiện tại
                    course['path'] = os.path.abspath(os.path.join(config.BASE_DIR, p))
            
            return data
        except Exception as e:
            print(f"❌ Lỗi đọc catalog: {e}")
            return {"total_courses": 0, "courses": []}

    # --- PHẦN XỬ LÝ DỮ LIỆU LESSON ---

    def get_course_lessons(self, course_id):
        """Lấy danh sách phẳng tất cả lesson để phục vụ so sánh"""
        course_path = os.path.join(self.courses_dir, course_id)
        meta_file = os.path.join(course_path, "course_meta.json")
        
        if not os.path.exists(meta_file):
            return []

        with open(meta_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        all_lessons = []
        for chapter in data.get('structure', []):
            for lesson in chapter.get('lessons', []):
                # Gắn thêm ID chapter để biết lesson này thuộc chapter nào
                lesson['chapter_id'] = chapter.get('id')
                all_lessons.append(lesson)
        return all_lessons

    def find_lesson_by_prompt(self, user_prompt, course_id):
        """
        Ủy quyền cho NLPProcessor tìm bài học phù hợp nhất.
        Giúp code ở đây cực kỳ ngắn gọn.
        """
        lessons = self.get_course_lessons(course_id)
        if not lessons:
            return None
        
        # Gọi chuyên gia NLP xử lý tính toán Cosine
        return self.nlp.find_best_lesson(user_prompt, lessons)