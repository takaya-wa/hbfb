const int analogOutPin = 9; 
String cmd;
int OnTime;
int OffTime;
int outputValue = 200;

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
  String cmds[3] = {"\0"}; // 分割された文字列を格納する配列 
  
  if (Serial.available() > 0) {
    cmd = Serial.readString();
    int index = split(cmd, ',', cmds);
    for(int i = 0; i < index; i++){
      OnTime = cmds[0].toInt();
      OffTime = cmds[1].toInt();
    }
  }
  
  analogWrite(analogOutPin, outputValue);
  delay(OnTime);

  analogWrite(analogOutPin, 0);
  delay(OffTime);
}