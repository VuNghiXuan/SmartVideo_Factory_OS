from .vsc_ui import VSC
from .excel_ui import ExcelDrawer
from .info_ui import InfoDrawer
from .terminal_window import TerminalWindow

# 1. Khai báo Mapping: Tên loại cảnh -> Hàm vẽ tương ứng
# Việc dùng mapping giúp loại bỏ hoàn toàn các câu lệnh if-else rườm rà
SCENE_DRAWERS = {
    "vsc": VSC.draw_vsc,
    "excel": ExcelDrawer.draw_excel,
    "doc": InfoDrawer.draw_document,
    "document": InfoDrawer.draw_document,
    "mindmap": InfoDrawer.draw_mindmap,
    "summary": InfoDrawer.draw_mindmap,
    "cmd": TerminalWindow.draw_cmd,
    "terminal": TerminalWindow.draw_cmd,
    "cmd_overlay": TerminalWindow.draw_cmd,
}

# 2. Hàm helper để VideoEngine gọi lấy hàm vẽ
def get_drawer(scene_type):
    """
    Trả về hàm vẽ dựa trên scene_type. 
    Nếu không tìm thấy, mặc định trả về giao diện VSC.
    """
    s_type = str(scene_type).lower().strip()
    return SCENE_DRAWERS.get(s_type, VSC.draw_vsc)

# 3. Vẫn giữ các biến export cũ (nếu mày muốn gọi trực tiếp ở chỗ khác)
draw_vsc = VSC.draw_vsc
draw_excel = ExcelDrawer.draw_excel
draw_mindmap = InfoDrawer.draw_mindmap
draw_document = InfoDrawer.draw_document
draw_cmd = TerminalWindow.draw_cmd