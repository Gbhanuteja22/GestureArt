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
                "rect": (50, 70, 300, 270), # Adjusted height
                "brushes": [
                    {"name": "Standard", "rect": (60, 100, 120, 30), "active": True},
                    {"name": "Calligraphy", "rect": (60, 140, 120, 30), "active": False},
                    {"name": "Watercolor", "rect": (190, 140, 120, 30), "active": False},
                    {"name": "Eraser", "rect": (60, 180, 120, 30), "active": False},
                    {"name": "Pixel", "rect": (190, 180, 120, 30), "active": False}
                ],
                "sliders": [
                    {"name": "Size", "rect": (60, 240, 240, 20), "value": 15, "min": 1, "max": 50, "active": False},
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
            cv2.putText(result, "Brush Selector", (rect[0] + 10, rect[1] + 20), 
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
                    cv2.putText(result, line, (rect[0] + 10, rect[1] + 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
                else:
                    cv2.putText(result, line, (rect[0] + 10, rect[1] + 30 + i * line_height), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        if self.elements[UIElement.SETTINGS]["visible"]:
            settings = self.elements[UIElement.SETTINGS]
            rect = settings["rect"]
            overlay = result.copy()
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (240, 240, 240), -1)
            cv2.rectangle(overlay, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            alpha = 0.8
            result = cv2.addWeighted(overlay, alpha, result, 1 - alpha, 0)
            cv2.putText(result, "Settings", (rect[0] + 10, rect[1] + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
            for setting in settings["settings"]:
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
                cv2.putText(result, f"{setting['name']}: {setting['value']:.2f}", 
                           (setting_rect[0], setting_rect[1] - 5), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            for button in settings["buttons"]:
                button_rect = button["rect"]
                button_color = (150, 150, 150)
                text_color = (0, 0, 0)
                if button["active"]:
                    button_color = (100, 100, 255)
                    text_color = (255, 255, 255)
                cv2.rectangle(result, (button_rect[0], button_rect[1]), 
                             (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), 
                             button_color, -1)
                cv2.rectangle(result, (button_rect[0], button_rect[1]), 
                             (button_rect[0] + button_rect[2], button_rect[1] + button_rect[3]), 
                             (50, 50, 50), 1)
                text_size = cv2.getTextSize(button["name"], cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                text_x = button_rect[0] + (button_rect[2] - text_size[0]) // 2
                text_y = button_rect[1] + (button_rect[3] + text_size[1]) // 2
                cv2.putText(result, button["name"], (text_x, text_y), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)
        if self.gesture_indicator["visible"] and gesture_info:
            rect = self.gesture_indicator["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (200, 200, 200), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            cv2.putText(result, f"Gesture: {gesture_info}", (rect[0] + 10, rect[1] + 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)
        if self.status_bar["visible"]:
            rect = self.status_bar["rect"]
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (200, 200, 200), -1)
            cv2.rectangle(result, (rect[0], rect[1]), 
                         (rect[0] + rect[2], rect[1] + rect[3]), 
                         (100, 100, 100), 2)
            cv2.putText(result, self.status_bar["text"], (rect[0] + 10, rect[1] + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        end_time = time.time()
        render_time = end_time - start_time
        self.last_render_time = render_time
        self.render_count += 1
        self.avg_render_time = ((self.render_count - 1) * self.avg_render_time + render_time) / self.render_count
        return result
    def handle_interaction(self, point, is_clicking):
        if point is None:
            return None
        x, y = point
        result = None
        self.hover_element = None
        if self.elements[UIElement.HEADER]["visible"]:
            header = self.elements[UIElement.HEADER]
            header_rect = header["rect"]
            if self._is_point_in_rect(x, y, header_rect):
                for button in header["buttons"]:
                    button_rect = button["rect"]
                    if self._is_point_in_rect(x, y, button_rect):
                        self.hover_element = button
                        button["active"] = is_clicking
                        if is_clicking:
                            self.last_interaction_time = time.time()
                            if button["name"] == "Clear":
                                result = {"type": "clear"}
                            elif button["name"] == "Undo":
                                result = {"type": "undo"}
                            elif button["name"] == "Redo":
                                result = {"type": "redo"}
                            elif button["name"] == "Color":
                                self.elements[UIElement.COLOR_PICKER]["visible"] = not self.elements[UIElement.COLOR_PICKER]["visible"]
                                self.elements[UIElement.BRUSH_SELECTOR]["visible"] = False
                            elif button["name"] == "Brush":
                                self.elements[UIElement.BRUSH_SELECTOR]["visible"] = not self.elements[UIElement.BRUSH_SELECTOR]["visible"]
                                self.elements[UIElement.COLOR_PICKER]["visible"] = False
                            elif button["name"] == "Save":
                                result = {"type": "save"}
                            elif button["name"] == "Help":
                                self.elements[UIElement.HELP]["visible"] = not self.elements[UIElement.HELP]["visible"]
                    else:
                        button["active"] = False
        if self.elements[UIElement.COLOR_PICKER]["visible"]:
            color_picker = self.elements[UIElement.COLOR_PICKER]
            rect = color_picker["rect"]
            if self._is_point_in_rect(x, y, rect):
                self.last_interaction_time = time.time()
                for color_item in color_picker["colors"]:
                    color_rect = color_item["rect"]
                    if self._is_point_in_rect(x, y, color_rect):
                        self.hover_element = color_item
                        if is_clicking:
                            for c in color_picker["colors"]:
                                c["active"] = False
                            color_item["active"] = True
                            color_picker["current_color"] = color_item["color"]
                            color_picker["sliders"][0]["value"] = color_item["color"][2]
                            color_picker["sliders"][1]["value"] = color_item["color"][1]
                            color_picker["sliders"][2]["value"] = color_item["color"][0]
                            result = {"type": "color_selected", "color": color_item["color"]}
                for slider in color_picker["sliders"]:
                    slider_rect = slider["rect"]
                    if self._is_point_in_rect(x, y, slider_rect):
                        self.hover_element = slider
                        if is_clicking:
                            slider["active"] = True
                            value = (x - slider_rect[0]) / slider_rect[2] * 255
                            value = max(0, min(255, value))
                            slider["value"] = int(value)
                            if slider["name"] == "R":
                                color_picker["current_color"] = (color_picker["current_color"][0], color_picker["current_color"][1], int(value))
                            elif slider["name"] == "G":
                                color_picker["current_color"] = (color_picker["current_color"][0], int(value), color_picker["current_color"][2])
                            elif slider["name"] == "B":
                                color_picker["current_color"] = (int(value), color_picker["current_color"][1], color_picker["current_color"][2])
                            result = {"type": "slider_changed", "name": slider["name"], "value": slider["value"]}
                    else:
                        slider["active"] = False
        if self.elements[UIElement.BRUSH_SELECTOR]["visible"]:
            brush_selector = self.elements[UIElement.BRUSH_SELECTOR]
            rect = brush_selector["rect"]
            if self._is_point_in_rect(x, y, rect):
                self.last_interaction_time = time.time()
                for brush in brush_selector["brushes"]:
                    brush_rect = brush["rect"]
                    if self._is_point_in_rect(x, y, brush_rect):
                        self.hover_element = brush
                        if is_clicking:
                            for b in brush_selector["brushes"]:
                                b["active"] = False
                            brush["active"] = True
                            result = {"type": "brush_selected", "name": brush["name"]}
                for slider in brush_selector["sliders"]:
                    slider_rect = slider["rect"]
                    if self._is_point_in_rect(x, y, slider_rect):
                        self.hover_element = slider
                        if is_clicking:
                            slider["active"] = True
                            value = (x - slider_rect[0]) / slider_rect[2] * (slider["max"] - slider["min"]) + slider["min"]
                            value = max(slider["min"], min(slider["max"], value))
                            slider["value"] = int(value)
                            result = {"type": "brush_property_changed", "name": slider["name"].lower(), "value": slider["value"]}
                    else:
                        slider["active"] = False
        if self.elements[UIElement.SETTINGS]["visible"]:
            settings = self.elements[UIElement.SETTINGS]
            rect = settings["rect"]
            if self._is_point_in_rect(x, y, rect):
                self.last_interaction_time = time.time()
                for setting in settings["settings"]:
                    setting_rect = setting["rect"]
                    if self._is_point_in_rect(x, y, setting_rect):
                        self.hover_element = setting
                        if is_clicking:
                            setting["active"] = True
                            value = (x - setting_rect[0]) / setting_rect[2] * (setting["max"] - setting["min"]) + setting["min"]
                            value = max(setting["min"], min(setting["max"], value))
                            setting["value"] = value
                            result = {"type": "setting_changed", "name": setting["name"], "value": setting["value"]}
                    else:
                        setting["active"] = False
                for button in settings["buttons"]:
                    button_rect = button["rect"]
                    if self._is_point_in_rect(x, y, button_rect):
                        self.hover_element = button
                        button["active"] = is_clicking
                        if is_clicking:
                            if button["name"] == "Apply":
                                result = {"type": "settings_apply"}
                            elif button["name"] == "Cancel":
                                self.elements[UIElement.SETTINGS]["visible"] = False
                    else:
                        button["active"] = False
        return result
    def _is_point_in_rect(self, x, y, rect):
        return rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]
    def set_status(self, text):
        self.status_bar["text"] = text
    def get_performance_metrics(self):
        return {
            "last_render_time": self.last_render_time * 1000,
            "avg_render_time": self.avg_render_time * 1000,
            "render_count": self.render_count
        }
