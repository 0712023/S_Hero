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
- Servo Motor - DC Motor
- Conveyer Belt - AC Motor
- ReSpeaker 4-Mic Array for Raspberry Pi
### Software
- Node-RED
- Arduino IDE
- MySQL
- phpMyAdmin
- Mosquitto
## Big Picture
- 가장 먼저 컨베이어 벨트 제어를 위해 음성인식의 결과값을 서버를 통하여 아두이노로 전송되며, 이 결과로 음성인식을 통한 컨베이어 벨트가 제어되도록 하였습니다. 또한 라즈베리파이 간 mqtt 통신을 통하여 음성인식의 데이터, 불량품 검출의 결과 데이터를 전송시켜 컨베이어 벨트 제어 및 서보모터의 불량품 검출 분류를 가능하게 하도록 하였습니다. 서버를 구축함으로 인해 스마트 팩토리의 시스템처럼 가동하여 모든 공정을 제어할 수 있도록 하였습니다.
- 아래의 System Architecture에서 라즈베리파이 엣지 #1에서 음성인식을 통한 제어 명령을 전달하게 되면, 음성인식 후 제어 명령을 블루투스를 통해 전달하게 됩니다. 이 결과 컨베이어 벨트가 제어되며, 또한 라즈베리파이 디바이스#2에서 불량품 검출의 결괏값을 서버를 통해 디바이스#3으로 전송하고 그 결괏값에 따라 서보모터가 불량품을 분리해 내게 됩니다. 이러한 라즈베리파이 간의 mqtt는 와이파이를 통해서 통신하게 됩니다.
<p align=center><img src=https://i.imgur.com/hWJth4y.png></p><br>

