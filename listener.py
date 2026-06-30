
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        try:
            payload = json.loads(data)
            print("Received:", payload)
        except:
            print("Raw:", data)

        self.send_response(200)
        self.end_headers()

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Listening on port 8000...")
server.serve_forever()
