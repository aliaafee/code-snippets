/*
 * Install these libraries
 * 
 * https://github.com/adafruit/Adafruit_SSD1306 (SSD1306 library)
 * https://github.com/adafruit/Adafruit-GFX-Library (GFX library)
 * 
 */

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define OLED_RESET 4

Adafruit_SSD1306 display(OLED_RESET);

int x = 0;
int y = 0;
int vx = 1;
int vy = 1;
int f_time;

void setup() {
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);

  display.clearDisplay();
  display.display();

  display.setTextSize(1);
  display.setTextColor(BLACK);
}

void loop() {
  int t = millis();
  
  display.clearDisplay();
  display.fillCircle(x, y, 6, WHITE);
  display.setCursor(x-5,y-3);
  display.setTextColor(BLACK);
  display.print(f_time);
  display.setTextColor(WHITE);
  display.println("This is a long sentance of text. That serves only to boggle the mind");
  display.display();
  f_time = millis() - t;
  

  x += vx;
  y += vy;

  if (x >= display.width()-7) {
    vx = -1;
  }

  if (x < 7) {
    vx = 1;
  }

  if (y >= display.height()-7) {
    vy = -1;
  }

  if (y < 7) {
    vy = 1;
  }

  delay(1);  
}
