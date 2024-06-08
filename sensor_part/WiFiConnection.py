import network
import time
import urequests
import ujson
import esp32
import socket
from machine import Pin, ADC

station = network.WLAN(network.STA_IF)
rain_sensor_value = 0
sensor = ADC(Pin(26))
sensor.atten(ADC.ATTN_11DB)
poruka = "cekamo ocitavanje senzora"

def connect(ssid, password):
    station = network.WLAN(network.STA_IF)

    
    station.active(False)
    station.active(True)

    if station.isconnected():
        station.disconnect()
        print (f'started in the connected state, but now disconnected')
    else:
        print (f'started in the disconnected state')

    station.connect(ssid, password)
    

    while station.isconnected() == False:
        time.sleep(1)
        print(".")
    
    print("Connection successful")
    print(station.ifconfig())

def get_rss_send():
    
    #udp_host = "192.168.1.2"
    #udp_port = 12345
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    
    while station.isconnected() == True:
        rss = station.status('rssi')
        temp_celsius = (esp32.raw_temperature() - 32) / 1.8
        print(rss, temp_celsius)
        data_to_send = b"{},{},{},{}".format(" ", rss, " ", temp_celsius)
        udp_socket.sendto(data_to_send, (udp_host, udp_port))
        time.sleep(0.2)
    

def read_sensor_data():
    global rain_sensor_value, poruka
    rain_sensor_value = sensor.read()
    print(rain_sensor_value)
    if rain_sensor_value == 0: # nekako 
        poruka = "kisa pada"
    else:
        poruka = "ne pada kisa";

def do_post():
    global rain_sensor_value, poruka
    url = 'http://192.168.0.26:3031/posts/66619897130a98d424aede6c' # --------------------------------------menjaj
    data = ujson.dumps({
        "sensor": "esp32",
        "value": rain_sensor_value,
        "result": poruka
    })  # Dictionary representing the data
    headers = {'Content-Type': 'application/json'}  # Headers dictionary
    
    while True:
        try:
            r = urequests.put(url, data=data, headers=headers)
            print("updated value")
            r.close()
            break
        except OSError as e:
            print("HTTP request error:", e)
            time.sleep(2)  # Retry after a short delay
            