## Project Details
### 1. 하드웨어 구축
컨베이어 벨트 구동을 위한 릴레이작동, 카메라실행 및 릴레이작동 및 정지를 위한 적외선 센서, 불량품 검출을 위한 서보모터 작동을 위해 아두이노를 사용하였고 이의 작동을위해 IDLE를  사용하였습니다. 이후 통신을 위해 라즈베리파이와 UART(Universal asynchronous receiver/transmitter)연결을 통해 Serial 통신으로 데이터를 송수신하도록 하였습니다.
#### 1) 컨베이어 벨트
음성명령이 내려졌을 때, 설비의 작동이 시작되기 위해서는 컨베이어 벨트의 제어가 필요합니다. 이때 컨베이어 벨트를 제어하기 위해 아두이노를 사용하기로 결정했습니다. 아두이노는 다양한 센서나 모터, 벨트와 같은 부품이 연결 가능하고 입출력, 중앙처리장치가 포함되어 있기 때문에 목적에 가장 알맞습니다. 일반적으로 컨베이어 벨트를 제어하려면 컨베이어 벨트를 구동하는 모터를 아두이노에 연결해야 합니다. DC모터인 경우, 아두이노에 직접 연결을 통해 제어가 가능하지만 우리가 구입한 컨베이어 벨트는 AC모터를 사용하고 있기 때문에 직접 연결을 통한 제어가 불가능하다고 여겼습니다. 따라서 컨베이어 벨트를 조작하는 별도의 인버터를 아두이노에 연결하여 벨트를 조작하는 방법을 이용하게 되었습니다.<br>
<p align=center><img src=https://i.imgur.com/l0cczis.png><br>컨베이어벨트</p>
<br>
아래 AC 인버터 모식도에서 확인할 수 있듯 스위치를 on하면 인버터가 작동하고, 스위치를 off하면 인버터 작동이 멈추는 가장 기본적인 연결입니다. 스위치는 현재 릴레이로써 이를 통하여 컨베이어 벨트를 작동 혹은 중지를 할 것입니다. 아래 인버터 사용 매뉴얼을 통해 인버터의 작동 모드에는 다이얼 조작 모드와 외부 단자 조작 모드 2가지가 있는데, 인버터의 여러 가지 세팅 값 중 79번 세팅 값을 1에서 3으로 변경함으로서 외부 단자 조작 모드로 바꿀 수 있었습니다. 이로써 외부 단자 연결을 통해 컨베이어 벨트를 제어할 수 있게 되었고, 브레드보드를 통해 아두이노와 직접적 쇼트를 해본 결과 컨베이어 벨트가 움직이는 것을 확인했습니다. 회로의 on, off를 직접 단자를 뺐다, 꽂았다 하는 방식이었었기 때문에 신호를 통해 자동으로 컨베이어 벨트가 동작, 중지하는지 확인이 필요했습니다. 이 경우 직접 연결을 하는 경우임으로 감전에 주의해야 했습니다. 이후 스위치 역할인 릴레이를 아래와 같이 연결하여 인버터에 연결 하였으며, 릴레이를 아두이노에 연결하여 스위치를 on/off 시키는 것과 같이 릴레이를 on/off 시켜줌으로 컨베이어의 작동/정지가 가능하도록 하였습니다.<br>
<p align=center>
<img src=https://i.imgur.com/eqZQgod.png><br>AC 인버터 연결 모식도<br><br><img src=https://i.imgur.com/mqsbOFl.png width = 400><br>인버터 사용 매뉴얼</p><br>
또한 컨베이어 벨트의 작동 및 정지 여부에 있어 음성인식을 통하여 정지 혹은 재가동을 하도록 구성하였습니다. 이는 비상정지상황이나 기타 작동을 멈춰야 될 경우 음성인식을 통하여 컨베이어 벨트를 제어 할 수 있도록 하였습니다. 이는 단순히 외부 컴퓨터로 제어 하는 것보다 더욱 간단하고 손쉬운 방법이라 판단했고, 우리가 구상하는 스마트 팩토리에 알맞은 것이라 생각했습니다.
음성인식을 위하여 라즈베리파이와 블루투스로 Serial 통신을 통하여 음성인식의 데이터를 아두이노에 전달하여 스위치의 역할인 릴레이를 On/off 하게 함으로써 컨베이어 벨트의 제어가 가능하도록 구성하였습니다. 음성마이크가 라즈베리파이에 부착되어있다는 점을 고려하였을 때 USB선을 통한 아두이노-라즈베리파이간 유선 통신은 휴대성이 매우 떨어지며 제한적인 위치를 가지게 됩니다. 하지만 블루투스 통신을 통하여, 무선 통신의 특성상 더욱 편리하고 휴대성이 높은 특성을 가지며, 접근성 높은 스마트 팩토리를 구축하고자 하였습니다.<br>
<p align=center><img src=https://i.imgur.com/w4jXKAx.png><br>아두이노-릴레이-인버터 연결 회로도<br><br><img src=https://i.imgur.com/VeKGpY8.png width = 400><br>인버터와 릴레이 연결</p><br>
다음으로 음성인식의 데이터가 전달되고 그에 따라 전압이 주어지면 스위치로 작동하는 릴레이가 켜짐으로 인해 컨베이어 벨트가 작동하게 됩니다. 위의 코드는 시리얼 통신을 통하여 음성인식의 데이터가 전달됨과 동시에 적외선 센서가 캔을 인식하면, 불량품 검출을 위한 카메라 촬영을 위해 3초간 작동을 멈추고, 이후 다시 재가동 되게 되는 코드입니다. 또한 비상상황 발생시 음성인식을 통해 ‘정지’라는 신호를 보내게 되면 그에 대응하여 작동을 멈추게 되며, ‘시작’이라는 신호를 보내게 되면 다시 컨베이어가 재가동 되게 되는 메커니즘을 가지고 있습니다. 이를 통해 다양한 상황에서 컨베이어벨트를 제어할 수 있으며 블루투스의 무선 통신 이라는 특성을 통해 더욱 편리하게 제어를 가능하게 하였습니다.<br><br>
*릴레이를 통한 컨베이어 벨트 구동*

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
*음성인식을 통한 컨베이어 벨트 제어*
```python
def callback1():
    ser.write(str.encode(‘0’))//정지 명령시 컨베이어벨트를 멈춤
def callback2():
    ser.write(str.encode(‘1’))//시작 명령시 컨베이어 벨트를 작동,
```
#### 2) 적외선 센서
적외선 센서는 제품이 컨베이어 벨트 위를 지나갈 때, 제품의 위치를 확인하고 공정의 다음 작업을 진행을 위해 사용됩니다. 우리 공정 모델에서 사용되는 적외선 센서는 총 3개입니다.
- 첫 번째, 카메라 실행용 센서 : 제품이 불량품 검출용 카메라에 도달했는지를 확인하여, 적외선 센서가 감지되면 카메라의 라즈베리 파이에 신호를 보냅니다.
- 두 번째, 컨베이어 벨트 제어용 센서 : 카메라 실행용 센서와 부착되는 위치는 동일하지만, 불량품 검출용 카메라의 촬영을 위해 잠깐 멈추기 위한 센서로, 센서가 인식하면 3초간 멈춘 후 다시 재가동 됩니다.
- 세 번째, 서보모터 제어용 센서 : 불량품 감식이 완료된 제품이 분류되기 위해 서보모터를 지나갈 때, 제품이 서보모터에 도달했는지 여부를 확인하여, 불량품인 경우 분류를 하기 위해 존재하는 센서입니다.
##### ① 카메라 실행용 센서
아래 코드를 통해 제품이 적외선 센서를 통과하게 되면, 카메라를 실행하는 라즈베리 파이에 신호가 가게 되어 불량품 검출 시스템이 실행됩니다. 불량품 검출 과정을 위해 제품이 센서를 통과한 그 즉시, 컨베이어 벨트 또한 작동을 3초간 멈추고 다시 작동합니다. 이 아두이노-라즈베리간 UART 통신을 위해서 아두이노에 firmata라는 라이브러리를 업로드하여 이후 라즈베리의 파이썬 환경을 통해 센서를 인식하도록 하였습니다.<br>
*카메라를 실행하는 라즈베리 파이와의 통신*
```python
board = Arduino('/dev/ttyUSB0')//아두이노와 연결
pin9_sensor = board.get_pin('d:9:i')//디지털 핀 9번에 센서를 연결하여
if pin_code.read() == False://센서가 캔을 인식하는 경우
 camera.capture(image, 'bgr')//카메라를 캡쳐하게 된다
```
##### ② 컨베이어 벨트 제어용 센서
제품이 카메라 실행용 센서를 통과해 불량품 검출을 촬영하는 센서와는 별개로 카메라 촬영을 위해 컨베이어벨트를 멈추게 하는 센서입니다. 캔이 센서에 인식되면, 불량품검출을 위한 사진촬영을 위해 약 3초간 멈췄다가 재가동 되게 합니다.
##### ③ 서보모터 제어용 센서
서보모터를 제어하기 위해서 센서 인식 또한 필요합니다. 이 경우 센서는 아두이노에 연결되는 것이 아닌 라즈베리파이에 직접 연결했습니다. 우리가 사용하는 적외선센서의 경우 디지털 신호를 통해 0, 1 값을 주고 받기에 라즈베리파이에 직접 연결이 가능했습니다. 따라서 센서가 인식됨에 따라 아두이노에 신호를 주어 서보모터를 가동하도록 했습니다. 이 결과로 불량품의 검출이 가능하게 되었습니다.<br><br>
*서보모터 제어용 센서 인식*
```python
if GPIO.input(11) == 0://센서가 인식되었을 때
   if data_saved[n] == 2:
               ser.write('2'.encode())
//불량품 검출 데이터가 불량품이라 인식하였을 때 서보모터를 회전시키기위한 통신을 한다.
```
#### 3) 서보 모터
서보모터의 작동을 위해 라즈베리파이-아두이노간 연결을 통해, 불량품의 검출결과 데이터와, 센서의 인식 데이터를 받아들이게 됩니다. 라즈베리파이를 통해 들어온 불량품 판단 여부 데이터는 list에 쌓이게 되고, 센서가 인식됨에 따라(캔이 서보모터 앞을 지나감) list에 저장되어진 불량품 여부의 데이터를 차례로 불러들여 불량품 여부에 따라 검출하게 됩니다.<br><br>
*서보모터 제어*
```python
if (in_data == '2'){
       for (pos = 0; pos <= 180; pos += 5) {
          EduServo.write(pos);
          delay(10);}
//이는 불량품 검출의 데이터가 “불량품이라고 인식하였을 때 서보모터를 회전하여 불량품을 검출하는 작업을 한다.
```
각각의 구성되어진 하드웨어는 라즈베리간 mqtt, 아두이노와 라즈베리파이의 UART 시리얼 통신, 아두이노와 라즈베리파이간의 블루투스 통신을 통하여 하나의 메커니즘으로 작동합니다. 블루투스 통신으로의 음성인식을 통해 제어되는 릴레이와 컨베이어 벨트에서 센서가 인식되면 카메라 작동을 위해서 3초간 컨베이어 벨트가 멈추고 불량품 검출을 위한 사진촬영 후 다시 재작동합니다. 이후 적외선센서가 인식 되었을 때 불량품의 판단 여부에 따라 서보모터가 작동하게 되며 불량품을 성공적으로 검출하게 되는 하나의 메커니즘을 형성하게 됩니다.
### 2. 이미지 처리
라즈베리파이3와 파이카메라 모듈을 결합하여 라즈베리파이3에서 불량품 검출에 필요한 사진을 찍을 수 있습니다. 파이카메라를 사용하기 위해서 따로 설치해야 하는 모듈은 없으며, 라즈베리파이3 보드 위의 코드에 결합하기만 하면 됩니다. 불량품 검출의 최종 목적이 원 형태의 인식 여부이기 때문에, 특정 사진에서 원의 형태를 인식하는 가장 좋은 방법은 파이썬3 환경에서 ‘OpenCV’ 모듈을 활용하는 것입니다. OpenCV 모듈은 라즈베리파이3의 카메라를 활용하여 사진을 찍거나, 저장, 불러오기, 보여주기, 원 그리기, 테두리 그리기, 등 다양한 분야에서 활용도가 높은 모듈입니다. 여기서 우리 팀이 해결하고자 하는 과제에 필요한 부분은, ‘사진에서 원 인식’, ‘사진에서 원 그리기’입니다. ‘사진에서 원 인식’은 메소드 ‘HoughCircles’를, ‘사진에서 원 그리기’는 메소드 ‘circle’을 사용하였습니다. 파이카메라를 통해 찍은 제품 사진에서 불량품인지, 정상제품인지 판단하는 기준은 프로젝트 진행에 있어서 최적의 방안을 찾기 위해 다음 세 가지 방법을 제시했습니다.
#### 1) 검출된 원과 실제 제품 테두리의 넓이 차이 비교를 통한 오차율 계산<br>

