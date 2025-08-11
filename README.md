# **🏠 Smart Room Multimodal Control System**

A cloud-integrated IoT solution for smart room automation using computer vision gesture recognition and voice commands, leveraging Azure IoT Hub, Raspberry Pi 4, and Arduino UNO for real-time appliance control.

###**📊 System Performance**

| Metric                           | Measured Value | Conditions                           
| -------------------------------- | -------------- | ------------------------------------ |
| **Gesture Recognition Accuracy** | 95%            | Well-lit environment (400–500 lux)   |
|                                  | 82%            | Low-light conditions                 |
| **Voice Recognition Accuracy**   | 91%            | Quiet room, single speaker           |
|                                  | 80%            | Moderate noise environment           |
| **End-to-End Latency**           | \~0.8 seconds  | Complete command execution cycle     |
| **System Uptime**                | 5+ hours       | Continuous operation without crashes |
| **False Positives (Voice)**      | 2–3%           | Due to accidental wake-word triggers |
| **False Negatives (Gesture)**    | 5–10%          | In low-light conditions              |



###**✨ Key Features**

🖐️ Gesture Control System

+ MediaPipe-based hand tracking with 21 3D landmarks detection
  
+ Real-time gesture classification at 15+ FPS
  
+ Finger counting algorithm for command mapping:

      1 finger → Turn ON Fan
      2 fingers → Turn OFF Fan
      3 fingers → Turn ON Light
      4 fingers → Turn OFF Light



**🎤 Voice Command System**

    Two-phase recognition: Wake-word activation + Command detection
    "Friday" wake-word for hands-free activation
    8-second command window after activation
    Multiple exception handling layers for robustness

**☁️ Cloud Integration**

    Azure IoT Hub with MQTT protocol
    TLS 1.2 encryption for secure communication
    Symmetric key authentication
    Unidirectional Cloud-to-Device (C2D) messaging

**🔌 Edge Computing**

    Raspberry Pi 4 as IoT edge device
    Arduino UNO for hardware control
    UART communication at 9600 baud rate
    Real-time proximity detection with ultrasonic sensor

### **🏗️ System Architecture**

      ┌─────────────────────────┐
      │   Input Recognition     │
      │  (Laptop/Computer)      │
      │ • MediaPipe Hands       │
      │ • Speech Recognition    │
      │ • Flask Web Server      │
      └───────────┬─────────────┘
                  │ MQTT over TLS 1.2
                  ▼
      ┌─────────────────────────┐
      │   Azure IoT Hub         │
      │ • Device Management     │
      │ • Message Routing       │
      │ • Secure Communication  │
      └───────────┬─────────────┘
                  │ C2D Messages
                  ▼
      ┌─────────────────────────┐
      │   Raspberry Pi 4        │
      │ • IoT Device Client     │
      │ • Message Processing    │
      │ • Serial Communication  │
      └───────────┬─────────────┘
                  │ UART (9600 baud)
                  ▼
      ┌─────────────────────────┐
      │   Arduino UNO           │
      │ • Command Parsing       │
      │ • Relay Control         │
      │ • Proximity Sensing     │
      └───────────┬─────────────┘
                  │
                  ▼
      ┌─────────────────────────┐
      │   Physical Devices      │
      │ • Fan (Relay Module)    │
      │ • Light (Relay Module)  │
      │ • Buzzer & LED          │
      └─────────────────────────┘
      
**🔧 Hardware Requirements**
Core Components

    Raspberry Pi 4 (3.3V logic)
    Arduino UNO (5V logic)
    USB Camera (minimum 640x480 resolution)
    USB Microphone
    Relay Module (with optocoupler isolation)
    HC-SR04 Ultrasonic Sensor
    Passive Buzzer
    LED with current-limiting resistor
    Common USB Hub (for stable power supply)


**💻 Software Stack**
Python Libraries

    bash# Core Libraries
    flask==2.3.2
    opencv-python==4.8.0
    numpy==1.24.3
    mediapipe==0.10.3
    
    # Azure IoT
    azure-iot-device==2.12.0
    azure-iot-hub==2.6.1
    
    # Voice Recognition
    SpeechRecognition==3.10.0
    pyaudio==0.2.11
    
    # Serial Communication
    pyserial==3.5

System Requirement

      Python 3.7-3.10
      Arduino IDE 1.8+
      Azure subscription with IoT Hub
      PortAudio19 (for voice recognition)




##**👨‍💻 Author**
###***Bhargavkumar Panchal***

GitHub: @bbhargavpanchal
LinkedIn: https://www.linkedin.com/in/bhargavpanchall/




📞 Support

Email: bhargavpanchal5151@gmail.com


⭐ If you find this project useful, please consider giving it a star!
