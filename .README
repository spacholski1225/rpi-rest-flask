# Mikroserwis Flask dla Raspberry Pi

Ten projekt zawiera prosty mikroserwis napisany w Pythonie z użyciem frameworka Flask, który obsługuje:
- Przełączanie stanu diody LED (/toggle)
- Odczyt temperatury i wilgotności (/temperature)

## Wymagania sprzętowe

- Raspberry Pi (dowolna wersja z GPIO)
- Dioda LED z rezystorem (podłączona do pinu GPIO 17)
- Czujnik temperatury DHT22 lub DHT11 (podłączony do pinu GPIO 4)

## Schemat podłączenia

### Dioda LED:
- Anoda (dłuższa nóżka) - przez rezystor 220Ω - do pinu GPIO 17
- Katoda (krótsza nóżka) - do GND (masa)

### Czujnik DHT22/DHT11:
- VCC (pin 1) - do 3.3V lub 5V (zależnie od modelu czujnika)
- DATA (pin 2) - do pinu GPIO 4
- GND (pin 4) - do GND (masa)

## Instalacja wymaganych bibliotek

```bash
# Aktualizacja menedżera pakietów
sudo apt-get update
sudo apt-get upgrade

# Instalacja pip i wymaganych narzędzi
sudo apt-get install python3-pip python3-dev

# Instalacja biblioteki RPi.GPIO (do obsługi pinów GPIO)
sudo pip3 install RPi.GPIO

# Instalacja biblioteki Adafruit_DHT (do obsługi czujnika temperatury)
sudo pip3 install Adafruit_DHT

# Instalacja Flask
sudo pip3 install flask
```

## Uruchomienie serwisu

1. Zapisz kod z pliku `app.py` na swoim Raspberry Pi
2. Uruchom aplikację:

```bash
python3 app.py
```

Serwis będzie dostępny pod adresem: `http://[adres_IP_Raspberry_Pi]:5000/`

## Testowanie endpointów

### Przełączanie diody LED:
```
http://[adres_IP_Raspberry_Pi]:5000/toggle
```

### Odczyt temperatury:
```
http://[adres_IP_Raspberry_Pi]:5000/temperature
```

## Konfiguracja uruchamiania przy starcie systemu

Aby serwis uruchamiał się automatycznie przy starcie Raspberry Pi, możesz dodać go jako usługę systemd:

1. Utwórz plik usługi:
```bash
sudo nano /etc/systemd/system/rpi-flask-service.service
```