```python
import cv2 as cv
import numpy as np

img1 = cv.imread('example.jpg', 0)
img1 = cv.medianBlur(img1,5)
img2 = img1.copy

circles = cv.HoughCircles(img1, cv.HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30)
if circles is not None:
    if len(circles.shape) < 3:
        print('circles not detected')
    else:
        a, b, c = circles.shape
    for j in range(b):
        cv.circle(img3, (circles[0][j][0], circles[0][j][1]), circles[0][j][2], (0, 0, 255), 3, cv.LINE_AA)
print('expected area = ', 3.14159*circles[0][j][2]**2)

ret, th = cv.threshold(img1, 150, 255, cv.THRESH_BINARY)
image, contours, hierarchy = cv.findContours(th, 1, 2)
img3 = cv.drawContours(img1, contours, -1 (0, 255, 0), 3)
area = cv.contourArea(contours[0])
print('real area = ', area)
```
우선 ‘example.jpg’라는 사진에서 Houghcircle 메소드를 통해 검출된 원의 반지름을 구하여, 에 대입하여 원의 넓이를 구합니다. 또, 사진을 threshold 메소드를 통해 원으로 보이는 부분의 실제 모양을 그대로 따옵니다. Threshold 메소드는 사진에서 rgb값 중 지정된 값 이상의 색은 전부 검은색, 그 외는 모두 흰색으로 처리하게 해줍니다. 즉, 제품의 윗면 전체의 색과 컨베이어 벨트의 색과 대조하여, 제품의 윗면만 검은색으로 표시되게 한 후, 검은색으로 표시된 부분의 넓이를 ‘contourArea’ 메소드를 통해 구합니다. 각각 구해진 이론값과 실제 넓이를 비교하여, 이 오차율이 팀에서 정한 특정 % 이상이 된 제품을 불량품으로 규정하는 방법입니다.
아래 사진에서 하나의 원에 대해 HoughCircle, contourArea 두 가지 방법으로 원의 넓이를 계산하면, 두 원의 오차는 약 17494.66 이고, 이는 약 6.7%의 오차가 발생했습니다.
<p align=center><img src=https://i.imgur.com/tNz3YGW.png><br>실제 원 검출 사진<br><img src=https://i.imgur.com/PRTj5KN.png><br>오차율 계산 영역</p>
하지만 이 방법은 Houghcircle, contourArea 두 메소드 각각 카메라의 흔들림, 사진의 낮은 화질, 등에서 오차가 발생할 가능성이 있고, 각각의 오차가 불량품인 제품을 정상제품이라고 오판할 가능성이 다소 있다고 판단하여 사용하지 않기로 결정했습니다.

