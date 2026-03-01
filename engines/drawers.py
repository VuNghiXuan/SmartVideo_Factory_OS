# import numpy as np
# from PIL import Image, ImageDraw, ImageFont
# import os
# import math

# class InterfaceDrawers:
#     @staticmethod
#     def get_fonts(base_size=32):
#         try:
#             # Ưu tiên các font hệ thống phổ biến
#             return {
#                 'code': ImageFont.truetype("consola.ttf", base_size),
#                 'term': ImageFont.truetype("consola.ttf", base_size - 6),
#                 'ui': ImageFont.truetype("arial.ttf", base_size - 12),
#                 'bold': ImageFont.truetype("arialbd.ttf", base_size + 10)
#             }
#         except:
#             return {k: ImageFont.load_default() for k in ['code', 'term', 'ui', 'bold']}

#     @staticmethod
#     def draw_win11_controls(draw, width, is_dark=True):
#         """Vẽ 3 nút Close/Max/Min kiểu Windows 11"""
#         color = (200, 200, 200) if is_dark else (60, 60, 60)
#         # Nút Close
#         draw.text((width - 45, 12), "✕", fill=color, font=ImageFont.truetype("arial.ttf", 20))
#         # Nút Max
#         draw.rectangle([(width - 85, 18), (width - 70, 33)], outline=color, width=1)
#         # Nút Min
#         draw.line([(width - 125, 33), (width - 110, 33)], fill=color, width=2)

#     @staticmethod
#     def draw_smooth_cursor(img, t, duration):
#         """Vẽ con chuột lướt mượt mà"""
#         draw = ImageDraw.Draw(img)
#         # Di chuyển từ phải dưới vào giữa màn hình
#         start_pos, end_pos = (1850, 1000), (960, 540)
#         prog = min(t / (duration * 0.5), 1.0)
#         # Dùng hàm Sin để làm mượt chuyển động (Ease-in-out)
#         curve = (1 - math.cos(prog * math.pi)) / 2
#         cur_x = start_pos[0] + (end_pos[0] - start_pos[0]) * curve
#         cur_y = start_pos[1] + (end_pos[1] - start_pos[1]) * curve
        
#         # Hình con trỏ chuột
#         draw.polygon([(cur_x, cur_y), (cur_x, cur_y + 25), (cur_x + 18, cur_y + 18)], fill="white", outline="black")

#     @classmethod
#     def draw_vsc(cls, t, duration, **kwargs):
#         file_name = kwargs.get('file_name', 'main.py')
#         content = kwargs.get('content', '')
        
#         # Tách nội dung
#         parts = content.split(">>")
#         code_to_type = parts[0].strip()
#         terminal_text = parts[1].strip() if len(parts) > 1 else ""

#         # Màu sắc theo ảnh mày gửi
#         bg_editor = (30, 30, 30)
#         bg_sidebar = (37, 37, 38)
#         bg_activity_bar = (51, 51, 51)
#         bg_tabs = (45, 45, 45)
#         text_gray = (150, 150, 150)
#         syntax_blue = (86, 156, 214)

#         img = Image.new('RGB', (1920, 1080), bg_editor)
#         draw = ImageDraw.Draw(img)
#         f = cls.get_fonts(24) # Font nhỏ lại cho giống tỉ lệ ảnh

#         # --- 1. Activity Bar (Ngoài cùng bên trái) ---
#         draw.rectangle([(0, 0), (60, 1080)], fill=bg_activity_bar)
#         # Vẽ vài icon giả (ô vuông nhỏ)
#         for i in range(5):
#             color = (255, 255, 255) if i == 0 else text_gray
#             draw.rectangle([(15, 20 + i*60), (45, 50 + i*60)], outline=color, width=2)

