# GestureArt API Reference

This document provides detailed API reference for all modules in the GestureArt application.

## Table of Contents

1. [Hand Tracking Module](#hand-tracking-module)
2. [Gesture Recognition Module](#gesture-recognition-module)
3. [Canvas Engine Module](#canvas-engine-module)
4. [UI Module](#ui-module)
5. [AI Features Module](#ai-features-module)
6. [Main Application](#main-application)

## Hand Tracking Module

The `HandTracker` class provides hand detection and tracking functionality using MediaPipe.

### Class: `HandTracker`

```python
class HandTracker:
    def __init__(self, static_mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5)
```

#### Parameters:

- `static_mode` (bool): If True, detection runs on every frame; if False, detection runs once and then tracking is used.
- `max_hands` (int): Maximum number of hands to detect.
- `detection_confidence` (float): Minimum confidence value for hand detection to be considered successful.
- `tracking_confidence` (float): Minimum confidence value for the hand landmarks to be considered tracked successfully.

#### Methods:

```python
def find_hands(self, img, draw=True)
```
Detects hands in an image.

**Parameters:**
- `img` (numpy.ndarray): Input image.
- `draw` (bool): Whether to draw landmarks on the image.

**Returns:**
- `img` (numpy.ndarray): Image with hand landmarks drawn (if draw=True).
- `hands_detected` (bool): Whether hands were detected.

```python
def find_positions(self, img, hand_no=0, draw=True)
```
Gets positions of all landmarks for a specific hand.

**Parameters:**
- `img` (numpy.ndarray): Input image.
- `hand_no` (int): Hand index (0 for first hand).
- `draw` (bool): Whether to draw landmarks on the image.

**Returns:**
- `landmarks` (list): List of landmark positions [id, x, y, z].
- `hand_detected` (bool): Whether the specified hand was detected.

```python
def fingers_up(self, landmarks)
```
Determines which fingers are up.

**Parameters:**
- `landmarks` (list): List of landmark positions.

**Returns:**
- `fingers` (list): List of 5 booleans indicating which fingers are up [thumb, index, middle, ring, pinky].

## Gesture Recognition Module

The `GestureRecognizer` class interprets hand landmarks into meaningful gestures.

### Enum: `GestureType`

```python
class GestureType(Enum):
    NONE = 0
    DRAW = 1
    SELECT = 2
    CLEAR = 3
    UNDO = 4
    SAVE = 5
    COLOR_PICK = 6
    TOOL_CHANGE = 7
```

### Enum: `GestureState`

```python
class GestureState(Enum):
    NONE = 0
    STARTED = 1
    ONGOING = 2
    COMPLETED = 3
```

### Class: `GestureRecognizer`

```python
class GestureRecognizer:
    def __init__(self, detection_threshold=0.8, cooldown_time=0.5)
```

#### Parameters:

- `detection_threshold` (float): Confidence threshold for gesture detection.
- `cooldown_time` (float): Time in seconds before the same gesture can be triggered again.

#### Methods:

```python
def recognize_gesture(self, landmarks, fingers_up)
```
Recognizes gestures based on hand landmarks and finger states.

**Parameters:**
- `landmarks` (list): List of landmark positions.
- `fingers_up` (list): List of 5 booleans indicating which fingers are up.

**Returns:**
- `gesture` (GestureType): Recognized gesture.
- `confidence` (float): Confidence score for the recognized gesture.
- `state` (GestureState): State of the gesture (NONE, STARTED, ONGOING, COMPLETED).

```python
def reset(self)
```
Resets the gesture recognizer state.

```python
def get_gesture_info(self)
```
Gets information about the current gesture.

**Returns:**
- `info` (dict): Dictionary containing gesture information.

## Canvas Engine Module

The `CanvasEngine` class manages drawing operations and canvas state.

### Enum: `BrushType`

```python
class BrushType(Enum):
    STANDARD = 0
    AIRBRUSH = 1
    CALLIGRAPHY = 2
    MARKER = 3
    PENCIL = 4
    WATERCOLOR = 5
    NEON = 6
    PIXEL = 7
```

### Class: `CanvasEngine`

```python
class CanvasEngine:
    def __init__(self, width=1280, height=720, background_color=(255, 255, 255))
```

#### Parameters:

- `width` (int): Width of the canvas.
- `height` (int): Height of the canvas.
- `background_color` (tuple): RGB background color.

#### Methods:

```python
def draw(self, point, pressure=1.0, is_drawing=True)
```
Draws on the canvas at the specified point.

**Parameters:**
- `point` (tuple or None): (x, y) coordinates to draw at, or None to stop drawing.
- `pressure` (float): Drawing pressure (0.0 to 1.0).
- `is_drawing` (bool): Whether drawing is active.

```python
def set_color(self, color)
```
Sets the current drawing color.

**Parameters:**
- `color` (tuple): RGB color.

```python
def set_brush(self, brush_type)
```
Sets the current brush type.

**Parameters:**
- `brush_type` (BrushType): Brush type to use.

```python
def set_brush_size(self, size)
```
Sets the current brush size.

**Parameters:**
- `size` (int): Brush size in pixels.

```python
def clear(self)
```
Clears the canvas.

```python
def undo(self)
```
Undoes the last drawing action.

```python
def redo(self)
```
Redoes the last undone action.

```python
def save(self, filename)
```
Saves the canvas to a file.

**Parameters:**
- `filename` (str): Path to save the file.

**Returns:**
- `success` (bool): Whether the save was successful.

```python
def get_transformed_canvas(self)
```
Gets the canvas with any transformations applied.

**Returns:**
- `canvas` (numpy.ndarray): Transformed canvas.

## UI Module

The `UIManager` class handles user interface elements and interactions.

### Enum: `UIElement`

```python
class UIElement(Enum):
    HEADER = 0
    COLOR_PICKER = 1
    BRUSH_SELECTOR = 2
    HELP = 3
    SETTINGS = 4
```

### Class: `UIManager`

```python
class UIManager:
    def __init__(self, width=1280, height=720)
```

#### Parameters:

- `width` (int): Width of the UI area.
- `height` (int): Height of the UI area.

#### Methods:

```python
def render(self, frame, landmarks=None, gesture_info=None)
```
Renders UI elements on the frame.

**Parameters:**
- `frame` (numpy.ndarray): Input frame to render UI on.
- `landmarks` (list, optional): Hand landmarks for interaction.
- `gesture_info` (dict, optional): Information about current gesture.

**Returns:**
- `frame` (numpy.ndarray): Frame with UI elements rendered.

```python
def handle_interaction(self, point, is_selecting=False)
```
Handles user interaction with UI elements.

**Parameters:**
- `point` (tuple or None): (x, y) coordinates of interaction point.
- `is_selecting` (bool): Whether the user is selecting (clicking) or just hovering.

**Returns:**
- `interaction` (dict): Information about the interaction result.

```python
def toggle_help(self)
```
Toggles the help overlay visibility.

**Returns:**
- `visible` (bool): Whether the help overlay is now visible.

## AI Features Module

The `AIFeatures` class provides AI-powered capabilities for GestureArt.

### Enum: `StyleTransferModel`

```python
class StyleTransferModel(Enum):
    VAN_GOGH = "van_gogh"
    PICASSO = "picasso"
    MONET = "monet"
    KANDINSKY = "kandinsky"
    SKETCH = "sketch"
    WATERCOLOR = "watercolor"
```

### Class: `AIFeatures`

```python
class AIFeatures:
    def __init__(self, models_dir=None)
```

#### Parameters:

- `models_dir` (str, optional): Directory to store/load AI models.

#### Methods:

```python
def initialize_tf(self)
```
Initializes TensorFlow and loads models.

**Returns:**
- `success` (bool): Whether initialization was successful.

```python
def apply_style_transfer(self, content_image, style_model, strength=1.0)
```
Applies style transfer to the content image.

**Parameters:**
- `content_image` (numpy.ndarray): Content image to stylize (RGB).
- `style_model` (StyleTransferModel): Style to apply.
- `strength` (float): Strength of the style transfer effect (0.0 to 1.0).

**Returns:**
- `stylized_image` (numpy.ndarray): Stylized image or None if failed.

```python
def suggest_colors(self, current_color, canvas=None)
```
Suggests colors based on current color and usage history.

**Parameters:**
- `current_color` (tuple): Current RGB color.
- `canvas` (numpy.ndarray, optional): Current canvas for context-aware suggestions.

**Returns:**
- `suggestions` (list): List of suggested RGB colors.

```python
def initialize_virtual_keyboard(self)
```
Initializes the virtual keyboard for text input.

**Returns:**
- `success` (bool): Whether initialization was successful.

```python
def render_virtual_keyboard(self, frame)
```
Renders the virtual keyboard on the frame.

**Parameters:**
- `frame` (numpy.ndarray): Input frame to render keyboard on.

**Returns:**
- `frame` (numpy.ndarray): Frame with keyboard rendered.
- `keyboard_state` (dict): Keyboard state information.

```python
def handle_keyboard_interaction(self, point, is_selecting=False)
```
Handles user interaction with the virtual keyboard.

**Parameters:**
- `point` (tuple): (x, y) coordinates of the interaction.
- `is_selecting` (bool): Whether the user is selecting (clicking) or just hovering.

**Returns:**
- `interaction` (dict): Information about the interaction result.

```python
def toggle_virtual_keyboard(self)
```
Toggles virtual keyboard visibility.

**Returns:**
- `visible` (bool): Whether the virtual keyboard is now visible.

```python
def get_performance_metrics(self)
```
Gets performance metrics for the AI features.

**Returns:**
- `metrics` (dict): Dictionary containing performance metrics.

## Main Application

The `GestureArt` class coordinates all modules and manages application flow.

### Enum: `AppMode`

```python
class AppMode(Enum):
    DRAWING = 0
    COLOR_PICKING = 1
    BRUSH_SELECTING = 2
    TEXT_INPUT = 3
    STYLE_TRANSFER = 4
    SETTINGS = 5
```

### Class: `GestureArt`

```python
class GestureArt:
    def __init__(self, width=1280, height=720, camera_id=0)
```

#### Parameters:

- `width` (int): Width of the application window.
- `height` (int): Height of the application window.
- `camera_id` (int): Camera device ID to use.

#### Methods:

```python
def run(self)
```
Runs the main application loop.

```python
def _process_frame(self, frame)
```
Processes a single frame from the webcam.

**Parameters:**
- `frame` (numpy.ndarray): Input frame from webcam.

**Returns:**
- `processed_frame` (numpy.ndarray): Processed frame with UI elements.

```python
def _handle_drawing_mode(self, gesture, state, landmarks, fingers_up)
```
Handles gestures in drawing mode.

**Parameters:**
- `gesture` (GestureType): Recognized gesture.
- `state` (GestureState): Gesture state.
- `landmarks` (list): Hand landmarks.
- `fingers_up` (list): List indicating which fingers are up.

```python
def _handle_color_picking_mode(self, gesture, state, landmarks, fingers_up)
```
Handles gestures in color picking mode.

**Parameters:**
- `gesture` (GestureType): Recognized gesture.
- `state` (GestureState): Gesture state.
- `landmarks` (list): Hand landmarks.
- `fingers_up` (list): List indicating which fingers are up.

```python
def _handle_brush_selecting_mode(self, gesture, state, landmarks, fingers_up)
```
Handles gestures in brush selecting mode.

**Parameters:**
- `gesture` (GestureType): Recognized gesture.
- `state` (GestureState): Gesture state.
- `landmarks` (list): Hand landmarks.
- `fingers_up` (list): List indicating which fingers are up.

```python
def _handle_text_input_mode(self, gesture, state, landmarks, fingers_up)
```
Handles gestures in text input mode.

**Parameters:**
- `gesture` (GestureType): Recognized gesture.
- `state` (GestureState): Gesture state.
- `landmarks` (list): Hand landmarks.
- `fingers_up` (list): List indicating which fingers are up.

```python
def _handle_style_transfer_mode(self, gesture, state, landmarks, fingers_up)
```
Handles gestures in style transfer mode.

**Parameters:**
- `gesture` (GestureType): Recognized gesture.
- `state` (GestureState): Gesture state.
- `landmarks` (list): Hand landmarks.
- `fingers_up` (list): List indicating which fingers are up.

```python
def _apply_style_transfer(self, style_model)
```
Applies style transfer to the canvas in a background thread.

**Parameters:**
- `style_model` (StyleTransferModel): Style to apply.

```python
def _save_canvas(self)
```
Saves the canvas to a file.

```python
def _auto_save_canvas(self)
```
Auto-saves the canvas to a file.

```python
def _cleanup(self)
```
Cleans up resources before exiting.

### Function: `parse_arguments`

```python
def parse_arguments()
```
Parses command line arguments.

**Returns:**
- `args` (argparse.Namespace): Parsed arguments.