#### 2) 10장의 사진을 찍어 각 사진에 대해 원을 검출, 최종 원 검출율이 90% 이상일 경우 정상품
```python
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2 as cv
import numpy as np
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
n = 0
m = 0
l = 0
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    if signal == 1:
        n = n + 1
        if n == 1:
            l = l + 1
            name = print('product' + l)
            cv.imwrite(name, img)
        else:
            break
        circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 60, 20, 30)
        if circles is not None:
            if len(circles.shape) == 3:
                a, b, c = circles.shape
                m = m + 1
            else:
                b = 0
            for i in range(b):
                cv.circle(img, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
            cv.imshow("tracking", img)
            key = cv.waitKey(1)
           rawCapture.truncate(0)
            if key == 27:
                break
        cv.destroyAllWindows()
    else:
        if m / n > 0.9:
            n = 1
        else:
            k = 0
        n = 0
        continue
```
우선 파이카메라를 통해 초당 32번의 사진을 찍어 사진마다 Houghcircle 메소드를 통해 원을 검출하고 이를 스크린을 통해 보여줍니다. 이러한 과정을 통해 스크린에서는 마치 실시간으로 원을 트래킹하는 스트리밍을 볼 수 있다는 장점이 있습니다. 시각적인 효과가 뛰어나기 때문에 오차율 계산이 적합하다면 원 인식 코드로 사용될 예정이었던 코드였습니다.<br>
파이카메라 모듈에도 실시간 비디오 스트리밍을 할 방법이 있지만, 그 방법은 실제로 라즈베리파이3 환경에서 실행하기에는 성능이 충분하지 않아, 과부하가 걸릴 가능성이 컸고, 무엇보다 오차율 계산에 있어서 사진을 통해 스트리밍하는 방법에 비해 일관성이 떨어지기 때문에 사용하지 않았습니다.<br>
작업 환경에서 적외선 센서로부터 제품이 카메라 앞에 도달하였다는 정보가 들어온 직후의 10개의 사진(프레임)을 검사하여, 10장의 사진 중 9장 이상의 사진에서 원이 검출된 제품을 정상제품의 기준으로 정하였습니다.
<p align=center><img src=https://i.imgur.com/i5ZHIpC.png><br>이동중에도 연속적으로 원 검출</p>

하지만 이 방법에서 ‘10장의 사진 중 9장’이라는 기준에서 9장이 그리 직관적이지 않고, 수많은 제품을 판단하는 과정에서 적절하지 못한 불량품 판단이 일어날 가능성이 큽니다. 또한, 컨베이어 벨트 위에서 10장의 사진을 찍는 동안, 제품이 이동하여 카메라 바로 밑이 아닌 약간 비스듬한 위치에서 찍힌 사진 또한 오차율 계산에 포함되게 되는데 이 때, 정상적인 제품임에도 타원형으로 사진이 찍힐 수 있어, 원 검출에 신빙성이 떨어지게 됩니다. 이러한 이유로 이 방법 또한 사용하지 않기로 결정했습니다.

