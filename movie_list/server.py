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
            movies = read_cache()
            if movies is None:
                data = render(STATIC_DIR, 'error.html',
                              message="UH OH! Something went wrong", code=500)
                self.send_response(500)
            else:
                data = render(STATIC_DIR, 'movies.html', films=movies)
                self.send_response(200)
        elif self.path.endswith(".css"):
            filename = STATIC_DIR + self.path
            with open(filename) as static_file:
                data = ''.join(static_file.readlines())
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
        else:
            data = render(STATIC_DIR, 'error.html',
                          message="UH OH! You're lost", code=404)
            self.send_response(404)
        self.end_headers()
        self.wfile.write(data.encode('utf-8'))
