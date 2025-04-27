# import cv2
# import time
# from hand_tracking import HandTracker
# from gesture_recognition import GestureRecognizer, GestureType, GestureState
# from canvas_engine import CanvasEngine, BrushType
# from ui import UIManager, UIElement
# class GestureArtApp:
#     def __init__(self, cam_id=0, width=1280, height=720):
#         self.cam_id = cam_id
#         self.width = width
#         self.height = height
#         self.cap = cv2.VideoCapture(cam_id)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#         self.tracker = HandTracker()
#         self.recognizer = GestureRecognizer(detection_threshold=0.75)
#         self.canvas = CanvasEngine(width, height, background_color=(255, 255, 255))
#         self.ui = UIManager(width, height)
#         self.last_draw_state = False
#         self.mouse_point = None
#         self.mouse_click = False
#     def run(self):
#         cv2.namedWindow("GestureArt")
#         cv2.setMouseCallback("GestureArt", self.mouse_callback)
#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("Camera Error")
#                 break
#             frame = cv2.flip(frame, 1)
#             frame, hands_detected = self.tracker.find_hands(frame)
#             gesture = GestureType.NONE
#             state = GestureState.NONE
#             conf = 0
#             interaction_point = self.mouse_point
#             if hands_detected:
#                 landmarks, found = self.tracker.find_positions(frame)
#                 if found:
#                     fingers = self.tracker.fingers_up(landmarks)
#                     gesture, conf, state = self.recognizer.recognize_gesture(landmarks, fingers)
#                     interaction_point = (landmarks[8][1], landmarks[8][2])  # Index fingertip
#                     if gesture == GestureType.DRAW:
#                         self.canvas.draw(interaction_point, pressure=1.0, is_drawing=True)
#                         self.last_draw_state = True
#                     else:
#                         if self.last_draw_state:
#                             self.canvas.draw(None)
#                             self.last_draw_state = False
#                         if state == GestureState.COMPLETED:
#                             if gesture == GestureType.CLEAR:
#                                 self.canvas.clear()
#                             elif gesture == GestureType.UNDO:
#                                 self.canvas.undo()
#                             elif gesture == GestureType.REDO:
#                                 self.canvas.redo()
#                             elif gesture == GestureType.SAVE:
#                                 self.canvas.save("output/drawing.png")
#                             elif gesture == GestureType.TOOL_CHANGE:
#                                 brushes = list(BrushType)
#                                 idx = brushes.index(self.canvas.brush_type)
#                                 self.canvas.set_brush(brushes[(idx + 1) % len(brushes)])
#             interaction = self.ui.handle_interaction(interaction_point, gesture == GestureType.SELECT or self.mouse_click)
#             if interaction:
#                 if interaction["type"] == "clear":
#                     self.canvas.clear()
#                 elif interaction["type"] == "undo":
#                     self.canvas.undo()
#                 elif interaction["type"] == "redo":
#                     self.canvas.redo()
#                 elif interaction["type"] == "save":
#                     self.canvas.save("output/drawing.png")
#                 elif interaction["type"] == "color_selected":
#                     self.canvas.set_color(interaction["color"])
#                 elif interaction["type"] == "brush_selected":
#                     self.canvas.set_brush(interaction["name"])
#                 elif interaction["type"] == "brush_property_changed":
#                     prop = interaction["name"]
#                     val = interaction["value"]
#                     if prop == "size":
#                         self.canvas.set_brush_size(int(val))
#                     elif prop == "opacity":
#                         self.canvas.set_opacity(float(val))
#                     elif prop == "hardness":
#                         self.canvas.set_hardness(float(val))
#                     elif prop == "flow":
#                         self.canvas.set_flow(float(val))
#             self.mouse_click = False
#             canvas_img = self.canvas.get_transformed_canvas()
#             composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)
#             final_frame = self.ui.render(composed)
#             cv2.putText(final_frame, f"Gesture: {gesture.name} ({conf:.2f})", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
#             cv2.imshow("GestureArt", final_frame)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         self.cap.release()
#         cv2.destroyAllWindows()
#     def mouse_callback(self, event, x, y, flags, param):
#         self.mouse_point = (x, y)
#         if event == cv2.EVENT_LBUTTONDOWN:
#             self.mouse_click = True
# if __name__ == '__main__':
#     app = GestureArtApp()
#     app.run()








# import cv2
# import time
# from hand_tracking import HandTracker
# from gesture_recognition import GestureRecognizer, GestureType, GestureState
# from canvas_engine import CanvasEngine, BrushType
# from ui import UIManager, UIElement

# class GestureArtApp:
#     def __init__(self, cam_id=0, width=1280, height=720):
#         self.cam_id = cam_id
#         self.width = width
#         self.height = height
#         self.cap = cv2.VideoCapture(cam_id)
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
#         self.tracker = HandTracker()
#         self.recognizer = GestureRecognizer(detection_threshold=0.75)
#         self.canvas = CanvasEngine(width, height, background_color=(255, 255, 255))
#         self.ui = UIManager(width, height)
#         self.last_draw_state = False
#         self.mouse_point = None
#         self.mouse_click = False

#     def run(self):
#         cv2.namedWindow("GestureArt")
#         cv2.setMouseCallback("GestureArt", self.mouse_callback)

#         while True:
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("Camera Error")
#                 break

#             frame = cv2.flip(frame, 1)
#             frame, hands_detected = self.tracker.find_hands(frame)