#         # --- 2. Side Bar (Explorer) ---
#         draw.rectangle([(60, 0), (300, 1080)], fill=bg_sidebar)
#         draw.text((80, 20), "EXPLORER", font=f['ui'], fill=text_gray)
#         draw.text((80, 60), "▼ SMARTVIDEO_FACTORY_OS", font=f['ui'], fill=(255, 255, 255))
#         draw.text((100, 100), f"🐍 {file_name}", font=f['ui'], fill=syntax_blue)

#         # --- 3. Tabs Bar ---
#         draw.rectangle([(300, 0), (1920, 50)], fill=bg_tabs)
#         # Active Tab (Có đường viền xanh ở trên cùng theo style VSC)
#         draw.rectangle([(300, 0), (520, 50)], fill=bg_editor)
#         draw.rectangle([(300, 0), (520, 2)], fill=(0, 120, 215)) # Blue line top
#         draw.text((330, 12), f"🐍 {file_name}", font=f['ui'], fill=(212, 212, 212))

#         # --- 4. Editor (Vùng gõ code) ---
#         # Số dòng (Line Numbers)
#         for i in range(1, 20):
#             draw.text((310, 80 + (i-1)*30), str(i), font=f['code'], fill=(100, 100, 100))
        
#         typing_dur = duration * 0.7
#         char_idx = int((t/typing_dur) * len(code_to_type)) if t < typing_dur else len(code_to_type)
#         current_code = code_to_type[:char_idx]
        
#         # Vẽ code với lề trái trừ ra cho số dòng
#         draw.multiline_text((350, 80), current_code, font=f['code'], fill=(212, 212, 212), spacing=10)
        
#         # Con trỏ gõ (Blinking Cursor)
#         if int(t*5) % 2 == 0:
#             # Tính toán vị trí con trỏ dựa trên dòng cuối
#             lines = current_code.split('\n')
#             last_line = lines[-1] if lines else ""
#             y_cursor = 80 + (len(lines)-1)*40 # 40 là spacing (30 font + 10 spacing)
#             # Dùng textlength để lấy độ dài dòng cuối
#             x_cursor = 350 + draw.textlength(last_line, font=f['code'])
#             draw.line([(x_cursor, y_cursor), (x_cursor, y_cursor + 30)], fill=(255, 255, 255), width=2)

#         # --- 5. Terminal (Nằm dưới cùng) ---
#         term_y = 750
#         draw.rectangle([(300, term_y), (1920, 1080)], fill=(15, 15, 15))
#         draw.rectangle([(300, term_y), (1920, term_y + 35)], fill=bg_editor) # Terminal header
#         draw.text((320, term_y + 5), "TERMINAL  DEBUG CONSOLE  OUTPUT", font=f['ui'], fill=text_gray)
        
#         # Prompt PowerShell chuẩn
#         prompt = "PS D:\\ThanhVu\\AI_code\\SmartVideo_Factory_OS> "
#         draw.text((320, term_y + 50), prompt, font=f['term'], fill=(34, 196, 56))
        
#         if t > duration * 0.75:
#             prompt_w = draw.textlength(prompt, f['term'])
#             draw.text((320 + prompt_w, term_y + 50), f"python {file_name}", font=f['term'], fill="white")
#             if t > duration * 0.9:
#                 draw.text((320, term_y + 90), f">> {terminal_text}", font=f['term'], fill=(180, 180, 180))

#         import numpy as np
#         return np.array(img)

#     @classmethod
#     def draw_excel(cls, t, duration, **kwargs):
#         """Excel: Giao diện Office 365 đầy đủ Logo, Tabs Menu, Sheet và Grid"""
#         file_name = kwargs.get('file_name', 'Data_Automation.xlsx')
#         data_content = kwargs.get('content', 'Dữ liệu đang được xử lý...')
        
#         # 1. Khởi tạo
#         img = Image.new('RGB', (1920, 1080), (255, 255, 255))
#         draw = ImageDraw.Draw(img)
#         f = cls.get_fonts(24) # Font nhỏ hơn cho menu
#         f_ui = cls.get_fonts(28)
        
#         excel_green = (33, 115, 70)
#         bg_gray = (243, 243, 243)

