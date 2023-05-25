# SeleniumAPI

The `SeleniumAPI` class provides a wrapper for interacting with web APIs using Selenium and the Chrome WebDriver. It enables making asynchronous API calls and includes a rate limit mechanism to ensure requests are made within specified limits.

## Features

- Asynchronous API calls using `XMLHttpRequest` in the browser context.
- Automatic handling of request headers, payload, and response handling.
- Rate limit enforcement to prevent exceeding a specified number of requests within a specific time frame.
- Chrome WebDriver integration for automated browser interactions.

## Installation

To use the `SeleniumAPI` class, you need to have Python 3.x and the necessary dependencies installed. Follow these steps:

1. Install the required packages using pip:
`pip install selenium`

2. Download the appropriate Chrome WebDriver for your operating system from the official Selenium website: [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

3. Extract the WebDriver executable and make sure it is accessible in your system's `PATH`.

## Usage

To use the `SeleniumAPI` class, follow these steps:

1. Create an instance of the SeleniumAPI class, providing the login URL, main URL, and optionally the path to a cookies file:

`api = SeleniumAPI(login_url='https://example.com/login', main_url='https://example.com/main', cookies_file='cookies.pkl')`

2. Use the call method to make API requests:

```
url = 'https://example.com/api/endpoint'
method = 'GET'
headers = {'Content-Type': 'application/json'}
response = api.call(url, method, headers=headers)
```

3. Handle the API response according to your requirements.

4. Quit the SeleniumAPI instance when done:
`api.quit()`

##Known issues
- Error handling when POST call with missing payload returns a bad response.
- Tests for batch jobs and concurrency didn't pass.

##ToDO
- Handling non-json responses
- Test for DEL and PUT requests.




