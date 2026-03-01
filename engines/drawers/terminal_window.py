import numpy as np
from PIL import Image, ImageDraw
from .base import BaseDrawer

class TerminalWindow(BaseDrawer):
    @classmethod
    def draw_cmd(cls, t, duration, **kwargs):
        """CMD/Terminal: Giao diện hiện đại, gõ lệnh thong thả và có output thực tế"""
        command = kwargs.get('content', 'pip install xlwings')
        project_path = f"PS C:\\Users\\AI_Factory\\{kwargs.get('title', 'Project')}> "
        
        # 1. Khởi tạo nền
        img = Image.new('RGB', (1920, 1080), (30, 30, 30))
        draw = ImageDraw.Draw(img)
        f = cls.get_fonts(40) 
        
        # 2. Title Bar
        draw.rectangle([(0, 0), (1920, 60)], fill=(45, 45, 45))
        draw.rectangle([(20, 15), (45, 40)], fill=(0, 120, 215)) 
        draw.text((65, 12), "Windows Terminal - PowerShell", font=f['ui'], fill=(200, 200, 200))
        cls.draw_win11_controls(draw, 1920)

        # 3. Logic gõ lệnh
        start_typing = duration * 0.1
        end_typing = duration * 0.6
        
        if t < start_typing:
            current_text = ""
        elif t < end_typing:
            progress = (t - start_typing) / (end_typing - start_typing)
            char_idx = int(progress * len(command))
            current_text = command[:char_idx]
        else:
            current_text = command

        cursor = "_" if int(t * 3) % 2 == 0 else ""
        
        # Vẽ dòng Prompt
        draw.text((40, 100), project_path, font=f['code'], fill=(131, 209, 131))
        prompt_w = draw.textlength(project_path, font=f['code'])
        draw.text((40 + prompt_w, 100), current_text + cursor, font=f['code'], fill=(255, 255, 255))

        # 4. Hiển thị Output (Sửa lỗi lọt khe ở đây)
        if t > duration * 0.7:
            # Xác định nội dung output dựa trên lệnh
            if "pip install" in command.lower():
                pkg = command.split()[-1]
                output = (
                    f"Collecting {pkg}...\n"
                    f"  Downloading {pkg}-3.0.1-py3-none-any.whl (1.2 MB)\n"
                    f"Installing collected packages: {pkg}\n"
                    f"Successfully installed {pkg}-3.0.1"
                )
            elif "python" in command.lower():
                output = "🚀 Chạy file thành công!\n[Dữ liệu đã được ghi vào Excel]"
            else:
                output = "Lệnh đã được thực hiện..."

            # Vẽ Output màu xám nhẹ dưới dòng lệnh
            draw.text((40, 160), output, font=f['code'], fill=(180, 180, 180))

        # ⚠️ QUAN TRỌNG: DÒNG NÀY LÀ CỨU TINH CỦA MÀY
        import numpy as np
        return np.array(img)