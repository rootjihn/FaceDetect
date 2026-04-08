#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <SPI.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// --- SPI OLED 핀 설정 (성공했던 핀 그대로!) ---
#define OLED_MOSI  23 // DIN
#define OLED_CLK   18 // CLK
#define OLED_DC     2 // D/C
#define OLED_CS     5 // CS
#define OLED_RESET  4 // RES

// --- 시리얼 통신 핀 설정 ---
#define RXD2 27  // 라즈베리 파이 TX와 연결

// 'display' 객체 선언 (이게 없어서 아까 에러가 났던 겁니다!)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, OLED_MOSI, OLED_CLK, OLED_DC, OLED_RESET, OLED_CS);

void setup() {
  Serial.begin(115200);
  Serial2.begin(115200, SERIAL_8N1, RXD2, -1); 

  if(!display.begin(SSD1306_SWITCHCAPVCC)) {
    Serial.println(F("OLED 시작 실패!"));
    for(;;);
  }

  showWaitingScreen();
}

void loop() {
  if (Serial2.available()) {
    delay(100); 
    String name = Serial2.readStringUntil('\n');
    name.trim();

    if (name.length() > 0) {
      display.clearDisplay();
      display.setTextColor(SSD1306_WHITE);
      
      // 1. 맨 윗줄 (y=0)
      display.setTextSize(1);
      display.setCursor(0, 0);
      display.println(F(">>> ACCESS GRANTED <<<")); 

      // 2. 구분선 (y=12)
      display.drawFastHLine(0, 12, 128, SSD1306_WHITE);

      // 3. 안내 문구 (y=20)
      display.setTextSize(1);
      display.setCursor(0, 20);
      display.println(F("Identity Verified."));

      // 4. Welcome 문구 (y=32)
      display.setCursor(0, 32);
      display.print(F("Welcome, "));

      // 5. 이름 출력 (y=45) - 큼직하게!
      display.setTextSize(2); 
      display.setCursor(0, 45);
      display.println(name); // "박진원" 또는 "Jinwon" 출력
      
      display.display(); // [중요] 한 화면에 다 그리려면 맨 마지막에 딱 한 번!

      delay(3000); 
      showWaitingScreen();
    }
  }
}

// 대기 화면 함수 (이게 빠지면 안 돼요!)
void showWaitingScreen() {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println(F("AI DoorLock System"));
  
  display.drawFastHLine(0, 12, 128, SSD1306_WHITE);

  display.setTextSize(2);
  display.setCursor(0, 30);
  display.println(F("SCANNING.."));
  
  display.setTextSize(1);
  display.setCursor(0, 55);
  display.println(F("Ready for Recognition"));
  
  display.display();
}