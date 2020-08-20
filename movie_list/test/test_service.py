from unittest import TestCase, mock

import requests

from movie_list import service


class TestService(TestCase):

    @mock.patch("movie_list.service.requests.get")
    def test_get_data_when_response_is_ok(self, mock_get):
        data = [{
            'id': "2baf70d1-42bb-4437-b551-e5fed5a87abe",
            "title": "Castle in the Sky",
            "director": "Hayao Miyazaki",
            "producer": "Isao Takahata",
            "release_date": "1986",
            "rt_score": "95"
        }]
        mock_get.return_value = mock.Mock(ok=True)
        mock_get.return_value.json.return_value = data
        response = service.get_data("/path")
        mock_get.assert_called_once
        self.assertListEqual(response, data)

    @mock.patch('movie_list.service.requests.get')
    def test_get_data_when_response_is_not_ok(self, mock_get):
        mock_get.return_value.ok = False
        response = service.get_data("/path")
        self.assertRaises(requests.exceptions.HTTPError)

    @mock.patch('movie_list.service.requests.get',
                side_effect=requests.exceptions.Timeout())
    def test_get_data_when_timeout(self, mock_get):
        response = service.get_data("/path")
        self.assertRaises(requests.exceptions.Timeout)
        self.assertIs(response, None)
