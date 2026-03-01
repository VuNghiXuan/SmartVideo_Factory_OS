import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import config

class NLPProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    # --- HÀM MỚI: TÁCH BIỆT CODE VÀ LỆNH TERMINAL ---
    import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import config

class NLPProcessor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    # --- HÀM MỚI: TÁCH BIỆT CODE VÀ LỆNH TERMINAL ---
    def split_editor_terminal(self, text_content):
        """
        Phân tích text_content để tách phần Code (Editor) và Lệnh (Terminal).
        Quy tắc:
        - Nếu có ký tự '>>', 'PS ', '$ ' hoặc 'C:\\' -> Đó là phần Terminal.
        - Nếu nội dung bắt đầu bằng 'python ', 'pip ', 'cd ' -> Đó là Terminal.
        """
        lines = text_content.split('\n')
        editor_parts = []
        terminal_parts = []

        # Các dấu hiệu nhận biết dòng đó thuộc về Terminal
        terminal_markers = ['>>', 'PS ', '$ ', 'C:\\', 'python ', 'pip ', 'cd ', 'git ']

        for line in lines:
            is_terminal = any(marker in line for marker in terminal_markers)
            if is_terminal:
                # Xóa sạch các dấu hiệu dư thừa để template tự thêm lại cho đẹp
                clean_line = line.replace('>>', '').replace('PS ', '').strip()
                terminal_parts.append(clean_line)
            else:
                editor_parts.append(line)

        # Gộp lại theo định dạng: Code Editor >> Terminal Output
        code = "\n".join(editor_parts).strip()
        terminal = " ".join(terminal_parts).strip() or "Success"
        
        return f"{code} >> {terminal}"

    # --- CÁC HÀM CŨ CỦA MÀY (ĐÃ TỐI ƯU) ---
    def _calculate_best_match(self, query, reference_list, labels, threshold):
        if not reference_list: return None, 0
        documents = [query.lower()] + [ref.lower() for ref in reference_list]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        best_idx = scores.argmax()
        max_score = scores[best_idx]
        return (labels[best_idx], max_score) if max_score >= threshold else (None, max_score)

    def predict_action(self, text_content):
        text_lower = text_content.lower()
        if ".py" in text_lower or "python" in text_lower: return "vsc"
        if ".xlsx" in text_lower or "excel" in text_lower or "sheet" in text_lower: return "excel"
        if "http" in text_lower or "www." in text_lower: return "chrome"

        label, score = self._calculate_best_match(
            text_content, config.REFERENCE_TEXTS, config.REFERENCE_LABELS, config.NLP_THRESHOLD_ACTION
        )
        return label if label else "vsc"

    def find_best_lesson(self, user_prompt, lessons):
        titles = [l['title'] for l in lessons]
        best_title, score = self._calculate_best_match(
            user_prompt, titles, titles, config.NLP_THRESHOLD_LESSON
        )
        if best_title:
            for l in lessons:
                if l['title'] == best_title:
                    l['similarity_score'] = round(float(score), 2)
                    return l
        return None

    