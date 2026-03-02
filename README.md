# VISCA PTZ Camera Controller

**Control your VISCA PTZ camera directly from your browser. No installation required.**

🌐 **[Launch App](https://urfdvw.github.io/visca_ptz_camera_control/)**

---

## ✨ Features

🎮 **Multiple Control Options**
- Virtual joysticks (pan/tilt + zoom)
- WASD keyboard controls
- On-screen button controls
- Touch screen support

💾 **Preset Management**
- Save up to 6 camera positions
- One-click recall
- Rename & organize with edit mode

⚡ **Smart Features**
- Variable speed control (1-5)
- Auto-reconnect on disconnect
- Works offline after first load

---

## 🚀 Quick Start

1. **Open**: Visit https://urfdvw.github.io/visca_ptz_camera_controll/
2. **Connect**: Click "Connect to Camera" and select your serial port
3. **Control**: Use keyboard, buttons, or joystick to control your camera

**Requirements**: Chrome, Edge, or Opera browser • VISCA-compatible camera

---

## ⌨️ Keyboard Shortcuts

```
Pan/Tilt:    W ↑   A ←   S ↓   D →
Zoom:        + IN   - OUT
Speed:       1-5 (slow to fast)
```

---

## 🎯 Quick Guide

**Control Your Camera**
- Drag the circular joystick for pan/tilt
- Drag the vertical slider for zoom
- Click WASD buttons or use keyboard
- Adjust speed with slider or number keys (1-5)

**Save Presets**
1. Position camera where you want
2. Click 💾 button on any preset slot
3. Enter a name

**Recall Presets**
- Click the blue preset button

**Edit Presets**
- Toggle "Edit" switch to rename (✏️) or clear (🗑️) presets

---

## 🔧 Troubleshooting

**Port won't open?**
- Close other apps using the serial port (Arduino IDE, PuTTY, etc.)
- Make sure no other browser tabs are connected

**Keyboard not working?**
- Close any open dialogs
- Click on the page to focus

**Camera not responding?**
- Check camera power and connections
- Verify camera uses VISCA protocol (9600 baud)
- Open browser console (F12) to see serial communication

---

## 📡 Technical

- **Protocol**: VISCA (Sony)
- **Baud Rate**: 9600, 8N1
- **API**: Web Serial API
- **Storage**: Browser localStorage (presets only)
- **Privacy**: 100% local, no data sent to servers
