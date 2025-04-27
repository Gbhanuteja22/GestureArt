# GestureArt User Manual

## Introduction

Welcome to GestureArt, an AI-powered virtual drawing application that allows you to create digital art using hand gestures in the air. This user manual will guide you through the installation, setup, and usage of GestureArt.

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Interface Overview](#interface-overview)
4. [Gesture Controls](#gesture-controls)
5. [Keyboard Shortcuts](#keyboard-shortcuts)
6. [Drawing Tools](#drawing-tools)
7. [Color Selection](#color-selection)
8. [AI Features](#ai-features)
9. [Saving and Exporting](#saving-and-exporting)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#faq)

## Installation

### System Requirements

- Python 3.8 or higher
- Webcam
- 4GB RAM minimum (8GB recommended)
- GPU support recommended for optimal performance
- Operating System: Windows 10/11, macOS, or Linux

### Installation Steps

#### Option 1: Using pip

1. Open a terminal or command prompt
2. Create a virtual environment (recommended):
   ```bash
   python -m venv gestureart-env
   source gestureart-env/bin/activate  # On Windows: gestureart-env\Scripts\activate
   ```
3. Install GestureArt:
   ```bash
   pip install gestureart
   ```
4. Launch the application:
   ```bash
   gestureart
   ```

#### Option 2: From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/GestureArt.git
   cd GestureArt
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the application:
   ```bash
   python src/main.py
   ```

## Getting Started

1. After launching GestureArt, you'll see the main application window with your webcam feed.
2. Position yourself in front of the webcam, ensuring good lighting conditions.
3. Hold your hand up with your palm facing the camera at a distance of approximately 30-60 cm (1-2 feet).
4. The application will detect your hand and display landmarks on your fingers.
5. Try the basic drawing gesture: extend your index finger while keeping other fingers closed.
6. Move your index finger in the air to draw on the canvas.

## Interface Overview

The GestureArt interface consists of the following elements:

1. **Main Canvas**: The central area where your drawings appear.
2. **Webcam Feed**: Your camera feed with hand tracking overlay.
3. **Floating Header**: Contains buttons for various tools and options.
4. **Status Bar**: Displays current tool, color, and application status.
5. **Gesture Indicator**: Shows the currently recognized gesture.

## Gesture Controls

GestureArt uses a set of intuitive hand gestures for drawing and controlling the application:

### Basic Gestures

| Gesture | Hand Position | Action |
|---------|--------------|--------|
| Draw | Index finger up, others down | Draw on the canvas |
| Select | Index and middle fingers up | Select UI elements or tools |
| Clear Canvas | All fingers up | Clear the entire canvas |
| Undo | Thumb and index form a "C" shape | Undo the last action |
| Redo | Reverse "C" shape with thumb and index | Redo the last undone action |
| Color Picker | Index and pinky up | Open the color selection panel |
| Brush Selector | Ring and pinky up | Open the brush selection panel |
| Save | Thumb, index, and pinky up | Save the current canvas |

### Tips for Better Gesture Recognition

- Ensure good lighting conditions
- Keep your hand within the camera frame
- Make clear, distinct gestures
- Hold gestures steady for a moment for better recognition
- Practice the gestures to improve recognition accuracy

## Keyboard Shortcuts

GestureArt also supports keyboard shortcuts for quick access to common functions:

| Key | Action |
|-----|--------|
| ESC | Exit application |
| F | Toggle fullscreen mode |
| D | Toggle debug information display |
| S | Save canvas |
| C | Clear canvas |
| Z | Undo last action |
| Y | Redo last undone action |
| H | Toggle help overlay |
| T | Toggle virtual keyboard for text input |

## Drawing Tools

GestureArt offers various drawing tools and brushes:

### Brush Types

1. **Standard Brush**: Basic round brush with solid edges
2. **Airbrush**: Soft-edged brush with opacity falloff
3. **Calligraphy**: Angle-sensitive brush for varied stroke width
4. **Marker**: Solid brush with slight transparency
5. **Pencil**: Textured brush simulating pencil strokes
6. **Watercolor**: Brush with color blending and spread effects
7. **Neon**: Glowing brush with bright center and soft edges
8. **Pixel**: Creates pixelated strokes

### Brush Settings

- **Size**: Adjust brush size using the slider in the brush panel
- **Opacity**: Control brush transparency
- **Flow**: Adjust how much color is applied with each stroke
- **Hardness**: Control the edge softness of the brush

## Color Selection

GestureArt provides multiple ways to select colors:

### Color Picker

1. Use the "Color Picker" gesture (index and pinky up) to open the color panel
2. Select a color from the color wheel or palette
3. Use the brightness/saturation sliders to fine-tune your color

### AI Color Suggestions

GestureArt uses AI to suggest complementary colors based on your current selection:

1. Select a color from the color picker
2. View AI-suggested complementary colors in the suggestion panel
3. Click on a suggested color to select it

## AI Features

GestureArt includes several AI-powered features:

### Style Transfer

Apply artistic styles to your drawings:

1. Complete your drawing
2. Open the AI panel using the menu button
3. Select a style (Van Gogh, Picasso, Monet, etc.)
4. Adjust the style strength using the slider
5. Click "Apply" to transform your drawing

### Virtual Keyboard and Text Input

Add text to your drawings using gesture-controlled virtual keyboard:

1. Press 'T' or use the text tool button to open the virtual keyboard
2. Use the "Select" gesture (index and middle fingers up) to type
3. Position your hand where you want the text to appear
4. Type your text using the virtual keyboard
5. Press Enter to add the text to your drawing

### Smart Color Suggestions

Get AI-powered color suggestions based on your drawing:

1. Select the color picker tool
2. View the "Suggested Colors" panel
3. These colors are generated based on your current drawing and color scheme
4. Select any suggested color to use it

## Saving and Exporting

GestureArt offers several options for saving and exporting your artwork:

### Quick Save

1. Use the "Save" gesture (thumb, index, and pinky up)
2. Your drawing will be saved to the default output directory

### Save Options

1. Press 'S' or click the Save button in the menu
2. Choose from the following options:
   - PNG: Save with transparent background
   - JPG: Save with white background
   - SVG: Save as vector graphic (for certain brush types)
   - PSD: Save with layers (if using layer feature)

### Auto-Save

GestureArt automatically saves your work:

1. Auto-save is enabled by default (every 5 minutes)
2. Auto-saved files are stored in the output directory
3. You can adjust auto-save settings in the preferences

## Troubleshooting

### Hand Detection Issues

- **Problem**: Hand not being detected
- **Solution**: 
  - Ensure adequate lighting
  - Position your hand 30-60 cm from the camera
  - Keep your hand within the camera frame
  - Try adjusting the hand detection confidence in settings

### Performance Issues

- **Problem**: Application running slowly
- **Solution**:
  - Close other resource-intensive applications
  - Reduce the application window size
  - Enable GPU acceleration if available
  - Lower the camera resolution in settings

### Gesture Recognition Problems

- **Problem**: Gestures not being recognized correctly
- **Solution**:
  - Make more distinct gestures
  - Hold gestures steady for a moment
  - Recalibrate hand tracking in settings
  - Practice the gestures to improve recognition

### Camera Issues

- **Problem**: Camera not working or not detected
- **Solution**:
  - Ensure camera is connected and working
  - Check if other applications are using the camera
  - Try specifying a different camera ID when launching the application
  - Restart the application after connecting the camera

## FAQ

**Q: Can I use GestureArt without a webcam?**
A: No, GestureArt requires a webcam for hand tracking and gesture recognition.

**Q: Does GestureArt work with any webcam?**
A: Yes, GestureArt works with most standard webcams. Higher resolution cameras may provide better tracking accuracy.

**Q: Can I customize the gestures?**
A: The current version does not support custom gestures, but this feature is planned for future updates.

**Q: How can I improve hand tracking accuracy?**
A: Ensure good lighting, position your hand at an appropriate distance from the camera, and make clear gestures.

**Q: Does GestureArt support multiple hands?**
A: The current version focuses on single-hand tracking for optimal performance, but multi-hand support is planned for future updates.

**Q: Can I use GestureArt for professional artwork?**
A: Yes, GestureArt includes professional features like pressure sensitivity, various brush types, and high-resolution export options.

**Q: How do I update GestureArt?**
A: If installed via pip, run `pip install --upgrade gestureart`. If using the source code, pull the latest changes from the repository.

---

For additional support, please visit our website or contact our support team.
