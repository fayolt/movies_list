import requests
import threading
import time

from http.server import HTTPServer
from unittest import TestCase, mock

from movie_list import server


class TestServer(TestCase):

    @mock.patch('movie_list.server.read_cache')
    def test_get_request(self, mock_read_cache):
        httpd = HTTPServer(("127.0.0.1", 8001), server.Handler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        mock_read_cache.return_value = None
        server_thread.start()
        # Wait a bit for the server to come up
        time.sleep(1)
        response = requests.get("http://127.0.0.1:8001")
        self.assertEqual(response.status_code, 404)
        response = requests.get("http://127.0.0.1:8001/movies")
        self.assertEqual(response.status_code, 500)
        httpd.shutdown()
        httpd.server_close()
