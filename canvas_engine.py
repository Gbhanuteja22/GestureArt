import cv2
import numpy as np
import os
import time
from enum import Enum

class BrushType(Enum):
    STANDARD = 0
    AIRBRUSH = 1
    CALLIGRAPHY = 2
    MARKER = 3
    PENCIL = 4
    WATERCOLOR = 5
    NEON = 6
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
        self.opacity = 1.0
        self.flow = 1.0
        self.hardness = 0.5
        self.prev_point = None
        self.history = []
        self.redo_stack = []
        self.max_history_size = 20
        self.layers = [self.canvas.copy()]
        self.active_layer = 0
        self._save_state()
        self.last_draw_time = 0
        self.draw_count = 0
        self.avg_draw_time = 0

    def draw(self, point, pressure=1.0, is_drawing=True):
        start_time = time.time()
        if point is None:
            self.prev_point = None
            return
        x, y = point
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        effective_size = int(self.brush_size * pressure)
        if effective_size < 1:
            effective_size = 1

        canvas = self.layers[self.active_layer]
        if self.brush_type == BrushType.STANDARD:
            self._draw_standard_brush(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.AIRBRUSH:
            self._draw_airbrush(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.CALLIGRAPHY:
            self._draw_calligraphy(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.MARKER:
            self._draw_marker(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.PENCIL:
            self._draw_pencil(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.WATERCOLOR:
            self._draw_watercolor(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.NEON:
            self._draw_neon(canvas, (x, y), effective_size)
        elif self.brush_type == BrushType.PIXEL:
            self._draw_pixel(canvas, (x, y), effective_size)
        else:
            self._draw_standard_brush(canvas, (x, y), effective_size)

        if self.prev_point is not None and is_drawing:
            self._connect_points(canvas, self.prev_point, (x, y), effective_size)

        if is_drawing:
            self.prev_point = (x, y)
        else:
            self.prev_point = None
            self._save_state()
        end_time = time.time()
        draw_time = end_time - start_time
        self.last_draw_time = draw_time
        self.draw_count += 1
        self.avg_draw_time = ((self.draw_count - 1) * self.avg_draw_time + draw_time) / self.draw_count

    def _draw_standard_brush(self, canvas, point, size):
        x, y = point
        eff = self.opacity * self.flow
        color_scaled = tuple(min(255, int(c * eff)) for c in self.color)
        cv2.circle(canvas, (x, y), size, color_scaled, -1)

    def _draw_airbrush(self, canvas, point, size):
        x, y = point
        eff_alpha = self.opacity * self.flow
        temp = np.zeros_like(canvas)
        for i in range(3):
            radius = int(size * (i + 1) / 2)
            factor = (3 - i) / 3.0
            color_scaled = tuple(min(255, int(c * self.opacity * factor)) for c in self.color)
            cv2.circle(temp, (x, y), radius, color_scaled, -1)
        y_min = max(0, y - size*2)
        y_max = min(self.height, y + size*2)
        x_min = max(0, x - size*2)
        x_max = min(self.width, x + size*2)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            blended = cv2.addWeighted(region, 1 - eff_alpha, temp_region, eff_alpha, 0)
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = blended[mask]

    def _draw_calligraphy(self, canvas, point, size):
        x, y = point
        angle = 45
        if self.prev_point:
            dx = x - self.prev_point[0]
            dy = y - self.prev_point[1]
            if dx != 0 or dy != 0:
                angle = np.degrees(np.arctan2(dy, dx))
        axes = (size, size // 3)
        eff_color = tuple(min(255, int(c * self.opacity * self.flow)) for c in self.color)
        cv2.ellipse(canvas, (x, y), axes, angle, 0, 360, eff_color, -1)

    def _draw_marker(self, canvas, point, size):
        x, y = point
        eff_alpha = self.opacity * self.flow * 0.7
        temp = np.zeros_like(canvas)
        cv2.circle(temp, (x, y), size, self.color, -1)
        y_min = max(0, y - size)
        y_max = min(self.height, y + size)
        x_min = max(0, x - size)
        x_max = min(self.width, x + size)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            blended = cv2.addWeighted(region, 1 - eff_alpha, temp_region, eff_alpha, 0)
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = blended[mask]

    def _draw_pencil(self, canvas, point, size):
        x, y = point
        eff_alpha = self.opacity * self.flow
        temp = np.zeros_like(canvas)
        cv2.circle(temp, (x, y), size, self.color, -1)
        max_noise = int(50 * (1 - self.hardness))
        if max_noise > 0:
            noise = np.random.randint(0, max_noise, temp.shape, dtype=np.uint8)
            temp = cv2.subtract(temp, noise)
        y_min = max(0, y - size)
        y_max = min(self.height, y + size)
        x_min = max(0, x - size)
        x_max = min(self.width, x + size)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            blended = cv2.addWeighted(region, 1 - eff_alpha, temp_region, eff_alpha, 0)
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = blended[mask]

    def _draw_watercolor(self, canvas, point, size):
        x, y = point
        temp = np.zeros_like(canvas)
        for i in range(5):
            radius = int(size * (0.5 + np.random.random()))
            color_var = [int(max(0, min(255, c * (0.9 + np.random.random() * 0.2)))) for c in self.color]
            cv2.circle(temp, (x, y), radius, tuple(color_var), -1)
        k = int((1 - self.hardness) * 20)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        temp = cv2.GaussianBlur(temp, (k, k), 0)
        eff_alpha = self.opacity * self.flow * 0.7
        y_min = max(0, y - size*3)
        y_max = min(self.height, y + size*3)
        x_min = max(0, x - size*3)
        x_max = min(self.width, x + size*3)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            blended = cv2.addWeighted(region, 1 - eff_alpha, temp_region, eff_alpha, 0)
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = blended[mask]

    def _draw_neon(self, canvas, point, size):
        x, y = point
        temp = np.zeros_like(canvas)
        for i in range(3):
            radius = int(size * (3 - i) / 3)
            brightness = min(255, 50 * (i + 1))
            glow_color = tuple(min(255, c + brightness) for c in self.color)
            cv2.circle(temp, (x, y), radius, glow_color, -1)
        k = int((1 - self.hardness) * 20)
        if k % 2 == 0:
            k += 1
        if k < 1:
            k = 1
        temp = cv2.GaussianBlur(temp, (k, k), 0)
        eff_alpha = self.opacity * self.flow
        y_min = max(0, y - size*3)
        y_max = min(self.height, y + size*3)
        x_min = max(0, x - size*3)
        x_max = min(self.width, x + size*3)
        if y_min < y_max and x_min < x_max:
            region = canvas[y_min:y_max, x_min:x_max]
            temp_region = temp[y_min:y_max, x_min:x_max]
            blended = cv2.addWeighted(region, 1 - eff_alpha, temp_region, eff_alpha, 0)
            mask = np.any(temp_region != 0, axis=2)
            region[mask] = blended[mask]

    def _draw_pixel(self, canvas, point, size):
        x, y = point
        pixel_size = max(1, size // 3)
        x_grid = (x // pixel_size) * pixel_size
        y_grid = (y // pixel_size) * pixel_size
        eff_color = tuple(min(255, int(c * self.opacity * self.flow)) for c in self.color)
        cv2.rectangle(canvas, (x_grid, y_grid), (x_grid + pixel_size, y_grid + pixel_size), eff_color, -1)

    def _connect_points(self, canvas, p1, p2, size):
        x1, y1 = p1
        x2, y2 = p2
        dist = np.hypot(x2 - x1, y2 - y1)
        if dist < 2:
            return
        num_points = max(2, int(dist / 2))
        for i in range(1, num_points):
            t = i / num_points
            x = int((1 - t) * x1 + t * x2)
            y = int((1 - t) * y1 + t * y2)
            if self.brush_type == BrushType.STANDARD:
                self._draw_standard_brush(canvas, (x, y), size)
            elif self.brush_type == BrushType.AIRBRUSH:
                self._draw_airbrush(canvas, (x, y), size)
            elif self.brush_type == BrushType.CALLIGRAPHY:
                self._draw_calligraphy(canvas, (x, y), size)
            elif self.brush_type == BrushType.MARKER:
                self._draw_marker(canvas, (x, y), size)
            elif self.brush_type == BrushType.PENCIL:
                self._draw_pencil(canvas, (x, y), size)
            elif self.brush_type == BrushType.WATERCOLOR:
                self._draw_watercolor(canvas, (x, y), size)
            elif self.brush_type == BrushType.NEON:
                self._draw_neon(canvas, (x, y), size)
            elif self.brush_type == BrushType.PIXEL:
                self._draw_pixel(canvas, (x, y), size)
            else:
                self._draw_standard_brush(canvas, (x, y), size)

    def set_color(self, color):
        self.color = color

    def set_brush(self, brush_type):
        self.brush_type = brush_type

    def set_brush_size(self, size):
        self.brush_size = max(1, size)

    def set_opacity(self, opacity):
        self.opacity = max(0.0, min(1.0, opacity))

    def set_flow(self, flow):
        self.flow = max(0.0, min(1.0, flow))

    def set_hardness(self, hardness):
        self.hardness = max(0.0, min(1.0, hardness))

    def clear(self):
        self.layers[self.active_layer][:] = self.background_color
        self._save_state()

    def undo(self):
        if len(self.history) > 1:
            self.redo_stack.append(self.layers[self.active_layer].copy())
            self.history.pop()
            self.layers[self.active_layer] = self.history[-1].copy()
            if len(self.redo_stack) > self.max_history_size:
                self.redo_stack.pop(0)
            return True
        return False

    def redo(self):
        if self.redo_stack:
            state = self.redo_stack.pop()
            self.history.append(self.layers[self.active_layer].copy())
            if len(self.history) > self.max_history_size:
                self.history.pop(0)
            self.layers[self.active_layer] = state
            return True
        return False

    def _save_state(self):
        self.history.append(self.layers[self.active_layer].copy())
        if len(self.history) > self.max_history_size:
            self.history.pop(0)
        self.redo_stack = []

    def save(self, filename):
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            cv2.imwrite(filename, self.layers[self.active_layer])
            return True
        except Exception as e:
            print(f"Error saving canvas: {e}")
            return False

    def get_transformed_canvas(self):
        return self.layers[self.active_layer].copy()

    def get_performance_metrics(self):
        return {
            "last_draw_time": self.last_draw_time * 1000,
            "avg_draw_time": self.avg_draw_time * 1000,
            "draw_count": self.draw_count
        }

if __name__ == "__main__":
    canvas_engine = CanvasEngine(800, 600)
    canvas = canvas_engine.get_transformed_canvas()
    cv2.namedWindow("Canvas Test", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Canvas Test", 800, 600)
    drawing = False
