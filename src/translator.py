import os
import requests
from dotenv import load_dotenv

load_dotenv()

class AmadeusTranslator:
    
    def __init__(self):
        self.google_api = os.getenv("GOOGLE_TRANSLATE_URL")
    
    def __call__(self, text, src, dest, method="google"):
        return self.translate(text, src, dest, method)

    def translate(self, text, src, dest, method="google"):
        if method == "google":
            return self._google_translate(text, src, dest)
        else:
            raise NotImplementedError("Translator method not implemented")
    
    def _google_translate(self, text, src, dest):
        """
        translate the text using google translator
        """
        
        # Encode the text to be URL-safe
        encoded_text = requests.utils.quote(text)

        # make the request
        full_url = self.google_api.format(src, dest, encoded_text)
        response = requests.get(full_url)

        # post-process the response
        response = response.json()
        
        return ''.join(txt[0] for txt in response[0])