#### 3) Hough circle 매소드 내 여러 변수들을 통한 원 인식
```python
import picamera
import numpy as np
import cv2 as cv
from pyfirmata import Arduino, util
import time
import paho.mqtt.client as mqtt
def connect_connect(client, userdata, flags, rc):
    print("Connected with voice ip_/start" + str(rc))
    client.subscribe("/control")
def control_message(client, userdata, msg):
    global sign
    sign = msg.payload
    if sign == b'111':
        print("initiate detected_b\n")
    elif sign == '111':
        print("initiate detected_0\n")
    elif sign == b'000' :
        print("stop detected_b\n")
    elif sign == '000' :
        print("stop detected_0\n")
controlsub = mqtt.Client()
controlsub.connect("203.252.47.59", 1883)
controlsub.on_connect = control_connect
controlsub.on_message = control_message
servopub = mqtt.Client()
servopub.connect("localhost", 1883)
controlpub = mqtt.Client()
controlpub.connect("localhost",1883)
board = Arduino('/dev/ttyUSB0')
pin9_sensor = board.get_pin('d:9:i')
it = util.Iterator(board)
it.start()
pin9_sensor.enable_reporting
pin_code = pin9_sensor
sign = b'111'
if sign == '111':
    sign = b'111'
n = 0
p = 0
while True:
    controlpub.loop_start()
    controlsub.loop_start()
    servopub.loop_start()
    if sign == b'111':
        controlpub.publish("/conveyorstate", "111111")
        if pin_code.read() == False:
            n = n + 1
            if n == 1:
                p = p + 1
                with picamera.PiCamera() as camera:
                    camera.resolution = (320, 240)
                    camera.framerate = 24
                    image = np.empty((240, 320, 3), dtype=np.uint8)
                    camera.capture(image, 'bgr')
                    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                        circles = cv.HoughCircles(image_gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 60, 20, 30)
                    if circles is not None:
                        if len(circles.shape) == 3:
                            a, b, c = circles.shape
                            group = "1"
                            servopub.publish("/servo", "22")
                        else:
                            b = 0
                            group = "0"
                            servopub.publish("/servo", "33")
                        for i in range(b):
                            cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
                p1 = str(p)
                log = open('/home/pi/coding/product_result/results.txt', "a")
                log.write('product' + p1 + ' is ' + group + '\n')
                log.close()
                name = p1 + '.jpg'
                cv.imwrite(name, '/home/pi/coding/product_result', image)
                cv.destroyAllWindows()
        else:
            n = 0
    controlpub.publish("/conveyorstate", "000000")
    time.sleep(1)
    controlpub.loop_stop()
    controlsub.loop_stop()
    servopub.loop_stop()
```
위 코드는 원래 단순히 하나의 제품 사진에 대해 HoughCircle 메소드를 통해 원이 검출되었는가, 되지 않았는가를 판단하여 정상제품, 불량품으로 각각 분류합니다. Houghcircle 메소드에 적용되는 변수들은 순서대로, (image, method, dp, minDist[, circles[, param1[, param2[,, minRadius[, maxRadius]]]]])로 나타내어지고 각각의 변수의 의미는 다음과 같습니다.
- image : 8-bit single-channel 흑백 이미지.
- method : 검출 방법. 현재는 HOUGH_GRADIENT가 있음.
- dp : dp=1이면 Input Image와 동일한 해상도.
- minDist : 검출한 원의 중심과의 최소거리. 값이 작으면 원이 아닌 것들도 검출이 되고, 너무 크면 원을 놓칠 수 있음.
- param1 : 내부적으로 사용하는 canny edge 검출기에 전달되는 Paramter
- param2 : 이 값이 작을 수록 오류가 높아짐. 크면 검출률이 낮아짐.
- minRadius : 원의 최소 반지름.
- maxRadius : 원의 최대 반지름.<br>

이들 중 정상제품임을 판단할 중요한 변수는 param2, minRadius, maxRadius 세 가지입니다. 이 세 가지 변수들은 실제로 사진을 다수 찍어보면서 적절한 값을 찾아내는 방법을 통해 각각 60, 20, 30으로 설정하는 것이 가장 정확하다는 것을 알 수 있었습니다. 각각의 단위는 pixel이며, 해당 값은 파이카메라를 통해 찍는 사진의 크기(320x240)과 이를 통해 실제로 보이는 제품의 크기를 토대로 계산한 값입니다.<br>
처리된 제품의 원 인식 결과에 해당하는 제품 사진과, 제품의 로그는 검출 즉시 라즈베리파이3 내부 경로에 저장되고, 곧바로 서버에 업로드되어, 책임자 등이 자유롭게 열람할 수 있습니다.<br>
<p align=center><img src=https://i.imgur.com/iCAwgmZ.png></p>
원을 검출하는 코드는 루프를 통해 무한히 돌아갑니다. 매 루프마다 제품이 카메라 앞에 도달하였는지에 대해서 아두이노 보드의 디지털 적외선 센서를 통해 정보를 받습니다. 아두이노 보드와 라즈베리파이3는 유선상의 시리얼 통신을 통해 정보를 전달합니다. 카메라 앞에 제품이 도달하였다는 신호를 받기 전까지 원 인식 코드는 실행되지 않고, 루프만 계속 돕니다. 하지만, 제품이 카메라 앞에 도달하였다는 신호를 받으면 원 인식 코드를 단 1회 실행하게 되고 다시 루프를 돕니다.<br>
원 인식 코드를 실행하는 루프는 책임 사용자가 원하는 때에 실행할 수 있고, 또 원하는 때에 중지할 수 있어야 합니다. 그러한 on/off 스위치 역할을 하는 것이 바로 뒤에서 설명할 음성인식입니다.

