import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils

    def find_position(self, frame):
        h, w, c = frame.shape
        cursor_pos = None
        is_firing = False

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_lms in results.multi_hand_landmarks:
                # Lấy tọa độ đầu ngón trỏ (Index Finger Tip)
                index_tip = hand_lms.landmark[8]
                cursor_pos = (int((1 - index_tip.x) * 1280), int(index_tip.y * 720)) # Mirror x

                # Logic bắn: Nếu đầu ngón cái (4) gần đầu ngón trỏ (8) -> Bóp cò
                thumb_tip = hand_lms.landmark[4]
                distance = ((index_tip.x - thumb_tip.x)**2 + (index_tip.y - thumb_tip.y)**2)**0.5
                if distance < 0.05:
                    is_firing = True
                
                # Vẽ xương tay lên frame (tùy chọn để debug)
                # self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)

        return cursor_pos, is_firing