2. Dodaj następującą zawartość (dostosuj ścieżki do swojego środowiska):
```
[Unit]
Description=Raspberry Pi Flask Microservice
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/rpi-flask-service
ExecStart=/usr/bin/python3 /home/pi/rpi-flask-service/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Włącz i uruchom usługę:
```bash
sudo systemctl enable rpi-flask-service.service
sudo systemctl start rpi-flask-service.service
```

4. Sprawdź status usługi:
```bash
sudo systemctl status rpi-flask-service.service
```


![alt text](image.png)

![alt text](image-1.png)




---

# Instrukcje montażu układu na Raspberry Pi

W niniejszym pliku znajdziesz instrukcje jak podłączyć diodę LED oraz termometr. Przyjmujemy, że Raspberry Pi używa numeracji pinów zgodnie z układem BCM. Dostępne są dwie wersje podłączenia czujnika temperatury:
- **Wersja 1:** Termometr DHT22 (można też zastosować DHT11 – ale poniższe instrukcje dotyczą DHT22)
- **Wersja 2:** Termometr DS18B20

---

## Wspólne elementy

### Potrzebne komponenty:
- Raspberry Pi (dowolny model, np. Raspberry Pi 3 lub 4)
- Płytka stykowa (breadboard)
- Kilka przewodów połączeniowych (dupont)
- Rezystor 220 Ω (opcjonalnie – dla LED)
- Zasilanie 5V/3,3V zgodne z używanymi komponentami

### Podłączenie diody LED
1. **Dioda LED:**  
   - **Anoda (dłuższa nóżka):** Podłączona przez rezystor 220 Ω do wyjścia GPIO (w naszym przykładzie używamy pinu **GPIO 17**).
   - **Katoda (krótsza nóżka):** Połączona z masą (GND) Raspberry Pi.

2. **Schemat dla LED:**
   - GPIO 17 → (rezystor 220 Ω) → Anoda LED  
   - Katoda LED → GND

---

## Wersja 1: Podłączenie termometru DHT22

### Elementy dla DHT22:
- Czujnik DHT22 (lub DHT11 – analogicznie)
- Rezystor podciągający 10 kΩ (zalecany)

### Schemat połączenia DHT22:
1. **Pin zasilania czujnika:**  
   - Podłączony do **3.3V** Raspberry Pi (niektóre moduły DHT22 mogą działać również na 5V, sprawdź specyfikację).
2. **Pin danych:**  
   - Połączony z określonym GPIO (w naszym przykładzie **GPIO 4**).
   - Umieść rezystor podciągający 10 kΩ między pinem danych a 3.3V.
3. **Pin GND:**  
   - Podłączony do masy (GND) Raspberry Pi.

### Schemat:
3.3V -----+-----[10 kΩ]----- Pin DHT22 (Dane) | +----> do GPIO 4

GND ------------------------- Pin GND 3.3V/5V --------------------- Pin VCC (zasilania)



### Dodatkowe uwagi:
- Upewnij się, że używasz rezystora podciągającego, aby stabilizować sygnał.
- Biblioteka `Adafruit_DHT` używana w kodzie potrafi odczytywać dane z czujnika po poprawnym podłączeniu.

---

## Wersja 2: Podłączenie termometru DS18B20

### Elementy dla DS18B20:
- Czujnik DS18B20
- Rezystor podciągający 4.7 kΩ (konieczny)
- Opcjonalnie: moduł „waterproof” w wersji z obudową

### Schemat połączenia DS18B20:
DS18B20 komunikuje się w oparciu o interfejs 1-Wire. Raspberry Pi musi mieć włączoną obsługę tego interfejsu.

1. **Pin zasilania (VCC):**  
   - Podłączony do **3.3V** Raspberry Pi.
2. **Pin danych:**  
   - Podłączony do wybranego GPIO – domyślnie używa się GPIO 4 (pin 7 na złączu 40-pinowym).  
   - Podłącz do niego rezystor podciągający 4.7 kΩ między pinem danych a 3.3V.
3. **Pin masy (GND):**  
   - Połączony z GND Raspberry Pi.

### Schemat:


3.3V -----+-----[4.7 kΩ]----- Pin danych DS18B20 (do GPIO 4)
          |
          +-------------------- Pin danych DS18B20
          
GND ---------------------- Pin GND DS18B20
3.3V --------------------- Pin VCC DS18B20


### Konfiguracja systemowa:
1. **Włączenie interfejsu 1-Wire:**
   - Edytuj plik `/boot/config.txt` i dodaj linię:
     ```
     dtoverlay=w1-gpio
     ```
   - Możesz wskazać konkretny pin, np.:
     ```
     dtoverlay=w1-gpio,gpiopin=4
     ```
2. **Załaduj moduły:**
   - Uruchom polecenia:
     ```bash
     sudo modprobe w1-gpio
     sudo modprobe w1-therm
     ```
   - Po restarcie systemu dane będą dostępne w katalogu `/sys/bus/w1/devices/`.

3. **Biblioteka do odczytu:**
   - Aby odczytać dane, można użyć dedykowanych bibliotek lub odczytać bezpośrednio pliki systemowe.

---

## Podsumowanie

W obu wersjach Raspberry Pi steruje diodą LED przez GPIO 17, a termometr jest podłączony do GPIO 4. Różnica leży w sposobie obsługi czujnika:
- **DHT22:** korzysta z biblioteki `Adafruit_DHT`, gdzie konieczne jest zastosowanie rezystora podciągającego 10 kΩ.
- **DS18B20:** wymaga użycia interfejsu 1-Wire, odpowiedniej konfiguracji systemowej oraz rezystora podciągającego 4.7 kΩ.

Upewnij się, że podczas montażu stosujesz odpowiednie rezystory oraz sprawdzasz napięcia zasilania, aby nie uszkodzić podłączanych elementów. Zawsze wykonuj montaż przy wyłączonym zasilaniu Raspberry Pi i dbaj o bezpieczne lutowanie lub stosowanie płytki stykowej.