### 3. 음성인식
음성인식은 원 인식 코드가 작동하고 있는 라즈베리파이3가 아닌 또 다른 라즈베리파이3에서 실행되고 있는데, 여기서 on에 해당하는 명령을 받으면 멈춰있는 루프를 작동시키게 하고, off에 해당하는 명령을 받으면, 동작하고 있는 루프를 무조건 정지시킵니다. 이 두 라즈베리파이3 사이의 통신은 mqtt를 통해서 작동합니다. 또한, 라즈베리파이3 내부에 저장된 제품 로그는 곧바로 서보모터를 돌리는 데 필요한 정보를 제공하기 위해 서보모터 라즈베리파이3로 mqtt통신을 통해 전달하게 됩니다.<br>
<p align=center><img src=https://i.imgur.com/nlWRLlm.png><br>ReSpeaker 4-Mic Array for Raspberry Pi</p>
ReSpeaker 4-Mic Array for Raspberry Pi는 4개의 마이크가 적용된 보드로서, 라즈베리파이3에 가장 최적화된 스피커입니다. 매우 높은 감도의 음성 탐지가 가능하여, jarvisfactory 팀의 음성인식에 필요한 장비입니다. 파이카메라와 달리 초기 설정을 해주어야 하는데, 필요한 모듈을 내려받아 간단하게 사용할 수 있습니다.<br>
음성인식을 하는 방법에는 크게 두 가지가 있는데, 구글 어시스턴트(Google assistant)와 스노우보이(Snowboy)가 그것입니다.<br>

- 구글 어시스턴트는 음성인식과, 인식된 음성을 문자로 변환하여, 이를 구글 어시스턴트 서버에 보내 적절한 대답을 해 주는 ‘비서’역할을 합니다. 설치는 actions on google을 통해 프로파일을 등록 후 라즈베리파이3와 같은 기기에서 사용할 수 있습니다. 구글 어시스턴트는 인공지능으로써 필요한 정보들을 음성 명령을 통해 수집하는 데에 큰 의미가 있으므로, 음성 명령을 내리면 피드백을 주는 단순명료한 작업에는 적절하지 못하기 때문에 사용하지 않았습니다.
- 스노우보이는 음성 명령을 내리면 피드백을 주는 단순명료한 작업에 매우 적절한 모듈입니다. 스노우보이는 Kitt.ai에서 개발한 무료 라이센스 프로그램으로, 개인 사용자가 음성 녹음을 통해 특정 단어 패턴에 대한 프로파일을 생성하면, 라즈베리파이3와 같은 개인 기기에서 다양한 환경(파이썬2, 파이썬3, C, C+, 등등)에서 프로파일에 해당하는 단어가 인식되면 그에 대한 콜백이 작동합니다.
```python
import snowboydecoder
import sys
import signal
import paho.mqtt.client as mqtt
import serial
import time
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
mqtt = mqtt.Client()
mqtt.connect("localhost", 1883)
interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
def interrupt_callback():
    global interrupted
    return interrupted
models = sys.argv[1:]
signal.signal(signal.SIGINT, signal_handler)
sensitivity = [0.5]
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
def callback1():
    mqtt.publish("/control", "111")
    ser.write(str.encode('1'))
def callback2():
    mqtt.publish("/control", "000")
    ser.write(str.encode('0'))
mqtt.loop(2)
callbacks = [callback1, callback2]
detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)
detector.terminate()
```
이 프로젝트에서는 전체 동작 과정을 ‘실행’하는 것과, ‘중지’하는 것에 우선 주안점을 두고, 각각의 명령어를 ‘시작해’와 ‘중지해’로 녹음하여 프로파일을 생성하였습니다. 또, 그 단어가 인식되었을 때 실행에 해당하는 신호와 중지에 해당하는 신호를 시리얼 통신으로는 컨베이어 벨트와 연결된 아두이노 보드에, mqtt통신으로는 원 인식 라즈베리파이3에 전달되도록 합니다. 그렇게 함으로써 처음 시작 명령을 받게 되면 컨베이어 벨트와 원 인식 코드가 작동하게 되고, 도중에 중지해야 할 상황에서 중지 명령을 받게 되면 컨베이어 벨트와 원 인식 코드가 작동을 중지하게 됩니다.
### 4. 서버
#### 1) 서버 구축
서버에서의 기본적인 목표는 스피커와 카메라, 컨베이어 벨트간의 통신을 이어주는 역할을 하는 것입니다. 여기에 이 통신에서 이루어진 데이터를 사용자에게 시각화하는 역할이 더해집니다. 이 역할을 통해서 사용자가 이 시스템에 대한 접근성을 가질 수 있다. 이를 바탕으로 시스템이 잘 작동되는지를 판단할 수 있습니다.<br>
공정 과정에서 축적되는 데이터들을 저장할 데이터베이스를 ‘MySQL’이라는 도구와 php라는 ‘Hypertext preprocessor’라는 언어를 통해서 구축했습니다. 여기에 사용자 인터페이스가 좀 더 좋은 ‘phpMyAdmin’이라는 무료 소프트웨어를 통해서 서버와 연결했습니다. 이렇게 데이터베이스를 사용하면 데이터가 서버에서 정적으로 묶여있는 상태가 아니라 데이터베이스에서 동적으로 계속 축적 또는 변형되기 때문에 데이터 수정이 간단합니다.<br>
먼저, 아래 사진들과 같이 데이터베이스를 통해 텍스트를 처리할 수 있었습니다. 데이터는 단순한 한 줄 형식에 긴 줄 텍스트가 아니라 표로 정리하여 나타내집니다. 이는 ‘MySQL’에서 query문을 통해서 테이블을 만들 수 있기 때문인데 이 만들어진 표는 ‘phpMyAdmin’에 시각화되어 나타나고, 이 테이블을 통해서 서버로 가져오게 됩니다.
<p align=center><img src=https://i.imgur.com/7ra23Gj.png><br>phpMyAdimin<br><img src=https://i.imgur.com/Xn0biuJ.png><br>데이터베이스를 통한 텍스트 처리</p>
다음으로 사진 정보를 서버에 저장해야 합니다. 사진을 http 프로토콜을 통한 URL에 먼저 올린 후, 서버에서는 라즈베리파이로 찍을 물건을 지정하는 텍스트를 하이퍼텍스트링크형식으로 만듭니다. 이렇게 되면 지정된 텍스트를 클릭했을 때, 지정된 URL 주소로 접속하게 되는데 이때 저장된 사진이 보이는 구조입니다.
<p align=center><img src=https://i.imgur.com/IrL7hjX.png><br>사진 처리 Node-RED flow<br><img src=https://i.imgur.com/GoMdtAF.png><br>사진 확인이 가능한 UI</p>

