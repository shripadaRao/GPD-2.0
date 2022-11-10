#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <LiquidCrystal.h>

LiquidCrystal lcd(19, 23, 18, 17, 16, 15);

const char* ssid = "Galaxy M218905";
const char* password = "whui4989";

const char* serverName = "http://firebaseapi1.pythonanywhere.com/fetchFromFirebase";

String serverResp;
String serverRespArr[2];

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");

  lcd.begin(16, 2);
 }

void loop() {
    
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
              
      serverResp = httpGETRequest(serverName);
      
      Serial.println(serverResp);
      JSONVar myObject = JSON.parse(serverResp);
  
      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
    
      Serial.print("JSON object = ");
      Serial.println(myObject);
    
      // myObject.keys() can be used to get an array of all the keys in the object
      JSONVar keys = myObject.keys();
//    
//      for (int i = 0; i < keys.length(); i++) {
//        JSONVar value = myObject[keys[i]];
//        Serial.print(keys[i]);
//        Serial.print(" = ");
//        Serial.println(value);
//        serverRespArr[i] = double(value);
//      }

      JSONVar display_text = myObject[keys[0]];
      JSONVar time_table = myObject[keys[1]];

      
      
//      Serial.print("1 = ");
//      Serial.println(sensorReadingsArr[0]);
//      Serial.print("2 = ");
//      Serial.println(sensorReadingsArr[1]);
//      Serial.print("3 = ");
//      Serial.println(sensorReadingsArr[2]);
//    }
//    else {
//      Serial.println("WiFi Disconnected");
//    }
//    lastTime = millis();
lcd.clear();
  lcd.print(display_text[0]);
  lcd.setCursor(0, 1);
  lcd.print(time_table);
  Serial.println(display_text[0]);
  Serial.println(time_table);


 
  }
  delay(100);
   
}
  
String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}