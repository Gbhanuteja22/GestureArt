import cv2
import numpy as np
import os
import time
from enum import Enum

class BrushType(Enum):
    STANDARD = 0
    # AIRBRUSH = 1 # Removed
    CALLIGRAPHY = 2
    MARKER = 3
    # WATERCOLOR = 5 # Removed
    NEON = 6 # Internally represents Eraser
    PIXEL = 7

class CanvasEngine:
    def __init__(self, width=1280, height=720, background_color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.canvas = np.ones((height, width, 3), dtype=np.uint8)
        self.canvas[:] = background_color
        self.alpha = np.ones((height, width), dtype=np.uint8) * 255
        self.color = (0, 0, 0)
        self.brush_type = BrushType.STANDARD
        self.brush_size = 15
        self.hardness = 0.5
        self.prev_point = None
        self.history = []
        self.history_index = -1 # Points to the current state in history
        self.max_history_size = 20
        self.layers = [np.ones((height, width, 3), dtype=np.uint8)] # Start with one layer
        self.layers[0][:] = background_color
        self.active_layer = 0 # Initialize active_layer BEFORE using it
        self._add_history_state(self.layers[self.active_layer].copy()) # Save initial state
        self.last_draw_time = 0
        self.draw_count = 0
        self.avg_draw_time = 0

    def draw(self, point, pressure=1.0, is_drawing=True):
        start_time = time.time()
        if point is None:
            # Save state only when the drawing stroke ends (is_drawing is False)
            if self.prev_point is not None and not is_drawing: # Check if there was a stroke
                 self._add_history_state(self.layers[self.active_layer].copy())
            self.prev_point = None
            return
        
        x, y = point
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        effective_size = int(self.brush_size * pressure)
        if effective_size < 1:
            effective_size = 1

        canvas = self.layers[self.active_layer]
        # Dynamically call the correct drawing method based on brush_type
        draw_method_name = f'_draw_{self.brush_type.name.lower()}'
        draw_method = getattr(self, draw_method_name, self._draw_standard_brush)
        draw_method(canvas, (x, y), effective_size)

        if self.prev_point is not None and is_drawing:
            self._connect_points(canvas, self.prev_point, (x, y), effective_size)

        if is_drawing:
            self.prev_point = (x, y)
            
        end_time = time.time()
        draw_time = end_time - start_time
        self.last_draw_time = draw_time
        self.draw_count += 1
        self.avg_draw_time = ((self.draw_count - 1) * self.avg_draw_time + draw_time) / self.draw_count

    def _draw_standard_brush(self, canvas, point, size):
        x, y = point
        color_scaled = self.color
        cv2.circle(canvas, (x, y), size, color_scaled, -1)

    def _draw_calligraphy(self, canvas, point, size):
        x, y = point
        angle = 45
        if self.prev_point:
            dx = x - self.prev_point[0]
            dy = y - self.prev_point[1]
            if dx != 0 or dy != 0:
                angle = np.degrees(np.arctan2(dy, dx))
        axes = (size, size // 3)
        eff_color = self.color
        cv2.ellipse(canvas, (x, y), axes, angle, 0, 360, eff_color, -1)

    def _draw_marker(self, canvas, point, size):
        x, y = point
        # Marker effect: slightly transparent overlay
        eff_alpha = 0.7 
        temp = np.zeros_like(canvas)
        cv2.circle(temp, (x, y), size, self.color, -1)
        y_min = max(0, y - size)
        y_max = min(self.height, y + size)
        x_min = max(0, x - size)
        x_max = min(self.width, x + size)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = cv2.addWeighted(region[mask], 1 - eff_alpha, temp_region[mask], eff_alpha, 0)

    def _draw_neon(self, canvas, point, size):
        """
        Renamed from Neon to Eraser functionality with optimized performance
        """
        x, y = point
        # Simple eraser - just draw with background color
        cv2.circle(canvas, (x, y), size, self.background_color, -1)

    def _draw_pixel(self, canvas, point, size):
        x, y = point
        pixel_size = max(1, size // 2) # Adjust pixel size calculation if needed
        x_grid = (x // pixel_size) * pixel_size
        y_grid = (y // pixel_size) * pixel_size
        eff_color = self.color
        cv2.rectangle(canvas, (x_grid, y_grid), (x_grid + pixel_size, y_grid + pixel_size), eff_color, -1)

    def _connect_points(self, canvas, p1, p2, size):
        x1, y1 = p1
        x2, y2 = p2
        dist = np.hypot(x2 - x1, y2 - y1)
        if dist < 1: # Connect only if points are sufficiently far apart
            return
        num_points = max(2, int(dist)) # Interpolate based on distance
        draw_method_name = f'_draw_{self.brush_type.name.lower()}'
        draw_method = getattr(self, draw_method_name, self._draw_standard_brush)
        for i in range(1, num_points + 1):
            t = i / num_points
            x = int((1 - t) * x1 + t * x2)
            y = int((1 - t) * y1 + t * y2)
            draw_method(canvas, (x, y), size)

    def set_color(self, color):
        self.color = color

    def set_brush(self, brush_type):
        if isinstance(brush_type, BrushType):
            self.brush_type = brush_type
        else:
            print(f"Warning: Invalid brush type {brush_type}")

    def set_brush_size(self, size):
        self.brush_size = max(1, int(size))

    def set_hardness(self, hardness):
        # Hardness might be used by some brushes, keep method signature
        self.hardness = max(0.0, min(1.0, hardness))

    def clear(self):
        # Check if canvas is already clear to avoid redundant history states
        if not np.all(self.layers[self.active_layer] == self.background_color):
            self.layers[self.active_layer][:] = self.background_color
            self._add_history_state(self.layers[self.active_layer].copy()) # Save cleared state

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.layers[self.active_layer] = self.history[self.history_index].copy()
            return True
        return False

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.layers[self.active_layer] = self.history[self.history_index].copy()
            return True
        return False

    def _add_history_state(self, state):
        # If we undo and then draw, clear the future redo states
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add the new state
        self.history.append(state)
        
        # Enforce history limit
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
            # Index remains pointing to the last element after pop(0)
            self.history_index = len(self.history) - 1
        else:
            # Only increment index if we didn't pop
            self.history_index += 1

    def save(self, filename):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            cv2.imwrite(filename, self.layers[self.active_layer])
            print(f"Canvas saved to {filename}")
            return True
        except Exception as e:
            print(f"Error saving canvas: {e}")
            return False

    def get_transformed_canvas(self):
        # Return a copy to prevent external modification
        return self.layers[self.active_layer].copy()

    def get_performance_metrics(self):
        return {
            "last_draw_time": self.last_draw_time * 1000,
            "avg_draw_time": self.avg_draw_time * 1000,
            "draw_count": self.draw_count
        }
