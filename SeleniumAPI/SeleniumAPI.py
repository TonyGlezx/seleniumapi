import json
import logging

# Configure the logging
logging.basicConfig(level=logging.INFO)  # This will enable all debug logs

def SeleniumAPI(driver, url, method_original, headers=None, payload=None):
    logger = logging.getLogger(f"SeleniumAPI")
    logger.debug(f"Starting Selenium {method_original} API call to {url}")

    if not url or not method_original:
        logger.error("URL or method is missing")
        raise ValueError("URL or method is missing")

    method = method_original.upper()
    logger.debug(f"HTTP Method: {method}")

    if headers:
        logger.debug(f"Headers: {headers}")
    headers_script = "\n".join(
        f'xhr.setRequestHeader("{header}", "{value}");'
        for header, value in (headers or {}).items()
    )

    # Prepare the payload for insertion into the JavaScript snippet
    payload_script = 'null' if payload is None else json.dumps(payload, ensure_ascii=False)
    logger.debug(f"Payload: {payload_script}")

    script = f""" 
        var callback = arguments[arguments.length - 1];
        try {{
            var xhr = new XMLHttpRequest();
            xhr.open("{method}", "{url}", true);
            {headers_script}
            xhr.onload = function () {{
                if (xhr.status >= 400) {{
                    callback({{"ok": false, "status": xhr.status, "statusText": xhr.statusText, "error": "Error response from server"}});
                }} else if (xhr.responseText !== "") {{
                    try {{
                        //var jsonResponse = JSON.parse(xhr.responseText);
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
            xhr.send({payload_script});
        }} catch(err) {{
            callback({{"ok": false, "status": 0, "statusText": "", "error": err.message}});
        }}
    """
    logger.debug("Executing script on the browser...")
    response = driver.execute_async_script(script)
    
    logger.debug(f"Response received: {response}")

    if response:
        logger.debug(f"Response OK: {response.get('ok')}")
        if response.get("ok"):
            logger.debug(f"Valid response: {response.get('response')}")
            if isinstance(response.get("response"), str):
                try:
                    # Attempt to parse the response as JSON
                    return json.loads(response["response"])
                except json.JSONDecodeError:
                    # If an error is raised, return the response as a plain string
                    logger.debug("Response is not valid JSON. Returning as plain text.")
                    return response["response"]
            else:
                return response["response"]

        else:
            error_message = f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}"
            logger.error(error_message)
            raise Exception(error_message)
    else:
        logger.error("No response received")
        raise Exception("No response received")
