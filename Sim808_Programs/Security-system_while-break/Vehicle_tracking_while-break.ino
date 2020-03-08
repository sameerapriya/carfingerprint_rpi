    #include <DFRobot_sim808.h>
    #include <SoftwareSerial.h>
    
    #define MESSAGE_LENGTH 160
    char message[MESSAGE_LENGTH];
    int messageIndex = 0;
    char MESSAGE[300];
    char lat[12];
    char lon[12];
    char wspeed[12];
    char phone[] = "8328132839";
    char datetime[24];
    
    
    #define PIN_TX    7
    #define PIN_RX    8
    SoftwareSerial mySerial(PIN_TX, PIN_RX);
    DFRobot_SIM808 sim808(&mySerial);//Connect RX,TX,PWR,
    
    void setup()
    {
      mySerial.begin(9600);
      Serial.begin(9600);
    
      //******** Initialize sim808 module *************
      while (!sim808.init())
      {
        Serial.print("Sim808 init error\r\n");
        delay(1000);
      }
      delay(3000);
    
      if ( sim808.attachGPS())
        Serial.println("Open the GPS power success");
      else
        Serial.println("Open the GPS power failure");
    
      Serial.println("Init Success");
      delay(10000);
    }
    
    void loop()
    {
    
      while (!sim808.getGPS())
      {}
      Serial.print(sim808.GPSdata.year);
      Serial.print("/");
      Serial.print(sim808.GPSdata.month);
      Serial.print("/");
      Serial.print(sim808.GPSdata.day);
      Serial.print(" ");
      Serial.print(sim808.GPSdata.hour);
      Serial.print(":");
      Serial.print(sim808.GPSdata.minute);
      Serial.print(":");
      Serial.print(sim808.GPSdata.second);
      Serial.print(":");
      Serial.println(sim808.GPSdata.centisecond);
      Serial.print("latitude :");
      Serial.println(sim808.GPSdata.lat);
      Serial.print("longitude :");
      Serial.println(sim808.GPSdata.lon);
      Serial.print("speed_kph :");
      Serial.println(sim808.GPSdata.speed_kph);
      Serial.print("heading :");
      Serial.println(sim808.GPSdata.heading);
      Serial.println();
    
      float la = sim808.GPSdata.lat;
      float lo = sim808.GPSdata.lon;
      float ws = sim808.GPSdata.speed_kph;
    
      dtostrf(la, 4, 6, lat); //put float value of la into char array of lat. 6 = number of digits before decimal sign. 2 = number of digits after the decimal sign.
      dtostrf(lo, 4, 6, lon); //put float value of lo into char array of lon
      dtostrf(ws, 6, 2, wspeed);  //put float value of ws into char array of wspeed
    
      sprintf(MESSAGE, "Latitude : %s\nLongitude : %s\nWind Speed : %s kph\nSmart security system, your appliance was trued to access. please find it here.\nhttp://maps.google.com/maps?q=loc:%s,%s\n", lat, lon, wspeed, lat, lon);
      Serial.println("Sim808 init success");
      Serial.println("Start to send message ...");
      Serial.println(MESSAGE);
      Serial.println(phone);
    
      while (Serial.available() > 0)
      {
        int state = Serial.read();
        Serial.print(state);
        if (state == 49)
        {
          sim808.sendSMS(phone, MESSAGE);
          Serial.println("Message Sent");
          sim808.detachGPS();
        }
        else
        {
          Serial.println("Enter 1");
        }
        break;
      }
    }
