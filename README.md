# Smart Factory Monitoring System
## Project Synopsis
- 행사명 : 2018 성균관대학교 실전문제해결형 S-HERO
- 주최 : 성균관대학교 실전문제 해결형 S-HERO 공학인재 양성 사업단
- 진행 기간 : '18.3.1 ~ '18.12.7
- 목적 :  Vision 및 음성인식 기술을 활용하여, 캔 제조 공정에서 발생할 수 있는 불량품을 선별하고, 로그 기록 및 공정 제어가 가능한 제품 품질 관리 시스템 구축하여 지속 가능한 생산 방안에 관한 연구를 목적으로 하였습니다.
- 내용 : 라즈베리 파이 환경에서 OpenCV를 통한 이미지 처리로 불량품 검출, Snowboy 모듈을 통한 음성인식, 음성인식을 기반으로 한 공장의 제어, 불량품 검출의 데이터를 받아 불량품을 검출해내는 공장 시스템의 데모를 구축하였습니다. 그리고 이를 시연해보고 이를 바탕으로 추후 실제 공장에 적용될 수 있도록 서버, 디바이스, 하드웨어 각각을 테스트했습니다.
- 결과
  - 라즈베리파이 환경에서 OpenCV를 이미지 처리를 통해 캔의 불량품 여부를 판단할 수 있었습니다.
  - 이 데이터를 받아 서보모터가 불량품 여부에 따라 불량품을 검출할 수 있도록 하였습니다.
  - 음성인식 모듈은 Snowboy를 통한 컨베이어 벨트의 제어가 가능했습니다.
  - 이는 공장의 효과적인 제어가 가능하다는 것을 보여줍니다. 디바이스에서 시작 신호를 보내면 컨베이어 벨트가 작동하며, 정지 신호를 보내면 멈추게 됩니. 이러한 시스템을 위한 서버도 구축했습니다.
  - 음성인식 신호를 제어할 뿐만 아니라, 불량품 검출의 결과를 서버를 거쳐 웹페이지에 검출결과의 이미지를 보여주었습니다. 이러한 데이터 전송을 위해서 라즈베리파이 간 와이파이를 통한 mqtt 통신으로 디바이스 간의 데이터 전송이 이루어지게 하였습니다. 이러한 각각의 분야들이 하나의 서버를 통하여 서로 연결되어 하나의 공장의 형태를 이루게 됨을 보여주고 있습니다
