🐦 Bird Shooting Game - MediaPipe Edition
Trò chơi bắn chim tương tác bằng cử chỉ tay sử dụng công nghệ thị giác máy tính (Computer Vision). Thay vì dùng chuột, bạn sẽ điều khiển tâm ngắm và bắn bằng chính bàn tay của mình thông qua Camera.

🌟 Tính năng nổi bật
Điều khiển bằng cử chỉ (Hand Tracking): - 🖐️ Tâm ngắm: Di chuyển ngón trỏ để điều khiển tâm ngắm trên màn hình.

👌 Bắn: Chụm ngón cái và ngón trỏ để khai hỏa.

🤘 Nạp đạn: Thực hiện cử chỉ "Rock" (ngón trỏ và út giơ lên) để nạp đầy băng đạn.

Hệ thống câu hỏi: Tích hợp các câu hỏi toán học/kiến thức giúp vừa chơi vừa học.

AI Assist: Nhấn phím H để hiển thị đáp án và mục tiêu cần bắn.

Bảng xếp hạng (Top Ranking): Lưu giữ lịch sử người chơi, điểm số và tỉ lệ chính xác (ACC).

Trình quản lý dữ liệu: Giao diện chỉnh sửa câu hỏi và xem lịch sử chi tiết tích hợp sẵn.

Âm thanh sống động: Hiệu ứng bắn, nạp đạn, nhạc nền và âm thanh thắng/thua.

🛠 Yêu cầu hệ thống
Python 3.10 trở lên.

Camera/Webcam hoạt động tốt.

🚀 Hướng dẫn cài đặt
Tải mã nguồn:

Bash
git clone https://github.com/6789aggy/XL_Anh.git
cd XL_Anh
Cài đặt thư viện cần thiết:

Bash
pip install -r requirements.txt
Chạy Game:

Bash
python main.py
🎮 Cách chơi
Nhập tên: Nhập tên của bạn tại Menu chính để ghi danh vào bảng xếp hạng.

Ngắm bắn: Đưa ngón trỏ lên trước camera để di chuyển tâm ngắm. Bắn vào con chim mang đáp án đúng cho câu hỏi hiện tại.

Nạp đạn: Bạn có tối đa 5 viên đạn. Khi hết đạn, hãy làm cử chỉ Rock trước camera.

Mạng (Lives): Bạn có 3 mạng. Bắn sai hoặc bắn trượt sẽ bị trừ mạng.

Hỗ trợ: Nhấn phím H hoặc nút Help trên màn hình để bật chế độ trợ giúp nếu câu hỏi quá khó.

📁 Cấu trúc thư mục
main.py: File thực thi chính của trò chơi.

src/: Chứa các module xử lý (nhận diện tay, tiện ích dữ liệu).

data/: Chứa file questions.json (câu hỏi) và history.json (điểm số).

assets/: Chứa hình ảnh (images) và âm thanh (sounds).

🛠 Công nghệ sử dụng
Pygame: Xử lý đồ họa và logic game.

MediaPipe: Nhận diện và theo dõi các điểm mốc trên bàn tay.

OpenCV: Xử lý luồng video từ Camera.

Tkinter: Giao diện quản lý dữ liệu câu hỏi.

Author: [Your Name/GitHub Name]

Version: 1.0.0

Project: Xử lý ảnh & Thị giác máy tính.
