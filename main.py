#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Manus sandbox testing: Handle user input and gestures for drawing.

Potential stability issues:
1. Rapid start/stop of drawing strokes due to gesture flicker might cause excessive history saves or other state issues.
2. Crashes after a few strokes suggest potential memory issues or errors in drawing/blending logic.

Fixes implemented:
- Modified main loop to require the DRAW gesture to be absent for several frames before ending a stroke, improving drawing consistency.
- Added clamping in canvas_engine._connect_points for interpolated coordinates.
- Added basic try-except around the main frame processing loop for better error reporting if crashes persist.
"""

import cv2
import time
import traceback # Added for error logging

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
        # self.last_draw_state = False # Replaced by draw_gesture_active
        self.mouse_point = None
        self.mouse_click = False
        self.last_action_time = time.time()
        self.action_cooldown = 0.3  # Cooldown in seconds

        # State for improved drawing consistency
        self.draw_gesture_active = False
        self.draw_gesture_lost_frames = 0
        self.max_lost_frames_threshold = 3 # Frames to wait before stopping draw

    def run(self):
        cv2.namedWindow("GestureArt")
        cv2.setMouseCallback("GestureArt", self.mouse_callback)

        while True:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    print("Camera Error: Failed to grab frame.")
                    time.sleep(0.5) # Wait a bit before retrying or breaking
                    continue # Or break, depending on desired behavior

                frame = cv2.flip(frame, 1)
                # frame_copy_for_hands = frame.copy() # No longer needed, draw directly on frame
                frame, hands_detected = self.tracker.find_hands(frame, draw=True) # Draw landmarks/connections on main frame

                gesture = GestureType.NONE
                state = GestureState.NONE
                conf = 0
                interaction_point = self.mouse_point # Default to mouse if no hand
                current_time = time.time()

                if hands_detected:
                    landmarks, found = self.tracker.find_positions(frame, draw=True) # Use main frame and draw landmarks
                    if found and landmarks and len(landmarks) > 8:
                        # Use index finger tip (landmark 8) for interaction
                        interaction_point = (landmarks[8][1], landmarks[8][2])
                        # Ensure interaction point is within bounds (safety check)
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
                            # Handle end of drawing stroke with delay
                            if self.draw_gesture_active:
                                self.draw_gesture_lost_frames += 1
                                if self.draw_gesture_lost_frames > self.max_lost_frames_threshold:
                                    self.canvas.draw(None, is_drawing=False) # End the stroke
                                    self.draw_gesture_active = False
                                    self.draw_gesture_lost_frames = 0

                            # Handle other gestures (CLEAR, SAVE) only when stroke is not active
                            if not self.draw_gesture_active and state == GestureState.COMPLETED and current_time - self.last_action_time > self.action_cooldown:
                                if gesture == GestureType.CLEAR:
                                    self.canvas.clear()
                                    self.last_action_time = current_time
                                elif gesture == GestureType.SAVE:
                                    self.canvas.save("output/drawing.png") # Ensure output dir exists
                                    self.last_action_time = current_time
                                # Removed UNDO, REDO, TOOL_CHANGE gesture handling
                    else:
                         # Hand detected but landmarks not found or insufficient
                         if self.draw_gesture_active:
                            self.draw_gesture_lost_frames += 1
                            if self.draw_gesture_lost_frames > self.max_lost_frames_threshold:
                                self.canvas.draw(None, is_drawing=False)
                                self.draw_gesture_active = False
                                self.draw_gesture_lost_frames = 0
                else:
                    # No hands detected, ensure drawing stops
                    if self.draw_gesture_active:
                        self.canvas.draw(None, is_drawing=False)
                        self.draw_gesture_active = False
                        self.draw_gesture_lost_frames = 0

                # Determine if UI interaction is happening (select gesture or mouse click)
                is_interacting_ui = (gesture == GestureType.SELECT and not self.draw_gesture_active) or self.mouse_click
                interaction = self.ui.handle_interaction(interaction_point, is_interacting_ui)

                if interaction:
                    action_type = interaction.get("type")
                    # Cooldown check for specific UI actions
                    if action_type in ["clear", "undo", "redo", "save"] and current_time - self.last_action_time <= self.action_cooldown:
                        pass # Skip action if in cooldown
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
                    elif action_type == "slider_changed": # Assuming this is for color sliders
                        current_color = self.ui.elements[UIElement.COLOR_PICKER]["current_color"]
                        self.canvas.set_color(current_color)
                    elif action_type == "brush_selected":
                        brush_name = interaction["name"]
                        if isinstance(brush_name, str):
                            try:
                                # Map UI's "Eraser" back to backend's "NEON"
                                if brush_name.upper() == "ERASER":
                                    brush_enum = BrushType.NEON
                                else:
                                    # Find the correct enum member by name
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
                                # Add other properties like hardness if needed
                            except Exception as e:
                                print(f"Error setting brush property: {prop} = {val} ({e})")

                self.mouse_click = False # Reset mouse click state

                # --- Rendering --- #
                canvas_img = self.canvas.get_transformed_canvas()

                # Ensure dimensions match before blending
                if frame.shape != canvas_img.shape:
                    print(f"Warning: Frame shape {frame.shape} and Canvas shape {canvas_img.shape} differ. Resizing canvas image.")
                    # Option 1: Resize canvas_img to frame shape (might distort drawing)
                    # canvas_img = cv2.resize(canvas_img, (frame.shape[1], frame.shape[0]))
                    # Option 2: Create a compatible background and overlay canvas (better)
                    compatible_canvas = np.full_like(frame, self.canvas.background_color)
                    h, w = canvas_img.shape[:2]
                    compatible_canvas[0:h, 0:w] = canvas_img
                    canvas_img = compatible_canvas

                # Blend camera feed and canvas
                composed = cv2.addWeighted(frame, 0.5, canvas_img, 0.5, 0)

                # Render UI elements on top
                gesture_name_to_display = gesture.name if gesture != GestureType.NONE else "NONE"
                gesture_info_str = f"{gesture_name_to_display} ({conf:.2f}) St: {state.name}"
                final_frame = self.ui.render(composed, gesture_info=gesture_info_str)

                # Update status bar
                brush_name_ui = self.canvas.brush_type.name
                if brush_name_ui == "NEON":
                    brush_name_ui = "ERASER" # Show NEON as ERASER in UI
                status_text = f"Brush: {brush_name_ui} | Size: {self.canvas.brush_size}"
                self.ui.set_status(status_text)

                # Display the final frame
                cv2.imshow("GestureArt", final_frame)


            except Exception as e:
                print("An error occurred in the main loop:")
                traceback.print_exc()
                # Optionally break or attempt recovery
                break # Exit on error for now

            # --- Event Handling --- #
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27: # Quit on 'q' or ESC
                break
            elif key == ord('c'): # Clear
                 if current_time - self.last_action_time > self.action_cooldown:
                    self.canvas.clear()
                    self.last_action_time = current_time
            elif key == ord('z'): # Undo
                 if current_time - self.last_action_time > self.action_cooldown:
                    if self.canvas.undo():
                        self.last_action_time = current_time
            elif key == ord('y'): # Redo
                 if current_time - self.last_action_time > self.action_cooldown:
                    if self.canvas.redo():
                        self.last_action_time = current_time
            elif key == ord('s'): # Save
                 if current_time - self.last_action_time > self.action_cooldown:
                    self.canvas.save("output/drawing.png")
                    self.last_action_time = current_time
            elif key == ord('h'): # Toggle Help
                 self.ui.elements[UIElement.HELP]["visible"] = not self.ui.elements[UIElement.HELP]["visible"]
                 # self.last_interaction_time = current_time # Keep UI visible - This variable is not defined here, use self.last_action_time or update interaction time in UI
                 self.ui.last_interaction_time = current_time # Correctly update UI's interaction time

        self.cap.release()
        cv2.destroyAllWindows()
        print("GestureArt Application Closed.")

    def mouse_callback(self, event, x, y, flags, param):
        # Clamp mouse coordinates to be safe
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        self.mouse_point = (x, y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_click = True
            # If mouse click interacts with UI, prevent drawing start
            interaction = self.ui.handle_interaction(self.mouse_point, True)
            if interaction:
                 self.draw_gesture_active = False # Prevent drawing if UI clicked
        elif event == cv2.EVENT_LBUTTONUP:
             self.mouse_click = False
             # Reset active state for sliders etc.
             self.ui.handle_interaction(self.mouse_point, False)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_click: # Dragging mouse
                # Check if interacting with a UI element (e.g., slider)
                interaction = self.ui.handle_interaction(self.mouse_point, True)
                if not interaction: # Not interacting with UI, so draw
                    self.canvas.draw(self.mouse_point, pressure=1.0, is_drawing=True)
                    self.draw_gesture_active = True # Treat mouse drag as drawing
                else:
                    # If dragging started on UI, stop potential drawing
                    if self.draw_gesture_active:
                        self.canvas.draw(None, is_drawing=False)
                        self.draw_gesture_active = False
            else: # Just moving mouse, not clicking
                 self.ui.handle_interaction(self.mouse_point, False) # Update hover states

if __name__ == '__main__':
    # Create output directory if it doesn't exist
    import os
    if not os.path.exists("output"):
        os.makedirs("output")

    try:
        app = GestureArtApp()
        app.run()
    except Exception as e:
        print("Failed to initialize or run the application:")
        traceback.print_exc()

