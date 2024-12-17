### Imports ###
import sys
import os
import requests

import socketio
import uuid

from .tpvm_operations import TPVM_Operations
### ###

class TPVM_Connection:
    operations = []
    
    # Get the mac address of the device for unique communication
    mac = hex(uuid.getnode())
    
    def __init__(self, server_ip, ssl_verify):
        self.server_ip = server_ip
        self.ssl_verify = ssl_verify
        self.register()


    def start_connection(self):
        """
        """
        self.stopCommand = False
        with socketio.SimpleClient(ssl_verify=self.ssl_verify) as sio:
            sio.connect("https://" + self.server_ip)

            while not self.stopCommand:
                event = sio.receive()
                if(event[0] == "runOperation"):
                    self.run_operation(event[1])

    def register(self):
        api_url = "https://" + self.server_ip + "/api/client/register"
        response = requests.post(api_url, json={"address": self.mac}, verify=self.ssl_verify)
        self.id = response.json()["device_id"]

    def add_operation(self, name, description, function):
        operation = TPVM_Operations(name, description, function)
        operation.register(self.server_ip, self.ssl_verify, self.id)
        self.operations.append(operation)
        return operation

    def remove_operation(self, operation):
        operation = next((x for x in self.operations if x.call_id == operation.id), None)
        operation.delist(self.server_ip, self.ssl_verify, self.id)
        self.operations.remove(operation)

    def run_operation(self, id):
        operation = next((x for x in self.operations if x.call_id == id), None)
        if operation:
            operation.run()

    def delist(self):
        api_url = "https://" + self.server_ip + "/api/client/delist"
        requests.post(api_url, json={"address": self.mac}, verify=self.ssl_verify)

    def stop_connection(self):
        self.stopCommand = True