## Tools
### Platform
- Raspberry Pi 3B
- Arduino Uno
### Sensor
- PiCamera
- IR Sensor
- Servo Motor
- Conveyer Belt
- ReSpeaker 4-Mic Array
### Software
- Node-RED
- Arduino IDE
## Big Picture
- 가장 먼저 컨베이어 벨트 제어를 위해 음성인식의 결과값을 서버를 통하여 아두이노로 전송되며, 이 결과로 음성인식을 통한 컨베이어 벨트가 제어되도록 하였습니다. 또한 라즈베리파이 간 mqtt 통신을 통하여 음성인식의 데이터, 불량품 검출의 결과 데이터를 전송시켜 컨베이어 벨트 제어 및 서보모터의 불량품 검출 분류를 가능하게 하도록 하였습니다. 서버를 구축함으로 인해 스마트 팩토리의 시스템처럼 가동하여 모든 공정을 제어할 수 있도록 하였습니다.
- 아래의 System Architecture에서 라즈베리파이 엣지 #1에서 음성인식을 통한 제어 명령을 전달하게 되면, 음성인식 후 제어 명령을 블루투스를 통해 전달하게 됩니다. 이 결과 컨베이어 벨트가 제어되며, 또한 라즈베리파이 디바이스#2에서 불량품 검출의 결괏값을 서버를 통해 디바이스#3으로 전송하고 그 결괏값에 따라 서보모터가 불량품을 분리해 내게 됩니다. 이러한 라즈베리파이 간의 mqtt는 와이파이를 통해서 통신하게 됩니다.
<img src=https://i.imgur.com/hWJth4y.png><br>
## Project Details
### 1. 하드웨어 구축
컨베이어 벨트 구동을 위한 릴레이작동, 카메라실행 및 릴레이작동 및 정지를 위한 적외선 센서, 불량품 검출을 위한 서보모터 작동을 위해 아두이노를 사용하였고 이의 작동을위해 IDLE를  사용하였습니다. 이후 통신을 위해 라즈베리파이와 UART(Universal asynchronous receiver/transmitter)연결을 통해 Serial 통신으로 데이터를 송수신하도록 하였습니다.
#### 1) 컨베이어 벨트
음성명령이 내려졌을 때, 설비의 작동이 시작되기 위해서는 컨베이어 벨트의 제어가 필요합니다. 이때 컨베이어 벨트를 제어하기 위해 아두이노를 사용하기로 결정했습니다. 아두이노는 다양한 센서나 모터, 벨트와 같은 부품이 연결 가능하고 입출력, 중앙처리장치가 포함되어 있기 때문에 목적에 가장 알맞습니다. 일반적으로 컨베이어 벨트를 제어하려면 컨베이어 벨트를 구동하는 모터를 아두이노에 연결해야 합니다. DC모터인 경우, 아두이노에 직접 연결을 통해 제어가 가능하지만 우리가 구입한 컨베이어 벨트는 AC모터를 사용하고 있기 때문에 직접 연결을 통한 제어가 불가능하다고 여겼습니다. 따라서 컨베이어 벨트를 조작하는 별도의 인버터를 아두이노에 연결하여 벨트를 조작하는 방법을 이용하게 되었습니다.<br>
<center><img src=https://i.imgur.com/l0cczis.png><br>컨베이어벨트</center>
<br>
아래 AC 인버터 모식도에서 확인할 수 있듯 스위치를 on하면 인버터가 작동하고, 스위치를 off하면 인버터 작동이 멈추는 가장 기본적인 연결입니다. 스위치는 현재 릴레이로써 이를 통하여 컨베이어 벨트를 작동 혹은 중지를 할 것입니다. 아래 인버터 사용 매뉴얼을 통해 인버터의 작동 모드에는 다이얼 조작 모드와 외부 단자 조작 모드 2가지가 있는데, 인버터의 여러 가지 세팅 값 중 79번 세팅 값을 1에서 3으로 변경함으로서 외부 단자 조작 모드로 바꿀 수 있었습니다. 이로써 외부 단자 연결을 통해 컨베이어 벨트를 제어할 수 있게 되었고, 브레드보드를 통해 아두이노와 직접적 쇼트를 해본 결과 컨베이어 벨트가 움직이는 것을 확인했습니다. 회로의 on, off를 직접 단자를 뺐다, 꽂았다 하는 방식이었었기 때문에 신호를 통해 자동으로 컨베이어 벨트가 동작, 중지하는지 확인이 필요했습니다. 이 경우 직접 연결을 하는 경우임으로 감전에 주의해야 했습니다. 이후 스위치 역할인 릴레이를 아래와 같이 연결하여 인버터에 연결 하였으며, 릴레이를 아두이노에 연결하여 스위치를 on/off 시키는 것과 같이 릴레이를 on/off 시켜줌으로 컨베이어의 작동/정지가 가능하도록 하였습니다.
<center><img src=https://i.imgur.com/eqZQgod.png><br>AC 인버터 연결 모식도<br><br><img src=https://i.imgur.com/mqsbOFl.png width = 400><br>인버터 사용 매뉴얼</center>
또한 컨베이어 벨트의 작동 및 정지 여부에 있어 음성인식을 통하여 정지 혹은 재가동을 하도록 구성하였습니다. 이는 비상정지상황이나 기타 작동을 멈춰야 될 경우 음성인식을 통하여 컨베이어 벨트를 제어 할 수 있도록 하였습니다. 이는 단순히 외부 컴퓨터로 제어 하는 것보다 더욱 간단하고 손쉬운 방법이라 판단했고, 우리가 구상하는 스마트 팩토리에 알맞은 것이라 생각했습니다.
음성인식을 위하여 라즈베리파이와 블루투스로 Serial 통신을 통하여 음성인식의 데이터를 아두이노에 전달하여 스위치의 역할인 릴레이를 On/off 하게 함으로써 컨베이어 벨트의 제어가 가능하도록 구성하였습니다. 음성마이크가 라즈베리파이에 부착되어있다는 점을 고려하였을 때 USB선을 통한 아두이노-라즈베리파이간 유선 통신은 휴대성이 매우 떨어지며 제한적인 위치를 가지게 됩니다. 하지만 블루투스 통신을 통하여, 무선 통신의 특성상 더욱 편리하고 휴대성이 높은 특성을 가지며, 접근성 높은 스마트 팩토리를 구축하고자 하였습니다.
<center><img src=https://i.imgur.com/w4jXKAx.png><br>아두이노-릴레이-인버터 연결 회로도<br><br><img src=https://i.imgur.com/VeKGpY8.png width = 400><br>인버터와 릴레이 연결</center><br>

