import cv2
import numpy as np
from ultralytics import YOLO
import serial
import time
from picamera2 import Picamera2

# 1. YOLO 모델 로드
model = YOLO('best.pt')

# 2. ESP32 시리얼 설정
try:
    ser = serial.Serial('/dev/ttyAMA0', 115200, timeout=1)
    print("✅ ESP32 시리얼 연결 성공")
except Exception as e:
    print(f"⚠️ 시리얼 연결 실패: {e}")
    ser = None

# 3. Picamera2 설정 (라즈베리 파이 5 최적화)
picam2 = Picamera2()
# 여기서 포맷을 'BGR888'로 설정하면 OpenCV와 색상이 완벽히 일치합니다!
config = picam2.create_video_configuration(main={"format": "BGR888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

print("🚀 실시간 인식을 시작합니다. (종료: 'q')")

try:
    while True:
        # 카메라에서 프레임을 BGR 배열로 바로 가져오기
        frame = picam2.capture_array()
        
        # 탐지가 안 될 경우를 대비해 원본 프레임을 기본값으로 설정
        annotated_frame = frame.copy()

        # YOLO 추론 (얼굴 인식)
        results = model(frame, stream=True, conf=0.5, verbose=False)

        for r in results:
            # 바운딩 박스가 그려진 화면 생성
            annotated_frame = r.plot()
            
            for box in r.boxes:
                class_id = int(box.cls[0])
                name = model.names[class_id]
                
                # ESP32로 데이터 전송
                if ser:
                    ser.write(f"{name}\n".encode())
                    print(f"👤 인식 성공: {name}")

        # 실시간 화면 표시 (VNC 화면에서 확인 가능)
        cv2.imshow("SSAFY-GO AI DoorLock", annotated_frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"❌ 에러 발생: {e}")

finally:
    # 리소스 해제
    picam2.stop()
    cv2.destroyAllWindows()
    if ser:
        ser.close()
    print("👋 프로그램을 정상적으로 종료합니다.")
