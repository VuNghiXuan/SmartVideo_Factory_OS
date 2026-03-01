def get_excel_template(safe_content, filename):
    excel_rows = ""
    cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    
    for i in range(1, 31):
        excel_rows += f'<tr><th class="row-header">{i}</th>'
        for j in range(len(cols)):
            is_active = 'class="active-cell"' if i == 2 and j == 1 else ""
            val = safe_content if i == 2 and j == 1 else ""
            excel_rows += f'<td {is_active}>{val}</td>'
        excel_rows += "</tr>"

    return f"""
    <div class="window" style="display: flex; flex-direction: column; height: 950px; background: white;">
        <div class="win-title" style="flex-shrink: 0;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Microsoft_Office_Excel_%282019%E2%80%93present%29.svg/1200px-Microsoft_Office_Excel_%282019%E2%80%93present%29.svg.png" 
                     width="18" height="18" style="display: block;">
                <span style="font-weight: 500;">{filename}.xlsx - Excel</span>
            </div>
            <div class="win-buttons">
                <i class="fa-solid fa-minus"></i>
                <i class="fa-regular fa-square"></i>
                <i class="fa-solid fa-xmark"></i>
            </div>
        </div>

        <div style="flex-shrink: 0; background:#107c10; height:45px; display:flex; align-items:center; padding:0 20px; color:white; font-weight:bold; gap:20px;">
            <i class="fa-solid fa-bars"></i>
            <span>File</span>
            <span style="border-bottom: 3px solid white;">Home</span>
            <span style="opacity: 0.8; font-weight: normal;">Insert</span>
            <span style="opacity: 0.8; font-weight: normal;">Data</span>
        </div>

        <div style="flex-shrink: 0; background: white; padding: 6px 15px; display: flex; align-items: center; border-bottom: 1px solid #ccc; gap: 10px;">
            <div style="font-weight: bold; color: #107c10; border-right: 1px solid #ddd; padding-right: 15px; min-width: 40px; text-align: center;">B2</div>
            <div style="color: #999; font-style: italic; font-family: serif; font-size: 18px;">fx</div>
            <div style="flex-grow: 1; color: #333;">{safe_content}</div>
        </div>

        <div class="excel-grid-wrapper" style="flex-grow: 1; overflow: auto;">
            <table>
                <tr class="col-header">
                    <th style="width: 50px;"></th>
                    {" ".join([f'<th>{c}</th>' for c in cols])}
                </tr>
                {excel_rows}
            </table>
        </div>

        <div style="flex-shrink: 0; background: #f3f3f3; height: 35px; border-top: 1px solid #ccc; display: flex; align-items: center; padding: 0 15px; font-size: 13px;">
            <div style="display: flex; gap: 10px; padding-right: 15px; border-right: 1px solid #ccc;">
                <i class="fa-solid fa-chevron-left" style="color: #999;"></i>
                <i class="fa-solid fa-chevron-right" style="color: #999;"></i>
            </div>
            <div style="background: white; color: #107c10; font-weight: bold; height: 100%; display: flex; align-items: center; padding: 0 20px; border-right: 1px solid #ccc; position: relative;">
                Sheet1
                <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: #107c10;"></div>
            </div>
            <div style="padding: 0 20px; color: #666;">Data_Source</div>
            <div style="padding: 0 10px; color: #107c10;"><i class="fa-solid fa-plus"></i></div>
            
            <div style="margin-left: auto; display: flex; gap: 15px; align-items: center; color: #666;">
                <span>Ready</span>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <i class="fa-solid fa-minus"></i>
                    <div style="width: 60px; height: 2px; background: #ccc;"></div>
                    <i class="fa-solid fa-plus"></i>
                    <span>100%</span>
                </div>
            </div>
        </div>
    </div>
    """