다음으로 음성인식의 데이터가 전달되고 그에 따라 전압이 주어지면 스위치로 작동하는 릴레이가 켜짐으로 인해 컨베이어 벨트가 작동하게 됩니다. 위의 코드는 시리얼 통신을 통하여 음성인식의 데이터가 전달됨과 동시에 적외선 센서가 캔을 인식하면, 불량품 검출을 위한 카메라 촬영을 위해 3초간 작동을 멈추고, 이후 다시 재가동 되게 되는 코드입니다. 또한 비상상황 발생시 음성인식을 통해 ‘정지’라는 신호를 보내게 되면 그에 대응하여 작동을 멈추게 되며, ‘시작’이라는 신호를 보내게 되면 다시 컨베이어가 재가동 되게 되는 메커니즘을 가지고 있습니다. 이를 통해 다양한 상황에서 컨베이어벨트를 제어할 수 있으며 블루투스의 무선 통신 이라는 특성을 통해 더욱 편리하게 제어를 가능하게 하였습니다.

릴레이를 통한 컨베이어 벨트 구동 코드

```c
pinMode(cds, INPUT);//센서값을 받아들인다
 pinMode(relay, OUTPUT);//센서 값이 받아 들임에 따라 컨베이어작동을 위한 output을 보낸다/
if(val == LOW){ //센서가 인식 되면
       digitalWrite(relay, LOW);//카메라 촬영을위해 컨베이어 작동 멈춘다
       delay(3000);//촬영 위한 딜레이 이후 다시 재가동 되게 된다.
 in_data = btSerial.read(); // 블루투스로 전달되는 음성인식의 데이터를 일거온다
         if(in_data == '0'){
           digitalWrite(relay,LOW);//만약 블루투스로 “정지”라는 신호를 보내면 멈춘다
         else if(in_data == '1'){ // 블루투스로 “시작”이라는 신호를 보내면 재가동 된다.
```
음성인식을 통해 컨베이어 벨트를 제어하는 파이썬 코드
```python
def callback1():
    ser.write(str.encode(‘0’))//정지 명령시 컨베이어벨트를 멈춤
def callback2():
    ser.write(str.encode(‘1’))//시작 명령시 컨베이어 벨트를 작동,
```
#### 2) 적외선 센서 연결
적외선 센서는 제품이 컨베이어 벨트 위를 지나갈 때, 제품의 위치를 확인하고 공정의 다음 작업을 진행을 위해 사용됩니다. 우리 공정 모델에서 사용되는 적외선 센서는 총 3개입니다.
- 첫 번째, 카메라 실행용 센서 : 제품이 불량품 검출용 카메라에 도달했는지를 확인하여, 적외선 센서가 감지되면 카메라의 라즈베리 파이에 신호를 보냅니다.
- 두 번째, 컨베이어 벨트 제어용 센서 : 카메라 실행용 센서와 부착되는 위치는 동일하지만, 불량품 검출용 카메라의 촬영을 위해 잠깐 멈추기 위한 센서로, 센서가 인식하면 3초간 멈춘 후 다시 재가동 됩니다.
- 세 번째, 서보모터 제어용 센서 : 불량품 감식이 완료된 제품이 분류되기 위해 서보모터를 지나갈 때, 제품이 서보모터에 도달했는지 여부를 확인하여, 불량품인 경우 분류를 하기 위해 존재하는 센서입니다.
##### ① 카메라 실행용 센서

## Demo

## Review
- 본 프로젝트에서 진행한 연구 결과, 저렴한 센서 및 라즈베리파이 & 아두이노를 통해 충분히 스마트 팩토리 컨셉의 시스템을 구축할 수 있었습니다. 이번 연구에서 이용한 비전과 보이스 인식을 통해서 사람과 기계, 기계와 기계 통신방식에 대해서 배웠고, 서로 연결되어 반응하는 지능형 공장 시스템의 데모를 구축해봄으로써, 중소기업 맞춤형 솔루션을 제안할 수 있는 결론을 도출할 수 있었습니다.
- 대상 공장에 다른 공정에 대한 확장이나 다른 형태의 제조공장에 대한 구축을 위해서는 모듈형식의 시스템 구축이 필요하고, 여러 IoT 디바이스들을 연결하고 관리할 수 있는 IoT 플랫폼을 통해서 더욱 고도화된 모니터링과 데이터 관리 및 불량에 대해 유지보전까지 할 수 있는 통합 시스템을 추가연구로써 진행이 필요합니다.
