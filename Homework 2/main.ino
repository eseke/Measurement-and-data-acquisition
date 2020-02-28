#include <TM1637Display.h>
#include <TimerOne.h>

volatile long distance = 0;
volatile byte ispis = 0;

bool stanje = false;
TM1637Display display(9, 8);
uint8_t data[4];

void setup() {
	pinMode(2, INPUT);
	pinMode(4, OUTPUT);
	pinMode(7, OUTPUT);
	pinMode(10, INPUT);
	pinMode(11, OUTPUT);
	display.setBrightness(0x0f);
	attachInterrupt(digitalPinToInterrupt(2), TOUCH, RISING);
	Timer1.initialize(100000);
	Timer1.attachInterrupt(getDistance);
	Serial.begin(9600);
}
int tmp1=0;

//primanje informacija sa serial porta
void serialEvent() { 
	data[0] = display.encodeDigit(10);//ispisuje A
	data[2] = display.encodeDigit(11);//ispisuje b

		while (Serial.available()) {
			if (tmp1 == 1) {
				data[1] = display.encodeDigit(Serial.read());
				tmp1 = 2;
			}
			else if (tmp1 == 2) {
				data[3] = display.encodeDigit(Serial.read());
				display.setSegments(data);
				stanje = false;
				tmp1 = 0;
			}
			else {
				char tmp = Serial.read();
				if (tmp == '1') {
					//prvi igrac na potezu
					digitalWrite(7, LOW);
					digitalWrite(4, HIGH);
					stanje = true;
				}
				else if (tmp == '2') {
					//drugi igrac na potezu
					digitalWrite(4, LOW);
					digitalWrite(7, HIGH);
					stanje = true;
				}
				else if (tmp == '3') {
					/*ispis rezultata
					podaci se salju u formatu 3 prvi_broj drugi_broj
					sa razmacima izmedju brojeva
					Npr 3 4 5
					*/
					tmp1 = 1;
					digitalWrite(4, LOW);
					digitalWrite(7, LOW);
				}
			}
		}

}

void loop() {
	//Mogucnost ispisa sa displaj razdaljine
	/*if (ispis && stanje) {

		data[3] = display.encodeDigit(distance%10);
		data[2] = display.encodeDigit((distance / 10)%10);
		data[1] = display.encodeDigit((distance / 100) % 10);
		data[0] = display.encodeDigit((distance / 1000) % 10);
		display.setSegments(data);
		ispis = 0;
	}
	delay(100);*/
}

//Interrupt za senzor dodira, salje se razdaljina na serijski port
void TOUCH() {
	if (stanje) {
		digitalWrite(4, LOW);
		digitalWrite(7, LOW);

		Serial.println(distance);//salje na serijski port udaljenost u cm
		stanje = false;
	}
}

//Interrupt za tajmer,vrsi se akvizicija razdaljine
void getDistance() {
	digitalWrite(11, HIGH);
	delayMicroseconds(10);
	digitalWrite(11, LOW);

	distance = pulseIn(10, HIGH) * 0.0170;
	ispis = 1;

}
