from bs4 import BeautifulSoup
import unittest
from watcher import get_event_title, get_event_city, get_event_date


class TestWatcher(unittest.TestCase):

    bs = None
    bs_bad = None

    def setUpClass():
        with open('event_tag.htm', 'r', encoding='utf-8') as f:
            html = f.read()
            TestWatcher.bs = BeautifulSoup(html, 'html.parser')

        with open('event_tag_bad.htm', 'r', encoding='utf-8') as f:
            html = f.read()
            TestWatcher.bs_bad = BeautifulSoup(html, 'html.parser')

    def test_get_event_title(self):

        self.assertEqual(
            get_event_title(TestWatcher.bs),
            'Poznej Digitální dovednosti'
        )
        self.assertEqual(get_event_title(TestWatcher.bs_bad), '?')

    def test_get_event_city(self):

        self.assertEqual(get_event_city(TestWatcher.bs), 'Online')
        self.assertEqual(get_event_city(TestWatcher.bs_bad), '?')

    def test_get_event_date(self):

        self.assertEqual(get_event_date(TestWatcher.bs), '14.11.')
        self.assertEqual(get_event_date(TestWatcher.bs_bad), '')


if __name__ == '__main__':
    unittest.main()
