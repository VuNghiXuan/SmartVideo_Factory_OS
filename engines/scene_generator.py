import os
import shutil
from html2image import Html2Image
from templates.template_manager import TemplateManager
from config import config


class SceneGenerator:
    def __init__(self):
        # self.hti = Html2Image(...) # Tạm đóng băng để đỡ tốn RAM, mai môta có lấy code bên dưới
        pass


# class SceneGenerator:
#     def __init__(self):
#         # self.hti = Html2Image(size=(1920, 1080), custom_flags=['--no-sandbox', '--disable-gpu'])
#         self.hti = Html2Image(size=(1920, 1080), custom_flags=['--no-sandbox', '--disable-gpu', '--hide-scrollbars'])
#         self.template_mgr = TemplateManager()

#     def generate_background(self, type, content, output_path, filename=None, duration=5.0, **kwargs):    
#         """
#         Nâng cấp: Nhận thêm biến duration (giây) để khớp hiệu ứng gõ chữ với lời thoại.
#         """
#         try:
#             course_name = kwargs.get('course_name', "KHÓA HỌC TRI THỨC")
            
#             # 1. Lấy HTML gốc từ TemplateManager
#             html_str = self.template_mgr.get_template(
#                 type, 
#                 content, 
#                 filename, 
#                 course_name=course_name
#             )

#             # 2. CHÈN LOGIC KHỚP LỜI THOẠI (TYPING EFFECT)
#             # Chúng ta sẽ "hack" vào html_str để thêm CSS animation dựa trên duration
#             typing_css = f"""
#             <style>
#                 .typewriter-text {{
#                     overflow: hidden;
#                     white-space: pre-wrap;
#                     display: inline-block;
#                     animation: typing {duration}s steps(100, end) forwards;
#                 }}
#                 .cursor-blink {{
#                     border-right: 3px solid #00ff00;
#                     animation: blink 0.7s infinite;
#                     margin-left: 5px;
#                 }}
#                 @keyframes typing {{
#                     from {{ max-height: 0; opacity: 0; }}
#                     to {{ max-height: 2000px; opacity: 1; }}
#                 }}
#                 @keyframes blink {{
#                     0%, 100% {{ border-color: transparent; }}
#                     50% {{ border-color: #00ff00; }}
#                 }}
#             </style>
#             """
            
#             # Chèn CSS vào trước thẻ đóng </head> hoặc </body>
#             if "</head>" in html_str:
#                 html_str = html_str.replace("</head>", f"{typing_css}</head>")
#             else:
#                 html_str = f"{typing_css}{html_str}"

#             # 3. Render
#             temp_file_name = f"temp_{os.path.basename(output_path)}"
#             self.hti.screenshot(html_str=html_str, save_as=temp_file_name)
            
#             if os.path.exists(temp_name := temp_file_name):
#                 return self._finalize_image(temp_name, output_path, type)
#             else:
#                 raise FileNotFoundError("Chụp ảnh thất bại")

#         except Exception as e:
#             print(f"❌ [LỖI CẢNH] {filename}: {e}")
#             return self._generate_fallback(content, filename, output_path)

#     def _generate_fallback(self, content, filename, output_path):
#         """Hàm vẽ fallback giữ nguyên logic của mày"""
#         fallback_html = f"""
#         <div style="background: #1a1a1a; color: #00ff00; width: 1920px; height: 1080px; 
#                     display: flex; flex-direction: column; justify-content: center; 
#                     align-items: center; font-family: 'Consolas', monospace; border: 10px solid #333;">
#             <div style="border: 2px solid #00ff00; padding: 40px; background: #000;">
#                 <h1>> SYSTEM_RECOVERY_MODE</h1>
#                 <p style="color: #fff; font-size: 24px;">FILE: {filename or 'Unknown'}</p>
#                 <hr style="border: 1px solid #333;">
#                 <p style="color: #888;">{str(content)[:200]}...</p>
#             </div>
#         </div>
#         """
#         fb_temp = f"fb_{os.path.basename(output_path)}"
#         self.hti.screenshot(html_str=fallback_html, save_as=fb_temp)
#         return self._finalize_image(fb_temp, output_path, "FALLBACK")

#     def _finalize_image(self, temp_name, final_path, type_name):
#         target_dir = os.path.dirname(final_path)
#         if target_dir: os.makedirs(target_dir, exist_ok=True)
#         if os.path.exists(final_path): os.remove(final_path)
#         shutil.move(temp_name, final_path)
#         return final_path