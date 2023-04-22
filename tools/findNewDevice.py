from ctypes import c_char_p
from multiprocessing import Process, Manager
import getmac
import socket


def getMac(ip, mac):
    macAddress = getmac.get_mac_address(ip=ip)
    mac.value = macAddress


def getIPFromDevice():
    deviceList = []
    deviceCount = int(input('How many devices do you have in your local network?: '))
    print('\n[INFO] Please wait. This may take up to 2 minutes.')
    localIP = socket.gethostbyname(socket.gethostname())
    localIP = localIP[:localIP.rfind('.') - len(localIP) + 1]
    for i in range(255):
        ip = localIP + str(i)
        print(round(i / 254 * 100), '%', end='\r')
        mac = Manager().Value(c_char_p, 'None')
        p = Process(target=getMac, args=[ip, mac])
        p.start()
        p.join(0.5)
        if p.is_alive():
            p.terminate()
        if mac.value != 'None':
            if mac.value.startswith('00:55:da:5') or mac.value.startswith('80:8a:f7'):      # registered prefixes for nanoleaf MAC addresses https://maclookup.app/vendors/nanoleaf
                deviceList.append(ip)
                if len(deviceList) == deviceCount:
                    break
    if len(deviceList) > 0:
        print(f'\n\n[SUCCESS] {len(deviceList)} device(s) found:\n')
        for i, device in enumerate(deviceList):
            print(f'Device {i + 1}: {device}')
    else:
        print('\n\n[ERROR] No devices found. Please try again later.')


if __name__ == '__main__':
    getIPFromDevice()