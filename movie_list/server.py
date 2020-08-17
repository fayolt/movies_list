import time
from http.server import HTTPServer, BaseHTTPRequestHandler

from .api import get_data

HOSTNAME = '0.0.0.0'
PORT_NUMBER = 8000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to a GET request."""
        data = ""
        if self.path == "/movies":
            data = str(len(get_data("/people")))
            self.send_response(200)
        else:
            data = "Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))

def start_server():
    httpd = HTTPServer((HOSTNAME, PORT_NUMBER), Handler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOSTNAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOSTNAME, PORT_NUMBER))