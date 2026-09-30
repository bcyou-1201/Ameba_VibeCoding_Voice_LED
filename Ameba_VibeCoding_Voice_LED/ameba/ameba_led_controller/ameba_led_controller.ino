/*
 AMB82-MINI / RTL8735B
 LED_B = Blue, Arduino pin 23
 LED_G = Green, Arduino pin 24
 Serial: 115200
*/
const int LED_ON=HIGH, LED_OFF=LOW;
bool blueState=false, greenState=false;
void applyState(bool b,bool g){blueState=b;greenState=g;digitalWrite(LED_B,b?LED_ON:LED_OFF);digitalWrite(LED_G,g?LED_ON:LED_OFF);}
void reportState(){Serial.print("STATE BLUE=");Serial.print(blueState?1:0);Serial.print(" GREEN=");Serial.println(greenState?1:0);}
void ack(const char*c){Serial.print("ACK ");Serial.println(c);reportState();}
void flash3(int pin){applyState(false,false);for(int i=0;i<3;i++){digitalWrite(pin,LED_ON);delay(300);digitalWrite(pin,LED_OFF);delay(300);}applyState(false,false);}
void both3(){applyState(false,false);for(int i=0;i<3;i++){digitalWrite(LED_B,LED_ON);digitalWrite(LED_G,LED_ON);delay(300);digitalWrite(LED_B,LED_OFF);digitalWrite(LED_G,LED_OFF);delay(300);}applyState(false,false);}
void handle(String c){c.trim();if(c=="LEFT_ON"){applyState(true,false);ack("LEFT_ON");}else if(c=="RIGHT_ON"){applyState(false,true);ack("RIGHT_ON");}else if(c=="ALL_OFF"){applyState(false,false);ack("ALL_OFF");}else if(c=="FLASH_BLUE_3"){flash3(LED_B);ack("FLASH_BLUE_3");}else if(c=="FLASH_GREEN_3"){flash3(LED_G);ack("FLASH_GREEN_3");}else if(c=="FLASH3"){both3();ack("FLASH3");}else if(c=="GET_STATUS"){ack("GET_STATUS");}else if(c.length()){Serial.print("NACK UNKNOWN ");Serial.println(c);reportState();}}
void setup(){pinMode(LED_B,OUTPUT);pinMode(LED_G,OUTPUT);applyState(false,false);Serial.begin(115200);delay(300);Serial.println("READY AMB82-MINI");reportState();}
void loop(){if(Serial.available())handle(Serial.readStringUntil('\n'));}
