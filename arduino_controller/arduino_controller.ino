/*
 *  Created by TheCircuit
*/

#define RST_PIN 3 //D1
#define SS_PIN 4  //D2

//#define lockcont 10 // Lock Control
#include <SPI.h>
#include <MFRC522.h>

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
int statuss = 0;
int out = 0;
void setup() 
{
 // pinMode(lockcont, OUTPUT);
  
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
}
void loop() 
{
//
////recieve incomming order from computer
// if (Serial.available() > 0) {
//    // get incoming byte:
//    int val = char(Serial.read())-'0';
////    Serial.println(val);
////    Serial.write("\n");
//    if(val == 1){
//       Serial.println(val);
//    
//       //digitalWrite(greenled, HIGH);
//      // digitalWrite(lockcont,LOW);
//       delay(4000);
//         
//      
//       //digitalWrite(greenled,LOW);
//       // digitalWrite(lockcont,HIGH);
//       delay(1000);
//      } 
//                           }
//  
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
//    Serial.println("No card");
//    delay(50);
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    
    return;
  }
  //Show UID on serial monitor
  Serial.println();
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
    
  }
delay(2000);
  
} 
