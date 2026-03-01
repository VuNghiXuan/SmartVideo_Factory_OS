import numpy as np
from PIL import Image, ImageDraw
from .base import BaseDrawer
from .config import EXCEL_GREEN, BG_EXCEL_GRAY

class ExcelDrawer(BaseDrawer):
    @classmethod
    def draw_excel(cls, t, duration, **kwargs):
        """Excel: Giao diện Office 365 đầy đủ Logo, Tabs Menu, Sheet và Grid"""
        file_name = kwargs.get('file_name', 'Data_Automation.xlsx')
        data_content = kwargs.get('content', 'Dữ liệu đang được xử lý...')
        
        # 1. Khởi tạo
        img = Image.new('RGB', (1920, 1080), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        f = cls.get_fonts(24) # Font nhỏ hơn cho menu
        f_ui = cls.get_fonts(28)
        
        excel_green = (33, 115, 70)
        bg_gray = (243, 243, 243)

        # --- 2. THANH TIÊU ĐỀ (Top Bar) ---
        draw.rectangle([(0, 0), (1920, 45)], fill=excel_green)
        # Logo X
        draw.rectangle([(15, 8), (40, 33)], fill="white")
        draw.text((22, 7), "X", font=f['ui'], fill=excel_green)
        # Tên file
        draw.text((60, 8), f"{file_name} - Excel", font=f['ui'], fill="white")
        cls.draw_win11_controls(draw, 1920, is_dark=False)

        # --- 3. HỆ THỐNG TABS MENU (Ribbon Tabs) ---
        # Nền của dải Menu
        draw.rectangle([(0, 45), (1920, 90)], fill="white")
        
        # Tab "File" đặc biệt (Nền xanh chữ trắng)
        draw.rectangle([(0, 45), (80, 90)], fill=excel_green)
        draw.text((18, 55), "File", font=f['ui'], fill="white")
        
        # Các Tab khác
        menus = ["Home", "Insert", "Page Layout", "Formulas", "Data", "Review", "View"]
        x_offset = 100
        for menu in menus:
            # Highlight Tab "Home" hoặc "Data" tùy cảnh (ở đây mặc định Home)
            if menu == "Home":
                draw.line([(x_offset, 88), (x_offset + 60, 88)], fill=excel_green, width=3)
                draw.text((x_offset, 55), menu, font=f['ui'], fill=excel_green)
            else:
                draw.text((x_offset, 55), menu, font=f['ui'], fill=(100, 100, 100))
            x_offset += 130

        # --- 4. THANH CÔNG THỨC (Formula Bar) ---
        draw.rectangle([(0, 90), (1920, 135)], fill=bg_gray)
        # Ô địa chỉ (ví dụ B2)
        draw.rectangle([(10, 98), (70, 128)], outline=(200, 200, 200), fill="white")
        draw.text((20, 100), "A1", font=f['ui'], fill="black")
        
        draw.text((95, 100), "fx", font=f['code'], fill="gray")
        draw.line([(130, 102), (130, 125)], fill=(200, 200, 200)) # Ngăn cách
        
        if t > duration * 0.4:
            # Chữ chạy trên thanh công thức
            display_text = data_content[:int(t*15)] if t < duration else data_content
            draw.text((150, 100), display_text, font=f['ui'], fill="black")

        # --- 5. GRID HEADERS (A, B, C... và 1, 2, 3...) ---
        header_fill = (235, 235, 235)
        grid_start_y = 135
        
        # Cột A, B, C
        draw.rectangle([(50, grid_start_y), (1920, grid_start_y + 35)], fill=header_fill)
        cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for i, col in enumerate(cols):
            x_p = 50 + (i * 190)
            draw.text((x_p + 85, grid_start_y + 3), col, font=f['ui'], fill="black")
            draw.line([(x_p, grid_start_y), (x_p, 1080)], fill=(210, 210, 210))

        # Dòng 1, 2, 3
        draw.rectangle([(0, grid_start_y), (50, 1080)], fill=header_fill)
        for i in range(1, 22):
            y_p = grid_start_y + (i * 40)
            draw.text((15, y_p + 5), str(i), font=f['ui'], fill="black")
            draw.line([(0, y_p), (1920, y_p)], fill=(210, 210, 210))

        # --- 6. TRẠNG THÁI & SHEET TABS ---
        draw.rectangle([(0, 1030), (1920, 1080)], fill=bg_gray)
        # Active Sheet
        draw.rectangle([(40, 1030), (160, 1070)], fill="white")
        draw.line([(40, 1030), (160, 1030)], fill=excel_green, width=3)
        draw.text((65, 1038), "Sheet1", font=f['ui'], fill=excel_green)
        
        # Zoom slider giả lập
        draw.text((1750, 1038), "-  100%  +", font=f['ui'], fill="gray")

        # --- 7. ĐỔ DỮ LIỆU (Tối ưu hóa chia cột) ---
        
        if t > duration * 0.4:
            rows = data_content.split('\n')
            
            # FIX FX BAR: Chỉ lấy giá trị ô A1 (ô đầu tiên)
            first_cell_value = ""
            if rows:
                first_row_cells = [c.strip() for c in rows[0].split('|')]
                if first_row_cells:
                    first_cell_value = first_row_cells[0]
                    
            # Vẽ giá trị ô A1 lên thanh công thức (thay vì toàn bộ data_content)
            draw.text((150, 100), first_cell_value, font=f['ui'], fill="black")

            for row_idx, row_str in enumerate(rows):
                if row_idx > 15: break 
                cells = [c.strip() for c in row_str.split('|')]
                
                for col_idx, cell_value in enumerate(cells):
                    if col_idx > 8: break 
                    
                    # Tọa độ chuẩn cho cột A, B, C...
                    cell_x = 50 + (col_idx * 190) 
                    cell_y = (grid_start_y + 35) + (row_idx * 40) # +35 để nhảy xuống dưới Header A,B,C
                    
                    if t > (duration * 0.4) + (row_idx * 0.05):
                        draw.text((cell_x + 10, cell_y + 8), cell_value, font=f['ui'], fill="black")
                        
                        # Highlight Header (Cột A, B, C...) khi có dữ liệu đổ xuống
                        header_x = 50 + (col_idx * 190)
                        draw.rectangle([(header_x, grid_start_y), (header_x + 190, grid_start_y + 35)], outline=excel_green, width=2)
            
            # Cập nhật thanh Formula (fx) cho ô A1
            first_val = rows[0].split('|')[0].strip() if rows else ""
            draw.rectangle([(140, 95), (1900, 130)], fill=bg_gray) 
            draw.text((150, 100), first_val, font=f['ui'], fill="black")
            
            # Di chuyển ô Address Bar từ "B2" thành "A1" cho khớp kết quả
            draw.rectangle([(10, 98), (70, 128)], fill="white") # Xóa chữ B2 cũ
            draw.text((20, 100), "A1", font=f['ui'], fill="black")

        return np.array(img)