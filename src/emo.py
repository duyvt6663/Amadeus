from dotenv import load_dotenv
import os
from prompt import emo_prompt
import google.generativeai as genai 
from config import generation_config, safety_settings

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AmadeusEmo:
    
    emotions=[
        "Sleep","Interest","Sad","Very Default","Wink","Serious","Disappoint","Tired","Fun","Angry","Embarassed","Very Not Interest","Default","Very Embarassed","Calm","Very Serious","Surprise","Not Interest","Closed Sleep","Back"
    ]

    def __init__(self):
        self.base_prompt = emo_prompt
        self.predictor = genai.GenerativeModel(
                                model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings
                            )

    def predict_emo(self, text):
        full_prompt = self.base_prompt + ["input: " + text, "output: "]
        response = self.predictor.generate_content(full_prompt)
        emo = response.text.strip(" ").strip("[").strip("]")
        return emo
