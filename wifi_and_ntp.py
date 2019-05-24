#connects to the WiFi network and sync time via NTP
try:
    from config import wifi_ssid, wifi_passwd
except:
    raise Exception("Failed to load wifi SSID and/or password from config")

import time
import network
import ntptime
import utime


# create networking interface
sta_if = network.WLAN(network.STA_IF)


def wifi_connect(ssid, pwd):
    ''' connect to wifi with provided password and print the result
        20 sec delay loop the check if we're connected
    '''
    # activate the interface
    sta_if.active(True)

    # connect it to the network
    sta_if.connect(ssid, pwd)
    
    # check result
    print("Connection attempt to WiFi SSID:", ssid)
    for i in range(0,20):
        if not(sta_if.isconnected()):
            print('.' * i)
            time.sleep(1)
        else:
            break
    print("Wifi connected:", sta_if.isconnected())
    print("Wifi config:", sta_if.ifconfig())


def sync_ntp_time():
    ''' In case we have active and connected wifi, sync RTC via NTP '''
    if not(sta_if.active()):
        print("Can't sync NTP. Wifi not active.")
    elif not(sta_if.isconnected()):
        print("Can't sync NTP. Wifi not connected.")
    else:
        ntptime.settime()
        dt = utime.localtime()
        dt = [str(d) for d in dt] # int to str for concat
        print("NTP time loaded:", "-".join(dt[0:3]), ":".join(dt[3:6]))


def startup():
    wifi_connect(wifi_ssid, wifi_passwd)
    sync_ntp_time()
