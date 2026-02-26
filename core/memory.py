# ChromaDB/FAISS: Luu/Tra cuu kien thuc tu bai cu

import chromadb
from config import config
import os

class LongTermMemory:
    def __init__(self, course_id):
        # Tạo thư mục lưu trữ database cho từng khóa học riêng biệt
        self.db_path = os.path.join(config.COURSES_DIR, course_id, "memory_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        # Mỗi khóa học là một "Collection" trong não bộ
        self.collection = self.client.get_or_create_collection(name=f"{course_id}_knowledge")

    def save_lesson_context(self, lesson_id, summary):
        """Lưu tóm tắt bài học vào bộ nhớ"""
        self.collection.add(
            documents=[summary],
            ids=[lesson_id],
            metadatas=[{"type": "lesson_summary"}]
        )

    def search_context(self, query, n_results=3):
        """Tìm kiếm kiến thức liên quan từ các bài cũ"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        # Trả về danh sách các đoạn kiến thức cũ liên quan
        return results['documents'][0] if results['documents'] else []

# Cách dùng sau này: 
# memory = LongTermMemory("python_coban")
# memory.save_lesson_context("lesson_1", "Bài này dạy về cài đặt Python và in Hello World")