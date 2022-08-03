import requests
import json

class Sender(object):
    def __init__(self):
        print("[SENDER]:\tDECLARADO")
        self.headers = {'Content-type': 'application/json'}
        self.inctaddr = open('config.json','r')
        self.inctaddr = json.load(self.inctaddr)
        self.inctaddr = self.inctaddr['inctaddr']
    
    def sendData(self,resourceData, uuid):
        print("[SENDER]:\tINICIADO")
        response = 0

        print(uuid)
        print(resourceData)
        response = requests.post (self.inctaddr + '/adaptor/resources/' + uuid + '/data', data = json.dumps(resourceData), headers=self.headers)
        print(response.text)
        print("[SENDER]:\tDadis enviados")
        return response.text