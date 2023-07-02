import json
import base64
from urllib.parse import parse_qs

encoded_params = 'eyJpZF91c2VyIjozfQ=='

decoded_params = base64.b64decode(encoded_params).decode('utf-8')

parameters = json.loads(decoded_params)

print(parameters)