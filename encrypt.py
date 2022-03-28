import base64
import json
class Encrypt:
    def decode(self,name):
        return json.loads(base64.b64decode(name).decode('utf-8'))
    def encode(self,name_decoded):
        json_encoded_list = json.dumps(name_decoded)
        return base64.b64encode(json_encoded_list.encode())