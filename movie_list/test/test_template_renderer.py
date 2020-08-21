import os
from unittest import TestCase

from movie_list import template_renderer


class TestTemplateRenderer(TestCase):

    def test_render(self):
        movie = {
            'title': 'Titanic',
            'director': 'Steven Spielberg'
        }
        template_dir = os.path.join(os.path.dirname(__file__), 'static')
        response = template_renderer.render(template_dir,
                                            'template.txt', movie=movie)
        self.assertEqual(response, 'Titanic by Steven Spielberg')
