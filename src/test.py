from translator import AmadeusTranslator
from audio import AmadeusVoice
from brain import AmadeusBrain
from emo import AmadeusEmo
from characterai import PyCAI
from sprite import AmadeusSprite


def test_translator():
    translator = AmadeusTranslator()
    translated_text = translator.translate("hello", "en", "es")
    assert translated_text == "hola" or translated_text == "Hola"

    text = "In the pursuit of time travel, it is difficult to predict which country will prevail. Several countries have been researching and developing the technology, and it is a very complex and daunting task. However, it seems likely that whoever succeeds first in developing a fully functional time machine will establish themselves as the leader in the field and have a significant advantage over the other nations."
    translated = translator.translate(text, "en", "ja")
    print(translated)

def test_audio():
    tts = AmadeusVoice()
    response = tts.save_voice("hello", "en", "ja")
    # with open("asset/audio.flac", "wb") as file:
    #     file.write(response)

def test_brain():
    processor = AmadeusBrain()
    question = "I think our project is going to be a success"
    # response = processor(question, "gemini")
    # print(response)
    response = processor(question, "cai")
    print(response)

def test_cai():
    token = "d301b6ee6b8949e00dd03eea08ce0f3e53dae469"
    client = PyCAI(token)

    char = "NbOISAxpDy88mPv7YB-PfHFwNzVcZv0GDA2OlcWgeZY"
    chat = client.chat.get_chat(char)

    participants = chat['participants']

    if not participants[0]['is_human']:
        tgt = participants[0]['user']['username']
    else:
        tgt = participants[1]['user']['username']

    while True:
        message = input('You: ')

        data = client.chat.send_message(
            chat['external_id'], tgt, message
        )

        name = data['src_char']['participant']['name']
        text = data['replies'][0]['text']

        print(f"{name}: {text}")

def test_emo_predictor():
    emo = AmadeusEmo()
    emo = emo.predict_emo("wh-what did you say?")
    print(emo)

def test_sprite():
    spr = AmadeusSprite()
    t = spr.make_sprite("Angry", duration=12000)
    print(t)

if __name__ == "__main__":
    test_translator()
    # test_audio()
    # test_brain()
    # test_cai()
    # test_emo_predictor()
    # test_sprite()
    print("All tests passed!")