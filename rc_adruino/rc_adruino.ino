const int forwardPin = 2;
const int backPin = 4;
const int leftPin = 7;
const int rightPin = 8;

void setup(){
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  pinMode(4, OUTPUT);
  digitalWrite(4, HIGH);
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  pinMode(8, OUTPUT);
  digitalWrite(8, HIGH);
}

void loop(){
  if (Serial.available() > 0){
    int cmd = Serial.readString().toInt();
    if (cmd == 0){
      digitalWrite(2, LOW);
    }
    if (cmd == 1){
      digitalWrite(4, LOW);
    }
    if (cmd == 2){
      digitalWrite(7, LOW);
    }
    if (cmd == 3){
      digitalWrite(8, LOW);
    }
    if (cmd == 4){
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(7, HIGH);
      digitalWrite(8, HIGH);
    }
  }
}
