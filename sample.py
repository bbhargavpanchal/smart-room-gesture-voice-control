import cv2
import mediapipe as mp
import threading
import time
import speech_recognition as sr
from flask import Flask, Response, render_template_string
from azure.iot.hub import IoTHubRegistryManager

# Azure IoT Hub config
IOTHUB_CONNECTION_STRING = "HostName=SmartRoom.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=8Up0jrGJrtoA33/55hZWWFNM784dtP94XAIoTLPUVuA="
DEVICE_ID = "raspberrypi4"
manager = IoTHubRegistryManager(IOTHUB_CONNECTION_STRING)

# Gesture and voice command mappings
finger_commands = {1: "FAN_ON", 2: "FAN_OFF", 3: "LIGHT_ON", 4: "LIGHT_OFF"}
voice_commands = {
    "turn on fan": "FAN_ON",
    "turn off fan": "FAN_OFF",
    "turn on light": "LIGHT_ON",
    "turn off light": "LIGHT_OFF",
}

# MediaPipe
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

# Voice
recognizer = sr.Recognizer()
mic = sr.Microphone()

# Gesture state
last_gesture_time = 0
last_gesture_cmd = "None"
GESTURE_COOLDOWN = 2  # seconds

app = Flask(__name__)

def count_fingers(hand_landmarks):
    tips = [8, 12, 16, 20]
    return sum(hand_landmarks.landmark[t].y < hand_landmarks.landmark[t - 2].y for t in tips)

def generate_video_stream():
    global last_gesture_cmd, last_gesture_time

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        current_time = time.time()

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
                fingers = count_fingers(hand)
                cmd = finger_commands.get(fingers)

                if cmd and (cmd != last_gesture_cmd or (current_time - last_gesture_time) > GESTURE_COOLDOWN):
                    manager.send_c2d_message(DEVICE_ID, cmd)
                    last_gesture_cmd = cmd
                    last_gesture_time = current_time
                    print(f"🖐️ Sent gesture command: {cmd}")

        # Show current command on video
        cv2.putText(frame, f"Gesture: {last_gesture_cmd}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

def voice_loop():
    print("🎙️ Voice recognition started... Say 'friday' before every command...")
    listening_for_command = False
    command_start_time = 0
    COMMAND_TIMEOUT = 8

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("✅ Ambient noise adjusted!")

    while True:
        try:
            with mic as source:
                print("🎧 Listening...")
                audio = recognizer.listen(source, timeout=2)
            text = recognizer.recognize_google(audio).lower()
            print(f"🗣️ Heard: {text}")
            current_time = time.time()

            if not listening_for_command:
                if "friday" in text:
                    listening_for_command = True
                    command_start_time = current_time
                    print("✅ 'friday' detected! Now say your command...")
            else:
                if (current_time - command_start_time) > COMMAND_TIMEOUT:
                    print("⌛ Command timeout.")
                    listening_for_command = False
                    continue

                for phrase, command in voice_commands.items():
                    if phrase in text:
                        manager.send_c2d_message(DEVICE_ID, command)
                        print(f"🎤 Sent voice command: {command}")
                        listening_for_command = False
                        break
                else:
                    print("⚠️ Command not recognized.")
                    listening_for_command = False

        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
        except sr.WaitTimeoutError:
            print("⏳ Listening timeout.")
        except sr.RequestError:
            print("⚠️ Google Speech Recognition failed.")

@app.route("/")
def index():
    return render_template_string("""
    <html>
        <head><title>Smart Room Control</title></head>
        <body style="text-align: center;">
            <h2>Smart Room Control</h2>
            <img src="/video_feed" width="640"><br>
            <p><strong>Live gesture detection feed</strong></p>
        </body>
    </html>
    """, cmd=last_gesture_cmd)

@app.route("/video_feed")
def video_feed():
    return Response(generate_video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    voice_thread = threading.Thread(target=voice_loop)
    voice_thread.daemon = True
    voice_thread.start()
    print("🌐 Running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
