int PulseSensorPurplePin = 0;        
int Signal;                
unsigned long time;

void setup() {
  Serial.begin(115200);      
}

void loop() {
  time = millis();
  Signal = analogRead(PulseSensorPurplePin);  
  Serial.println(Signal);
  Serial.println(time);                    
  delay(10);
}