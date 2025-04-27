# GestureArt: AI-Powered Virtual Drawing Application

GestureArt is a production-ready Python-based AI-powered virtual drawing application that allows users to draw in the air using finger gestures. The application uses a webcam to track hand movements and translates them into digital art on screen.


## Features

- **Intuitive Hand Tracking**: Precise hand and finger tracking using MediaPipe
- **Advanced Gesture Recognition**: Intelligent recognition of multiple drawing and control gestures
- **Dynamic Brush Tools**: Various brush styles, sizes, and effects
- **AI-Powered Features**:
  - Style transfer for applying artistic styles to drawings
  - Smart color suggestions based on current palette
  - Gesture-based text insertion with virtual keyboard
- **Responsive UI**: Floating header with intuitive controls
- **Performance Optimized**: Asynchronous processing and GPU acceleration
- **Comprehensive Canvas Features**:
  - Transparent background support
  - Multiple save options
  - Undo/redo functionality
  - Layer management

## System Requirements

- Python 3.8 or higher
- Webcam
- 4GB RAM minimum (8GB recommended)
- GPU support recommended for optimal performance
- Operating System: Windows 10/11, macOS, or Linux

## Installation

### Option 1: Using pip

```bash
# Create a virtual environment
python -m venv gestureart-env
source gestureart-env/bin/activate  # On Windows: gestureart-env\Scripts\activate

# Install GestureArt
pip install gestureart

# Launch the application
gestureart
```

### Option 2: From Source

```bash
# Clone the repository
git clone https://github.com/yourusername/GestureArt.git
cd GestureArt

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch the application
python src/main.py
```

## Dependencies

- OpenCV: Computer vision and image processing
- MediaPipe: Hand tracking and landmark detection
- NumPy: Numerical operations
- TensorFlow: AI features including style transfer
- Matplotlib: Visualization for testing and reports

## Quick Start Guide

1. Launch GestureArt using the installation instructions above
2. Position your hand in front of the webcam
3. Use the following gestures to draw and control the application:
   - **Draw**: Index finger up, others down
   - **Select**: Index and middle fingers up
   - **Clear Canvas**: All fingers up
   - **Color Picker**: Index and pinky up
   - **Brush Selector**: Ring and pinky up
   - **Save**: Thumb, index, and pinky up
4. Experiment with different brushes, colors, and AI features

## Gesture Controls

| Gesture | Description | Action |
|---------|-------------|--------|
| ![Draw] Index finger up, others down | Draw on canvas |
| ![Select] Index and middle fingers up | Select UI elements |
| ![Clear] All fingers up | Clear canvas |
| ![Undo] Thumb and index form a "C" shape | Undo last action |
| ![Color Pick] Index and pinky up | Open color picker |
| ![Tool Change] Ring and pinky up | Open brush selector |
| ![Save] Thumb, index, and pinky up | Save canvas |

## Keyboard Controls

| Key | Action |
|-----|--------|
| ESC | Exit application |
| F | Toggle fullscreen |
| D | Toggle debug information |
| S | Save canvas |
| C | Clear canvas |
| Z | Undo |
| Y | Redo |
| H | Toggle help |
| T | Toggle virtual keyboard |

## Architecture

GestureArt is built with a modular architecture that separates concerns and allows for easy extension:

1. **Hand Tracking Module**: Detects and tracks hand landmarks using MediaPipe
2. **Gesture Recognition Module**: Interprets hand positions into meaningful gestures
3. **Canvas Engine**: Manages drawing operations and canvas state
4. **UI Module**: Handles user interface elements and interactions
5. **AI Features Module**: Provides AI-powered capabilities like style transfer and color suggestions
6. **Main Application**: Coordinates all modules and manages application flow

## Advanced Usage

### Command Line Arguments

```bash
python src/main.py --width 1280 --height 720 --camera 0 --fullscreen --debug
```

| Argument | Description | Default |
|----------|-------------|---------|
| --width | Width of the application window | 1280 |
| --height | Height of the application window | 720 |
| --camera | Camera device ID to use | 0 |
| --fullscreen | Start in fullscreen mode | False |
| --debug | Show debug information | False |

### Configuration

You can customize GestureArt by modifying the settings in the main application:

```python
# Settings
self.settings = {
    "hand_detection_confidence": 0.7,
    "hand_tracking_confidence": 0.5,
    "gesture_detection_threshold": 0.8,
    "max_hands": 1,
    "canvas_background_color": (255, 255, 255),
    "auto_save": True,
    "auto_save_interval": 300,  # seconds
    "auto_save_dir": os.path.join(os.path.dirname(os.path.abspath(__file__)), "../output"),
    "use_gpu": True
}
```

## Testing and Performance

GestureArt includes a comprehensive testing module that evaluates:

- Hand tracking accuracy
- Gesture recognition reliability
- Canvas engine performance
- UI responsiveness
- AI features performance
- End-to-end application performance

Run the tests to generate detailed performance reports:

```bash
python src/test_and_optimize.py
```

## Contributing

Contributions to GestureArt are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The MediaPipe team for their excellent hand tracking solution
- TensorFlow team for the style transfer models
- OpenCV community for computer vision tools
- All contributors and testers who helped improve GestureArt

## Contact

For questions, feedback, or support, please open an issue on the GitHub repository or contact the maintainers directly.

---

© 2025 GestureArt Team
