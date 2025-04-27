import cv2
import numpy as np
import time
from enum import Enum
class UIElement(Enum):
    HEADER = 0
    COLOR_PICKER = 1
    BRUSH_SELECTOR = 2
    HELP = 3
    SETTINGS = 4
class UIManager:
    def __init__(self, width=1280, height=720):
        self.width = width
        self.height = height
        self.elements = {
            UIElement.HEADER: {
                "visible": True,
                "rect": (0, 0, width, 60),
                "buttons": [
                    {"name": "Clear", "rect": (10, 10, 80, 40), "active": False},
                    {"name": "Undo", "rect": (100, 10, 80, 40), "active": False},
                    {"name": "Redo", "rect": (190, 10, 80, 40), "active": False},
                    {"name": "Color", "rect": (280, 10, 80, 40), "active": False},
                    {"name": "Brush", "rect": (370, 10, 80, 40), "active": False},
                    {"name": "Save", "rect": (460, 10, 80, 40), "active": False},
                    {"name": "Help", "rect": (550, 10, 80, 40), "active": False}
                ]
            },
            UIElement.COLOR_PICKER: {
                "visible": False,
                "rect": (50, 70, 300, 300),
                "colors": [
                    {"color": (0, 0, 0), "rect": (60, 80, 40, 40), "active": False},      # Black
                    {"color": (255, 255, 255), "rect": (110, 80, 40, 40), "active": False}, # White
                    {"color": (0, 0, 255), "rect": (160, 80, 40, 40), "active": False},   # Red
                    {"color": (0, 255, 0), "rect": (210, 80, 40, 40), "active": False},   # Green
                    {"color": (255, 0, 0), "rect": (260, 80, 40, 40), "active": False},   # Blue
                    {"color": (0, 255, 255), "rect": (60, 130, 40, 40), "active": False}, # Yellow
                    {"color": (255, 0, 255), "rect": (110, 130, 40, 40), "active": False}, # Magenta
                    {"color": (255, 255, 0), "rect": (160, 130, 40, 40), "active": False}, # Cyan
                    {"color": (128, 0, 0), "rect": (210, 130, 40, 40), "active": False},  # Dark blue
                    {"color": (0, 128, 0), "rect": (260, 130, 40, 40), "active": False},  # Dark green
                    {"color": (0, 0, 128), "rect": (60, 180, 40, 40), "active": False},   # Dark red
                    {"color": (128, 128, 0), "rect": (110, 180, 40, 40), "active": False}, # Dark cyan
                    {"color": (128, 0, 128), "rect": (160, 180, 40, 40), "active": False}, # Dark magenta
                    {"color": (0, 128, 128), "rect": (210, 180, 40, 40), "active": False}, # Dark yellow
                    {"color": (128, 128, 128), "rect": (260, 180, 40, 40), "active": False}, # Gray
                ],
                "sliders": [
                    {"name": "R", "rect": (60, 230, 240, 20), "value": 0, "active": False},
                    {"name": "G", "rect": (60, 260, 240, 20), "value": 0, "active": False},
                    {"name": "B", "rect": (60, 290, 240, 20), "value": 0, "active": False}
                ],
                "current_color": (0, 0, 0),
                "custom_color_rect": (310, 230, 30, 80)
            },
            UIElement.BRUSH_SELECTOR: {
                "visible": False,
                "rect": (50, 70, 300, 300),
                "brushes": [
                    {"name": "Standard", "rect": (60, 80, 120, 30), "active": True},
                    {"name": "Airbrush", "rect": (190, 80, 120, 30), "active": False},
                    {"name": "Calligraphy", "rect": (60, 120, 120, 30), "active": False},
                    {"name": "Marker", "rect": (190, 120, 120, 30), "active": False},
                    {"name": "Pencil", "rect": (60, 160, 120, 30), "active": False},
                    {"name": "Watercolor", "rect": (190, 160, 120, 30), "active": False},
                    {"name": "Neon", "rect": (60, 200, 120, 30), "active": False},
                    {"name": "Pixel", "rect": (190, 200, 120, 30), "active": False}
                ],
                "sliders": [
                    {"name": "Size", "rect": (60, 240, 240, 20), "value": 15, "min": 1, "max": 50, "active": False},
                    {"name": "Opacity", "rect": (60, 270, 240, 20), "value": 100, "min": 0, "max": 100, "active": False},
                    {"name": "Flow", "rect": (60, 300, 240, 20), "value": 100, "min": 0, "max": 100, "active": False}
                ]
            },
            UIElement.HELP: {
                "visible": False,
                "rect": (width // 4, height // 4, width // 2, height // 2),
                "content": [
                    "GestureArt Help",
                    "",
                    "Gestures:",
                    "- Draw: Index finger up",
                    "- Select: Index and middle fingers up",
                    "- Clear: All fingers up",
                    "- Undo: Thumb and index form a 'C'",
                    "- Color Pick: Index and pinky up",
                    "- Tool Change: Ring and pinky up",
                    "- Save: Thumb, index, and pinky up",
                    "",
                    "Keyboard Shortcuts:",
                    "- ESC: Exit application",
                    "- C: Clear canvas",
                    "- Z: Undo",
                    "- Y: Redo",
                    "- S: Save canvas",
                    "- H: Toggle help"
                ]
            },
            UIElement.SETTINGS: {
                "visible": False,
                "rect": (width // 4, height // 4, width // 2, height // 2),
                "settings": [
                    {"name": "Hand Detection Confidence", "rect": (width // 4 + 20, height // 4 + 50, width // 2 - 40, 20), "value": 0.7, "min": 0.1, "max": 1.0, "active": False},
                    {"name": "Hand Tracking Confidence", "rect": (width // 4 + 20, height // 4 + 80, width // 2 - 40, 20), "value": 0.5, "min": 0.1, "max": 1.0, "active": False},
                    {"name": "Gesture Detection Threshold", "rect": (width // 4 + 20, height // 4 + 110, width // 2 - 40, 20), "value": 0.8, "min": 0.1, "max": 1.0, "active": False},
                    {"name": "Max Hands", "rect": (width // 4 + 20, height // 4 + 140, width // 2 - 40, 20), "value": 1, "min": 1, "max": 2, "active": False}
                ],
                "buttons": [
                    {"name": "Apply", "rect": (width // 4 + width // 4 - 100, height // 4 + height // 2 - 50, 80, 30), "active": False},
                    {"name": "Cancel", "rect": (width // 4 + width // 4 + 20, height // 4 + height // 2 - 50, 80, 30), "active": False}
                ]
            }
        }
        self.gesture_indicator = {
            "visible": True,
            "rect": (width - 200, height - 50, 190, 40)
        }
        self.status_bar = {
            "visible": True,
            "rect": (0, height - 30, width, 30),
            "text": "Ready"
        }
        self.hover_element = None
        self.active_element = None
        self.last_interaction_time = time.time()
        self.auto_hide_delay = 3.0 
        self.last_render_time = 0
        self.render_count = 0
        self.avg_render_time = 0
    def render(self, frame, landmarks=None, gesture_info=None):
        start_time = time.time()
        result = frame.copy()
        current_time = time.time()
        if current_time - self.last_interaction_time > self.auto_hide_delay:
            self.elements[UIElement.COLOR_PICKER]["visible"] = False
            self.elements[UIElement.BRUSH_SELECTOR]["visible"] = False
        if self.elements[UIElement.HEADER]["visible"]:
            header_rect = self.elements[UIElement.HEADER]["rect"]
            cv2.rectangle(result, (header_rect[0], header_rect[1]), 
                         (header_rect[0] + header_rect[2], header_rect[1] + header_rect[3]), 
                         (200, 200, 200), -1)
            cv2.rectangle(result, (header_rect[0], header_rect[1]), 
                         (header_rect[0] + header_rect[2], header_rect[1] + header_rect[3]), 
                         (100, 100, 100), 2)
            for button in self.elements[UIElement.HEADER]["buttons"]:
                button_color = (150, 150, 150)
                text_color = (0, 0, 0)
                if button["active"]:
                    button_color = (100, 100, 255)
                    text_color = (255, 255, 255)
                cv2.rectangle(result, (button["rect"][0], button["rect"][1]), 
                             (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), 
                             button_color, -1)
                cv2.rectangle(result, (button["rect"][0], button["rect"][1]), 
                             (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), 
                             (50, 50, 50), 1)
                text_size = cv2.getTextSize(button["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_x = button["rect"][0] + (button["rect"][2] - text_size[0]) // 2
                text_y = button["rect"][1] + (button["rect"][3] + text_size[1]) // 2
                cv2.putText(result, button["name"], (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
        if self.elements[UIElement.COLOR_PICKER]["visible"]:
            color_picker = self.elements[UIElement.COLOR_PICKER]
            rect = color_picker["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            cv2.putText(result, "Color Picker", (rect[0] + 10, rect[1] + 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
            for color_item in color_picker["colors"]:
                color = color_item["color"]
                color_rect = color_item["rect"]
                cv2.rectangle(result, (color_rect[0], color_rect[1]), 
                             (color_rect[0] + color_rect[2], color_rect[1] + color_rect[3]), 
                             color, -1)
                border_color = (100, 100, 100)
                if color_item["active"]:
                    border_color = (0, 255, 0)
                cv2.rectangle(result, (color_rect[0], color_rect[1]), 
                             (color_rect[0] + color_rect[2], color_rect[1] + color_rect[3]), 
                             border_color, 2)
            for slider in color_picker["sliders"]:
                slider_rect = slider["rect"]
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + slider_rect[2], slider_rect[1] + slider_rect[3]), 
                             (200, 200, 200), -1)
                value_width = int(slider["value"] * slider_rect[2] / 255)
                slider_color = (0, 0, 0)
                if slider["name"] == "R":
                    slider_color = (0, 0, 255)
                elif slider["name"] == "G":
                    slider_color = (0, 255, 0)
                elif slider["name"] == "B":
                    slider_color = (255, 0, 0)
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + value_width, slider_rect[1] + slider_rect[3]), 
                             slider_color, -1)
                border_color = (100, 100, 100)
                if slider["active"]:
                    border_color = (0, 255, 0)
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + slider_rect[2], slider_rect[1] + slider_rect[3]), 
                             border_color, 1)
                cv2.putText(result, f"{slider['name']}: {slider['value']}", 
                           (slider_rect[0] - 30, slider_rect[1] + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            custom_rect = color_picker["custom_color_rect"]
            current_color = color_picker["current_color"]
            cv2.rectangle(result, (custom_rect[0], custom_rect[1]), 
                         (custom_rect[0] + custom_rect[2], custom_rect[1] + custom_rect[3]), 
                         current_color, -1)
            cv2.rectangle(result, (custom_rect[0], custom_rect[1]), 
                         (custom_rect[0] + custom_rect[2], custom_rect[1] + custom_rect[3]), 
                         (0, 0, 0), 1)
        if self.elements[UIElement.BRUSH_SELECTOR]["visible"]:
            brush_selector = self.elements[UIElement.BRUSH_SELECTOR]
            rect = brush_selector["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            cv2.putText(result, "Brush Selector", (rect[0] + 10, rect[1] + 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
            for brush in brush_selector["brushes"]:
                brush_rect = brush["rect"]
                button_color = (200, 200, 200)
                text_color = (0, 0, 0)
                if brush["active"]:
                    button_color = (100, 100, 255)
                    text_color = (255, 255, 255)
                cv2.rectangle(result, (brush_rect[0], brush_rect[1]), 
                             (brush_rect[0] + brush_rect[2], brush_rect[1] + brush_rect[3]), 
                             button_color, -1)
                cv2.rectangle(result, (brush_rect[0], brush_rect[1]), 
                             (brush_rect[0] + brush_rect[2], brush_rect[1] + brush_rect[3]), 
                             (100, 100, 100), 1)
                text_size = cv2.getTextSize(brush["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_x = brush_rect[0] + (brush_rect[2] - text_size[0]) // 2
                text_y = brush_rect[1] + (brush_rect[3] + text_size[1]) // 2
                cv2.putText(result, brush["name"], (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
            for slider in brush_selector["sliders"]:
                slider_rect = slider["rect"]
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + slider_rect[2], slider_rect[1] + slider_rect[3]), 
                             (200, 200, 200), -1)
                value_width = int((slider["value"] - slider["min"]) * slider_rect[2] / (slider["max"] - slider["min"]))
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + value_width, slider_rect[1] + slider_rect[3]), 
                             (100, 100, 255), -1)
                border_color = (100, 100, 100)
                if slider["active"]:
                    border_color = (0, 255, 0)
                cv2.rectangle(result, (slider_rect[0], slider_rect[1]), 
                             (slider_rect[0] + slider_rect[2], slider_rect[1] + slider_rect[3]), 
                             border_color, 1)
                cv2.putText(result, f"{slider['name']}: {slider['value']}", 
                           (slider_rect[0] - 30, slider_rect[1] + 15), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if self.elements[UIElement.HELP]["visible"]:
            help_element = self.elements[UIElement.HELP]
            rect = help_element["rect"]
            overlay = result.copy()
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            alpha = 0.8
            result = cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0)
            line_height = 25
            for i, line in enumerate(help_element["content"]):
                if i == 0:
                    cv2.putText(result, line, (rect[0] + 20, rect[1] + 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
                else:
                    cv2.putText(result, line, (rect[0] + 20, rect[1] + 30 + i * line_height), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        if self.elements[UIElement.SETTINGS]["visible"]:
            settings_element = self.elements[UIElement.SETTINGS]
            rect = settings_element["rect"]
            overlay = result.copy()
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            alpha = 0.8
            result = cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0)
            cv2.putText(result, "Settings", (rect[0] + 20, rect[1] + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
            for setting in settings_element["settings"]:
                setting_rect = setting["rect"]
                cv2.rectangle(result, (setting_rect[0], setting_rect[1]), 
                             (setting_rect[0] + setting_rect[2], setting_rect[1] + setting_rect[3]), 
                             (200, 200, 200), -1)
                value_width = int((setting["value"] - setting["min"]) * setting_rect[2] / (setting["max"] - setting["min"]))
                cv2.rectangle(result, (setting_rect[0], setting_rect[1]), 
                             (setting_rect[0] + value_width, setting_rect[1] + setting_rect[3]), 
                             (100, 100, 255), -1)
                border_color = (100, 100, 100)
                if setting["active"]:
                    border_color = (0, 255, 0)
                cv2.rectangle(result, (setting_rect[0], setting_rect[1]), 
                             (setting_rect[0] + setting_rect[2], setting_rect[1] + setting_rect[3]), 
                             border_color, 1)
                cv2.putText(result, f"{setting['name']}: {setting['value']:.1f}", 
                           (setting_rect[0], setting_rect[1] - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            for button in settings_element["buttons"]:
                button_rect = button["rect"]
                button_color = (200, 200, 200)
                text_color = (0, 0, 0)
                if button["active"]:
                    button_color = (100, 100, 255)
                    text_color = (255, 255, 255)
                cv2.rectangle(result, (button_rect[0], button_rect[1]), 
                             (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), 
                             button_color, -1)
                cv2.rectangle(result, (button_rect[0], button_rect[1]), 
                             (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), 
                             (100, 100, 100), 1)
                text_size = cv2.getTextSize(button["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_x = button_rect[0] + (button_rect[2] - text_size[0]) // 2
                text_y = button_rect[1] + (button_rect[3] + text_size[1]) // 2
                cv2.putText(result, button["name"], (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
        if self.gesture_indicator["visible"] and gesture_info:
            rect = self.gesture_indicator["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 1)
            gesture_name = gesture_info["gesture"].name if "gesture" in gesture_info else "NONE"
            gesture_state = gesture_info["state"].name if "state" in gesture_info else "NONE"
            cv2.putText(result, f"Gesture: {gesture_name}", (rect[0] + 10, rect[1] + 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(result, f"State: {gesture_state}", (rect[0] + 10, rect[1] + 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if self.status_bar["visible"]:
            rect = self.status_bar["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (200, 200, 200), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 1)
            cv2.putText(result, self.status_bar["text"], (rect[0] + 10, rect[1] + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if landmarks:
            self._highlight_interactive_elements(result, landmarks)
        end_time = time.time()
        self.last_render_time = end_time - start_time
        self.render_count += 1
        self.avg_render_time = ((self.render_count - 1) * self.avg_render_time + self.last_render_time) / self.render_count
        return result
    
    def _highlight_interactive_elements(self, frame, landmarks):
        index_tip = None
        for lm in landmarks:
            if lm[0] == 8: 
                index_tip = (lm[1], lm[2])
                break
        
        if not index_tip:
            return
        if self.elements[UIElement.HEADER]["visible"]:
            for button in self.elements[UIElement.HEADER]["buttons"]:
                if self._is_point_in_rect(index_tip, button["rect"]):
                    cv2.rectangle(frame, (button["rect"][0], button["rect"][1]), 
                                 (button["rect"][0] + button["rect"][2], button["rect"][1] + button["rect"][3]), 
                                 (0, 255, 0), 2)
        if self.elements[UIElement.COLOR_PICKER]["visible"]:
            color_picker = self.elements[UIElement.COLOR_PICKER]
            for color_item in color_picker["colors"]:
                if self._is_point_in_rect(index_tip, color_item["rect"]):
                    cv2.rectangle(frame, (color_item["rect"][0], color_item["rect"][1]), 
                                 (color_item["rect"][0] + color_item["rect"][2], color_item["rect"][1] + color_item["rect"][3]), 
                                 (0, 255, 0), 2)
            for slider in color_picker["sliders"]:
                if self._is_point_in_rect(index_tip, slider["rect"]):
                    cv2.rectangle(frame, (slider["rect"][0], slider["rect"][1]), 
                                 (slider["rect"][0] + slider["rect"][2], slider["rect"][1] + slider["rect"][3]), 
                                 (0, 255, 0), 2)
        if self.elements[UIElement.BRUSH_SELECTOR]["visible"]:
            brush_selector = self.elements[UIElement.BRUSH_SELECTOR]
            for brush in brush_selector["brushes"]:
                if self._is_point_in_rect(index_tip, brush["rect"]):
                    cv2.rectangle(frame, (brush["rect"][0], brush["rect"][1]), 
                                 (brush["rect"][0] + brush["rect"][2], brush["rect"][1] + brush["rect"][3]), 
                                 (0, 255, 0), 2)
            for slider in brush_selector["sliders"]:
                if self._is_point_in_rect(index_tip, slider["rect"]):
                    cv2.rectangle(frame, (slider["rect"][0], slider["rect"][1]), 
                                 (slider["rect"][0] + slider["rect"][2], slider["rect"][1] + slider["rect"][3]), 
                                 (0, 255, 0), 2)
    def handle_interaction(self, point, is_selecting=False):
        if point is None:
            return {"type": "none"}
        self.last_interaction_time = time.time()
        if self.elements[UIElement.HEADER]["visible"]:
            for button in self.elements[UIElement.HEADER]["buttons"]:
                if self._is_point_in_rect(point, button["rect"]):
                    if is_selecting:
                        if button["name"] == "Clear":
                            return {"type": "clear"}
                        elif button["name"] == "Undo":
                            return {"type": "undo"}
                        elif button["name"] == "Redo":
                            return {"type": "redo"}
                        elif button["name"] == "Color":
                            self.elements[UIElement.COLOR_PICKER]["visible"] = not self.elements[UIElement.COLOR_PICKER]["visible"]
                            if self.elements[UIElement.COLOR_PICKER]["visible"]:
                                self.elements[UIElement.BRUSH_SELECTOR]["visible"] = False
                            return {"type": "toggle_color_picker"}
                        elif button["name"] == "Brush":
                            self.elements[UIElement.BRUSH_SELECTOR]["visible"] = not self.elements[UIElement.BRUSH_SELECTOR]["visible"]
                            if self.elements[UIElement.BRUSH_SELECTOR]["visible"]:
                                self.elements[UIElement.COLOR_PICKER]["visible"] = False
                            return {"type": "toggle_brush_selector"}
                        elif button["name"] == "Save":
                            return {"type": "save"}
                        elif button["name"] == "Help":
                            self.elements[UIElement.HELP]["visible"] = not self.elements[UIElement.HELP]["visible"]
                            return {"type": "toggle_help"}
                    else:
                        return {"type": "hover", "element": "button", "name": button["name"]}
        if self.elements[UIElement.COLOR_PICKER]["visible"]:
            color_picker = self.elements[UIElement.COLOR_PICKER]
            if self._is_point_in_rect(point, color_picker["rect"]):
                for color_item in color_picker["colors"]:
                    if self._is_point_in_rect(point, color_item["rect"]):
                        if is_selecting:
                            color_picker["current_color"] = color_item["color"]
                            color_picker["sliders"][0]["value"] = color_item["color"][2]
                            color_picker["sliders"][1]["value"] = color_item["color"][1]
                            color_picker["sliders"][2]["value"] = color_item["color"][0]
                            return {"type": "color_selected", "color": color_item["color"]}
                        else:
                            return {"type": "hover", "element": "color", "color": color_item["color"]}
                for slider in color_picker["sliders"]:
                    if self._is_point_in_rect(point, slider["rect"]):
                        if is_selecting:
                            x_rel = point[0] - slider["rect"][0]
                            slider["value"] = int(x_rel * 255 / slider["rect"][2])
                            slider["value"] = max(0, min(255, slider["value"]))
                            r = color_picker["sliders"][0]["value"]
                            g = color_picker["sliders"][1]["value"]
                            b = color_picker["sliders"][2]["value"]
                            color_picker["current_color"] = (b, g, r)
                            return {"type": "slider_changed", "name": slider["name"], "value": slider["value"]}
                        else:
                            return {"type": "hover", "element": "slider", "name": slider["name"]}
                return {"type": "color_picker_interaction"}
        if self.elements[UIElement.BRUSH_SELECTOR]["visible"]:
            brush_selector = self.elements[UIElement.BRUSH_SELECTOR]
            if self._is_point_in_rect(point, brush_selector["rect"]):
                for brush in brush_selector["brushes"]:
                    if self._is_point_in_rect(point, brush["rect"]):
                        if is_selecting:
                            for b in brush_selector["brushes"]:
                                b["active"] = False
                            brush["active"] = True
                            return {"type": "brush_selected", "name": brush["name"]}
                        else:
                            return {"type": "hover", "element": "brush", "name": brush["name"]}
                for slider in brush_selector["sliders"]:
                    if self._is_point_in_rect(point, slider["rect"]):
                        if is_selecting:
                            x_rel = point[0] - slider["rect"][0]
                            value_range = slider["max"] - slider["min"]
                            slider["value"] = int(slider["min"] + x_rel * value_range / slider["rect"][2])
                            slider["value"] = max(slider["min"], min(slider["max"], slider["value"]))
                            return {"type": "brush_property_changed", "name": slider["name"], "value": slider["value"]}
                        else:
                            return {"type": "hover", "element": "slider", "name": slider["name"]}
                return {"type": "brush_selector_interaction"}
        if self.elements[UIElement.SETTINGS]["visible"]:
            settings_element = self.elements[UIElement.SETTINGS]
            if self._is_point_in_rect(point, settings_element["rect"]):
                for setting in settings_element["settings"]:
                    if self._is_point_in_rect(point, setting["rect"]):
                        if is_selecting:
                            x_rel = point[0] - setting["rect"][0]
                            value_range = setting["max"] - setting["min"]
                            setting["value"] = setting["min"] + x_rel * value_range / setting["rect"][2]
                            setting["value"] = max(setting["min"], min(setting["max"], setting["value"]))
                            return {"type": "setting_changed", "name": setting["name"], "value": setting["value"]}
                        else:
                            return {"type": "hover", "element": "setting", "name": setting["name"]}
                for button in settings_element["buttons"]:
                    if self._is_point_in_rect(point, button["rect"]):
                        if is_selecting:
                            if button["name"] == "Apply":
                                return {"type": "apply_settings"}
                            elif button["name"] == "Cancel":
                                self.elements[UIElement.SETTINGS]["visible"] = False
                                return {"type": "cancel_settings"}
                        else:
                            return {"type": "hover", "element": "button", "name": button["name"]}
                return {"type": "settings_interaction"}
        return {"type": "canvas"}
    def _is_point_in_rect(self, point, rect):
        x, y = point
        rx, ry, rw, rh = rect
        return rx <= x <= rx + rw and ry <= y <= ry + rh
    def toggle_help(self):
        self.elements[UIElement.HELP]["visible"] = not self.elements[UIElement.HELP]["visible"]
        return self.elements[UIElement.HELP]["visible"]
    def set_status(self, text):
        self.status_bar["text"] = text
    def get_active_brush(self):
        for brush in self.elements[UIElement.BRUSH_SELECTOR]["brushes"]:
            if brush["active"]:
                return brush["name"]
        return "Standard"
    def get_brush_properties(self):
        brush_selector = self.elements[UIElement.BRUSH_SELECTOR]
        properties = {}
        for slider in brush_selector["sliders"]:
            properties[slider["name"].lower()] = slider["value"]
        return properties
    def get_current_color(self):
        return self.elements[UIElement.COLOR_PICKER]["current_color"]
    def get_performance_metrics(self):
        return {
            "last_render_time": self.last_render_time * 1000,
            "avg_render_time": self.avg_render_time * 1000,  
            "render_count": self.render_count
        }
if __name__ == "__main__":
    cv2.namedWindow("UI Test", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("UI Test", 1280, 720)
    ui_manager = UIManager(1280, 720)
    canvas = np.ones((720, 1280, 3), dtype=np.uint8) * 255
    mouse_x, mouse_y = 0, 0
    mouse_down = False
    def mouse_callback(event, x, y, flags, param):
        global mouse_x, mouse_y, mouse_down
        mouse_x, mouse_y = x, y
        if event == cv2.EVENT_LBUTTONDOWN:
            mouse_down = True
            interaction = ui_manager.handle_interaction((x, y), True)
            print(f"Interaction: {interaction}")
        elif event == cv2.EVENT_LBUTTONUP:
            mouse_down = False
    cv2.setMouseCallback("UI Test", mouse_callback)
    while True:
        img = canvas.copy()
        ui_manager.handle_interaction((mouse_x, mouse_y), False)
        result = ui_manager.render(img)
        cv2.imshow("UI Test", result)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('h'):
            ui_manager.toggle_help()
        elif key == ord('c'):
            ui_manager.elements[UIElement.COLOR_PICKER]["visible"] = not ui_manager.elements[UIElement.COLOR_PICKER]["visible"]
        elif key == ord('b'):
            ui_manager.elements[UIElement.BRUSH_SELECTOR]["visible"] = not ui_manager.elements[UIElement.BRUSH_SELECTOR]["visible"]
        elif key == ord('s'):
            ui_manager.elements[UIElement.SETTINGS]["visible"] = not ui_manager.elements[UIElement.SETTINGS]["visible"]
    cv2.destroyAllWindows()