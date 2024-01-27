from elevenlabs import voices, set_api_key
import os.path
from dotenv import load_dotenv

load_dotenv()

xi_api_key = os.getenv('XI_API_KEY')
set_api_key(xi_api_key)

def get_desired_voice(name):
    voices_list = voices()
    for voice in voices_list:
        if voice.name == name:
            break
            return voice