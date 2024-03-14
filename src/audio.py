import os
import asyncio
from dotenv import load_dotenv
import requests
from translator import AmadeusTranslator
import json

load_dotenv()

class AmadeusVoice:
    def __init__(self):
        """
        class to get voice for Amadeus
        """

        self.hf_model_url = os.getenv("HUGGING_FACE_AUDIO_MODEL_URL")
        self.hf_auth = os.getenv("HUGGING_FACE_KEY")
        self.translator = AmadeusTranslator()
    
    def __call__(self, text, src, dest, method="hf"):
        return self.get_voice(text, src, dest, method)
    
    def get_voice(self, text, src, dest, method="hf"):
        if method == "hf":
            return self._get_voice_via_hf(text, src, dest)
        else:
            raise NotImplementedError("Voice method not implemented")
    
    def _get_voice_via_hf(self, text, src, dest):
        """
        get voice via HF
        """
        if src != dest:
            # translate the text
            # TODO: use the translator class
            text = self.translator(text, src, dest)
        
        # make the request
        while True:
            response = requests.post(
                            self.hf_model_url, 
                            headers={"Authorization": f"Bearer {self.hf_auth}"},
                            json={ "inputs": text}
                        )   
            if response.status_code == 200:
                return response.content

class AudioPlayer:
    def __init__(self):
        pass
    
    def play(self, file_path):
        pass