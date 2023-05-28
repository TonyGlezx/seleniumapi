from SeleniumAPI import SeleniumAPI

import unittest
import asyncio
import json
from SeleniumAPI import SeleniumAPI
from unittest.mock import patch, MagicMock
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def time_side_effect():
    # yield the first few specified values
    for val in [0, 0.01, 61.01]:
        yield val
    # after the first few, yield an incrementing value
    counter = 62.01
    while True:
        yield counter
        counter += 1


class TestSeleniumAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.driver = None

    def test_call_get(self):
        url = "https://reqres.in/api/users"  # Public API url
        method = "GET"
        headers = {"Content-Type": "application/json"}
        self.driver.get(url)
        response = SeleniumAPI(self.driver, url, method, headers)
        self.assertIsNotNone(response)
        self.assertIn("data", response)

    def test_call_post(self):
        url = "https://reqres.in/api/users"  # Public API url
        method = "POST"
        headers = {"Content-Type": "application/json"}
        payload = {"name": "John Doe", "job": "Software Engineer"}
        self.driver.get(url)
        response = SeleniumAPI(self.driver, url, method, headers, payload)
        response = json.dumps(response)
        self.assertIsNotNone(response)
        self.assertIn("id", response)

    def test_call_put(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        method = "PUT"
        headers = {"Content-Type": "application/json"}
        payload = {"id": 1, "title": "foo", "body": "bar", "userId": 1}
        self.driver.get(url)
        response = SeleniumAPI(self.driver, url, method, headers, payload)
        self.assertIsNotNone(response)
        self.assertIn("title", response)

    def test_call_delete(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        method = "DELETE"
        self.driver.get(url)
        response = SeleniumAPI(self.driver, url, method)
        # The response from a DELETE request to the JSONPlaceholder API is an empty object, so we'll check for that.
        self.assertEqual(response, {})

    def test_call_patch(self):
        url = "https://jsonplaceholder.typicode.com/posts/1"
        method = "PATCH"
        headers = {"Content-Type": "application/json"}
        payload = {"title": "foo"}
        self.driver.get(url)
        response = SeleniumAPI(self.driver, url, method, headers, payload)
        self.assertIsNotNone(response)
        self.assertIn("title", response)

    def test_call_with_error(self):
        url = "https://reqres.in/api/users"  # Public API url
        method = "POST"
        payload = {"name": "John Doe", "job": "Software Engineer"}
        payload = {"title": "foo", "body": "bar", "userId": 1}
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, method, headers, payload)

    def test_non_existent_urls(self):
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, "non_existent_url")

    def test_call_missing_url(self):
        method = "GET"
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, None, method)

    def test_call_missing_method(self):
        url = "https://reqres.in/api/users"
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, None)

    def test_call_missing_headers(self):
        url = "https://reqres.in/api/users"
        method = "POST"
        payload = {"name": "John Doe", "job": "Software Engineer"}
        response = SeleniumAPI(self.driver, url, method, None, payload)
        self.assertIsNotNone(response)
        self.assertIn("id", response)

    def test_call_missing_payload(self):
        url = "https://reqres.in/api/users"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, method, headers, None)

    def test_call_missing_driver(self):
        method = "GET"
        with self.assertRaises(Exception):
            url = "https://reqres.in/api/users"
            SeleniumAPI(None, url, method)

    def test_call_missing_url_and_method(self):
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, None, None)

    def test_call_missing_url_and_headers(self):
        method = "GET"
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, None, method, None)

    def test_call_missing_url_and_payload(self):
        method = "POST"
        headers = {"Content-Type": "application/json"}
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, None, method, headers, None)

    def test_call_missing_method_and_headers(self):
        url = "https://reqres.in/api/users"
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, None, None)

    def test_call_missing_method_and_payload(self):
        url = "https://reqres.in/api/users"
        headers = {"Content-Type": "application/json"}
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, None, headers, None)

    def test_call_missing_headers_and_payload(self):
        url = "https://reqres.in/api/users"
        method = "POST"
        response = SeleniumAPI(self.driver, url, method, None, None)
        self.assertIsNotNone(response)

    def test_call_missing_payload(self):
        url = "https://reqres.in/api/users"
        method = "POST"
        headers = {"Content-Type": "application/json"}
        with self.assertRaises(Exception):
            SeleniumAPI(self.driver, url, method, headers, None)

    def test_call_missing_all(self):
        with self.assertRaises(Exception):
            SeleniumAPI(None, None, None, None, None)


if __name__ == "__main__":
    unittest.main()
