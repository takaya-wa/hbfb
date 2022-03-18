const int analogOutPin = 9; 
String cmd;
int delayTime;
int outputValue1;
int outputValue2;
int outputValue3;

int split(String data, char delimiter, String *dst){
  int index = 0;
  int arraySize = (sizeof(data)/sizeof((data)[0]));  
  int datalength = data.length();
  for (int i = 0; i < datalength; i++) {
    char tmp = data.charAt(i);
    if ( tmp == delimiter ) {
      index++;
      if ( index > (arraySize - 1)) return -1;
    }
    else dst[index] += tmp;
  }
  return (index + 1);
}
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  String cmds[5] = {"\0"}; // 分割された文字列を格納する配列 
  
  if (Serial.available() > 0) {
    cmd = Serial.readString();
    int index = split(cmd, ',', cmds);
    for(int i = 0; i < index; i++){
      delayTime = cmds[0].toInt();
      outputValue1 = cmds[1].toInt();
      outputValue2 = cmds[2].toInt();
      outputValue3 = cmds[3].toInt();

    }
  }
  analogWrite(analogOutPin, 0);
  delay(delayTime);
  analogWrite(analogOutPin, outputValue1);
  delay(delayTime);
  analogWrite(analogOutPin, outputValue2);
  delay(delayTime);
  analogWrite(analogOutPin, outputValue3);
  delay(delayTime);

}