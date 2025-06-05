import cv2
import time
import traceback

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
        if not self.cap.isOpened():
            raise IOError(f"Cannot open webcam {cam_id}")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.tracker = HandTracker()
        self.recognizer = GestureRecognizer(detection_threshold=0.75)
        self.canvas = CanvasEngine(width, height, background_color=(255, 255, 255))
        self.ui = UIManager(width, height)

        self.mouse_point = None
        self.mouse_click = False
        self.last_action_time = time.time()
        self.action_cooldown = 0.3


        self.draw_gesture_active = False
        self.draw_gesture_lost_frames = 0
        self.max_lost_frames_threshold = 3

    def run(self):
        cv2.namedWindow("GestureArt")
        cv2.setMouseCallback("GestureArt", self.mouse_callback)

        while True:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("Camera Error: Failed to grab frame.")
                    time.sleep(0.5)
                    continue

                frame = cv2.flip(frame, 1)

                frame, hands_detected = self.tracker.find_hands(frame, draw=True)

                gesture = GestureType.NONE
                state = GestureState.NONE
                conf = 0
                interaction_point = self.mouse_point
                current_time = time.time()

                if hands_detected:
                    landmarks, found = self.tracker.find_positions(frame, draw=True)
                    if found and landmarks and len(landmarks) > 8:

                        interaction_point = (landmarks[8][1], landmarks[8][2])

                        ix = max(0, min(interaction_point[0], self.width - 1))
                        iy = max(0, min(interaction_point[1], self.height - 1))
                        interaction_point = (ix, iy)

                        fingers = self.tracker.fingers_up(landmarks)
                        gesture, conf, state = self.recognizer.recognize_gesture(landmarks, fingers)

                        if gesture == GestureType.DRAW:
                            self.canvas.draw(interaction_point, pressure=1.0, is_drawing=True)
                            self.draw_gesture_active = True
                            self.draw_gesture_lost_frames = 0
                        else:

                            if self.draw_gesture_active:
                                self.draw_gesture_lost_frames += 1
                                if self.draw_gesture_lost_frames > self.max_lost_frames_threshold:
                                    self.canvas.draw(None, is_drawing=False)
                                    self.draw_gesture_active = False
                                    self.draw_gesture_lost_frames = 0


                            if not self.draw_gesture_active and state == GestureState.COMPLETED and current_time - self.last_action_time > self.action_cooldown:
                                if gesture == GestureType.CLEAR:
                                    self.canvas.clear()
                                    self.last_action_time = current_time
                                elif gesture == GestureType.SAVE:
                                    self.canvas.save("output/drawing.png")
                                    self.last_action_time = current_time

                    else:

                         if self.draw_gesture_active:
                            self.draw_gesture_lost_frames += 1
                            if self.draw_gesture_lost_frames > self.max_lost_frames_threshold:
                                self.canvas.draw(None, is_drawing=False)
                                self.draw_gesture_active = False
                                self.draw_gesture_lost_frames = 0
                else:

                    if self.draw_gesture_active:
                        self.canvas.draw(None, is_drawing=False)
                        self.draw_gesture_active = False
                        self.draw_gesture_lost_frames = 0


                is_interacting_ui = (gesture == GestureType.SELECT and not self.draw_gesture_active) or self.mouse_click
                interaction = self.ui.handle_interaction(interaction_point, is_interacting_ui)

                if interaction:
                    action_type = interaction.get("type")

                    if action_type in ["clear", "undo", "redo", "save"] and current_time - self.last_action_time <= self.action_cooldown:
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

                                if brush_name.upper() == "ERASER":
                                    brush_enum = BrushType.NEON
                                else:

                                    brush_enum = BrushType[brush_name.upper()]
                                self.canvas.set_brush(brush_enum)
                            except KeyError:
                                print(f"Warning: Invalid brush name selected in UI: {brush_name}")
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


                if frame.shape != canvas_img.shape:
                    print(f"Warning: Frame shape {frame.shape} and Canvas shape {canvas_img.shape} differ. Resizing canvas image.")



                    compatible_canvas = np.full_like(frame, self.canvas.background_color)
                    h, w = canvas_img.shape[:2]
                    compatible_canvas[0:h, 0:w] = canvas_img
                    canvas_img = compatible_canvas


                composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)


                gesture_name_to_display = gesture.name if gesture != GestureType.NONE else "NONE"
                gesture_info_str = f"{gesture_name_to_display} ({conf:.2f}) St: {state.name}"
                final_frame = self.ui.render(composed, gesture_info=gesture_info_str)


                brush_name_ui = self.canvas.brush_type.name
                if brush_name_ui == "NEON":
                    brush_name_ui = "ERASER"
                status_text = f"Brush: {brush_name_ui} | Size: {self.canvas.brush_size}"
                self.ui.set_status(status_text)


                cv2.imshow("GestureArt", final_frame)


            except Exception as e:
                print("An error occurred in the main loop:")
                traceback.print_exc()

                break


            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('c'):
                 if current_time - self.last_action_time > self.action_cooldown:
                    self.canvas.clear()
                    self.last_action_time = current_time
            elif key == ord('z'):
                 if current_time - self.last_action_time > self.action_cooldown:
                    if self.canvas.undo():
                        self.last_action_time = current_time
            elif key == ord('y'):
                 if current_time - self.last_action_time > self.action_cooldown:
                    if self.canvas.redo():
                        self.last_action_time = current_time
            elif key == ord('s'):
                 if current_time - self.last_action_time > self.action_cooldown:
                    self.canvas.save("output/drawing.png")
                    self.last_action_time = current_time
            elif key == ord('h'):
                 self.ui.elements[UIElement.HELP]["visible"] = not self.ui.elements[UIElement.HELP]["visible"]

                 self.ui.last_interaction_time = current_time

        self.cap.release()
        cv2.destroyAllWindows()
        print("GestureArt Application Closed.")

    def mouse_callback(self, event, x, y, flags, param):

        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        self.mouse_point = (x, y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click = True

            interaction = self.ui.handle_interaction(self.mouse_point, True)
            if interaction:
                 self.draw_gesture_active = False
        elif event == cv2.EVENT_LBUTTONUP:
             self.mouse_click = False

             self.ui.handle_interaction(self.mouse_point, False)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_click:

                interaction = self.ui.handle_interaction(self.mouse_point, True)
                if not interaction:
                    self.canvas.draw(self.mouse_point, pressure=1.0, is_drawing=True)
                    self.draw_gesture_active = True
                else:

                    if self.draw_gesture_active:
                        self.canvas.draw(None, is_drawing=False)
                        self.draw_gesture_active = False
            else:
                 self.ui.handle_interaction(self.mouse_point, False)

if __name__ == '__main__':

    import os
    if not os.path.exists("output"):
        os.makedirs("output")

    try:
        app = GestureArtApp()
        app.run()
    except Exception as e:
        print("Failed to initialize or run the application:")
        traceback.print_exc()

