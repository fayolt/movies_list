from unittest import TestCase

from movie_list import service_exit


class TestServiceExit(TestCase):

    def test_service_shutdown(self):
        with self.assertRaises(service_exit.ServiceExit):
            with self.assertLogs('movie_list.service_exit', level='INFO') as m:
                service_exit.service_shutdown(100, 2)
            self.assertEqual(
                m.output,
                ['INFO:movie_list.service_exit:Caught signal']
            )
