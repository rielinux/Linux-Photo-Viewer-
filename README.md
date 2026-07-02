# Windows Photo Viewer Clone for Linux

A lightweight, Python-based desktop photo viewer for Linux (specifically optimized for Kali Linux and Debian/XFCE environments) designed to replicate the classic Windows Photo Viewer experience.

## Features
- **Classic UI**: Familiar top-bar menus and bottom rounded capsule navigation bar.
- **Custom Vector Icons**: Rendered programmatically to bypass common Linux GTK/Qt theme compatibility issues (ensuring icons show up correctly on any theme).
- **Interactive Zooming**: Support for zooming in/out using the mouse scroll wheel.
- **Mouse Panning/Dragging**: Easily hold and drag the image with the left mouse button to view details when zoomed in.
- **Fullscreen Mode**: Toggle fullscreen by clicking the monitor icon, and exit seamlessly by pressing `ESC`.
- **File Navigation**: Navigate through pictures in the same folder using the previous/next buttons or keyboard arrow keys (Left/Right).
- **External Open**: "Open with" submenu to easily direct files to GIMP, Ristretto, Firefox, or System Default.
- **Local Deletion**: Delete photo files directly from the app interface with a confirmation safety prompt.

## Requirements
You only need Python 3 and PyQt5:
```bash
sudo apt update
sudo apt install python3-pyqt5 -y
```

## How to Run Locally
Simply run the Python script
```bash
python3 photo_viewer.py
```
