from typing import List
import requests


class Cerebrate:
    def __init__(self, api_key: str, url: str = 'https://app.cerebrate.ai/api/predict'):
        self._api_key = api_key
        self._url = url

    def predict(self, task: str, examples: [str], query: str) -> List[str]:
        examples_string = '\n'.join(examples)
        prompt = f"{task}\n\nexamples:\n{examples_string}\n\n{query}"

        response = self._send_request(prompt)
        return list(response)

    def raw(self, prompt: str) -> List[str]:
        response = self._send_request(prompt)

        return list(response)

    # def match(self):
    #     raise Exception("Not implemented!")

    # def recommend(self):
    #     raise Exception("Not implemented!")

    def _send_request(self, prompt: str):
        body = {
            "data": {
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 100,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "stop": ["Q:"],
                "best_of": 1,
            }
        }

        response = requests.post(
            self._url,
            json=body,
            headers={"Authorization": self._api_key, "Content-Type": "application/json"}
        )
        if response.status_code != 200:
            raise Exception('error making request to cerebrate')

        return response.json()
