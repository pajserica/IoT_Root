import WiFiConnection as wifi
import ap_server as localSrv
from time import sleep
#from utime import sleep #need this?

print(localSrv.wifiSSID, localSrv.wifiPass)

wifi.connect(localSrv.wifiSSID, localSrv.wifiPass)

while(1):
    wifi.read_sensor_data()
    wifi.do_post()
    wifi.time.sleep(3)
#wifi.get_rss_send()