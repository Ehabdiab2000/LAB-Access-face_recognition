/* Read RFID Tag with RC522 RFID Reader
 *  Made by miliohm.com
 */
 
#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 0 //D1
#define SS_PIN 2  //D2
#define greenled 4
#define redled 5
//constexpr uint8_t RST_PIN = 3;     // Configurable, see typical pin layout above
//constexpr uint8_t SS_PIN = 4;     // Configurable, see typical pin layout above
MFRC522 rfid(2, 0); // Instance of the class
MFRC522::MIFARE_Key key;
String tag;
void setup() {
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522

  pinMode(greenled, OUTPUT);
   pinMode(redled, OUTPUT);

   digitalWrite(redled,HIGH);
}
void loop() {

//recieve incomming order from computer
 if (Serial.available() > 0) {
    // get incoming byte:
    int val = char(Serial.read())-'0';
//    Serial.println(val);
//    Serial.write("\n");
    if(val == 1){
           
       digitalWrite(greenled, HIGH);
      digitalWrite(redled,LOW);
       delay(4000);
               
       digitalWrite(greenled,LOW);
        digitalWrite(redled,HIGH);
       delay(1000);
      } 
                          }

  
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
  if (rfid.PICC_ReadCardSerial()) {
    for (byte i = 0; i < 4; i++) {
      tag += rfid.uid.uidByte[i];
    }
    Serial.println(tag);
    tag = "";
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}
