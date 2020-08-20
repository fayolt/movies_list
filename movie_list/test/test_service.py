import json
import requests

from unittest import TestCase, mock
from collections import defaultdict

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

    @mock.patch('movie_list.service.get_data', return_value=None)
    def test_movie_people_with_no_people_fetched(self, mock_get_data):
        expected_calls = [
            mock.call("/people")
        ]
        response = service.movie_people()
        mock_get_data.assert_called_once
        mock_get_data.assert_has_calls(expected_calls)
        self.assertEqual(response, {})

    @mock.patch('movie_list.service.get_data')
    @mock.patch('movie_list.service.client.set')
    def test_movie_people_with_people(self, mock_client_set, mock_get_data):
        expected_calls = [
            mock.call("/people")
        ]
        people = [{
            "id": "89026b3a-abc4-4053-ab1a-c6d2eea68faa",
            "name": "Niya",
            "gender": "Male",
            "age": "NA",
            "eye_color": "White",
            "hair_color": "Beige",
            "films": [
                "/films/2de9426b-914a-4a06-a3a0-5e6d9d3886f6"
            ]
        }, {
            "id": "6b3facea-ea33-47b1-96ce-3fc737b119b8",
            "name": "Renaldo Moon aka Moon aka Muta",
            "gender": "Male",
            "age": "NA",
            "eye_color": "White",
            "hair_color": "Beige",
            "films": [
                "/films/90b72513-afd4-4570-84de-a56c312fdf81",
                "/films/2de9426b-914a-4a06-a3a0-5e6d9d3886f6"
            ]
        }]
        movie_people = {
            "2de9426b-914a-4a06-a3a0-5e6d9d3886f6":
                ["Niya", "Renaldo Moon aka Moon aka Muta"],
            "90b72513-afd4-4570-84de-a56c312fdf81":
                ["Renaldo Moon aka Moon aka Muta"]
        }
        mock_get_data.return_value = people
        response = service.movie_people()
        mock_get_data.assert_called_once
        mock_get_data.assert_has_calls(expected_calls)
        mock_client_set.assert_called_once
        self.assertEqual(response, movie_people)

    @mock.patch('movie_list.service.get_data', return_value=None)
    def test_films_without_films(self, mock_get_data):
        expected_calls = [
            mock.call("/films")
        ]
        response = service.films()
        mock_get_data.assert_called_once
        mock_get_data.assert_has_calls(expected_calls)
        self.assertIs(response, None)

    @mock.patch('movie_list.service.get_data')
    @mock.patch('movie_list.service.client.get')
    @mock.patch('movie_list.service.client.set')
    @mock.patch('movie_list.service.movie_people')
    def test_films_with_no_movie_people_cached(self,
                                               mock_movie_people,
                                               mock_client_set,
                                               mock_client_get, mock_get_data):
        films = [{
            "id": "2de9426b-914a-4a06-a3a0-5e6d9d3886f6",
            "people": [
                "https://ghibliapi.herokuapp.com/people/"
            ]
        }, {
            "id": "90b72513-afd4-4570-84de-a56c312fdf81",
            "title": "The Cat Returns",
            "people": [
                "https://ghibliapi.herokuapp.com/people/"
            ]}
        ]
        movie_people = {
            "2de9426b-914a-4a06-a3a0-5e6d9d3886f6":
                ["Niya", "Renaldo Moon aka Moon aka Muta"],
            "90b72513-afd4-4570-84de-a56c312fdf81":
                ["Renaldo Moon aka Moon aka Muta"]
        }
        expected_get_calls = [
            mock.call("movie-people")
        ]
        expected_set_calls = [
            mock.call("movies", films)
        ]
        output = [{
            "id": "2de9426b-914a-4a06-a3a0-5e6d9d3886f6",
            "people": [
                "Niya", "Renaldo Moon aka Moon aka Muta"
            ]
        }, {
            "id": "90b72513-afd4-4570-84de-a56c312fdf81",
            "title": "The Cat Returns",
            "people": [
                "Renaldo Moon aka Moon aka Muta"
            ]}
        ]
        mock_get_data.return_value = films
        mock_client_get.return_value = None
        mock_movie_people.return_value = movie_people
        response = service.films()
        mock_get_data.assert_called_once
        mock_client_get.assert_called_once
        mock_client_get.assert_has_calls(expected_get_calls)
        mock_movie_people.assert_called_once
        mock_client_set.assert_called_once
        mock_client_set.assert_has_calls(expected_set_calls)
        self.assertEqual(response, output)

    @mock.patch('movie_list.service.get_data')
    @mock.patch('movie_list.service.client.get')
    @mock.patch('movie_list.service.client.set')
    def test_films_with_movie_people_cached(self,
                                            mock_client_set,
                                            mock_client_get, mock_get_data):
        films = [{
            "id": "2de9426b-914a-4a06-a3a0-5e6d9d3886f6",
            "people": [
                "https://ghibliapi.herokuapp.com/people/"
            ]
        }, {
            "id": "90b72513-afd4-4570-84de-a56c312fdf81",
            "title": "The Cat Returns",
            "people": [
                "https://ghibliapi.herokuapp.com/people/"
            ]}
        ]
        movie_people = {
            "2de9426b-914a-4a06-a3a0-5e6d9d3886f6":
                ["Niya", "Renaldo Moon aka Moon aka Muta"],
            "90b72513-afd4-4570-84de-a56c312fdf81":
                ["Renaldo Moon aka Moon aka Muta"]
        }
        expected_get_calls = [
            mock.call("movie-people")
        ]
        expected_set_calls = [
            mock.call("movies", films)
        ]
        output = [{
            "id": "2de9426b-914a-4a06-a3a0-5e6d9d3886f6",
            "people": [
                "Niya", "Renaldo Moon aka Moon aka Muta"
            ]
        }, {
            "id": "90b72513-afd4-4570-84de-a56c312fdf81",
            "title": "The Cat Returns",
            "people": [
                "Renaldo Moon aka Moon aka Muta"
            ]}
        ]
        mock_get_data.return_value = films
        mock_client_get.return_value = json.dumps(movie_people).encode('utf-8')
        response = service.films()
        mock_get_data.assert_called_once
        mock_client_get.assert_called_once
        mock_client_get.assert_has_calls(expected_get_calls)
        mock_client_set.assert_called_once
        mock_client_set.assert_has_calls(expected_set_calls)
        self.assertEqual(response, output)

    @mock.patch('movie_list.service.client.get', return_value=None)
    def test_read_cache_miss(self, mock_client_get):
        response = service.read_cache()
        self.assertIs(response, None)

    @mock.patch('movie_list.service.client.get', return_value=b"{'data':True}")
    def test_read_cache_hit(self, mock_client_get):
        response = service.read_cache()
        self.assertEqual(response, {'data': True})
