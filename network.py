import requests
from spinner import start_spinner, stop_spinner

# Custom exception for network-related errors
class NetworkError(Exception):
    def __init__(self, message="An unexpected network error occurred"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"NetworkError: {self.message}"
...

USER_AGENT_HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# GET network operation
def network_GET(baseUrl, endpoint, params=None, raiseStatus=True):
    (stop, thread) = start_spinner()
    try:
        headers = { **USER_AGENT_HEADER }
        response = requests.get(f"{baseUrl}/{endpoint}", params=params, headers=headers)
        if raiseStatus: response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise NetworkError(f"An error occurred with the request: {e}")
    except TypeError as e:
        raise NetworkError(f"There was an issue with your parameters: {e}")
    except Exception as e:
        raise NetworkError(f"An unexpected error occurred: {e}")
    finally:
        stop_spinner(stop, thread)
...

# POST network operation
def network_POST(baseUrl, endpoint, data, raiseStatus=True):
    (stop, thread) = start_spinner()
    try:
        response = requests.post(f"{baseUrl}/{endpoint}", json=data)
        if raiseStatus: response.raise_for_status()
        return response
    except requests.RequestException as e:
        raise NetworkError(f"An error occurred with the request: {e}")
    except TypeError as e:
        raise NetworkError(f"There was an issue with your request data: {e}")
    except Exception as e:
        raise NetworkError(f"An unexpected error occurred: {e}")
    finally:
        stop_spinner(stop, thread)
...
