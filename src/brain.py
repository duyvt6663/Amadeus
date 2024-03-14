from dotenv import load_dotenv
import os
from prompt import kurisu_normal_prompt
import google.generativeai as genai 
from config import generation_config, safety_settings
from emo import AmadeusEmo
from characterai import PyCAI
from utils import timeit


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AmadeusBrain:

    def __init__(self):
        """
        class to process the text
        """
        
        # initialize the Gemini processor
        self.base_prompt = kurisu_normal_prompt
        self.processor = genai.GenerativeModel(
                                model_name="gemini-1.0-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings
                            )

        # initialize the CAI session
        self.client = PyCAI(os.getenv("CAI_TOKEN"))
        self.chat = self.client.chat.get_chat(os.getenv("CAI_KURISU_ID"))

        participants = self.chat['participants']
        if not participants[0]['is_human']:
            self.tgt = participants[0]['user']['username']
        else:
            self.tgt = participants[1]['user']['username']
        
        # initialize the emotion predictor
        self.emo = AmadeusEmo()

        
    def __call__(self, text, method="gemini"):
        return self.process(text, method)
    
    def process(self, text, method="gemini"):
        if method == "gemini":
            return self._process_via_gemini(text)
        elif method == "cai":
            return self._process_via_cai(text)
        else:
            raise NotImplementedError("Processing method not implemented")
    
    # @timeit
    def _process_via_gemini(self, text):
        """
        process the text via Gemini
        """
        
        # make prompt
        full_prompt = self.base_prompt + ["input: " + text, "output: "]

        # make the request
        response = self.processor.generate_content(full_prompt)

        # post-process the response
        emo, ans = response.text.split("\n",1)[0].strip(" ").strip("[").strip("]"), response.text.split("\n",1)[1]

        return emo, ans
    
    # @timeit
    def _process_via_cai(self, text):
        """
        process the text via CAI
        """
        
        # make the request
        response = self.client.chat.send_message(
                        self.chat['external_id'], self.tgt, text
                    )
        ans = response['replies'][0]['text']
        
        # predict the emotion from the answer
        emo = self.emo.predict_emo(ans)

        return emo, ans
