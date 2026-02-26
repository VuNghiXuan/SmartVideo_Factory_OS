
"""Cập nhật core/classifier.py (Dùng não linh hoạt)
Bây giờ, thằng Classifier sẽ không quan tâm Groq là thằng nào nữa, nó chỉ cần biết gọi "Bộ não đang được chọn"."""


from .llm_factory import LLMProvider
from config import config

class SceneClassifier:
    def __init__(self, provider_name=None):
        # Mày có thể truyền provider_name từ giao diện Streamlit vào đây
        self.llm = LLMProvider(provider_name)
        self.dna = config.MODULE_DNA

    def classify_scene(self, scene_text):
        prompt = f"""
        Phân loại kịch bản video dựa trên nội dung: "{scene_text}"
        Dữ liệu ADN Modules: {self.dna}
        Trả về DUY NHẤT tên module phù hợp nhất.
        """
        # Gọi bộ não đã được chọn
        return self.llm.ask(prompt)