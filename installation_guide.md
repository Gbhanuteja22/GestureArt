# GestureArt Installation Guide

This guide provides detailed instructions for installing and setting up the GestureArt application on different operating systems.

## System Requirements

Before installing GestureArt, ensure your system meets the following requirements:

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Processor**: Intel Core i5 or equivalent (i7 recommended for better performance)
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free disk space
- **Webcam**: Built-in or external webcam
- **Python**: Python 3.8 or higher
- **GPU**: Optional but recommended for better performance (NVIDIA GPU with CUDA support)

## Installation Methods

GestureArt can be installed using one of the following methods:

1. Using pip (recommended for most users)
2. From source code (recommended for developers)
3. Using the standalone installer (Windows only)

## Method 1: Using pip

This is the simplest method and works on all supported operating systems.

### Step 1: Install Python

If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/).

- **Windows**: Download the installer and run it. Make sure to check "Add Python to PATH" during installation.
- **macOS**: Download the installer or use Homebrew: `brew install python`
- **Linux**: Use your distribution's package manager, e.g., `sudo apt install python3 python3-pip`

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment helps avoid conflicts with other Python packages.

```bash
# Windows
python -m venv gestureart-env
gestureart-env\Scripts\activate

# macOS/Linux
python3 -m venv gestureart-env
source gestureart-env/bin/activate
```

### Step 3: Install GestureArt

```bash
pip install gestureart
```

### Step 4: Launch GestureArt

```bash
gestureart
```

## Method 2: From Source Code

This method is recommended for developers who want to modify the code or contribute to the project.

### Step 1: Install Git

If you don't have Git installed, download and install it from the [official Git website](https://git-scm.com/downloads).

### Step 2: Clone the Repository

```bash
git clone https://github.com/yourusername/GestureArt.git
cd GestureArt
```

### Step 3: Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Launch GestureArt

```bash
python src/main.py
```

## Method 3: Standalone Installer (Windows Only)

For Windows users who prefer not to use Python directly, we provide a standalone installer.

### Step 1: Download the Installer

Download the latest installer from the [releases page](https://github.com/yourusername/GestureArt/releases).

### Step 2: Run the Installer

Double-click the downloaded `.exe` file and follow the installation wizard.

### Step 3: Launch GestureArt

After installation, you can launch GestureArt from the Start menu or desktop shortcut.

## Installing Optional Dependencies

### GPU Support (for better performance)

If you have an NVIDIA GPU, you can install TensorFlow with GPU support for better performance:

```bash
pip install tensorflow-gpu
```

For detailed instructions on setting up CUDA and cuDNN, refer to the [TensorFlow GPU guide](https://www.tensorflow.org/install/gpu).

### Development Tools

If you want to contribute to the project or run the tests, install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Troubleshooting Installation Issues

### Common Issues on Windows

1. **Missing Visual C++ Redistributable**:
   - Error: `ImportError: DLL load failed`
   - Solution: Install the [Microsoft Visual C++ Redistributable](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)

2. **Path Too Long Error**:
   - Error: `ERROR: Could not install packages due to an OSError: [Errno 2]`
   - Solution: Use a shorter path for installation or enable long paths in Windows

### Common Issues on macOS

1. **Permission Denied**:
   - Error: `PermissionError: [Errno 13] Permission denied`
   - Solution: Use `sudo pip install gestureart` or install in a virtual environment

2. **Camera Access**:
   - Error: Camera not working
   - Solution: Grant camera permissions in System Preferences > Security & Privacy > Camera

### Common Issues on Linux

1. **Missing OpenCV Dependencies**:
   - Error: `ImportError: libGL.so.1: cannot open shared object file`
   - Solution: Install OpenCV dependencies: `sudo apt install libgl1-mesa-glx`

2. **Webcam Access**:
   - Error: `cv2.error: OpenCV(4.x.x) (...) failed to initialize video capture`
   - Solution: Ensure your user has permission to access the webcam: `sudo usermod -a -G video $USER`

## Verifying Installation

To verify that GestureArt is installed correctly, run:

```bash
# If installed via pip
gestureart --version

# If installed from source
python src/main.py --version
```

You should see the version number of GestureArt displayed.

## Updating GestureArt

### Updating pip Installation

```bash
pip install --upgrade gestureart
```

### Updating Source Installation

```bash
cd GestureArt
git pull
pip install -r requirements.txt
```

## Uninstalling GestureArt

### Uninstalling pip Installation

```bash
pip uninstall gestureart
```

### Uninstalling Source Installation

Simply delete the GestureArt directory.

### Uninstalling Standalone Installation (Windows)

Use the Windows Control Panel > Programs > Uninstall a program.

## Getting Help

If you encounter any issues during installation, please:

1. Check the [Troubleshooting](#troubleshooting-installation-issues) section above
2. Visit our [GitHub Issues page](https://github.com/yourusername/GestureArt/issues)
3. Join our [Discord community](https://discord.gg/gestureart) for real-time help

## Next Steps

After installation, refer to the [User Manual](user_manual.md) to learn how to use GestureArt.
