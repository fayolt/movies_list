import json
from http.server import BaseHTTPRequestHandler

from .service import read_cache


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to a GET request."""
        data = ""
        if self.path == "/movies":
            m_list = read_cache()
            data = m_list
            self.send_response(200)
        else:
            data = "Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))
