def get_vsc_template(safe_content, filename, duration=5.0):
    # Logic tách nội dung: Nếu content có dấu ">>", phần sau đó là kết quả Terminal
    parts = str(safe_content).split(">>")
    code_content = parts[0].strip()
    terminal_output = parts[1].strip() if len(parts) > 1 else "Success"

    return f"""
    <div class="window" style="background:#1e1e1e; border: 1px solid #333; font-family: 'Consolas', monospace;">
        <div class="win-title" style="background:#323233; color:#ccc; display:flex; justify-content:space-between; align-items:center; padding: 5px 10px;">
            <span><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/2048px-Visual_Studio_Code_1.35_icon.svg.png" width="16" style="vertical-align:middle; margin-right:5px;"> {filename}.py - Visual Studio Code</span>
            <div class="win-buttons" style="display:flex; gap:10px; font-size:12px;">
                <span>_</span> <span>▢</span> <span>X</span>
            </div>
        </div>
        
        <div class="vsc-main" style="display:flex; height: 1000px;">
            <div style="width:50px; background:#333; display:flex; flex-direction:column; align-items:center; padding-top:15px; gap:25px; color:#858585;">
                <span style="color:#fff; font-size:20px;">📄</span>
                <span style="font-size:20px;">🔍</span>
                <span style="font-size:20px;">🌿</span>
            </div>

            <div style="width:220px; background:#252526; padding:15px; font-size:13px; color:#858585;">
                <b style="font-size:11px;">EXPLORER</b><br><br>
                <span style="color:#ccc">▼</span> <b style="color:#ccc">SMART_PROJECT</b><br>
                &nbsp;&nbsp;&nbsp;🐍 <span style="color:#fff">{filename}.py</span>
            </div>

            <div style="display:flex; flex-direction:column; flex-grow:1; background:#1e1e1e;">
                <div class="vsc-editor" style="padding: 20px; font-size: 26px; line-height: 1.5; flex-grow: 1;">
                    <div style="color:#569cd6">import <span style="color:#4ec9b0">xlwings</span> as <span style="color:#9cdcfe">xw</span></div>
                    <br>
                    <div class="typing-effect" style="color:#dcdcaa; white-space: pre-wrap;">{code_content}</div>
                </div>

                <div class="vsc-terminal" style="background:#000; height:350px; padding: 15px; border-top: 1px solid #333; font-size: 22px;">
                    <div style="color:#ccc; font-size:14px; margin-bottom:10px;">TERMINAL</div>
                    <div style="color:#fff;">
                        <span style="color:#00ff00;">PS C:\\Users\\Vũ_Thanh></span> 
                        <span class="cmd-typing">python {filename}.py</span>
                    </div>
                    <div class="terminal-result" style="color:#aaa; margin-top:10px; opacity:0;">
                        >> [SUCCESS] {terminal_output}
                        <br>
                        <span style="color:#00ff00;">PS C:\\Users\\Vũ_Thanh></span> <span class="cursor">_</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <style>
        /* Hiệu ứng gõ chữ cho Code */
        .typing-effect {{
            overflow: hidden;
            border-right: .15em solid orange;
            animation: typing {duration}s steps(40, end), blink-caret .75s step-end infinite;
            max-height: 100%;
        }}

        /* Hiện kết quả Terminal sau khi gõ xong */
        .terminal-result {{
            animation: fadeIn 0.1s forwards;
            animation-delay: {duration}s;
        }}

        @keyframes typing {{ from {{ max-height: 0 }} to {{ max-height: 1000px }} }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
        @keyframes blink-caret {{ from, to {{ border-color: transparent }} 50% {{ border-color: orange; }} }}
        .cursor {{ animation: blink 1s infinite; }}
        @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    </style>
    """