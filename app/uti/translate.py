import aiohttp
import json


class Translator:
    def __init__(self, iam_token, folder_id):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.iam_token}"
        }
        self.translated_cache = {}

    async def translate(self, text, target_language="cv"):
        if text in self.translated_cache:
            return self.translated_cache[text]

        data = {
            "folder_id": self.folder_id,
            "texts": [text],
            "targetLanguageCode": target_language
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=json.dumps(data)) as response:
                if response.status == 200:
                    result = await response.json()
                    translated_text = result["translations"][0]["text"]
                    self.translated_cache[text] = translated_text
                    return translated_text
                else:
                    print(f"Ошибка перевода: {response.status}")
                    return None
