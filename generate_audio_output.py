import os.path
from dotenv import load_dotenv
from elevenlabs import generate, voices, set_api_key, save

load_dotenv()

xi_api_key = os.getenv('XI_API_KEY')
set_api_key(xi_api_key)

def get_desired_voice(name):
    voices_list = voices()
    for voice in voices_list:
        if voice.name == name:
            break
            return voice.name

def generate_audio(script):

    audio = generate(
        text=script,
        voice='Bella',
        model='eleven_monolingual_v1'
    )
    return audio

def main():
    script = "Hi my name is Alina, your hottest AI reporter on internet"
    mp3 = generate_audio(script)
    save(mp3, filename='aphrodite.mp3')
if __name__ == "__main__":
    main()

