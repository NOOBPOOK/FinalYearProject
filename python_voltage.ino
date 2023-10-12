const int analogInPin = A0; // Analog input pin
const unsigned long sampleInterval = 10000; // Sampling interval in microseconds (1 second / 200 samples = 5000 microseconds per sample)
unsigned long int start = millis();
void setup() {
  Serial.begin(500000);
  analogReference(DEFAULT);
  pinMode(13, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    int cmd = Serial.readString().toInt();
    if (cmd == 1){
      digitalWrite(13, HIGH);
    }
    else{
      digitalWrite(13, LOW);
    }
  }
  else{
    unsigned long startTime = micros(); // Get the current time in microseconds
    int integer_value = analogRead(analogInPin);
    Serial.write(integer_value & 0xFF);
    Serial.write((integer_value >> 8) & 0xFF);
    unsigned long endTime = micros();
    unsigned long elapsedTime = endTime - startTime;
    delayMicroseconds(sampleInterval - elapsedTime);
  }
}