#### 2) I/O 포트 제어
전체적인 공정 진행 과정에 있어서 서버에 접근이 가능한 관리자 입장에서 모든 프로세스의 제어 권하는 가져야 한다고 생각했습니다. 그렇기 때문에 대부분의 통신 및 정보 전달을 메인 서버를 통해 이루어져야 하고, 각각의 신호는 무선으로 연결되어야 합니다.<br>
- Node-RED를 이용하여 서버_통신 부분을 단계별로 구축하였습니다. Node-RED(서버)에서 아두이노 I/O 포트를 제어했습니다. 아래 사진은 아두이노를 제어하는 플로우입니다. 1과 0의 신호 및 버튼으로 LED를 제어하고, 시간 루프로 서보모터를 동작시키도록 했습니다.
<p align=center><img src=https://i.imgur.com/daFzJDm.png><br>Node-RED를 활용한 I/O 포트 제어</p>

#### 3) MQTT 제어
- 서버에서 MQTT broker를 열고, Node-RED가 MQTT client 역할을 하여 통신하는 모습입니다. 차례대로 json 파일에 저장된 데이터를 읽어 데이터에 따라 디버깅하는 플로우, 외부 mqtt 브로커 (websocket) 통신 플로우, 내부 mqtt(nodered) 통신 플로우입니다.
<p align=center><img src=https://i.imgur.com/xhTfUXb.png></p>

이와 같은 플로우들로 nodered로 아두이노 포트를 쉽게 제어할 수 있는 것과, mqtt 통신이 가능하다는 것을 확인하였습니다.

-  라즈베리파이와 아두이노 보드에서 블루투스 / 와이파이 통신 포트 열었습니다. 두 가지 통신 방법 중, 하나의 와이파이 공유기 아래에 있을 시 통신이 편리하다는 점 때문에 와이파이 통신으로 결정하게 되었습니다. MQTT통신 방식으로 라즈베리파이에서 아두이노로 제어 신호를 보냈는데, 라즈베리파이가 MQTT broker, 노트북이 MQTT client로 설정하여 아두이노 제어를 시도하였습니다.<br>
- 이후 mqtt통신을 위해 mosquitto라는 오픈 서비스를 이용하였습니다. Mosquitto는 mqtt에 필요한 기본적인 요소를 모두 지원하며, 라즈베리파이에는 mqtt통신을 가능하게 하기 위해서 paho python client라는 mqtt 라이브러리를 사용하였습니다.
- 마지막으로 라즈베리 파이간의 통신 및 라즈베리파이와 아두이노의 통신을 처리했습니다.<p align=center><br>라즈베리파이_1 (MQTT server & client)<br>&#8597;<br>라즈베리파이_2 (MQTT client & server)<br>&#8597;<br>라즈베리 파이_3 (broker & server with servo motor)</p><br>구독하고 있는 라즈베리 파이에서는 같은 topic과 정해진 ip로 발행하고 있는 라즈베리파이의 신호를 읽을 수 있으며, 이를 이용해 라즈베리 파이에 구축된 서버에서 제어권을 갖게 했습니다.
<p align=center><img src=https://i.imgur.com/5hYV7Sk.png><br>cmd에서 mqtt를 구독/발행</p>

