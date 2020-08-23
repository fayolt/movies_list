import logging
import time

from datetime import timedelta
from unittest import TestCase, mock

from movie_list import cache_refresher, service


class TestCacheRefresher(TestCase):

    @mock.patch('movie_list.service.refresh')
    def test_refresher(self, mock_refresh):
        refresher = cache_refresher.CacheRefresher(
            "Refresher", timedelta(seconds=1),
            service.refresh)
        with self.assertLogs('movie_list.cache_refresher', level='INFO') as cm:
            refresher.start()
            refresher.shutdown_flag.set()
            refresher.join()
        self.assertEqual(
            cm.output,
            ['INFO:movie_list.cache_refresher:Starting Refresher Thread']
        )
        mock_refresh.assert_called_once
