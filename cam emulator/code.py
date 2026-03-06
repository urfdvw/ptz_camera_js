import usb_cdc
import time

# Use the USB CDC data port (raw binary, doesn't interpret control chars)
serial = usb_cdc.data

# Emulated PTZ state
pan_pos = 0     # -1000 to +1000 (left to right)
tilt_pos = 0    # -500 to +500 (down to up)
zoom_pos = 0    # 0 to 1000 (wide to tele)

# Movement state
pan_speed = 0
tilt_speed = 0
pan_dir = 3     # 1=left, 2=right, 3=stop
tilt_dir = 3    # 1=up, 2=down, 3=stop
zoom_speed = 0
zoom_dir = 0    # 0=stop, 2=in, 3=out

# Presets storage (6 presets)
presets = {}

# VISCA response codes
ACK = bytes([0x90, 0x41, 0xFF])
COMPLETION = bytes([0x90, 0x51, 0xFF])

print("VISCA Camera Emulator Ready")
print("Initial State - Pan: 0, Tilt: 0, Zoom: 0")

last_update = time.monotonic()

def parse_visca_command(data):
    global pan_dir, tilt_dir, pan_speed, tilt_speed, zoom_dir, zoom_speed

    if len(data) < 3 or data[0] != 0x81 or data[-1] != 0xFF:
        return None

    # Pan/Tilt command: 0x81 0x01 0x06 0x01 [panSpeed] [tiltSpeed] [panDir] [tiltDir] 0xFF
    if len(data) == 9 and data[1:4] == bytes([0x01, 0x06, 0x01]):
        pan_speed = data[4]
        tilt_speed = data[5]
        pan_dir = data[6]
        tilt_dir = data[7]
        return "PanTilt"

    # Zoom command: 0x81 0x01 0x04 0x07 [value] 0xFF
    if len(data) == 6 and data[1:4] == bytes([0x01, 0x04, 0x07]):
        zoom_value = data[4]
        if zoom_value == 0:
            zoom_dir = 0
            zoom_speed = 0
        elif (zoom_value & 0xF0) == 0x20:  # Zoom in
            zoom_dir = 2
            zoom_speed = zoom_value & 0x0F
        elif (zoom_value & 0xF0) == 0x30:  # Zoom out
            zoom_dir = 3
            zoom_speed = zoom_value & 0x0F
        return "Zoom"

    # Preset recall: 0x81 0x01 0x04 0x3F 0x02 [n] 0xFF
    if len(data) == 7 and data[1:5] == bytes([0x01, 0x04, 0x3F, 0x02]):
        preset_num = data[5]
        if preset_num in presets:
            global pan_pos, tilt_pos, zoom_pos
            pan_pos, tilt_pos, zoom_pos = presets[preset_num]
            print(f"Recalled Preset {preset_num}: Pan={pan_pos}, Tilt={tilt_pos}, Zoom={zoom_pos}")
        return "PresetRecall"

    # Preset set: 0x81 0x01 0x04 0x3F 0x01 [n] 0xFF
    if len(data) == 7 and data[1:5] == bytes([0x01, 0x04, 0x3F, 0x01]):
        preset_num = data[5]
        presets[preset_num] = (pan_pos, tilt_pos, zoom_pos)
        print(f"Saved Preset {preset_num}: Pan={pan_pos}, Tilt={tilt_pos}, Zoom={zoom_pos}")
        return "PresetSet"

    return "Unknown"

def update_positions(delta_time):
    global pan_pos, tilt_pos, zoom_pos

    changed = False

    # Update pan position
    if pan_dir == 1:  # Left
        pan_pos -= pan_speed * 10 * delta_time
        pan_pos = max(-1000, pan_pos)
        changed = True
    elif pan_dir == 2:  # Right
        pan_pos += pan_speed * 10 * delta_time
        pan_pos = min(1000, pan_pos)
        changed = True

    # Update tilt position
    if tilt_dir == 1:  # Up
        tilt_pos += tilt_speed * 5 * delta_time
        tilt_pos = min(500, tilt_pos)
        changed = True
    elif tilt_dir == 2:  # Down
        tilt_pos -= tilt_speed * 5 * delta_time
        tilt_pos = max(-500, tilt_pos)
        changed = True

    # Update zoom position
    if zoom_dir == 2:  # Zoom in
        zoom_pos += zoom_speed * 20 * delta_time
        zoom_pos = min(1000, zoom_pos)
        changed = True
    elif zoom_dir == 3:  # Zoom out
        zoom_pos -= zoom_speed * 20 * delta_time
        zoom_pos = max(0, zoom_pos)
        changed = True

    return changed

while True:
    # Check if data is available to read
    if serial.in_waiting > 0:
        # Read available bytes
        data = serial.read(serial.in_waiting)

        # Parse VISCA command
        cmd_type = parse_visca_command(data)

        if cmd_type:
            # Send ACK response
            serial.write(ACK)

            if cmd_type == "PanTilt":
                action = []
                if pan_dir == 1:
                    action.append(f"Pan LEFT speed={pan_speed}")
                elif pan_dir == 2:
                    action.append(f"Pan RIGHT speed={pan_speed}")
                if tilt_dir == 1:
                    action.append(f"Tilt UP speed={tilt_speed}")
                elif tilt_dir == 2:
                    action.append(f"Tilt DOWN speed={tilt_speed}")
                if not action:
                    action.append("STOP")
                print(f"Action: {' + '.join(action)}")

            elif cmd_type == "Zoom":
                if zoom_dir == 2:
                    print(f"Action: Zoom IN speed={zoom_speed}")
                elif zoom_dir == 3:
                    print(f"Action: Zoom OUT speed={zoom_speed}")
                else:
                    print("Action: Zoom STOP")

            # Send completion response
            serial.write(COMPLETION)

    # Update positions based on current movement
    current_time = time.monotonic()
    delta_time = current_time - last_update
    last_update = current_time

    if update_positions(delta_time):
        print(f"Position: Pan={int(pan_pos)}, Tilt={int(tilt_pos)}, Zoom={int(zoom_pos)}")
        print((int(pan_pos), int(tilt_pos)))

    # Small delay to prevent CPU hogging
    time.sleep(0.01)
