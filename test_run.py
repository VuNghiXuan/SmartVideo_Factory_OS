import asyncio
import os
from main_orchestrator import MainOrchestrator

async def produce_my_first_video():
    # 1. Kịch bản test (Vợ mày sau này sẽ nhập cái này ở UI)
    test_script = [
        {
            "text": "Chào Vũ! Tôi là trợ lý AI của bạn. Chúc mừng bạn đã cài đặt FFmpeg thành công!",
            "action": "intro"
        },
        {
            "text": "Từ bây giờ, chúng ta có thể tự động hóa việc sản xuất hàng nghìn video bài giảng chỉ với một nút bấm.",
            "action": "content"
        },
        {
            "text": "Hệ thống Smart Video Factory đã sẵn sàng. Hãy bắt đầu kiếm tiền thôi nào!",
            "action": "outro"
        }
    ]

    print("🎬 Đang khởi động nhạc trưởng...")
    orchestrator = MainOrchestrator()
    
    # 2. Chạy quy trình sản xuất
    try:
        # Tạo folder nếu chưa có
        if not os.path.exists("outputs"): os.makedirs("outputs")
        
        output_path = await orchestrator.run_production(
            script_data=test_script, 
            course_id="KHOA_HOC_DAU_TIEN", 
            lesson_id="BAI_1_THANH_CONG"
        )
        
        print(f"\n✨ THÀNH CÔNG RỰC RỠ Vũ ơi!")
        print(f"👉 File video của mày nằm ở đây: {output_path}")
        print("Mày mở folder 'outputs' ra và tận hưởng thành quả đi!")

    except Exception as e:
        print(f"❌ Lỗi rồi đại ca ơi: {str(e)}")

if __name__ == "__main__":
    asyncio.run(produce_my_first_video())