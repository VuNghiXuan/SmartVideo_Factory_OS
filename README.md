🚀 SmartVideo\_Factory\_OS

Hệ điều hành xưởng sản xuất video bài giảng thông minh



Dự án này là một giải pháp tự động hóa quy trình sản xuất video khóa học từ kịch bản JSON. Hệ thống sử dụng AI để nhận diện nội dung, kết nối kiến thức giữa các bài học và render hình ảnh/âm thanh chất lượng cao thông qua các Engine chuyên biệt.



📂 Cấu trúc dự án

Plaintext

SmartVideo\_Factory\_OS/

├── app.py                      # Entry point: Khởi tạo Streamlit \& Điều hướng Class-based UI

├── main\_orchestrator.py        # Dispatcher: Nhận kịch bản -> Gọi Engine -> Nối Video

├── config.py                   # Cấu hình Global: API Keys, Font, Màu, DNA của Modules

├── .env                        # Biến môi trường

│

├── core/                       # TẦNG 1: TRÍ TUỆ \& QUẢN TRỊ (The Brain)

│   ├── classifier.py           # Phúng sự MiniLM: Nhận diện Module (Excel/Code) \& Logic (Flow/Deep)

│   ├── memory.py               # ChromaDB/FAISS: Lưu/Tra cứu kiến thức từ bài cũ (Context Aware)

│   ├── course\_manager.py       # Quản lý cấu trúc Phân cấp: Catalog -> Course -> Chapter -> Lesson

│   ├── checkpoint.py           # State manager: Lưu tiến độ render, hỗ trợ Resume/Retry

│   └── logger.py               # Ghi log chi tiết lỗi render để debug

│

├── interfaces/                 # TẦNG 2: GIAO DIỆN PHÂN TÁCH (Class-based UI)

│   ├── base\_ui.py              # Abstract Class: Quy định cấu chuẩn Header/Sidebar/Content

│   ├── dashboard\_ui.py         # Class: Tổng quan kho khóa học, tỉ lệ hoàn thành

│   ├── editor\_ui.py            # Class: Biên tập JSON, Preview kịch bản, Sửa thoại

│   ├── render\_ui.py            # Class: Console theo dõi tiến trình render real-time

│   └── assets\_ui.py            # Class: Quản lý kho nhạc, font, lottie files

│

├── engines/                    # TẦNG 3: ĐỘNG CƠ SẢN XUẤT (The Muscles)

│   ├── voice\_engine.py         # ElevenLabs/Azure/Edge-TTS + Pydub (Ducking music)

│   ├── logic\_engine.py         # Manim/Graphviz: Render sơ đồ luồng \& minh họa trừu tượng

│   ├── code\_engine.py          # Render VSC: Highlight mã nguồn, terminal gõ chữ

│   ├── office\_engine.py        # Render Excel/Word: Thao tác ô cột, bảng tính

│   └── video\_engine.py         # MoviePy Core: Mix layers, chèn transition, xuất MP4

│

├── storage/                    # TẦNG 4: KHO DỮ LIỆU ĐỐI TƯỢNG (The Vault)

│   ├── catalog.json            # Index quản lý danh sách các khóa học

│   └── courses/                # Thư mục lưu trữ khóa học theo ID

│       └── \[course\_id]/        

│           ├── course\_meta.json # Thông tin Branding, giọng đọc, cấu trúc chương/bài

│           ├── chapters/       # Folder chứa các chương và file JSON kịch bản

│           └── history/        # Log render và các bản export cũ

│

├── assets/                     # TẦNG 5: NGUYÊN LIỆU THÔ (The Library)

│   ├── branding/               # Logo, Intro/Outro mặc định

│   ├── lottie/                 # Icon động (.json) cho các ghi chú, cảnh báo

│   ├── music/                  # Nhạc nền phân loại theo Mood (Relax, Focus, v.v.)

│   └── templates/              # Jinja2 templates cho HTML/SVG/Manim

│

├── workspace/                  # Cache tạm thời (Tự xóa sau khi hoàn tất)

└── outputs/                    # Video thành phẩm phân loại theo Course/Chapter

🛠️ Stack Công Nghệ (Strike Team)

Semantic \& Memory: sentence-transformers (MiniLM), chromadb (Vector DB).



Voice \& Audio: elevenlabs (Giọng AI chuyên nghiệp), pydub (Xử lý âm thanh).



Visual Logic: manim (Animation toán học), graphviz (Sơ đồ luồng).



Video Engine: moviepy (Cắt ghép và xử lý Layer).



UI Framework: streamlit, streamlit-antd-components (Menu đa cấp).



🎯 Điểm Vàng Công Nghệ

1\. Class-based UI

Hệ thống giao diện được thiết kế theo tính đóng gói cao. Việc mở rộng tính năng mới (như Analytics hay AI Script Generator) chỉ đơn giản là tạo thêm một Class kế thừa từ BaseInterface mà không ảnh hưởng đến mã nguồn hiện tại.



2\. Quản lý phân cấp (The Hierarchy)

Tổ chức dữ liệu dạng Catalog -> Course -> Chapter -> Lesson giúp hệ thống quản lý hàng nghìn video một cách khoa học. Mọi thay đổi về Branding tại file course\_meta.json sẽ tự động cập nhật cho toàn bộ bài học thuộc khóa đó.



3\. Trí nhớ dài hạn (Cross-Lesson Memory)

Sử dụng VectorDB để lưu trữ "dấu vân tay" kiến thức của từng bài học. Khi render bài mới, AI sẽ tự động tra cứu để tạo các câu dẫn (Recap) hoặc nhắc lại kiến thức cũ, tạo sự gắn kết chặt chẽ cho toàn bộ khóa học.



4\. Logic Engine (Manim + Graphviz)

Tự động hóa việc biến văn bản thô thành sơ đồ tư duy động và các chuyển động hình học trừu tượng.



Ví dụ: Input "Luồng dữ liệu từ A qua B" -> Output clip Manim với mũi tên và các khối hộp chuyển động 60fps chuyên nghiệp.



💡 Quy trình vận hành

Dashboard: Tạo khóa học mới và thiết lập bộ nhận diện thương hiệu.



Editor: AI soạn kịch bản tự động hoặc nhập thủ công. Classifier sẽ tự động gán nhãn module xử lý cho từng phân cảnh.



Preparation: Kiểm tra trí nhớ bài cũ để tạo các đoạn dẫn nhập liên kết bài học.



Render: Nhấn nút sản xuất và theo dõi tiến trình qua Render Console. Hệ thống sẽ tự động phối hợp các Engine để xuất video hoàn chỉnh.



🤖 Hướng dẫn cho AI Collaborator

Sau này, bạn chỉ cần ra lệnh:



"Code Engine Logic dùng Manim vẽ sơ đồ mũi tên cho cảnh X."



"Xây dựng UI cho tab Editor để chỉnh sửa kịch bản bài học."



"Viết hàm Memory truy vấn kiến thức của Chương 1 để nối vào Chương 2."



Phát triển bởi Vũ - SmartVideo Factory OS 2026

