import json
import logging


def SeleniumAPI(driver, url, method_original, headers=None, payload=None):
    logger = logging.getLogger(f"Starting Selenium {method_original }API call to {url}")

    if not url or not method_original:
        raise ValueError("URL or method is missing")

    method = method_original.upper()

    headers_script = "\n".join(
        f'xhr.setRequestHeader("{header}", "{value}");'
        for header, value in (headers or {}).items()
    )

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

    response = driver.execute_async_script(script)

    if response and response.get("ok") and response.get("response", "").strip():
        return json.loads(response["response"])
    else:
        error_message = f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}"
        logger.error(error_message)
        raise Exception(error_message)
