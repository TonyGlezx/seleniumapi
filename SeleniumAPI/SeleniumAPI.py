import json
import logging

def SeleniumAPI(driver, url, method_original, headers=None, payload=None):
    logger = logging.getLogger('async_call')
 
    if not url or not method_original:
        raise ValueError("URL or method is missing")

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

        response = driver.execute_async_script(script)

        if response and response["ok"] and response["response"].strip():
            return json.loads(response["response"])
        else:
            logger.error(f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}")
            raise Exception(f"JavaScript error: {response.get('error')}, Status: {response.get('status')}, Status Text: {response.get('statusText')}")
            
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise