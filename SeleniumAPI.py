import asyncio
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import pickle


class SeleniumAPI:
    def __init__(self, login_url, main_url, cookies_file=None):
        self.logger = logging.getLogger('SeleniumAPI')
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)        
        self.login_url = login_url
        self.main_url = main_url
        self.cookies_file = cookies_file
        self.requests_count = 0
        self.time_of_last_request = time.time()

        if self.cookies_file:
            self.driver.get(self.login_url)
            time.sleep(random.randint(2, 5))  # random sleep

            cookies = pickle.load(open(self.cookies_file, "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        
        self.driver.get(self.main_url)
        time.sleep(random.randint(2, 5))  # random sleep

    def rate_limit_check(self):
      current_time = time.time()
      if self.requests_count >= 120:
          time_difference = current_time - self.time_of_last_request
          if time_difference < 60:
              time.sleep(60 - time_difference)
          self.requests_count = 0
          self.time_of_last_request = time.time()
      else:
          self.requests_count += 1
          self.time_of_last_request = current_time


    async def call(self, url, method_original, headers=None, payload=None):
        if not url or not method_original:
            raise ValueError("URL or method is missing")

        self.rate_limit_check()
        self.requests_count += 1
        method = method_original.upper()
    
        try:
            headers_script = ""
            if headers:
                for header, value in headers.items():
                    headers_script += f'xhr.setRequestHeader("{header}", "{value}");\n'

            script = f""" 
    var callback = arguments[arguments.length - 1];
    try {{
        var xhr = new XMLHttpRequest();
        xhr.open("{method}", "{url}", true);
        {headers_script if headers else ''}
        xhr.onload = function () {{
            if (xhr.status >= 400) {{
                callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": "Error response from server"}});
            }} else if (xhr.responseText !== "") {{
                try {{
                    JSON.parse(xhr.responseText);
                    callback({{"ok": true, "status": xhr.status, "statusText": xhr.statusText, "response": xhr.responseText}});
                }} catch (e) {{
                    callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": "Not valid JSON response"}});
                }}
            }} else {{
                callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": "Empty Response"}});
            }}
        }};
        xhr.onerror = function () {{ 
            callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": "Failed to execute request"}});
        }};
        xhr.send(JSON.stringify({json.dumps(payload) if payload else 'null'}));
    }} catch(err) {{
        callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": err.message}});
    }}
    """

            response = self.driver.execute_async_script(script)

            if response and response["ok"] and response["response"].strip():
                return json.loads(response["response"])
            else:
                self.logger.error(f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}")
                raise Exception(f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}")
            
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            raise


    def quit(self):
        # Check if driver is not None before calling quit
        if self.driver:
            self.driver.quit()
            self.driver = None