이후 cmd에서 라즈베리파이의 ip를 구독함으로써 이루던 통신을 python 코드로 진행 가능하도록 바꾸었습니다.

*mqtt 발행*
```python
import paho.mqtt.client as mqtt

mqtt = mqtt.Client("python_pub")                #create mqtt client object
mqtt.connect("localhost",1883)

mqtt.publish("/world", "111")
mqtt.publish("/world", "000")

mqtt.loop(2)        #timeout 2 sec
```

*mqtt 구독*
```python
import paho.mqtt.client as mqtt

#callback which is executed when get CONNTACK response from server
def on_connect(client, userdata, flags, rc):
    print("connected with result code "+str(rc))
    client.subscribe("/world") #subscribe "nodemcu"

#callback which is executed when get publish message from server
def on_message(client,userdata,msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()                      #create client object
client.on_connect = on_connect      #set callback
client.on_message = on_message #set callback
client.connect("localhos
```
#### 4) 시리얼 통신
Modbus Node-RED 노드를 활용하여 아두이노-서버-라즈베리파이간의 통신이 가능한 것을 확인할 수 있습니다. 따라서 라즈베리파이에서 인식한 명령이 아두이노의 시리얼 포트로 전송 가능하게 되었습니다.
<p align=center><img src=https://i.imgur.com/IL0vU2U.png><br>Node-RED를 통한 시리얼 통신</p>

## Demo
##### 1. alpha 버전 시스템 완성
[![](https://img.youtube.com/vi/tupZThvQLtQ/0.jpg)](https://www.youtube.com/watch?v=tupZThvQLtQ)
##### 1. beta 버전 시스템 완성
[![](https://img.youtube.com/vi/GobDD7CxsH4/0.jpg)](https://www.youtube.com/watch?v=GobDD7CxsH4)
##### 1. 서버를 통한 제품 사진 확인
[![](https://img.youtube.com/vi/T5GU1vwoyIE/0.jpg)](https://www.youtube.com/watch?v=T5GU1vwoyIE)
##### 1. 최종 발표회 시연
[![](https://img.youtube.com/vi/zX8AATmPfKY/0.jpg)](https://www.youtube.com/watch?v=zX8AATmPfKY)

## Research Prospects
중소기업들은 스마트팩토리 구축을 위해 정부의 스마트팩토리 관련 지원금에도 불구하고 대기업 중심의 최상급 서비스보다는 중소기업 맞춤형 스마트 팩토리가 필요하다고 생각합니다.<br>
본 프로젝트에서 진행한 연구 결과, 저렴한 센서 및 라즈베리파이 및 아두이노를 통해 충분히 스마트 팩토리 컨셉의 시스템을 구축 할 수 있었습니다. 이번 연구에서 이용한 비전과 보이스 인식을 통해서 사람과 기계, 기계와 기계 통신방식에 대해 이해한 내용을 바탕으로, 서로 연결되어 반응하는 지능형 공장 시스템의 데모를 구축해보았고, 중소기업 맞춤형 솔루션을 제안 할 수 있는 결론을 도출할 수 있었습니다.<br>
대상 공장에 다른 공정에 대한 확장이나 다른 형태의 제조공장에 대한 구축을 위해 모듈형식의 시스템 구축이 필요하고, 여러 IoT 디바이스들을 연결하고 관리할 수 있는 IoT 플랫폼을 통해서 더욱 고도화 된 모니터링과 데이터 관리 및 불량에 대한 예지보전까지 할 수 있는 통합 시스템을 추가연구로써 진행이 필요합니다.

## Review
- 본 프로젝트에서 진행한 연구 결과, 저렴한 센서 및 라즈베리파이, 아두이노를 통해 충분히 스마트 팩토리 컨셉의 시스템을 구축할 수 있었습니다. 이번 연구에서 이용한 비전과 보이스 인식을 통해서 사람과 기계, 기계와 기계 통신방식에 대해서 배웠고, 서로 연결되어 반응하는 지능형 공장 시스템의 데모를 구축해봄으로써, 중소기업 맞춤형 솔루션을 제안할 수 있는 결론을 도출할 수 있었습니다.
- 대상 공장에 다른 공정에 대한 확장이나 다른 형태의 제조공장에 대한 구축을 위해서는 모듈형식의 시스템 구축이 필요하고, 여러 IoT 디바이스들을 연결하고 관리할 수 있는 IoT 플랫폼을 통해서 더욱 고도화된 모니터링과 데이터 관리 및 불량에 대해 유지보전까지 할 수 있는 통합 시스템을 추가연구로써 진행이 필요합니다.
