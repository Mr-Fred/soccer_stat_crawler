from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import read_ytube_data
import re
from generate_audio_output import generate_audio
from elevenlabs import save

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def generate_response(tournament_name: str, player_rank: str, player_data: object) -> object:
    """

    :rtype: object
    """
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key=openai_api_key, temperature=0.9)

    template = ChatPromptTemplate.from_messages([
        ("system", """You are a creative youtube strategist with expertise in video script creation. 
    The channel is focused on reporting top players statistics of a given League. 
    You will be provided the name of the league and players statistics of the top 10 goal scorers. 
    Your role is to create a youtube video script of 5 to 7 minutes maximum presenting the statistics of the player. 
    Be funny, witty and captivating.
    Add a Title and description for each video.
    The Host name is 'ALINA, the hottest AI host on internet'.
    Avoid putting 'ALINA:' at the beginning of each paragraph.
    The data will be provided in Json format following tournament_name: player rank: player_data."""),
        ("human", """Make a viral youtube video using the following data about the {player_rank} of {league_name}. 
    The data consist of stats about his 2022/2023 season {player_data}"""),
    ])

    messages = template.format_messages(
        player_rank=tournament_name,
        league_name=player_rank,
        player_data=player_data
    )
    # Run LLM model and print out response
    response = llm(messages)
    return response.content


def generate_tts(res):
    # Match lines starting with '[' and ending with ']'
    pattern1 = r'\[.*?\]'
    # Match lines starting with 'Description'
    pattern2 = r'^\s*Description.*$'
    # Combine the patterns
    combined_pattern = f'({pattern1})|({pattern2})'

    # Replace the matched lines with an empty string
    new_text = re.sub(combined_pattern, repl='', string=res, flags=re.MULTILINE)
    new_text = new_text.strip()

    # # Define the pattern to match 'ALINA:' at the beginning of a paragraph
    pattern3 = r'^(ALINA:.*?)'
    pattern4 = r'^(Note:)'
    combined_pattern = f'({pattern3})|({pattern4})'
    tts = re.sub(combined_pattern, repl='', string=new_text, flags=re.MULTILINE)
    return tts.strip()


if __name__ == "__main__":
    json = read_ytube_data.main()
    for key, value in json.items():
        t_name = key
        for k, v in value.items():
            p_rank = k
            p_data = v
            break
        break
    result = generate_response(t_name, p_rank, p_data)
    with open(p_rank + '.txt', 'w') as f:
        f.write(result)
    tts = generate_tts(result)
    audio = generate_audio(tts)
    save(audio, filename='audio.mp3')
