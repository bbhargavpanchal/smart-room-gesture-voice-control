// Pin defs
const uint8_t FAN_PIN    = 3;
const uint8_t LIGHT_PIN  = 4;
const uint8_t TRIG_PIN   = 5;
const uint8_t ECHO_PIN   = 6;
const uint8_t BUZZER_PIN = 7;

// Serial cmd buffer
char cmdBuf[32];
uint8_t cmdPos = 0;

// Ultrasonic timing
unsigned long lastPingTime = 0;
const unsigned long PING_INTERVAL = 100; // ms

void setup() {
  Serial.begin(9600);
  pinMode(FAN_PIN,    OUTPUT);
  pinMode(LIGHT_PIN,  OUTPUT);
  pinMode(TRIG_PIN,   OUTPUT);
  pinMode(ECHO_PIN,   INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // start with everything off
  digitalWrite(FAN_PIN, LOW);
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
  serviceSerial();             // always check for incoming commands
  
  unsigned long now = millis();
  if (now - lastPingTime >= PING_INTERVAL) {
    lastPingTime = now;
    int dist = readUltrasonic();     
    // buzzer on if object is 5ï¿½20 cm away
    digitalWrite(BUZZER_PIN, (dist >= 5 && dist <= 20) ? HIGH : LOW);
  }
}

// Non-blocking serial reader + dispatcher
void serviceSerial() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (cmdPos > 0) {
        cmdBuf[cmdPos] = '\0';
        handleCommand(cmdBuf);
        cmdPos = 0;
      }
    }
    else if (cmdPos < sizeof(cmdBuf) - 1) {
      cmdBuf[cmdPos++] = c;
    }
  }
}

// Act on a single command string
void handleCommand(const char* cmd) {
  if      (strcmp(cmd, "FAN_ON")    == 0) digitalWrite(FAN_PIN,   HIGH);
  else if (strcmp(cmd, "FAN_OFF")   == 0) digitalWrite(FAN_PIN,   LOW);
  else if (strcmp(cmd, "LIGHT_ON")  == 0) digitalWrite(LIGHT_PIN, HIGH);
  else if (strcmp(cmd, "LIGHT_OFF") == 0) digitalWrite(LIGHT_PIN, LOW);
  else if (strcmp(cmd, "ALL_ON")    == 0) {
    digitalWrite(FAN_PIN,   HIGH);
    digitalWrite(LIGHT_PIN, HIGH);
  }
  // example gesture feedback (optional)
  else if (strcmp(cmd, "LEFT")      == 0) Serial.println(F("Gesture: LEFT"));
  else if (strcmp(cmd, "RIGHT")     == 0) Serial.println(F("Gesture: RIGHT"));
  else {
    Serial.print(F("Unknown cmd: "));
    Serial.println(cmd);
  }
}

// Trigger & measure HC-SR04 (max 30 ms wait)
int readUltrasonic() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  unsigned long duration = pulseIn(ECHO_PIN, HIGH, 30000UL);
  if (duration == 0) return -1;               // timeout
  return int(duration * 0.034 / 2 + 0.5);     // cm
}