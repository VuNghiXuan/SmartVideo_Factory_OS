def get_terminal_template(content, filename="PowerShell"):
    # Tách nội dung thành các dòng
    raw_lines = content.split('<br>')
    terminal_html = ""
    
    for line in raw_lines:
        line = line.strip()
        if not line: continue
        
        # Nếu dòng bắt đầu bằng ">" -> Đây là lệnh người dùng gõ
        if line.startswith(">"):
            cmd_text = line.replace(">", "").strip()
            terminal_html += f"""
            <div class='term-line'>
                <span class='prompt'>PS C:\\Users\\Vu_Thanh&gt;</span> 
                <span class='typewriter'>{cmd_text}</span>
            </div>"""
        else:
            # Đây là kết quả trả về từ hệ thống
            terminal_html += f"<div class='term-output'>{line}</div>"

    return f"""
    <div class="window terminal-window" style="background: #0c0c0c; color: #cccccc; font-family: 'Consolas', monospace;">
        <div class="win-title" style="background: #333; color: #fff; padding: 5px 15px; display: flex; align-items: center;">
            <div class="win-buttons" style="display: flex; gap: 8px; margin-right: 15px;">
                <span style="width: 12px; height: 12px; background: #ff5f56; border-radius: 50%;"></span>
                <span style="width: 12px; height: 12px; background: #ffbd2e; border-radius: 50%;"></span>
                <span style="width: 12px; height: 12px; background: #27c93f; border-radius: 50%;"></span>
            </div>
            <span>{filename}</span>
        </div>
        <div class="terminal-body" style="padding: 20px; font-size: 24px; line-height: 1.6; height: 100%;">
            {terminal_html}
            <div class="cursor-line">
                <span class="prompt">PS C:\\Users\\Vu_Thanh&gt;</span><span class="cursor-blink">_</span>
            </div>
        </div>
    </div>
    <style>
        .prompt {{ color: #00ff00; font-weight: bold; }}
        .term-output {{ color: #ffffff; margin-bottom: 10px; opacity: 0.8; }}
        .cursor-blink {{ animation: blink 1s infinite; color: #00ff00; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    </style>
    """