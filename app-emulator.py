from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

# Definiujemy klasę do emulacji GPIO na Windows
class GPIOEmulator:
    BCM = 1
    OUT = 1
    IN = 0
    HIGH = 1
    LOW = 0
    
    @staticmethod
    def setmode(mode):
        print(f"[Emulator] Ustawiono tryb GPIO: {mode}")
    
    @staticmethod
    def setup(pin, mode):
        print(f"[Emulator] Skonfigurowano pin {pin} w trybie {mode}")
    
    @staticmethod
    def output(pin, state):
        print(f"[Emulator] Ustawiono pin {pin} na stan {'WYSOKI' if state==1 else 'NISKI'}")
    
    @staticmethod
    def cleanup():
        print("[Emulator] Wyczyszczono stan GPIO")

# Definiujemy klasę do emulacji czujnika DHT
class DHT_Emulator:
    @staticmethod
    def read_retry(sensor, pin):
        # Zwracamy losowe wartości do testów
        humidity = random.uniform(30.0, 80.0)
        temperature = random.uniform(15.0, 35.0)
        print(f"[Emulator] Odczytano temperaturę: {temperature:.1f}°C, wilgotność: {humidity:.1f}%")
        return humidity, temperature

# Używamy klasy emulacji zamiast rzeczywistych bibliotek
GPIO = GPIOEmulator
Adafruit_DHT = DHT_Emulator

# Konfiguracja pinów GPIO (emulowanych)
LED_PIN = 17  # Pin GPIO, do którego podłączona jest dioda LED
DHT_SENSOR = None  # Typ czujnika nie ma znaczenia w emulacji
DHT_PIN = 4  # Pin GPIO, do którego podłączony jest czujnik temperatury

# Inicjalizacja GPIO
GPIO.setmode(GPIO.BCM)  # Używamy numeracji BCM
GPIO.setup(LED_PIN, GPIO.OUT)  # Ustawiamy pin LED jako wyjście
GPIO.output(LED_PIN, GPIO.LOW)  # Początkowo dioda jest wyłączona

# Zmienna do śledzenia stanu diody
led_state = False

@app.route('/toggle', methods=['GET'])
def toggle_led():
    """
    Endpoint do przełączania stanu diody LED.
    Przełącza stan diody przy każdym wywołaniu.
    """
    global led_state
    led_state = not led_state  # Przełączamy stan
    
    # Ustawiamy nowy stan diody
    if led_state:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Włączamy diodę
        status = "on"
    else:
        GPIO.output(LED_PIN, GPIO.LOW)  # Wyłączamy diodę
        status = "off"
    
    return jsonify({
        "success": True,
        "led_state": status
    })

@app.route('/temperature', methods=['GET'])
def get_temperature():
    """
    Endpoint do odczytu temperatury z emulowanego czujnika DHT.
    Zwraca wygenerowane wartości temperatury i wilgotności.
    """
    # Symulujemy odczyt z czujnika
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    
    return jsonify({
        "success": True,
        "temperature": round(temperature, 1),  # Zaokrąglamy do 1 miejsca po przecinku
        "note": "Te wartości są symulowane - działa w trybie testowym"
    })

@app.route('/', methods=['GET'])
def index():
    """
    Prosty endpoint główny pokazujący dostępne endpointy.
    """
    return jsonify({
        "available_endpoints": [
            {"path": "/toggle", "method": "GET", "description": "Przełącza stan diody LED (emulowane)"},
            {"path": "/temperature", "method": "GET", "description": "Odczyt temperatury i wilgotności (emulowane)"}
        ],
        "environment": "Windows - Symulacja GPIO"
    })

# Obsługa czystego zamknięcia serwera (emulowane sprzątanie po GPIO)
def cleanup():
    GPIO.cleanup()

# Rejestracja funkcji sprzątającej, która zostanie wywołana przy zamknięciu
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        print("Uruchamianie mikroserwisu Flask z emulacją GPIO")
        print("UWAGA: To jest wersja deweloperska do testów na Windows")
        print("Na rzeczywistym Raspberry Pi należy użyć oryginalnej wersji kodu")
        # Uruchamiamy serwer na localhost na porcie 5000
        app.run(host='127.0.0.1', port=5000, debug=True)
    except KeyboardInterrupt:
        # Obsługa Ctrl+C
        cleanup()