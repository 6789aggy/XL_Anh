<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
        🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>

<h2 align="center">
    BIRD SHOOTING GAME - COMPUTER VISION
</h2>

<div align="center">
    <p>
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="FIT DNU Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

    <a href="https://www.facebook.com/DNUAIoTLab">
        <img src="https://img.shields.io/badge/AIoTLab-green?style=for-the-badge" />
    </a>

    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
        <img src="https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge" />
    </a>

    <a href="https://dainam.edu.vn">
        <img src="https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge" />
    </a>
</div>

---

# 📖 1. Giới thiệu

Dự án **Bird Shooting Game** là một ứng dụng tương tác thời gian thực được phát triển trong học phần **Xử lý ảnh & Thị giác máy tính**.

Ứng dụng sử dụng công nghệ **Computer Vision** để nhận diện cử chỉ bàn tay theo thời gian thực, từ đó cho phép người chơi điều khiển trò chơi mà không cần chuột hay bàn phím.

Hệ thống kết hợp giữa:
- **OpenCV** để xử lý hình ảnh webcam
- **MediaPipe Hands** để nhận diện bàn tay
- **Pygame** để xây dựng game engine
- **JSON** để quản lý dữ liệu câu hỏi và bảng xếp hạng

---

# 🔧 2. Công nghệ sử dụng

<div align="center">

## Hệ điều hành
<a href="https://www.microsoft.com/windows">
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" />
</a>

## Công nghệ chính

<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</a>

<a href="https://mediapipe.dev/">
    <img src="https://img.shields.io/badge/MediaPipe-008272?style=for-the-badge&logo=google&logoColor=white" />
</a>

<a href="https://opencv.org/">
    <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" />
</a>

<a href="https://www.pygame.org/">
    <img src="https://img.shields.io/badge/Pygame-111111?style=for-the-badge&logo=python&logoColor=white" />
</a>

</div>

---

# 🚀 3. Tính năng cốt lõi

### 🎯 Hand Tracking
- Nhận diện **21 điểm landmark bàn tay**
- Theo dõi chuyển động theo thời gian thực

### 🕹 Gesture Control
- Điều khiển tâm ngắm bằng **ngón trỏ**
- Bắn bằng cử chỉ **chụm ngón cái + ngón trỏ**
- Nạp đạn bằng cử chỉ **Rock (🤘)**

### 🎮 Gamification
- Hệ thống tính điểm
- Số mạng chơi (Lives)
- Số lượng đạn (Ammo)
- Câu hỏi tương tác
- Bảng xếp hạng người chơi

### 📂 Data Management
- Lưu lịch sử chơi bằng JSON
- Quản lý dữ liệu câu hỏi
- Lưu tên người chơi

---

# ⚙️ 4. Cài đặt

## 4.1 Clone project

```bash
git clone https://github.com/6789aggy/XL_Anh.git
cd XL_Anh
```

---

## 4.2 Cài thư viện

```bash
pip install -r requirements.txt
```

---

# ▶️ 5. Chạy game

```bash
python main.py
```

*(Nếu file chính của bạn tên khác thì thay `main.py` bằng tên file tương ứng.)*

---

# 🎮 6. Hướng dẫn chơi

Trò chơi sử dụng hoàn toàn bằng cử chỉ tay trước camera.

## 1. Nhập tên
- Click vào ô **ENTER NAME**
- Nhập tên người chơi

## 2. Điều khiển tâm ngắm
- Di chuyển **ngón trỏ** trước webcam
- Tâm ngắm sẽ di chuyển theo tay

## 3. Bắn
Thực hiện:

```text
Chụm ngón cái + ngón trỏ
```

để bắn mục tiêu.

## 4. Nạp đạn
Khi:

```text
Ammo = 0
```

thực hiện cử chỉ:

```text
🤘 Rock
```

để nạp lại đạn.

## 5. Hỗ trợ
- Nhấn phím **H**
- Hoặc nút **Help**

để hiện gợi ý.

---

# 🧠 7. Cơ chế hoạt động

## 7.1 Xử lý hình ảnh

### Thu thập
OpenCV lấy luồng video từ webcam theo thời gian thực.

### Phân tích
MediaPipe Hands xác định:
- vị trí bàn tay
- tọa độ landmark

### Chuẩn hóa
Ánh xạ từ camera sang màn hình game:

```text
1280 x 720
```

---

## 7.2 Nhận diện cử chỉ

### Logic bắn
Tính khoảng cách giữa:

```text
Landmark 4 (thumb tip)
Landmark 8 (index tip)
```

Nếu đủ gần → bắn.

### Logic nạp đạn
Phân tích trạng thái ngón tay để phát hiện:

```text
Rock gesture
```

---

## 7.3 Game Engine

### Va chạm
Pygame kiểm tra:
- tọa độ viên đạn
- vùng Rect của mục tiêu

### Gameplay
Quản lý:
- điểm số
- số mạng
- đạn
- trạng thái thắng/thua

---

# 📁 8. Cấu trúc project

```bash
BirdShootingGame/
│
├── main.py
├── requirements.txt
├── README.md
│
├── docs/
│   └── logo/
│       ├── aiotlab_logo.png
│       ├── fitdnu_logo.png
│       └── dnu_logo.png
│
├── assets/
│
├── data/
│   ├── questions.json
│   └── ranking.json
│
└── src/
```

---

# 📝 9. License

© 2026 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.