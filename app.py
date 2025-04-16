from flask import Flask, jsonify
import RPi.GPIO as GPIO
import Adafruit_DHT
import time

app = Flask(__name__)

# Konfiguracja pinów GPIO
LED_PIN = 17  # Pin GPIO, do którego podłączona jest dioda LED
DHT_SENSOR = Adafruit_DHT.DHT22  # Typ czujnika temperatury (DHT22 lub DHT11)
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
    Endpoint do odczytu temperatury z czujnika DHT.
    Zwraca aktualną temperaturę.
    """
    # Próbujemy odczytać dane z czujnika (kilka prób w przypadku błędów)
    max_retries = 3
    for _ in range(max_retries):
        _, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if temperature is not None:
            break
        time.sleep(1)
    
    # Sprawdzamy czy udało się odczytać dane
    if temperature is None:
        return jsonify({
            "success": False,
            "error": "Nie udało się odczytać danych z czujnika"
        }), 500
    
    return jsonify({
        "success": True,
        "temperature": round(temperature, 1)  # Zaokrąglamy do 1 miejsca po przecinku
    })

@app.route('/', methods=['GET'])
def index():
    """
    Prosty endpoint główny pokazujący dostępne endpointy.
    """
    return jsonify({
        "available_endpoints": [
            {"path": "/toggle", "method": "GET", "description": "Przełącza stan diody LED"},
            {"path": "/temperature", "method": "GET", "description": "Odczyt temperatury"}
        ]
    })

# Obsługa czystego zamknięcia serwera (sprzątanie po GPIO)
def cleanup():
    GPIO.cleanup()

# Rejestracja funkcji sprzątającej, która zostanie wywołana przy zamknięciu
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    try:
        # Uruchamiamy serwer na wszystkich interfejsach (0.0.0.0) na porcie 5000
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        # Obsługa Ctrl+C
        cleanup()