#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <DHT.h>

#define FIREBASE_HOST "irrigateiq-9fe90-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "QQSmwDTJeYIEHAHTcvoOUXTfXItYO6Bas3fiyxgI"
#define WIFI_SSID "DESKTOP"
#define WIFI_PASSWORD "ansh1234"

#define DHTPIN D1
#define DHTTYPE DHT11
#define RELAY_PIN D3  // Control pin (e.g., connected to a relay or LED)

DHT dht(DHTPIN, DHTTYPE);
int soilMoisturePin = A0;

void setup() {
  Serial.begin(9600);
  delay(1000);

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println();
  Serial.println("WiFi Connected");

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  dht.begin();

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW); // Default OFF
}

void loop() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();
  int soilMoisture = analogRead(soilMoisturePin);

  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print("°C | Humidity: ");
  Serial.print(humidity);
  Serial.print("% | Soil Moisture: ");
  Serial.println(soilMoisture);

  // Send sensor data to Firebase
  Firebase.setFloat("/SensorData/temperature", temperature);
  Firebase.setFloat("/SensorData/humidity", humidity);
  Firebase.setInt("/SensorData/soil_moisture", soilMoisture);

  if (Firebase.failed()) {
    Serial.print("Firebase set failed: ");
    Serial.println(Firebase.error());
  } else {
    Serial.println("Firebase update successful!");
  }

  // --- Read control value from Firebase ---
  int controlValue = Firebase.getInt("/control");  // 1 = ON, 0 = OFF

  if (Firebase.failed()) {
    Serial.print("Firebase get failed: ");
    Serial.println(Firebase.error());
  } else {
    Serial.print("Control value from Firebase: ");
    Serial.println(controlValue);

    if (controlValue == 1) {
      digitalWrite(RELAY_PIN, HIGH);  // Turn ON
    } else {
      digitalWrite(RELAY_PIN, LOW);   // Turn OFF
    }
  }

  delay(1000);  // Delay 1 second
}
