# SeleniumAPI

Welcome to SeleniumAPI, a streamlined utility for executing API calls directly from a Selenium driver. Designed with the needs of developers in mind, SeleniumAPI provides a solution for enhancing API interactions within a browser context.

Discover the unique benefits and innovative applications of SeleniumAPI:

**1. Advanced Website Testing & Validation**

SeleniumAPI allows you to make API calls on-the-go during your Selenium test sessions. This functionality provides the ability to cross-verify server responses with website UI, elevating the accuracy of your end-to-end testing.

**2. Comprehensive User Experience Simulation**

Recreate detailed user interactions that integrate UI manipulation and API calls. SeleniumAPI provides an accurate representation of user-triggered API calls, generating realistic data for improved UX analysis.

**3. Streamlined Automation & Web Scraping**

Enhance your data extraction processes by reaching application-specific data, usually hidden behind API calls, directly from your Selenium driver. Broaden the scope of your web scraping tasks by accessing dynamic data that might be unavailable through the page source.

**4. Optimal Proxy Usage**

Leverage your Selenium WebDriver's proxy settings during API interactions. This feature proves particularly useful for maintaining IP rotation during extensive web scraping operations or managing region-specific API responses.

**5. Intelligent Rate Limiting Management**

SeleniumAPI facilitates the handling of rate-limited APIs within the browsing context. By interspersing API requests with regular browser activity, it offers a sophisticated approach to managing request quotas.

SeleniumAPI seeks to redefine the boundaries of Selenium and API interaction by offering a solution tailored to the needs of today's developers. Step forward into a more dynamic browsing experience with SeleniumAPI.

# SeleniumAPI Installation Guide

Follow these simple steps to install SeleniumAPI and start executing API calls directly from a Selenium driver:

## Prerequisites

- [Python](https://www.python.org/downloads/) (version 3.6 or higher)
- [pip](https://pip.pypa.io/en/stable/installation/)

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/TonyGlezx/seleniumapi
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd seleniumapi
    ```

3. **Create a Virtual Environment (Optional but Recommended)**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

4. **Install the Package**

    ```bash
    pip install .
    ```

Now, you're ready to use SeleniumAPI in your projects!

To import and use the `SeleniumAPI` class in your own scripts, use:

```python
from SeleniumAPI import SeleniumAPI
```

# Examples of SeleniumAPI Usage

The following examples demonstrate some of the innovative ways you can leverage SeleniumAPI in your projects:

## Example 1: Real-Time Website Testing & Validation

You can use SeleniumAPI to make API calls while navigating a website, and cross-check the server's responses against the UI elements:

```python
from SeleniumAPI import SeleniumAPI
from selenium import webdriver

driver = webdriver.Firefox()
api = SeleniumAPI(driver)

response = api.call("https://api.example.com/data", method="GET")

# Now, compare the response with a UI element
element = driver.find_element_by_id("data-element")
assert element.text == response["data"]
```
### Example 2: User Experience Simulation

Perform detailed user interaction simulations that combine UI manipulation and API calls. Accurately mimic user-triggered API calls and collect user behavior data for UX analysis. Here's a simple demonstration of how you can achieve this with SeleniumAPI:

```python
from SeleniumAPI import SeleniumAPI
from selenium import webdriver

driver = webdriver.Firefox()
api = SeleniumAPI(driver)

# Navigate to the site and simulate user behavior
driver.get("https://www.example.com")
driver.find_element_by_id('submit_button').click()

# Perform the API call and collect data for UX analysis
response = api.call("https://api.example.com", method="POST", payload={"user_action": "click"})
```

## ToDo
- Handling non-json responses better
- Test case
- More Debug options
- Timeout management
- Improve performance with retry logic, long running operations and concurrency
- Return the full xhr object no matter the server response. Make it optional.
 
## Known issues
- Handle bad responses from POST calls with missing or malformed payloads. 
