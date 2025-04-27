import cv2
import numpy as np
import os
import time
class PerformanceOptimizer:
    def __init__(self):
        self.frame_times = []
        self.max_frame_times = 30
        self.fps = 0
        self.last_frame_time = 0
        self.draw_times = []
        self.max_draw_times = 30
        self.avg_draw_time = 0
        self.process_times = []
        self.max_process_times = 30
        self.avg_process_time = 0
        self.memory_usage = []
        self.max_memory_points = 30
        self.start_time = time.time()
        self.total_frames = 0
    def start_frame(self):
        self.frame_start_time = time.time()
        return self.frame_start_time
    def end_frame(self):
        end_time = time.time()
        frame_time = end_time - self.frame_start_time
        self.frame_times.append(frame_time)
        if len(self.frame_times) > self.max_frame_times:
            self.frame_times.pop(0)
        if self.frame_times:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        self.last_frame_time = frame_time
        self.total_frames += 1
        return frame_time
    def record_draw_time(self, draw_time):
        self.draw_times.append(draw_time)
        if len(self.draw_times) > self.max_draw_times:
            self.draw_times.pop(0)
        if self.draw_times:
            self.avg_draw_time = sum(self.draw_times) / len(self.draw_times)
    def record_process_time(self, process_time):
        self.process_times.append(process_time)
        if len(self.process_times) > self.max_process_times:
            self.process_times.pop(0)
        if self.process_times:
            self.avg_process_time = sum(self.process_times) / len(self.process_times)
    def get_metrics(self):
        return {
            "fps": self.fps,
            "last_frame_time": self.last_frame_time * 1000,
            "avg_frame_time": (sum(self.frame_times) / len(self.frame_times) if self.frame_times else 0) * 1000,
            "avg_draw_time": self.avg_draw_time * 1000,
            "avg_process_time": self.avg_process_time * 1000,
            "total_frames": self.total_frames,
            "uptime": time.time() - self.start_time
        }
    def render_debug_overlay(self, frame):
        metrics = self.get_metrics()
        cv2.putText(frame, f"FPS: {int(metrics['fps'])}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame time: {metrics['last_frame_time']:.1f} ms", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f"Draw time: {metrics['avg_draw_time']:.1f} ms", (10, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f"Process time: {metrics['avg_process_time']:.1f} ms", (10, 100), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        cv2.putText(frame, f"Total frames: {metrics['total_frames']}", (10, 120), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        uptime_seconds = metrics['uptime']
        minutes, seconds = divmod(uptime_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        cv2.putText(frame, f"Uptime: {int(hours)}h {int(minutes)}m {int(seconds)}s", (10, 140), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        return frame
class CameraOptimizer:
    def __init__(self, camera_id=0, width=1280, height=720):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.frame_buffer = None
        self.last_frame_time = 0
        self.is_initialized = False
    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.is_initialized = self.cap.isOpened()
        if self.is_initialized:
            self.frame_buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        return self.is_initialized
    def read_frame(self):
        if not self.is_initialized:
            if not self.initialize():
                return False, None
        success, frame = self.cap.read()
        if not success:
            return False, self.frame_buffer
        self.frame_buffer = frame
        self.last_frame_time = time.time()
        return True, frame
    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.is_initialized = False
class GestureOptimizer:
    def __init__(self, smoothing_factor=0.7, history_size=5):
        self.smoothing_factor = smoothing_factor
        self.history_size = history_size
        self.position_history = []
        self.smoothed_position = None
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.last_update_time = 0
    def update(self, position):
        if position is None:
            return None
        current_time = time.time()
        dt = current_time - self.last_update_time if self.last_update_time > 0 else 0
        self.last_update_time = current_time
        self.position_history.append(position)
        if len(self.position_history) > self.history_size:
            self.position_history.pop(0)
        if not self.smoothed_position:
            self.smoothed_position = position
        else:
            self.smoothed_position = (
                self.smoothing_factor * self.smoothed_position[0] + (1 - self.smoothing_factor) * position[0],
                self.smoothing_factor * self.smoothed_position[1] + (1 - self.smoothing_factor) * position[1]
            )
        if dt > 0 and len(self.position_history) >= 2:
            prev_pos = self.position_history[-2]
            curr_pos = position
            curr_velocity = np.array([
                (curr_pos[0] - prev_pos[0]) / dt,
                (curr_pos[1] - prev_pos[1]) / dt
            ])
            prev_velocity = self.velocity.copy()
            self.velocity = self.smoothing_factor * self.velocity + (1 - self.smoothing_factor) * curr_velocity
            self.acceleration = (self.velocity - prev_velocity) / dt if dt > 0 else np.zeros(2)
        return self.smoothed_position
    def predict_position(self, time_ahead=0.05):
        if self.smoothed_position is None:
            return None
        predicted_position = (
            self.smoothed_position[0] + self.velocity[0] * time_ahead + 0.5 * self.acceleration[0] * time_ahead * time_ahead,
            self.smoothed_position[1] + self.velocity[1] * time_ahead + 0.5 * self.acceleration[1] * time_ahead * time_ahead
        )
        return predicted_position
    def get_velocity(self):
        return np.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
    def get_acceleration(self):
        return np.sqrt(self.acceleration[0]**2 + self.acceleration[1]**2)
    def reset(self):
        self.position_history = []
        self.smoothed_position = None
        self.velocity = np.zeros(2)
        self.acceleration = np.zeros(2)
        self.last_update_time = 0
if __name__ == "__main__":
    performance_optimizer = PerformanceOptimizer()
    camera_optimizer = CameraOptimizer()
    gesture_optimizer = GestureOptimizer()
    if not camera_optimizer.initialize():
        print("Failed to initialize camera")
        exit()
    cv2.namedWindow("Optimizer Test", cv2.WINDOW_NORMAL)
    while True:
        performance_optimizer.start_frame()
        success, frame = camera_optimizer.read_frame()
        if not success:
            print("Failed to read frame")
            break
        frame = cv2.flip(frame, 1)
        process_start = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        process_time = time.time() - process_start
        performance_optimizer.record_process_time(process_time)
        draw_start = time.time()
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                position = (cx, cy)
                smoothed_position = gesture_optimizer.update(position)
                predicted_position = gesture_optimizer.predict_position()
                if smoothed_position:
                    cv2.circle(frame, (int(smoothed_position[0]), int(smoothed_position[1])), 10, (0, 255, 0), -1)
                if predicted_position:
                    cv2.circle(frame, (int(predicted_position[0]), int(predicted_position[1])), 5, (255, 0, 0), -1)
                    cv2.line(frame, 
                            (int(smoothed_position[0]), int(smoothed_position[1])), 
                            (int(predicted_position[0]), int(predicted_position[1])), 
                            (255, 255, 0), 2)
                velocity = gesture_optimizer.get_velocity()
                cv2.putText(frame, f"Velocity: {velocity:.1f} px/s", (cx, cy - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        draw_time = time.time() - draw_start
        performance_optimizer.record_draw_time(draw_time)
        frame = performance_optimizer.render_debug_overlay(frame)
        cv2.imshow("Optimizer Test", frame)
        performance_optimizer.end_frame()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    camera_optimizer.release()
    cv2.destroyAllWindows()