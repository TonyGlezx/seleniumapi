import unittest
import asyncio
import json
from SeleniumAPI import SeleniumAPI
from unittest.mock import patch, MagicMock
import time

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
    def setUp(self):
        self.login_url = 'https://reqres.in/api/users'  # Placeholder login url
        self.main_url = 'https://reqres.in/api/users'  # Placeholder main url
        self.selenium_api = SeleniumAPI(self.login_url, self.main_url)

    def tearDown(self):
        self.selenium_api.quit()
        self.assertIsNone(self.selenium_api.driver)

    def test_init(self):
        self.assertEqual(self.selenium_api.login_url, self.login_url)
        self.assertEqual(self.selenium_api.main_url, self.main_url)
        self.assertEqual(self.selenium_api.requests_count, 0)
        self.assertTrue(isinstance(self.selenium_api.time_of_last_request, float))

    def test_call_get(self):
      url = 'https://reqres.in/api/users'  # Public API url
      method = 'GET'
      headers = {'Content-Type': 'application/json'}
      response = asyncio.run(self.selenium_api.call(url, method, headers))
      self.assertIsNotNone(response)        
      self.assertIn('data', response)

    
    def test_call_post(self):
        url = 'https://reqres.in/api/users'  # Public API url
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        payload = {'name': 'John Doe', 'job': 'Software Engineer'}
        response = asyncio.run(self.selenium_api.call(url, method, headers, payload))
        response = json.dumps(response)
        self.assertIsNotNone(response)        
        self.assertIn('id', response)

    @patch('time.time', side_effect=time_side_effect())
    @patch('time.sleep', autospec=True)
    def test_rate_limit_check(self, mock_sleep, mock_time):
        for _ in range(120):  # perform 120 requests
            self.selenium_api.rate_limit_check()
        self.assertEqual(self.selenium_api.requests_count, 120)  # should be 120 requests
        self.assertEqual(mock_sleep.call_count, 0)  # sleep should not have been called
        self.selenium_api.rate_limit_check()  # 121st request, should hit rate limit
        self.assertEqual(self.selenium_api.requests_count, 0)  # should be reset to 0
        self.assertAlmostEqual(mock_sleep.call_args[0][0], 60, delta=1)  # sleep should have been called once with argument around 60
   
    
    @patch('SeleniumAPI.webdriver.Chrome.execute_async_script', side_effect=Exception('Network Error'))
    def test_call_with_error(self, mock_method):
        url = 'https://reqres.in/api/users'  # Public API url
        method = 'POST'
        payload = {'name': 'John Doe', 'job': 'Software Engineer'}
        payload = {'title': 'foo', 'body': 'bar', 'userId': 1}
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers, payload))

    @patch('SeleniumAPI.pickle.load', side_effect=Exception('Corrupted cookie file'))
    def test_init_with_corrupted_cookie(self, mock_method):
        with self.assertRaises(Exception):
            SeleniumAPI(self.login_url, self.main_url, 'corrupted_file.pkl')

    @patch('SeleniumAPI.webdriver.Chrome.get', side_effect=Exception('Invalid URL'))
    def test_init_with_invalid_url(self, mock_method):
        with self.assertRaises(Exception):
            SeleniumAPI('invalid_url', self.main_url)    

    def test_simultaneous_instances(self):
        selenium_api2 = SeleniumAPI(self.login_url, self.main_url)
        self.assertNotEqual(id(self.selenium_api), id(selenium_api2))

    @patch('SeleniumAPI.webdriver.Chrome.get', side_effect=Exception('Non-existent URL'))
    def test_non_existent_urls(self, mock_method):
        with self.assertRaises(Exception):
            SeleniumAPI('non_existent_url', self.main_url)

    def test_call_missing_url(self):
        method = 'GET'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(None, method))

    def test_call_missing_method(self):
        url = 'https://reqres.in/api/users'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, None))

    def test_call_missing_headers(self):
        url = 'https://reqres.in/api/users'
        method = 'POST'
        payload = {'name': 'John Doe', 'job': 'Software Engineer'}
        response = asyncio.run(self.selenium_api.call(url, method, None, payload))
        self.assertIsNotNone(response)        
        self.assertIn('id', response)
    
    def test_call_missing_payload(self):
        url = 'https://reqres.in/api/users'
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        response = asyncio.run(self.selenium_api.call(url, method, headers, None))
        self.assertIsNotNone(response)
    

    def test_call_missing_url_and_method(self):
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(None, None))

    def test_call_missing_url_and_headers(self):
        method = 'GET'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(None, method, None))

    def test_call_missing_url_and_payload(self):
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(None, method, headers, None))

    def test_call_missing_method_and_headers(self):
        url = 'https://reqres.in/api/users'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, None, None))

    def test_call_missing_method_and_payload(self):
        url = 'https://reqres.in/api/users'
        headers = {'Content-Type': 'application/json'}
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, None, headers, None))

    def test_call_missing_headers_and_payload(self):
        url = 'https://reqres.in/api/users'
        method = 'POST'
        response = asyncio.run(self.selenium_api.call(url, method, None, None))
        self.assertIsNotNone(response)

    def test_call_missing_all(self):
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(None, None, None, None))
    """"
    def test_concurrency(self):
        async def perform_call():
            url = 'https://reqres.in/api/users'
            method = 'GET'
            return await self.selenium_api.call(url, method)

        tasks = [perform_call() for _ in range(5)]
        responses = asyncio.run(asyncio.gather(*tasks))

        for response in responses:
            self.assertIsNotNone(response)
    """

    def test_cleanup(self):
        self.selenium_api.quit()
        self.assertIsNone(self.selenium_api.driver)
    """"
    def test_retry_logic(self):
        url = 'https://reqres.in/api/users'
        method = 'GET'

        with patch('SeleniumAPI.webdriver.Chrome.execute_async_script', side_effect=[Exception('Temporary failure'), None]) as mock_method:
            asyncio.run(self.selenium_api.call(url, method))
            self.assertEqual(mock_method.call_count, 2)
    """

    @patch('SeleniumAPI.webdriver.Chrome', side_effect=Exception('Failed to initialize driver'))
    def test_dependency_failure(self, mock_method):
        with self.assertRaises(Exception):
            SeleniumAPI(self.login_url, self.main_url)
    """"
    def test_long_running_operations(self):
        url = 'https://reqres.in/api/users'
        method = 'POST'
        payload = {'name': 'John Doe', 'job': 'Software Engineer'}
        headers = {'Content-Type': 'application/json'}
        start_time = time.time()
        response = asyncio.run(self.selenium_api.call(url, method, headers, payload))
        end_time = time.time()
        self.assertGreater(end_time - start_time, 1)  # Assuming a long-running operation takes more than 1 second
    """
    def test_data_consistency(self):
        url = 'https://reqres.in/api/users'
        method = 'GET'

        response1 = asyncio.run(self.selenium_api.call(url, method))
        response2 = asyncio.run(self.selenium_api.call(url, method))

        self.assertEqual(response1, response2)

    @patch('SeleniumAPI.logging.Logger.error')
    def test_logging(self, mock_error):
        url = 'https://reqres.in/api/users'
        method = 'POST'
        headers = {'Content-Type': 'application/json'}
        payload = 'invalid_payload'

        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers, payload))

        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers, payload))

        mock_error.assert_called()
    def test_call_unknown_method(self):
        url = 'https://reqres.in/api/users'
        method = 'UNKNOWN_METHOD'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method))
    
    def test_call_missing_headers_and_invalid_method(self):
        url = 'https://reqres.in/api/users'
        method = 'BAD_METHOD'
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, None))
    
    def test_call_invalid_headers_and_method(self):
        url = 'https://reqres.in/api/users'
        method = 'BAD_METHOD'
        headers = {'Invalid-Header': 'Invalid Value'}
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers))
    
    def test_call_bad_method_and_bad_payload(self):
        url = 'https://reqres.in/api/users'
        method = 'BAD_METHOD'
        headers = {'Content-Type': 'application/json'}
        payload = 'invalid_payload'  # Providing a string instead of a dictionary
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers, payload))
    
    def test_call_invalid_method_and_missing_payload(self):
        url = 'https://reqres.in/api/users'
        method = 'INVALID_METHOD'
        headers = {'Content-Type': 'application/json'}
        with self.assertRaises(Exception):
            asyncio.run(self.selenium_api.call(url, method, headers, None))



if __name__ == '__main__':
    unittest.main()
