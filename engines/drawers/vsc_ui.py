import numpy as np
import re
from PIL import Image, ImageDraw
from .base import BaseDrawer

class VSC(BaseDrawer):
    @classmethod
    def highlight_code(cls, draw, pos, code, font, spacing=15):
        """Hàm tô màu code theo style Monokai/VSC chuẩn"""
        x_start, y_start = pos
        lines = code.split('\n')
        
        # Định nghĩa bảng màu syntax
        colors = {
            'keyword': (197, 134, 192),  # Tím (import, def, return)
            'function': (220, 220, 170), # Vàng nhạt (print, App)
            'string': (206, 145, 120),   # Cam đất ('text')
            'comment': (106, 153, 85),   # Xanh lá (comment)
            'default': (212, 212, 212),  # Trắng xám (biến, dấu)
            'number': (181, 206, 168),   # Xanh bạc hà (số)
            'special': (86, 156, 214)    # Xanh dương (self, cls)
        }

        # Regex nhận diện thành phần
        token_specification = [
            ('comment',  r'#.*'),
            ('string',   r'f?".*?"|\'.*?\''),
            ('keyword',  r'\b(import|as|from|def|class|return|if|else|elif|for|while|in|with)\b'),
            ('special',  r'\b(self|cls|app|wb|ws|xw)\b'),
            ('number',   r'\b\d+\b'),
            ('function', r'\b\w+(?=\()'),
        ]
        
        for i, line in enumerate(lines):
            curr_x = x_start
            curr_y = y_start + i * (24 + spacing)
            
            # Tách dòng thành các mẩu nhỏ để tô màu
            last_idx = 0
            # Tìm tất cả các tokens trong dòng
            tokens = []
            for token_type, pattern in token_specification:
                for match in re.finditer(pattern, line):
                    tokens.append((match.start(), match.end(), token_type))
            
            # Sắp xếp tokens theo thứ tự xuất hiện
            tokens.sort()
            
            # Vẽ từng đoạn text
            for start, end, t_type in tokens:
                # Vẽ phần text mặc định trước token (nếu có)
                if start > last_idx:
                    plain_text = line[last_idx:start]
                    draw.text((curr_x, curr_y), plain_text, font=font, fill=colors['default'])
                    curr_x += draw.textlength(plain_text, font=font)
                
                # Vẽ token có màu
                token_text = line[start:end]
                draw.text((curr_x, curr_y), token_text, font=font, fill=colors[t_type])
                curr_x += draw.textlength(token_text, font=font)
                last_idx = end
            
            # Vẽ phần còn lại của dòng
            if last_idx < len(line):
                draw.text((curr_x, curr_y), line[last_idx:], font=font, fill=colors['default'])

    @classmethod
    def draw_vsc(cls, t, duration, **kwargs):
        # Lấy file_name từ kwargs (được scene_generator map từ JSON)
        # Nếu JSON không có, mặc định là script_logic.py cho 'pro'
        file_name = kwargs.get('file_name') or "automation_logic.py"
        content = kwargs.get('content', '')
        
        if ">>" in content:
            parts = content.split(">>")
            code_to_type = parts[0].strip()
            terminal_text = parts[1].strip()
        else:
            code_to_type = content.strip()
            terminal_text = ""

        bg_editor = (30, 30, 30)
        bg_sidebar = (37, 37, 38)
        bg_activity_bar = (51, 51, 51)
        bg_tabs = (45, 45, 45)
        text_gray = (150, 150, 150)
        syntax_blue = (86, 156, 214)

        img = Image.new('RGB', (1920, 1080), bg_editor)
        draw = ImageDraw.Draw(img)
        f = cls.get_fonts(24) 

        # --- 1. Activity Bar ---
        draw.rectangle([(0, 0), (60, 1080)], fill=bg_activity_bar)
        # Icons: Explorer, Search, Git, Debug, Extensions
        for i in range(5):
            color = (255, 255, 255) if i == 0 else text_gray
            draw.rectangle([(15, 25 + i*60), (45, 55 + i*60)], outline=color, width=2)

        # --- 2. Side Bar (Khớp với file_name) ---
        draw.rectangle([(60, 0), (320, 1080)], fill=bg_sidebar)
        draw.text((80, 20), "EXPLORER", font=f['ui'], fill=text_gray)
        draw.text((80, 60), "▼ PROJECT_AI", font=f['ui'], fill=(255, 255, 255))
        draw.text((100, 100), f"🐍 {file_name}", font=f['ui'], fill=syntax_blue)

        # --- 3. Tabs Bar ---
        draw.rectangle([(320, 0), (1920, 50)], fill=bg_tabs)
        draw.rectangle([(320, 0), (550, 50)], fill=bg_editor) # Tab active
        draw.rectangle([(320, 0), (550, 2)], fill=(0, 120, 215)) 
        draw.text((350, 12), f"🐍 {file_name}", font=f['ui'], fill=(212, 212, 212))

        # --- 4. Editor + Syntax Highlighting ---
        for i in range(1, 25):
            draw.text((335, 80 + (i-1)*39), str(i), font=f['code'], fill=(100, 100, 100))
        
        typing_dur = duration * 0.7
        # Hiệu ứng ngập ngừng (thinking)
        progress = min(1.0, t / typing_dur)
        thinking = np.sin(t * 4) * 0.01 if t < typing_dur else 0
        char_idx = int(max(0, (progress + thinking)) * len(code_to_type))
        current_code = code_to_type[:min(char_idx, len(code_to_type))]
        
        # Vẽ code có màu
        cls.highlight_code(draw, (380, 80), current_code, f['code'], spacing=15)
        
        # Con trỏ gõ
        if int(t * 5) % 2 == 0:
            lines = current_code.split('\n')
            last_line = lines[-1] if lines else ""
            y_cursor = 80 + (len(lines) - 1) * (24 + 15) 
            x_cursor = 380 + draw.textlength(last_line, font=f['code'])
            draw.line([(x_cursor, y_cursor), (x_cursor, y_cursor + 28)], fill=(255, 255, 255), width=2)

        # --- 5. Terminal (Khớp folder) ---
        term_y = 780
        draw.rectangle([(320, term_y), (1920, 1080)], fill=(15, 15, 15))
        draw.rectangle([(320, term_y), (1920, term_y + 35)], fill=bg_editor)
        draw.text((340, term_y + 8), "TERMINAL   DEBUG   OUTPUT", font=f['ui'], fill=text_gray)
        
        # Đường dẫn terminal giả lập theo folder explorer
        prompt = "PS C:\\Users\\Admin\\Project_AI> "
        draw.text((340, term_y + 55), prompt, font=f['term'], fill=(34, 196, 56))
        
        if t > duration * 0.75:
            prompt_w = draw.textlength(prompt, font=f['term'])
            draw.text((340 + prompt_w, term_y + 55), f"python {file_name}", font=f['term'], fill="white")
            if t > duration * 0.85 and terminal_text:
                draw.text((340, term_y + 95), f">> {terminal_text}", font=f['term'], fill=(180, 180, 180))

        return np.array(img)