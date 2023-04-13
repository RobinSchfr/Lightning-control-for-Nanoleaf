from ui_DeviceInitializerDialog import Ui_DeviceInitializerDialog
import json
import requests
import socket


class DeviceInitializer:
    def __init__(self, notifier):
        self.ip = None
        self.auth_token = None
        self.notifier = notifier

    def getIPFromDevice(self):
        localIP = socket.gethostbyname(socket.gethostname())
        localIP = localIP[:localIP.rfind('.') - len(localIP) + 1]
        for i in range(255):
            ip = f'http://{localIP}{i}'
            try:
                response = requests.get(ip, timeout=0.5)
                if response.text.find('nanoleaf') != -1:
                    self.ip = f'{localIP}{i}'
                    self.notifier.notify(message=f'Device found: {self.ip}', type='positive')
                    return self.ip
            except Exception:
                pass
        self.notifier.notify(message='Device not found. Please try again later.', type='negative')

    def setIP(self, ip):
        self.ip = ip

    def setAuthToken(self, token):
        self.auth_token = token

    async def createAuthToken(self):
        dialog = Ui_DeviceInitializerDialog()
        await dialog.show()
        response = requests.post(f'http://{self.ip}:16021/api/v1/new')
        data = json.loads(response.text)
        self.notifier.notify(message='Authentication token created.', type='positive')
        self.auth_token = data['auth_token']