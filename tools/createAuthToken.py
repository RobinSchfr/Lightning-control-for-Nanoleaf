import json
import requests


def createAuthToken():
    ip = input('Enter the IP: ')
    input('The power button on the device should be held for 5-7 seconds, then you need to press enter within 30 seconds.')
    print('Please wait.')
    response = requests.post(f'http://{ip}:16021/api/v1/new')
    data = json.loads(response.text)
    print('auth_token created:', data['auth_token'])


createAuthToken()