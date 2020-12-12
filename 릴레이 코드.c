#include <SoftwareSerial.h>

SoftwareSerial btSerial(2, 3);//RX 2번 TX 3번

int cds = 9;//센서 인식
int relay = 10;//릴레이 핀번호
boolean sensor_activate = true;//if구문 통제위한 전역변수 선언

void setup(){
  digitalWrite(relay, HIGH);//시작시 컨베이어 작동
  btSerial.begin(9600);//시리엁통신 오픈
  pinMode(cds, INPUT);//센서값을 인풋
  pinMode(relay, OUTPUT);//컨베이어 작동 아웃풋
}
 void loop(){
    int val=digitalRead(cds);//센서값 디지털로 받는다
    if (sensor_activate){  //전역변수가 true 이면 구문 실행
      if(val == LOW){ //센서값 인식
        digitalWrite(relay, LOW);//카메라 촬영을위해 컨베이어 작동 멈춘다
        delay(3000);//촬영 위해 딜레이를 준다
        //digitalWrite(relay,HIGH) 빼먹은거같은디;;
        if(btSerial.available()>0);//시리얼통신에 값이 들어오면
          char in_data;// in_data 선언
          in_data = btSerial.read();//시리얼 값읅 읽어온다
            if(in_data =='0'){  //데이터가 1이면(서버에서 통제권)
              digitalWrite(relay, LOW); //컨베이어 작동을멈춘다
              }
            else{
              digitalWrite(relay, HIGH);//그렇지 않다면 원래대로 촬영 딜레이를 준후 컨베이어를 다시 작동시킨다
             }
        sensor_activate = false; // if 구문 무한반복을막기위해 변수를 false로하여 센서가 인식되어있는 상태라도 다시 if구문 실행을 먹는다
        delay(500); // 오류없애기위한 ㅣㄷㄹ레이
        }
    }
    else if(btSerial.available()>0){//위에 구문은 센서값이 인식되어있는경우 카메라 촬영 및 센서값이 인식되었음에도 서버가 통제권을가지기위해 멈추게한다. 하지만 여기는 센서값이 high 즉 아무것도 인식되지 않았을때 서버가 통제하기 위함이다
        char in_data;//in_data 변수 선언한다
        in_data = btSerial.read(); // 시리얼 값을 읽어온다
          if(in_data == '0'){ //만약 시리얼값이 1이면 멈춘다
            digitalWrite(relay,LOW);
      }
          else if(in_data == '1'){ // 시리얼 값이 2이면 작동시킨다
            digitalWrite(relay, HIGH);
            delay(500); //오류를 없애기 위한 딜레이
      }
    }
    else if(val == HIGH){ // 만약  센서가 인식이 되지 않으면 전역변수를 다시 true로 반환하여 if구문이 실행되게한다
      sensor_activate = true;
    }
 }
