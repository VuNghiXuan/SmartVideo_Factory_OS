def get_chrome_template(safe_content, filename):
    return f"""
            <div class="window">
                <div style="background:#dee1e6; height:40px; display:flex; align-items:flex-end; padding:0 10px; gap:5px;">
                    <div style="background:white; width:200px; height:32px; border-radius:8px 8px 0 0; display:flex; align-items:center; padding:0 15px; font-size:12px; gap:10px;">
                        <img src="https://www.google.com/favicon.ico" width="14"> Google Search <i class="fa-solid fa-xmark" style="margin-left:auto; font-size:10px;"></i>
                    </div>
                    <div style="padding-bottom:8px; padding-left:5px;"><i class="fa-solid fa-plus" style="font-size:12px; color:#5f6368;"></i></div>
                </div>
                <div style="background:white; height:45px; border-bottom:1px solid #ddd; display:flex; align-items:center; padding:0 15px; gap:15px;">
                    <i class="fa-solid fa-arrow-left" style="color:#5f6368;"></i><i class="fa-solid fa-arrow-right" style="color:#ccc;"></i><i class="fa-solid fa-rotate-right" style="color:#5f6368;"></i>
                    <div style="background:#f1f3f4; flex-grow:1; height:28px; border-radius:14px; display:flex; align-items:center; padding:0 15px; color:#5f6368; font-size:13px;">
                        <i class="fa-solid fa-lock" style="font-size:10px; margin-right:10px;"></i> google.com/search?q={safe_content.replace(' ', '+')}
                    </div>
                    <i class="fa-solid fa-ellipsis-vertical" style="color:#5f6368;"></i>
                </div>
                <div style="flex-grow:1; background:white; display:flex; flex-direction:column; align-items:center; justify-content:center; padding-bottom:80px;">
                    <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" width="220">
                    <div style="margin-top:30px; width:580px; padding:12px 25px; border:1px solid #dfe1e5; border-radius:24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); font-size:18px; color:#202124;">
                        {safe_content}
                    </div>
                    <div style="margin-top:30px; display:flex; gap:10px;">
                        <div style="background:#f8f9fa; padding:10px 20px; border-radius:4px; font-size:14px; color:#3c4043; border:1px solid #f8f9fa;">Google Search</div>
                        <div style="background:#f8f9fa; padding:10px 20px; border-radius:4px; font-size:14px; color:#3c4043; border:1px solid #f8f9fa;">I'm Feeling Lucky</div>
                    </div>
                </div>
            </div>"""
        
        