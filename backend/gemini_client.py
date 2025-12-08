import requests

class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        headers = {}
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        try:
            resp = requests.post(url, headers=headers, json=data)
            resp.raise_for_status()
            response_json = resp.json()
            return response_json.get("candidates", [{}])[0].get("content", "")
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе к Gemini API: {e}"