#         # --- 2. THANH TIÊU ĐỀ (Top Bar) ---
#         draw.rectangle([(0, 0), (1920, 45)], fill=excel_green)
#         # Logo X
#         draw.rectangle([(15, 8), (40, 33)], fill="white")
#         draw.text((22, 7), "X", font=f['ui'], fill=excel_green)
#         # Tên file
#         draw.text((60, 8), f"{file_name} - Excel", font=f['ui'], fill="white")
#         cls.draw_win11_controls(draw, 1920, is_dark=False)

#         # --- 3. HỆ THỐNG TABS MENU (Ribbon Tabs) ---
#         # Nền của dải Menu
#         draw.rectangle([(0, 45), (1920, 90)], fill="white")
        
#         # Tab "File" đặc biệt (Nền xanh chữ trắng)
#         draw.rectangle([(0, 45), (80, 90)], fill=excel_green)
#         draw.text((18, 55), "File", font=f['ui'], fill="white")
        
#         # Các Tab khác
#         menus = ["Home", "Insert", "Page Layout", "Formulas", "Data", "Review", "View"]
#         x_offset = 100
#         for menu in menus:
#             # Highlight Tab "Home" hoặc "Data" tùy cảnh (ở đây mặc định Home)
#             if menu == "Home":
#                 draw.line([(x_offset, 88), (x_offset + 60, 88)], fill=excel_green, width=3)
#                 draw.text((x_offset, 55), menu, font=f['ui'], fill=excel_green)
#             else:
#                 draw.text((x_offset, 55), menu, font=f['ui'], fill=(100, 100, 100))
#             x_offset += 130

#         # --- 4. THANH CÔNG THỨC (Formula Bar) ---
#         draw.rectangle([(0, 90), (1920, 135)], fill=bg_gray)
#         # Ô địa chỉ (ví dụ B2)
#         draw.rectangle([(10, 98), (70, 128)], outline=(200, 200, 200), fill="white")
#         draw.text((20, 100), "B2", font=f['ui'], fill="black")
        
#         draw.text((95, 100), "fx", font=f['code'], fill="gray")
#         draw.line([(130, 102), (130, 125)], fill=(200, 200, 200)) # Ngăn cách
        
#         if t > duration * 0.4:
#             # Chữ chạy trên thanh công thức
#             display_text = data_content[:int(t*15)] if t < duration else data_content
#             draw.text((150, 100), display_text, font=f['ui'], fill="black")

#         # --- 5. GRID HEADERS (A, B, C... và 1, 2, 3...) ---
#         header_fill = (235, 235, 235)
#         grid_start_y = 135
        
#         # Cột A, B, C
#         draw.rectangle([(50, grid_start_y), (1920, grid_start_y + 35)], fill=header_fill)
#         cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
#         for i, col in enumerate(cols):
#             x_p = 50 + (i * 190)
#             draw.text((x_p + 85, grid_start_y + 3), col, font=f['ui'], fill="black")
#             draw.line([(x_p, grid_start_y), (x_p, 1080)], fill=(210, 210, 210))

#         # Dòng 1, 2, 3
#         draw.rectangle([(0, grid_start_y), (50, 1080)], fill=header_fill)
#         for i in range(1, 22):
#             y_p = grid_start_y + (i * 40)
#             draw.text((15, y_p + 5), str(i), font=f['ui'], fill="black")
#             draw.line([(0, y_p), (1920, y_p)], fill=(210, 210, 210))

#         # --- 6. TRẠNG THÁI & SHEET TABS ---
#         draw.rectangle([(0, 1030), (1920, 1080)], fill=bg_gray)
#         # Active Sheet
#         draw.rectangle([(40, 1030), (160, 1070)], fill="white")
#         draw.line([(40, 1030), (160, 1030)], fill=excel_green, width=3)
#         draw.text((65, 1038), "Sheet1", font=f['ui'], fill=excel_green)
        
#         # Zoom slider giả lập
#         draw.text((1750, 1038), "-  100%  +", font=f['ui'], fill="gray")

