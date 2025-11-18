# 🏏 Hand Cricket - Ultimate Gesture Game

A fun and interactive cricket game where you play against the computer using hand gestures! Show your fingers (1-6) to score runs. Match the computer's gesture and you're OUT! Written in Python using OpenCV and MediaPipe.

## 🎮 Game Features

- **Hand Gesture Recognition**: Use your webcam to show hand gestures (1-6 fingers)
- **Two-Innings Cricket**: Bat first to set a target, then bowl to defend it
- **Real-time Hand Detection**: Powered by MediaPipe for accurate gesture tracking
- **Beautiful GUI**: Modern, colorful interface with hover effects
- **Score Tracking**: Live scoreboard with innings and target display
- **Game Logic**: Professional cricket rules with OUT and run scoring

## 📋 Prerequisites

Before you start, make sure your system has:
- **Python 3.10** installed
- A working **webcam**
- **pip** (Python package manager)

## 🚀 Installation Guide

### Step 1: Install Python 3.10

#### On Windows:
1. Download Python 3.10 from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH" during installation
4. Click "Install Now"

#### On macOS:
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Verify installation
python3.10 --version
```

#### On Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Verify installation
python3.10 --version
```

### Step 2: Create a Virtual Environment

A virtual environment keeps your project dependencies isolated and clean.

#### On Windows:
```bash
# Navigate to your project folder
cd path/to/your/HandCricket/folder

# Create virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
# Navigate to your project folder
cd path/to/your/HandCricket/folder

# Create virtual environment
python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

**Note**: When activated, you'll see `(venv)` at the beginning of your terminal line.

### Step 3: Install Required Dependencies

With the virtual environment activated, install all required packages:

```bash
pip install --upgrade pip

pip install opencv-python
pip install mediapipe
pip install pillow
pip install numpy
```

Or install everything at once using a requirements file. Create `requirements.txt` in your project folder:

```
opencv-python==4.8.1.78
mediapipe==0.10.0
Pillow==10.0.0
numpy==1.24.3
```

Then install:
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

Test if everything is installed correctly:

```bash
python -c "import cv2; import mediapipe; import tkinter; print('All dependencies installed successfully!')"
```

If you see "All dependencies installed successfully!", you're good to go!

## 🎮 How to Play

### Running the Game

With your virtual environment activated:

```bash
python HandCricket.py
```

### Game Rules

1. **Welcome Screen**: Click "START GAME" to begin
2. **Choose Your Role**: Select "BAT FIRST" or "BOWL FIRST"
3. **First Innings**: 
   - If you bat: Show fingers to score runs (avoid matching computer's gesture - you'll be OUT!)
   - If you bowl: Computer bats and you defend. Same number as computer's = OUT!
4. **Second Innings**: 
   - Switch roles and try to chase or defend the target
5. **Win Condition**: First player to beat the target wins!

### Gesture Guide

Show these hand gestures to score:
- **1 finger**: 1 run (index finger only)
- **2 fingers**: 2 runs (index + middle)
- **3 fingers**: 3 runs (index + middle + ring)
- **4 fingers**: 4 runs (all 4 fingers)
- **5 fingers**: 5 runs (all 5 fingers open)
- **6 fingers**: 6 runs (fist with thumb out)

**⚠️ Same number as computer = OUT!**

### Controls

- **Q Key**: Quit the game during play
- **Mouse**: Click buttons in the GUI to navigate
- **Webcam**: Position your hand clearly in frame for best detection

## 🛠️ Troubleshooting

### Webcam Not Opening
```
Error: "Could not open camera!"
```
- Check if another app is using your webcam
- Restart the application
- Check device manager to see if webcam is recognized

### Hand Gestures Not Detected
- Ensure good lighting in your room
- Place your hand clearly in the center of the frame
- Keep your hand within the camera's view
- Try different hand positions (palm facing camera works best)

### Python Not Found
```
'python' is not recognized as an internal or external command
```
- You didn't add Python to PATH during installation
- Reinstall Python and check "Add Python to PATH"
- Or use `python3` or `python3.10` instead of `python`

### Virtual Environment Not Activating
- Check the path spelling
- Make sure you're in the correct directory
- Try: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'mediapipe'
```
- Ensure your virtual environment is activated (you see `(venv)` in terminal)
- Reinstall: `pip install mediapipe`

## 📁 Project Structure

```
HandCricket/
├── HandCricket.py          # Main game file
├── requirements.txt        # Python dependencies
├── venv/                   # Virtual environment folder
└── README.md              # This file
```

## 🎨 Features Explained

- **MediaPipe Hands**: Tracks 21 hand landmarks for accurate gesture recognition
- **OpenCV**: Captures video feed and draws UI elements
- **Tkinter**: Creates the GUI for welcome and result screens
- **PIL**: Handles image processing for the interface

## 💡 Tips for Better Performance

1. Use a well-lit environment
2. Keep your hand 30-50cm away from the camera
3. Show gestures clearly (don't rush)
4. Wait for the gesture to be recognized before showing the next one
5. Ensure your webcam has good resolution (720p or higher)

## 🐛 Known Issues

- Gesture detection accuracy depends on lighting and hand position
- Fast hand movements may not be recognized
- Some webcams may have delayed video feed

## 👨‍💻 How This Was Made (For CS Students)

### Libraries Used:

**OpenCV (`cv2`)**: Computer vision library for video capture and image processing
- Captures frames from webcam
- Draws hand landmarks and UI text
- Converts color spaces (BGR to RGB)

**MediaPipe (`mediapipe`)**: ML framework by Google for hand detection
- Detects 21 hand landmarks (finger joints)
- Real-time performance on CPU
- Returns hand positions with confidence scores

**Tkinter (`tkinter`)**: GUI toolkit for Python
- Creates windows and buttons
- Handles user interactions
- Displays welcome and result screens

**PIL (`Pillow`)**: Image processing library
- Handles image operations in GUI

**NumPy (`numpy`)**: Numerical computing library
- Matrix operations used by OpenCV and MediaPipe

### Code Concepts Used:

- **Global Variables**: Track game state (score, innings, gestures)
- **Threading**: Separate GUI and camera loop (implicit with cv2)
- **Gesture Recognition**: Finger position logic using coordinates
- **Game Logic**: Win/loss conditions and scoring
- **Event Handling**: Button clicks and keyboard inputs

## 📝 License

This project was created as an educational game. Feel free to modify and learn!

## 👤 Author

**Made with HandCricket using OpenCV & MediaPipe By Menda**

---

**Happy Gaming! 🏏🎮**

Questions? Check the troubleshooting section or verify your installation!
