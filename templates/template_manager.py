import json
import os

class TemplateManager:
    @staticmethod
    def get_base_style(course_theme="#0087ff"): # Mặc định màu xanh Blue
        return f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            ::-webkit-scrollbar {{ width: 12px; height: 12px; }}
            ::-webkit-scrollbar-track {{ background: #1e1e1e; }}
            ::-webkit-scrollbar-thumb {{ background: {course_theme}; border-radius: 10px; border: 3px solid #1e1e1e; }}

            body {{ 
                background: radial-gradient(circle at center, #2c3e50 0%, #000000 100%); 
                width: 1920px; height: 1080px; 
                display: flex; justify-content: center; align-items: center; 
                font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 0;
                overflow: hidden; position: relative;
            }}

            /* Lớp trang trí động */
            .bg-glow {{
                position: absolute; width: 600px; height: 600px;
                background: {course_theme}; filter: blur(150px);
                opacity: 0.15; z-index: 1; border-radius: 50%;
            }}

            /* Thông tin khóa học ở góc */
            .course-overlay {{
                position: absolute; top: 40px; left: 50px; color: white; z-index: 5;
            }}
            .course-tag {{ 
                background: {course_theme}; padding: 4px 12px; border-radius: 5px; 
                font-size: 14px; font-weight: bold; text-transform: uppercase;
            }}
            .course-name {{ font-size: 28px; margin-top: 10px; font-weight: 600; opacity: 0.9; }}

            .window {{ 
                background: white; 
                width: 1650px; 
                height: 850px; /* Giảm từ 900 xuống 850 để chừa khoảng trống dưới đáy */
                border-radius: 12px; 
                overflow: hidden; 
                box-shadow: 0 50px 100px rgba(0,0,0,0.7);
                display: flex; 
                flex-direction: column;
                border: 1px solid #444; 
                z-index: 10;
                
                /* QUAN TRỌNG: Dùng số âm để nhấc cửa sổ LÊN TRÊN */
                transform: translateY(-40px);
            }}
            
            .win-title {{
                background: #f3f3f3; height: 42px; display: flex; 
                align-items: center; justify-content: space-between; padding: 0 15px;
                font-size: 14px; color: #333; border-bottom: 1px solid #ddd;
            }}
            .win-buttons {{ display: flex; gap: 18px; }}
            .win-buttons i {{ font-size: 14px; color: #555; }}

            /* Excel Style */
            .excel-grid-wrapper {{ flex-grow: 1; overflow: auto; background: #e6e6e6; }}
            table {{ width: 100%; border-collapse: collapse; table-layout: fixed; background: white; }}
            th {{ background: #f3f3f3; border: 1px solid #bbb; width: 50px; font-size: 12px; color: #666; height: 25px; }}
            td {{ border: 1px solid #ddd; padding: 8px; font-size: 16px; height: 30px; }}
            .active-cell {{ border: 2px solid #107c10 !important; }}

            /* Terminal Style */
            .terminal {{
                background: #000; color: #00ff00; font-family: 'Consolas', monospace;
                padding: 20px; flex-grow: 1; font-size: 24px; line-height: 1.6;
            }}
            .term-path {{ color: #0087ff; }}

            /* VSC Style */
            .vsc-content {{ display: flex; flex-grow: 1; overflow: hidden; background: #1e1e1e; }}
            .vsc-editor {{ flex-grow: 1; padding: 30px; color: #d4d4d4; font-family: 'Consolas', monospace; font-size: 28px; line-height: 1.5; }}
        </style>
        """

    @staticmethod
    def get_template(template_type, content, filename="Project_V", course_name="LẬP TRÌNH PYTHON"):
        # Tự động chọn màu theo tên khóa học (Ví dụ: Excel -> Xanh lá, Python -> Xanh dương)
        theme_map = {
            "excel": "#107c10",
            "python": "#3776ab",
            "xlwings": "#ffce3a",
            "ai": "#8a2be2"
        }
        
        # Tìm màu chủ đạo dựa trên tên khóa học hoặc nội dung
        color = "#0087ff" # Default
        for key in theme_map:
            if key in course_name.lower() or key in str(content).lower():
                color = theme_map[key]
                break

        base_style = TemplateManager.get_base_style(course_theme=color)
        safe_content = str(content).replace('"', '&quot;').replace('\n', '<br>')
        t_type = str(template_type).lower().strip()

        # 1. Logic Routing Body (Vũ giữ nguyên các file lẻ nhé)
        
        if t_type in ["excel", "spreadsheet"]:
            from .excel import get_excel_template
            ui_body = get_excel_template(safe_content, filename)
        elif t_type in ["vsc", "vscode", "python"]:
            from .vsc import get_vsc_template
            ui_body = get_vsc_template(safe_content, filename)        

        elif t_type in ['pip', "terminal", "cmd"]:
            try:
                from .terminal import get_terminal_template
                ui_body = get_terminal_template(safe_content, filename)
            except:
                ui_body = f'<div class="window"><div class="terminal"><span class="term-path">PS C:\\></span> {safe_content}</div></div>'
        else:
            from .vsc import get_vsc_template
            ui_body = get_vsc_template(safe_content, filename)

        # 2. Gộp vào Layout tổng thể có Background chuyển cảnh
        return f"""
        <!DOCTYPE html>
        <html>
        <head>{base_style}</head>
        <body>
            <div class="bg-glow" style="top: -100px; right: -100px;"></div>
            <div class="bg-glow" style="bottom: -100px; left: -100px; opacity: 0.1;"></div>
            
            <div class="course-overlay">
                <span class="course-tag">Học cùng Vũ AI</span>
                <div class="course-name">{course_name}</div>
            </div>

            {ui_body}
        </body>
        </html>
        """