#         # --- 7. ĐỔ DỮ LIỆU ---
#         if t > duration * 0.5:
#             # Ô B2 (Cột B là index 1, Dòng 2 là index 2)
#             cell_x = 50 + 190 # Cột B
#             cell_y = grid_start_y + 40 # Dòng 2
            
#             # Border xanh bao quanh ô đang active
#             draw.rectangle([(cell_x, cell_y), (cell_x + 190, cell_y + 40)], outline=excel_green, width=3)
            
#             lines = data_content.split('\n')
#             for idx, line in enumerate(lines):
#                 draw.text((cell_x + 10, cell_y + 5 + (idx * 40)), line, font=f['ui'], fill="black")

#         return np.array(img)

#     @classmethod
#     def draw_cmd(cls, t, duration, **kwargs):
#         """CMD/Terminal: Giao diện hiện đại, gõ lệnh thong thả và có output thực tế"""
#         command = kwargs.get('content', 'pip install xlwings')
#         project_path = f"PS C:\\Users\\AI_Factory\\{kwargs.get('title', 'Project')}> "
        
#         # 1. Khởi tạo nền
#         img = Image.new('RGB', (1920, 1080), (30, 30, 30))
#         draw = ImageDraw.Draw(img)
#         f = cls.get_fonts(40) 
        
#         # 2. Title Bar
#         draw.rectangle([(0, 0), (1920, 60)], fill=(45, 45, 45))
#         draw.rectangle([(20, 15), (45, 40)], fill=(0, 120, 215)) 
#         draw.text((65, 12), "Windows Terminal - PowerShell", font=f['ui'], fill=(200, 200, 200))
#         cls.draw_win11_controls(draw, 1920)

#         # 3. Logic gõ lệnh
#         start_typing = duration * 0.1
#         end_typing = duration * 0.6
        
#         if t < start_typing:
#             current_text = ""
#         elif t < end_typing:
#             progress = (t - start_typing) / (end_typing - start_typing)
#             char_idx = int(progress * len(command))
#             current_text = command[:char_idx]
#         else:
#             current_text = command

#         cursor = "_" if int(t * 3) % 2 == 0 else ""
        
#         # Vẽ dòng Prompt
#         draw.text((40, 100), project_path, font=f['code'], fill=(131, 209, 131))
#         prompt_w = draw.textlength(project_path, font=f['code'])
#         draw.text((40 + prompt_w, 100), current_text + cursor, font=f['code'], fill=(255, 255, 255))

#         # 4. Hiển thị Output (Sửa lỗi lọt khe ở đây)
#         if t > duration * 0.7:
#             # Xác định nội dung output dựa trên lệnh
#             if "pip install" in command.lower():
#                 pkg = command.split()[-1]
#                 output = (
#                     f"Collecting {pkg}...\n"
#                     f"  Downloading {pkg}-3.0.1-py3-none-any.whl (1.2 MB)\n"
#                     f"Installing collected packages: {pkg}\n"
#                     f"Successfully installed {pkg}-3.0.1"
#                 )
#             elif "python" in command.lower():
#                 output = "🚀 Chạy file thành công!\n[Dữ liệu đã được ghi vào Excel]"
#             else:
#                 output = "Lệnh đã được thực hiện..."

#             # Vẽ Output màu xám nhẹ dưới dòng lệnh
#             draw.text((40, 160), output, font=f['code'], fill=(180, 180, 180))

#         # ⚠️ QUAN TRỌNG: DÒNG NÀY LÀ CỨU TINH CỦA MÀY
#         import numpy as np
#         return np.array(img)

#     @classmethod
#     def draw_document(cls, t, duration, **kwargs):
#         """Doc: Lấy title và content từ JSON"""
#         title = kwargs.get('title', 'Tài Liệu Hướng Dẫn')
#         content = kwargs.get('content', '')

