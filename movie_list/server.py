import json
import os
from http.server import BaseHTTPRequestHandler

from .service import read_cache
from .template_renderer import render

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Respond to a GET request."""
        data = ""
        if self.path == "/movies":
            data = render('movies.html', read_cache())
            self.send_response(200)
        elif self.path.endswith(".css"):
            filename = STATIC_DIR + self.path
            with open(filename, 'rb') as static_file:
                data = static_file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
        else:
            data = "Not Found"
            self.send_error(404)
        self.end_headers()
        if type(data) == str:
            self.wfile.write(bytes(data, "utf-8"))
        else:
            self.wfile.write(data)
