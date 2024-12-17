import uuid
import requests

class TPVM_Operations:

    def __init__(self, name, description, function):
        self.name = name
        self.description = description
        self.function = function
        self.call_id = uuid.uuid4().hex

    def register(self, server_ip, ssl_verify, device_id):
        api_url = "https://" + server_ip + "/api/operation/register"
        obj = { "device_id": device_id, 
                "window_name": self.name,
                "command": self.description,
                "call_id": self.call_id}
        response = requests.post(api_url, json=obj, verify=ssl_verify)
        self.id = response.json()["call_id"]
    
    def delist(self, server_ip, ssl_verify, device_id):
        api_url = "https://" + server_ip + "/api/operation/delist"
        obj = { "device_id": device_id, 
                "window_name": self.name,
                "command": self.description,
                "call_id": self.call_id}
        requests.post(api_url, json=obj, verify=ssl_verify)

    def run(self):
        self.function()