#         img = Image.new('RGB', (1920, 1080), (250, 250, 250))
#         draw = ImageDraw.Draw(img)
#         f = cls.get_fonts(45)
        
#         # Header bar
#         draw.rectangle([(0, 0), (1920, 120)], fill=(0, 120, 215))
#         draw.text((60, 35), f"📘 {title}", font=f['bold'], fill="white")
#         cls.draw_win11_controls(draw, 1920)
        
#         # Hiệu ứng hiện nội dung
#         draw.multiline_text((100, 220), content, font=f['code'], fill=(40, 40, 40), spacing=25)
        
#         # cls.draw_smooth_cursor(img, t, duration)
#         return np.array(img)
    
#     @classmethod
#     def draw_mindmap(cls, t, duration, **kwargs):
#         """Mindmap & Summary: Hiển thị lộ trình bài học hoặc tổng kết dưới dạng sơ đồ"""
#         title = kwargs.get('title', 'Lộ Trình Bài Học')
#         content = kwargs.get('content', '')
#         # Tự động đổi màu nếu là tổng kết
#         is_summary = "tổng kết" in title.lower() or "summary" in title.lower()
#         theme_color = (255, 87, 34) if is_summary else (0, 150, 136) # Cam hoặc Xanh teal
        
#         # 1. Khởi tạo nền sáng chuyên nghiệp
#         img = Image.new('RGB', (1920, 1080), (240, 242, 245))
#         draw = ImageDraw.Draw(img)
#         f = cls.get_fonts(40)
        
#         # 2. Vẽ Header bar
#         draw.rectangle([(0, 0), (1920, 100)], fill=theme_color)
#         draw.text((60, 25), f"📌 {title.upper()}", font=f['bold'], fill="white")
#         cls.draw_win11_controls(draw, 1920)

#         # 3. Xử lý danh sách các bước
#         steps = [s.strip() for s in content.split('\n') if s.strip()]
#         if not steps: steps = ["Bắt đầu...", "Thực hành...", "Hoàn thành!"]

#         # 4. Vẽ các Node sơ đồ
#         node_width = 500
#         node_height = 120
#         start_x = 100
#         start_y = 200
        
#         for i, step in enumerate(steps):
#             # Tính toán vị trí theo kiểu Z-shape hoặc dọc
#             # Ở đây tao vẽ dạng danh sách thẻ (Card list) có hiệu ứng hiện dần
#             y_pos = start_y + (i * (node_height + 40))
            
#             # Chỉ vẽ nếu thời gian t đã chạy đến bước đó
#             appearance_time = (i / len(steps)) * (duration * 0.8)
#             if t > appearance_time:
#                 # Vẽ bóng đổ (Shadow) cho Card
#                 draw.rectangle([(start_x + 5, y_pos + 5), (start_x + node_width + 1205, y_pos + node_height + 5)], fill=(200, 200, 200))
#                 # Vẽ Card chính
#                 draw.rectangle([(start_x, y_pos), (start_x + node_width + 1200, y_pos + node_height)], fill="white", outline=theme_color, width=2)
                
#                 # Vẽ số thứ tự (Circle)
#                 circle_r = 30
#                 circle_center = (start_x + 60, y_pos + node_height // 2)
#                 draw.ellipse([(circle_center[0]-circle_r, circle_center[1]-circle_r), 
#                              (circle_center[0]+circle_r, circle_center[1]+circle_r)], fill=theme_color)
#                 draw.text((circle_center[0]-12, circle_center[1]-20), str(i+1), font=f['bold'], fill="white")
                
#                 # Vẽ nội dung chữ
#                 draw.text((start_x + 130, y_pos + 35), step, font=f['ui'], fill=(50, 50, 50))
                
#                 # Vẽ mũi tên nối giữa các Node (trừ node cuối)
#                 if i < len(steps) - 1:
#                     arrow_y = y_pos + node_height
#                     draw.line([(start_x + 60, arrow_y), (start_x + 60, arrow_y + 40)], fill=theme_color, width=5)

#         return np.array(img)