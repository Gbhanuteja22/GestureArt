import cv2
import numpy as np
import mediapipe as mp
import time
class HandTracker:
    def __init__(self, static_mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        self.static_mode = static_mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.static_mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.prev_landmarks = None
        self.landmark_velocity = np.zeros((21, 2))
        self.last_update_time = time.time()
    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            self.results = self.hands.process(img_rgb)
        except Exception as e:
            print(f"Error processing hand image: {e}")
            return img, False
        hands_detected = self.results.multi_hand_landmarks is not None
        if draw and hands_detected:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    img, 
                    hand_landmarks, 
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
        return img, hands_detected
    def find_positions(self, img, hand_no=0, draw=True):
        h, w, c = img.shape
        landmarks = []
        hand_detected = False
        if self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                hand_landmarks = self.results.multi_hand_landmarks[hand_no]
                hand_detected = True
                current_time = time.time()
                dt = current_time - self.last_update_time if self.prev_landmarks is not None else 0
                self.last_update_time = current_time
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    landmarks.append([id, cx, cy, lm.z])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                if self.prev_landmarks is not None and dt > 0:
                    for i, landmark in enumerate(landmarks):
                        if i < len(self.prev_landmarks):
                            prev_x, prev_y = self.prev_landmarks[i][1], self.prev_landmarks[i][2]
                            curr_x, curr_y = landmark[1], landmark[2]
                            vx = (curr_x - prev_x) / dt
                            vy = (curr_y - prev_y) / dt
                            alpha = 0.7
                            self.landmark_velocity[i][0] = alpha * self.landmark_velocity[i][0] + (1 - alpha) * vx
                            self.landmark_velocity[i][1] = alpha * self.landmark_velocity[i][1] + (1 - alpha) * vy
                self.prev_landmarks = landmarks.copy()
        return landmarks, hand_detected
    def fingers_up(self, landmarks):
        if not landmarks:
            return [0, 0, 0, 0, 0]
        fingers = []
        if landmarks[4][1] > landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for tip_id in [8, 12, 16, 20]:
            if landmarks[tip_id][2] < landmarks[tip_id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    def get_landmark_velocity(self, landmark_id):
        if landmark_id < 0 or landmark_id >= 21:
            return (0, 0)
        return tuple(self.landmark_velocity[landmark_id])
    def get_hand_center(self, landmarks):
        if not landmarks:
            return None
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        center_x = (wrist[1] + middle_mcp[1]) // 2
        center_y = (wrist[2] + middle_mcp[2]) // 2
        return (center_x, center_y)
    def get_hand_size(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return 0
        wrist = landmarks[0]
        middle_tip = landmarks[12]
        dx = middle_tip[1] - wrist[1]
        dy = middle_tip[2] - wrist[2]
        return np.sqrt(dx*dx + dy*dy)
    def reset(self):
        self.prev_landmarks = None
        self.landmark_velocity = np.zeros((21, 2))
        self.last_update_time = time.time()
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    tracker = HandTracker()
    prev_time = 0
    curr_time = 0
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture frame from webcam")
            break
        img, hands_detected = tracker.find_hands(img)
        landmarks = []
        if hands_detected:
            landmarks, hand_detected = tracker.find_positions(img)
            if hand_detected:
                fingers_up = tracker.fingers_up(landmarks)
                hand_center = tracker.get_hand_center(landmarks)
                hand_size = tracker.get_hand_size(landmarks)
                cv2.putText(img, f"Fingers: {fingers_up}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if hand_center:
                    cv2.circle(img, hand_center, 10, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f"Center: {hand_center}", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                cv2.putText(img, f"Size: {int(hand_size)}", (10, 130), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if len(landmarks) > 8:
                    vx, vy = tracker.get_landmark_velocity(8)
                    cv2.putText(img, f"Velocity: ({int(vx)}, {int(vy)})", (10, 160), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
        prev_time = curr_time
        cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()