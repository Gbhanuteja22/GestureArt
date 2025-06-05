import cv2
import time
from hand_tracking import HandTracker
from gesture_recognition import GestureRecognizer, GestureType, GestureState
from canvas_engine import CanvasEngine, BrushType
from ui import UIManager, UIElement

class GestureArtApp:
    def __init__(self, cam_id=0, width=1280, height=720):
        self.cam_id = cam_id
        self.width = width
        self.height = height
        self.cap = cv2.VideoCapture(cam_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.tracker = HandTracker()
        self.recognizer = GestureRecognizer(detection_threshold=0.75)
        self.canvas = CanvasEngine(width, height, background_color=(255, 255, 255))
        self.ui = UIManager(width, height)
        self.last_draw_state = False
        self.mouse_point = None
        self.mouse_click = False
        self.last_action_time = time.time()
        self.action_cooldown = 0.3  # Cooldown in seconds to prevent rapid undo/redo

    def run(self):
        cv2.namedWindow("GestureArt")
        cv2.setMouseCallback("GestureArt", self.mouse_callback)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Camera Error")
                break

            frame = cv2.flip(frame, 1)
            frame, hands_detected = self.tracker.find_hands(frame)

            gesture = GestureType.NONE
            state = GestureState.NONE
            conf = 0
            interaction_point = self.mouse_point
            current_time = time.time()

            if hands_detected:
                landmarks, found = self.tracker.find_positions(frame)
                if found:
                    fingers = self.tracker.fingers_up(landmarks)
                    gesture, conf, state = self.recognizer.recognize_gesture(landmarks, fingers)
                    interaction_point = (landmarks[8][1], landmarks[8][2])

                    if gesture == GestureType.DRAW:
                        self.canvas.draw(interaction_point, pressure=1.0, is_drawing=True)
                        self.last_draw_state = True
                    else:
                        if self.last_draw_state:
                            # End drawing stroke
                            self.canvas.draw(None, is_drawing=False)
                            self.last_draw_state = False

                        # Add cooldown check for gesture actions
                        if state == GestureState.COMPLETED and current_time - self.last_action_time > self.action_cooldown:
                            if gesture == GestureType.CLEAR:
                                self.canvas.clear()
                                self.last_action_time = current_time
                            elif gesture == GestureType.UNDO:
                                if self.canvas.undo():
                                    self.last_action_time = current_time
                            elif gesture == GestureType.REDO:
                                if self.canvas.redo():
                                    self.last_action_time = current_time
                            elif gesture == GestureType.SAVE:
                                self.canvas.save("output/drawing.png")
                                self.last_action_time = current_time
                            elif gesture == GestureType.TOOL_CHANGE:
                                brushes = list(BrushType)
                                idx = brushes.index(self.canvas.brush_type)
                                new_brush = brushes[(idx + 1) % len(brushes)]
                                self.canvas.set_brush(new_brush)
                                self.last_action_time = current_time

            interaction = self.ui.handle_interaction(interaction_point, gesture == GestureType.SELECT or self.mouse_click)

            if interaction:
                action_type = interaction.get("type")
                # Add cooldown check for UI actions
                if action_type in ["clear", "undo", "redo", "save"] and current_time - self.last_action_time <= self.action_cooldown:
                    # Skip action if in cooldown period
                    pass
                elif action_type == "clear":
                    self.canvas.clear()
                    self.last_action_time = current_time
                elif action_type == "undo":
                    if self.canvas.undo():
                        self.last_action_time = current_time
                elif action_type == "redo":
                    if self.canvas.redo():
                        self.last_action_time = current_time
                elif action_type == "save":
                    self.canvas.save("output/drawing.png")
                    self.last_action_time = current_time
                elif action_type == "color_selected":
                    self.canvas.set_color(interaction["color"])
                elif action_type == "slider_changed":
                    current_color = self.ui.elements[UIElement.COLOR_PICKER]["current_color"]
                    self.canvas.set_color(current_color)
                elif action_type == "brush_selected":
                    brush_name = interaction["name"]
                    if isinstance(brush_name, str):
                        try:
                            # Handle the renamed Eraser brush
                            if brush_name.upper() == "ERASER":
                                brush_enum = BrushType.NEON  # Map UI's "Eraser" to backend's "NEON"
                            else:
                                brush_enum = BrushType[brush_name.upper()]
                            self.canvas.set_brush(brush_enum)
                        except KeyError:
                            print(f"Invalid brush name: {brush_name}")
                elif action_type == "brush_property_changed":
                    prop = interaction.get("name")
                    val = interaction.get("value")
                    if prop and val is not None:
                        try:
                            if prop == "size":
                                self.canvas.set_brush_size(int(val))
                        except Exception as e:
                            print(f"Error setting brush property: {prop} = {val} ({e})")

            self.mouse_click = False
            canvas_img = self.canvas.get_transformed_canvas()
            composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)
            final_frame = self.ui.render(composed)

            # Update status bar with current brush and size
            brush_name = self.canvas.brush_type.name
            if brush_name == "NEON":
                brush_name = "ERASER"  # Show as Eraser in UI
            status_text = f"Brush: {brush_name} | Size: {self.canvas.brush_size}"
            self.ui.set_status(status_text)

            cv2.putText(final_frame, f"Gesture: {gesture.name} ({conf:.2f})", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("GestureArt", final_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def mouse_callback(self, event, x, y, flags, param):
        self.mouse_point = (x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click = True

if __name__ == '__main__':
    app = GestureArtApp()
    app.run()
