from enum import Enum
import cv2
import numpy as np
import time
class GestureType(Enum):
    NONE = 0
    DRAW = 1
    SELECT = 2
    CLEAR = 3
    UNDO = 4
    REDO = 5
    SAVE = 6
    COLOR_PICK = 7
    TOOL_CHANGE = 8
    TEXT_INPUT = 9
class GestureState(Enum):
    NONE = 0
    STARTED = 1
    ONGOING = 2
    COMPLETED = 3
class GestureRecognizer:
    def __init__(self, detection_threshold=0.8):
        self.detection_threshold = detection_threshold
        self.current_gesture = GestureType.NONE
        self.current_state = GestureState.NONE
        self.current_confidence = 0.0
        self.gesture_start_time = 0
        self.gesture_duration = 0
        self.prev_fingers_up = [0, 0, 0, 0, 0]
        self.gesture_history = []
        self.max_history_size = 10
        self.gesture_cooldown = 0.5
        self.last_gesture_time = 0
    def recognize_gesture(self, landmarks, fingers_up):
        current_time = time.time()
        if not landmarks or not fingers_up:
            self._update_state(GestureType.NONE, 0.0, current_time)
            return GestureType.NONE, 0.0, GestureState.NONE
        gesture_type, confidence = self._detect_gesture(landmarks, fingers_up)
        if confidence < self.detection_threshold:
            gesture_type = GestureType.NONE
        self._update_state(gesture_type, confidence, current_time)
        return self.current_gesture, self.current_confidence, self.current_state
    def _detect_gesture(self, landmarks, fingers_up):
        if sum(fingers_up) == 1 and fingers_up[1] == 1:
            return GestureType.DRAW, 0.9
        elif sum(fingers_up) == 2 and fingers_up[1] == 1 and fingers_up[2] == 1:
            return GestureType.SELECT, 0.9
        elif sum(fingers_up) == 5:
            return GestureType.CLEAR, 0.9
        elif fingers_up[0] == 1 and fingers_up[1] == 1 and sum(fingers_up) == 2:
            return self._detect_undo_gesture(landmarks)
        elif fingers_up[0] == 1 and fingers_up[4] == 1 and sum(fingers_up) == 3:
            return GestureType.SAVE, 0.85
        elif fingers_up[1] == 1 and fingers_up[4] == 1 and sum(fingers_up) == 2:
            return GestureType.COLOR_PICK, 0.85
        elif fingers_up[3] == 1 and fingers_up[4] == 1 and sum(fingers_up) == 2:
            return GestureType.TOOL_CHANGE, 0.85
        elif fingers_up[1] == 1 and fingers_up[2] == 1 and fingers_up[3] == 1 and sum(fingers_up) == 3:
            return GestureType.TEXT_INPUT, 0.85
        return GestureType.NONE, 0.0
    def _detect_undo_gesture(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return GestureType.NONE, 0.0
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        distance = self._calculate_distance(
            (thumb_tip[1], thumb_tip[2]),
            (index_tip[1], index_tip[2])
        )
        thumb_mcp = landmarks[2]
        index_pip = landmarks[6]
        hand_size = self._calculate_distance(
            (thumb_mcp[1], thumb_mcp[2]),
            (index_pip[1], index_pip[2])
        )
        if distance < hand_size * 0.3:
            return GestureType.UNDO, 0.85
        return GestureType.NONE, 0.0
    def _calculate_distance(self, p1, p2):
        return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    def _update_state(self, gesture_type, confidence, current_time):
        self.current_confidence = confidence
        if gesture_type == GestureType.NONE:
            if self.current_gesture != GestureType.NONE and self.current_state == GestureState.ONGOING:
                self.current_state = GestureState.COMPLETED
                self.gesture_duration = current_time - self.gesture_start_time
                self._add_to_history(self.current_gesture, self.gesture_duration)
                self.last_gesture_time = current_time
            elif self.current_state == GestureState.COMPLETED and current_time - self.last_gesture_time > self.gesture_cooldown:
                self.current_gesture = GestureType.NONE
                self.current_state = GestureState.NONE
        else:
            if self.current_gesture == GestureType.NONE:
                self.current_gesture = gesture_type
                self.current_state = GestureState.STARTED
                self.gesture_start_time = current_time
            elif self.current_gesture == gesture_type:
                if self.current_state == GestureState.STARTED:
                    self.current_state = GestureState.ONGOING
            else:
                self.current_gesture = gesture_type
                self.current_state = GestureState.STARTED
                self.gesture_start_time = current_time
    def _add_to_history(self, gesture_type, duration):
        self.gesture_history.append({
            "gesture": gesture_type,
            "duration": duration,
            "timestamp": time.time()
        })
        if len(self.gesture_history) > self.max_history_size:
            self.gesture_history.pop(0)
    def get_gesture_info(self):
        return {
            "gesture": self.current_gesture,
            "state": self.current_state,
            "confidence": self.current_confidence,
            "duration": time.time() - self.gesture_start_time if self.current_state == GestureState.ONGOING else self.gesture_duration
        }
    def reset(self):
        self.current_gesture = GestureType.NONE
        self.current_state = GestureState.NONE
        self.current_confidence = 0.0
        self.gesture_start_time = 0
        self.gesture_duration = 0
        self.prev_fingers_up = [0, 0, 0, 0, 0]
        self.gesture_history = []
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    from hand_tracking import HandTracker
    tracker = HandTracker()
    recognizer = GestureRecognizer()
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture frame from webcam")
            break
        img, hands_detected = tracker.find_hands(img)
        if hands_detected:
            landmarks, hand_detected = tracker.find_positions(img)
            if hand_detected:
                fingers_up = tracker.fingers_up(landmarks)
                gesture, confidence, state = recognizer.recognize_gesture(landmarks, fingers_up)
                cv2.putText(img, f"Gesture: {gesture.name}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(img, f"State: {state.name}", (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                cv2.putText(img, f"Confidence: {confidence:.2f}", (10, 130), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                if gesture != GestureType.NONE:
                    info = recognizer.get_gesture_info()
                    cv2.putText(img, f"Duration: {info['duration']:.2f}s", (10, 160), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        cv2.imshow("Gesture Recognition", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()