const int forwardPin = 2;
const int backPin = 4;
const int leftPin = 7;
const int rightPin = 8;

void setup(){
  Serial.begin(500000);
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
    char cmd = Serial.read();
    
    //Stop all operations
    if (cmd == 's'){
      digitalWrite(2, HIGH);
      digitalWrite(4, HIGH);
      digitalWrite(7, HIGH);
      digitalWrite(8, HIGH);
    }
    
    //Move the car Forward and stop transmitting Reverse Signal if transmitting
    if (cmd == 'f'){
      Serial.println("Moving forward");
      digitalWrite(2, LOW);
      digitalWrite(4, HIGH);
    }
    //Reverse the car and stop transmitting Forward Signal if transmitting
    else if (cmd == 'b'){
      Serial.println("Moving Backward");
      digitalWrite(4, LOW);
      digitalWrite(2, HIGH);
    }

    //Steer the car left and stop transmitting right signal
    if (cmd == 'l'){
      Serial.println("Moving left");
      digitalWrite(7, LOW);
      digitalWrite(8, HIGH);
    }
    //Steer the car right and stop transmitting left signal
    else if(cmd == 'r'){
      Serial.println("Moving Right");
      digitalWrite(8, LOW);
      digitalWrite(7, HIGH);
    }

    //Steer the car straight and not steer the car (NO direction to motion of the car)
    if (cmd == 'n'){
      Serial.println("No direction");
      digitalWrite(8, HIGH);
      digitalWrite(7, HIGH);
    }
  }
}
