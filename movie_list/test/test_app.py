import logging
import os
import signal
import threading
import time

from datetime import timedelta
from http.server import HTTPServer
from unittest import TestCase, mock

from movie_list import cache_refresher, service, app, service_exit


class TestApp(TestCase):

    @mock.patch('movie_list.app.films', return_value=None)
    def test_run_when_warmup_fails(self, mock_films):
        with self.assertLogs('movie_list', level='INFO') as cm:
            app.run()
        self.assertEqual(
            cm.output,
            [
                'INFO:movie_list.app:Starting Now ...',
                'CRITICAL:movie_list.app:Cache Warmup Failed',
                'CRITICAL:movie_list.app:Exiting Now ...'
            ]
        )
        mock_films.assert_called_once

    @mock.patch.object(app.HTTPServer, 'server_close')
    @mock.patch.object(app.HTTPServer, 'serve_forever')
    @mock.patch('movie_list.app.films', return_value=[])
    def test_run_when_warmup_succeed(self,
                                     mock_films,
                                     mock_serve_forever,
                                     mock_server_close):
        mock_cache_refresher = mock.create_autospec(
            cache_refresher.CacheRefresher)
        mock_serve_forever.side_effect = service_exit.ServiceExit()
        with self.assertLogs('movie_list', level='INFO') as cm:
            app.run()
        self.assertEqual(
            cm.output,
            [
                'INFO:movie_list.app:Starting Now ...',
                'INFO:movie_list.app:Cache Warmup Succeeded',
                (f'INFO:movie_list.cache_refresher:'
                    f'Starting CacheRefresher Thread'),
                'INFO:movie_list.app:Server Starting 0.0.0.0:8000',
                (f'INFO:movie_list.cache_refresher:'
                    f'Stopping CacheRefresher Thread'),
                'INFO:movie_list.app:Server Stopping 0.0.0.0:8000',
            ]
        )
        mock_films.assert_called_once
        mock_cache_refresher.start.assert_called_once
        mock_cache_refresher.run.assert_called_once
        mock_serve_forever.assert_called_once
        mock_cache_refresher.stop.assert_called_once
        mock_cache_refresher.join.assert_called_once
        mock_server_close.assert_called_once
