#ESP 32 SERVER AP

try:
  import usocket as socket
except:
  import socket

import network
import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'MicroPython-AP'
password = '123456789'

wifiSSID = "test"
wifiPass = "testpss"

network.WLAN(network.AP_IF).active(False)
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig())

def web_page():
  html = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WiFi Configuration</title><style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background-color: #f7f7f7;
    }
    .container {
      background-color: #fff;
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    h1 {
      margin-top: 0;
    }
    label {
      display: block;
      margin-bottom: 8px;
      font-weight: bold;
    }
    input[type="text"], input[type="password"] {
      width: 100%;
      padding: 8px;
      margin-bottom: 16px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }
    input[type="submit"] {
      background-color: #4CAF50;
      color: white;
      padding: 10px 15px;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    input[type="submit"]:hover {
      background-color: #45a049;
    }
  </style></head><body>
  <div class="container">
    <h1>Configure WiFi</h1>
    <form action="/configure" method="POST">
      <label for="ssid">SSID:</label>
      <input type="text" id="ssid" name="ssid">
      
      <label for="password">Password:</label>
      <input type="password" id="password" name="password">
      
      <input type="submit" value="Submit">
    </form>
  </div>
  </body></html>"""
  return html

def handle_post(request):
  try:
    request = request.decode('utf-8')
    _, post_data = request.split('\r\n\r\n', 1)
    params = {}
    for param in post_data.split('&'):
      key, value = param.split('=')
      params[key] = value
    return params
  except Exception as e:
    print('Error parsing POST data:', e)
    return {}


try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)
    print('Socket created and listening on port 80')

    while wifiSSID == "test":
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        print('Content = %s' % str(request))
    
        request_str = request.decode('utf-8')
        if 'POST /configure' in request_str:
            params = handle_post(request)
        
            wifiSSID = params.get('ssid', '')
            wifiPass = params.get('password', '')
            print('Received SSID:', wifiSSID)
            print('Received Password:', wifiPass)
            response = "<html><body><h1>Configuration Saved. You can now connect to internet and goto site</h1></body></html>"
        else:
            response = web_page()
    
        http_response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + response
        conn.send(http_response)
        conn.close()
except OSError as e:
    print('Failed to create socket or bind to address:', e)
finally:
    if s:
        s.close()
        print('Socket closed')