#             gesture = GestureType.NONE
#             state = GestureState.NONE
#             conf = 0
#             interaction_point = self.mouse_point

#             if hands_detected:
#                 landmarks, found = self.tracker.find_positions(frame)
#                 if found:
#                     fingers = self.tracker.fingers_up(landmarks)
#                     gesture, conf, state = self.recognizer.recognize_gesture(landmarks, fingers)
#                     interaction_point = (landmarks[8][1], landmarks[8][2])  # Index fingertip

#                     if gesture == GestureType.DRAW:
#                         self.canvas.draw(interaction_point, pressure=1.0, is_drawing=True)
#                         self.last_draw_state = True
#                     else:
#                         if self.last_draw_state:
#                             self.canvas.draw(None)
#                             self.last_draw_state = False

#                         if state == GestureState.COMPLETED:
#                             if gesture == GestureType.CLEAR:
#                                 self.canvas.clear()
#                             elif gesture == GestureType.UNDO:
#                                 self.canvas.undo()
#                             elif gesture == GestureType.REDO:
#                                 self.canvas.redo()
#                             elif gesture == GestureType.SAVE:
#                                 self.canvas.save("output/drawing.png")
#                             elif gesture == GestureType.TOOL_CHANGE:
#                                 brushes = list(BrushType)
#                                 idx = brushes.index(self.canvas.brush_type)
#                                 new_brush = brushes[(idx + 1) % len(brushes)]
#                                 self.canvas.set_brush(new_brush)

#             interaction = self.ui.handle_interaction(interaction_point, gesture == GestureType.SELECT or self.mouse_click)

#             if interaction:
#                 action_type = interaction.get("type")

#                 if action_type == "clear":
#                     self.canvas.clear()
#                 elif action_type == "undo":
#                     self.canvas.undo()
#                 elif action_type == "redo":
#                     self.canvas.redo()
#                 elif action_type == "save":
#                     self.canvas.save("output/drawing.png")
#                 elif action_type == "color_selected":
#                     self.canvas.set_color(interaction["color"])
#                 elif action_type == "brush_selected":
#                     brush_name = interaction["name"]
#                     if isinstance(brush_name, str):
#                         try:
#                             brush_enum = BrushType[brush_name.upper()]
#                             self.canvas.set_brush(brush_enum)
#                         except KeyError:
#                             print(f"Invalid brush name: {brush_name}")
#                 elif action_type == "brush_property_changed":
#                     prop = interaction.get("name")
#                     val = interaction.get("value")
#                     if prop and val is not None:
#                         try:
#                             if prop == "size":
#                                 self.canvas.set_brush_size(int(val))
#                             elif prop == "opacity":
#                                 self.canvas.set_opacity(float(val))
#                             elif prop == "hardness":
#                                 self.canvas.set_hardness(float(val))
#                             elif prop == "flow":
#                                 self.canvas.set_flow(float(val))
#                         except Exception as e:
#                             print(f"Error setting brush property: {prop} = {val} ({e})")

#             self.mouse_click = False
#             canvas_img = self.canvas.get_transformed_canvas()
#             composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)
#             final_frame = self.ui.render(composed)

#             cv2.putText(final_frame, f"Gesture: {gesture.name} ({conf:.2f})", (10, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#             cv2.imshow("GestureArt", final_frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         self.cap.release()
#         cv2.destroyAllWindows()

#     def mouse_callback(self, event, x, y, flags, param):
#         self.mouse_point = (x, y)
#         if event == cv2.EVENT_LBUTTONDOWN:
#             self.mouse_click = True

# if __name__ == '__main__':
#     app = GestureArtApp()
#     app.run()












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
                            self.canvas.draw(None)
                            self.last_draw_state = False

                        if state == GestureState.COMPLETED:
                            if gesture == GestureType.CLEAR:
                                self.canvas.clear()
                            elif gesture == GestureType.UNDO:
                                self.canvas.undo()
                            elif gesture == GestureType.REDO:
                                self.canvas.redo()
                            elif gesture == GestureType.SAVE:
                                self.canvas.save("output/drawing.png")
                            elif gesture == GestureType.TOOL_CHANGE:
                                brushes = list(BrushType)
                                idx = brushes.index(self.canvas.brush_type)
                                new_brush = brushes[(idx + 1) % len(brushes)]
                                self.canvas.set_brush(new_brush)

            interaction = self.ui.handle_interaction(interaction_point, gesture == GestureType.SELECT or self.mouse_click)

            if interaction:
                action_type = interaction.get("type")
                if action_type == "clear":
                    self.canvas.clear()
                elif action_type == "undo":
                    self.canvas.undo()
                elif action_type == "redo":
                    self.canvas.redo()
                elif action_type == "save":
                    self.canvas.save("output/drawing.png")
                elif action_type == "color_selected":
                    self.canvas.set_color(interaction["color"])
                elif action_type == "brush_selected":
                    brush_name = interaction["name"]
                    if isinstance(brush_name, str):
                        try:
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
                            elif prop == "opacity":
                                self.canvas.set_opacity(float(val))
                            elif prop == "hardness":
                                self.canvas.set_hardness(float(val))
                            elif prop == "flow":
                                self.canvas.set_flow(float(val))
                        except Exception as e:
                            print(f"Error setting brush property: {prop} = {val} ({e})")

            self.mouse_click = False
            canvas_img = self.canvas.get_transformed_canvas()
            composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)
            final_frame = self.ui.render(composed)

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








