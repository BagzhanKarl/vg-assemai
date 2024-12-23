import requests
import logging

class AssemMessage:
    def __init__(self):
        self.token = 'THjJOt2vo26nYYj4IbqKXVqInFv1wx55'
        self.url = 'https://gate.whapi.cloud/messages/'
        self.typing_time = 5
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {self.token}"
        }
        logging.basicConfig(level=logging.ERROR)

    def _send_request(self, endpoint, payload):
        try:
            response = requests.post(self.url + endpoint, json=payload, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "data": response.json()}
        except requests.exceptions.RequestException as e:
            logging.error(f"Request to {endpoint} failed: {e}")
            return {"success": False, "error": str(e)}

    def send_text(self, message, chat_id):
        payload = {
            "typing_time": self.typing_time,
            "to": chat_id,
            "body": message
        }
        return self._send_request("text", payload)

    def send_document(self, chat_id, file_url):
        payload = {
            "to": chat_id,
            "media": file_url
        }
        return self._send_request("documents", payload)
