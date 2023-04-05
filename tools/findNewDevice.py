import requests
import socket


def getIPFromDevice():
    print('\n[INFO] This may take up to 2 minutes.')
    localIP = socket.gethostbyname(socket.gethostname())
    localIP = localIP[:localIP.rfind('.') - len(localIP) + 1]
    for i in range(255):
        ip = f'http://{localIP}{i}'
        print(round(i / 254 * 100), '%', end='\r')
        try:
            response = requests.get(ip, timeout=0.5)
            if response.text.find('nanoleaf') != -1:
                print(f'\n\n[SUCCESS] Device found:', ip)
                return
        except Exception:
            pass
    print('\n\n[ERROR] Device not found. Please try again later.')


getIPFromDevice()