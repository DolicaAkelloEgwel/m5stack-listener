
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def rssi_to_distance(rssi):
    n = 4
    tx_power = 12
    return 10 ** ((tx_power - rssi)/(10 * n))

class ThreeValues():
    def __init__(self):
        self._values = [0.0 for _ in range(3)]
    def add(self, new_val):
        self._values = self._values[1:]
        self._values.append(rssi_to_distance(new_val))
    def average(self):
        return sum(self._values) / 3.0

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        try:
            payload = json.loads(data)
            print(payload)
        except:
            print("Raw:", data)

        self.send_response(200)
        self.end_headers()

values = ThreeValues()
server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Listening on port 8000...")
server.serve_forever()
