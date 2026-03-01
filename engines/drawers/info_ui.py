import numpy as np
from PIL import Image, ImageDraw
from .base import BaseDrawer
from .config import COLOR_MINDMAP, COLOR_SUMMARY

class InfoDrawer(BaseDrawer):
    @classmethod
    def draw_document(cls, t, duration, **kwargs):
        """Doc: Lấy title và content từ JSON"""
        title = kwargs.get('title', 'Tài Liệu Hướng Dẫn')
        content = kwargs.get('content', '')

        img = Image.new('RGB', (1920, 1080), (250, 250, 250))
        draw = ImageDraw.Draw(img)
        f = cls.get_fonts(45)
        
        # Header bar
        draw.rectangle([(0, 0), (1920, 120)], fill=(0, 120, 215))
        draw.text((60, 35), f"📘 {title}", font=f['bold'], fill="white")
        cls.draw_win11_controls(draw, 1920)
        
        # Hiệu ứng hiện nội dung
        draw.multiline_text((100, 220), content, font=f['code'], fill=(40, 40, 40), spacing=25)
        
        # cls.draw_smooth_cursor(img, t, duration)
        return np.array(img)
    
    @classmethod
    def draw_mindmap(cls, t, duration, **kwargs):
        """Mindmap & Summary: Hiển thị lộ trình bài học hoặc tổng kết dưới dạng sơ đồ"""
        title = kwargs.get('title', 'Lộ Trình Bài Học')
        content = kwargs.get('content', '')
        # Tự động đổi màu nếu là tổng kết
        is_summary = "tổng kết" in title.lower() or "summary" in title.lower()
        theme_color = (255, 87, 34) if is_summary else (0, 150, 136) # Cam hoặc Xanh teal
        
        # 1. Khởi tạo nền sáng chuyên nghiệp
        img = Image.new('RGB', (1920, 1080), (240, 242, 245))
        draw = ImageDraw.Draw(img)
        f = cls.get_fonts(40)
        
        # 2. Vẽ Header bar
        draw.rectangle([(0, 0), (1920, 100)], fill=theme_color)
        draw.text((60, 25), f"📌 {title.upper()}", font=f['bold'], fill="white")
        cls.draw_win11_controls(draw, 1920)

        # 3. Xử lý danh sách các bước
        steps = [s.strip() for s in content.split('\n') if s.strip()]
        if not steps: steps = ["Bắt đầu...", "Thực hành...", "Hoàn thành!"]

        # 4. Vẽ các Node sơ đồ
        node_width = 500
        node_height = 120
        start_x = 100
        start_y = 200
        
        for i, step in enumerate(steps):
            # Tính toán vị trí theo kiểu Z-shape hoặc dọc
            # Ở đây tao vẽ dạng danh sách thẻ (Card list) có hiệu ứng hiện dần
            y_pos = start_y + (i * (node_height + 40))
            
            # Chỉ vẽ nếu thời gian t đã chạy đến bước đó
            appearance_time = (i / len(steps)) * (duration * 0.8)
            if t > appearance_time:
                # Vẽ bóng đổ (Shadow) cho Card
                draw.rectangle([(start_x + 5, y_pos + 5), (start_x + node_width + 1205, y_pos + node_height + 5)], fill=(200, 200, 200))
                # Vẽ Card chính
                draw.rectangle([(start_x, y_pos), (start_x + node_width + 1200, y_pos + node_height)], fill="white", outline=theme_color, width=2)
                
                # Vẽ số thứ tự (Circle)
                circle_r = 30
                circle_center = (start_x + 60, y_pos + node_height // 2)
                draw.ellipse([(circle_center[0]-circle_r, circle_center[1]-circle_r), 
                             (circle_center[0]+circle_r, circle_center[1]+circle_r)], fill=theme_color)
                draw.text((circle_center[0]-12, circle_center[1]-20), str(i+1), font=f['bold'], fill="white")
                
                # Vẽ nội dung chữ
                draw.text((start_x + 130, y_pos + 35), step, font=f['ui'], fill=(50, 50, 50))
                
                # Vẽ mũi tên nối giữa các Node (trừ node cuối)
                if i < len(steps) - 1:
                    arrow_y = y_pos + node_height
                    draw.line([(start_x + 60, arrow_y), (start_x + 60, arrow_y + 40)], fill=theme_color, width=5)

        return np.array(img)