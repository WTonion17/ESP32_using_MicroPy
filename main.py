from machine import Pin, ADC, I2C
import ssd1306
import network
import time
import math
import onewire, ds18x20

# # ESP32 Pin assignment 
# i2c = I2C(1, scl=Pin(22), sda=Pin(21))

# oled_width = 128
# oled_height = 64
# oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# oled.text('Hello, Wokwi!', 0, 0)      
# oled.show()

ssid = 'NHATRO BM T1S'
password = 'nhatro123456t1'
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print('Connecting to network...')
        time.sleep(1)

    print('connected wifi: ', ssid)
    print('Network config:', wlan.ifconfig())
    

connect_wifi(ssid, password)

# Turbidity sensor
def read_turbidity():
    adc = ADC(Pin(34))
    volt = 0
    for _ in range(800):
        volt += adc.read() / 4095 * 3.3 * 2.41
    volt /= 800
    volt = round(volt, 1)
    if volt < 2.5:
        NTU = 3000
    else:
        NTU = -1120.4 * math.sqrt(volt) + 5742.3 * volt - 4352.9
    print(f"{volt} V\t{NTU} NTU")

# pH sensor
def read_ph():
    adc = ADC(Pin(35))
    buf = [adc.read() for _ in range(10)]
    buf.sort()
    avgValue = sum(buf[2:8]) / 6
    phVol = avgValue * 3.3 / 4095 / 4.3
    phValue = 14.2 - (-5.70 * phVol + 29.5)
    print(f"pH: {phValue}")

# Temperature sensor
# DS18B20 Temperature sensor setup
dat = Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(dat))
def read_temperature():
    roms = ds_sensor.scan()
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        print(f"{temp} C")

while True:
        read_turbidity()
        read_ph()
        read_temperature()