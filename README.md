<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    BIRD SHOOTING GAME - COMPUTER VISION
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

---

## 📖 1. Giới thiệu
Dự án **Bird Shooting Game** là một ứng dụng tương tác thời gian thực được thực hiện trong học phần **Xử lý ảnh & Thị giác máy tính**. Ứng dụng sử dụng công nghệ nhận diện cử chỉ bàn tay (Hand Tracking) để tạo ra trải nghiệm chơi game tương tác không tiếp xúc.

## 🔧 2. Các công nghệ sử dụng
<div align="center">

### Hệ điều hành
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)

### Công nghệ chính
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-008272?style=for-the-badge&logo=google&logoColor=white)](https://mediapipe.dev/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![Pygame](https://img.shields.io/badge/Pygame-111111?style=for-the-badge&logo=python&logoColor=white)](https://www.pygame.org/)

</div>

---

## 🚀 3. Tính năng cốt lõi
* **Hand Tracking:** Nhận diện 21 điểm mốc xương bàn tay.
* **Gesture Control:** Điều khiển hồng tâm bằng ngón trỏ, bắn bằng cử chỉ chụm và nạp đạn bằng cử chỉ "Rock".
* **Gamification:** Hệ thống câu hỏi, tính điểm, mạng (lives) và lưu lịch sử Ranking.

---

## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ và môi trường

#### 4.1.1. Tải dự án
```bash
git clone [https://github.com/6789aggy/XL_Anh.git](https://github.com/6789aggy/XL_Anh.git)
cd XL_Anh

---

### 4.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi lệnh sau để cài đặt tự động toàn bộ các thư viện được yêu cầu:

Bash
pip install -r requirements.txt
🎮 5. Hướng dẫn cách chơi
Trò chơi sử dụng hoàn toàn bằng tương tác cử chỉ tay trước Camera:

Nhập tên: Click vào ô "ENTER NAME" tại Menu chính và nhập tên để ghi danh.

Điều khiển tâm ngắm: Di chuyển ngón tay trỏ trước camera để di chuyển hồng tâm.

Thao tác bắn: Chụm đầu ngón cái và ngón trỏ lại với nhau để thực hiện lệnh bắn.

Cơ chế nạp đạn: Khi hết đạn (Ammo: 0/5), thực hiện cử chỉ Rock (🤘) để nạp lại.

Hỗ trợ: Nhấn phím H hoặc nút Help trên màn hình để hiện đáp án gợi ý.

⚙️ 6. Cơ chế hoạt động của Game
6.1. Xử lý hình ảnh (Computer Vision)
Thu thập: OpenCV xử lý luồng video từ webcam theo thời gian thực.

Phân tích: MediaPipe Hands xác định tọa độ các điểm mốc xương bàn tay.

Chuẩn hóa: Ánh xạ tọa độ từ khung hình camera sang độ phân giải màn hình Game (1280x720).

6.2. Nhận diện cử chỉ (Gesture Recognition)
Logic bắn: Tính toán khoảng cách giữa Landmark 4 (ngón cái) và Landmark 8 (ngón trỏ).

Logic nạp đạn: Nhận diện trạng thái các ngón tay để kích hoạt nạp đạn khi phát hiện cử chỉ 🤘.

6.3. Logic Trò chơi (Game Engine)
Xử lý va chạm: Pygame kiểm tra tọa độ bắn so với vùng bao (Rect) của các mục tiêu.

Quản lý dữ liệu: Lưu trữ và truy xuất câu hỏi/lịch sử thông qua các file JSON.

📝 7. License
© 2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.