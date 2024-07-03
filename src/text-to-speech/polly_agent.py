from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import json
import subprocess
from datetime import datetime
from uuid import uuid4 as uuid
from tempfile import gettempdir


PROFILE_NAME = "asafg"

polly = None
agent_voices = ['Danielle', 'Gregory', 'Ivy', 'Joanna', 'Kendra', 'Kimberly', 'Salli', 'Joey',
                'Justin', 'Kevin', 'Matthew', 'Ruth', 'Stephen']

agent_voices_mapping = {
    'ui': 'Gregory',
    'orchestrator': 'Danielle',
    'llm-1': 'Stephen',
    'llm-2': 'Joey',
    'llm-3': 'Kendra'
}

def get_polly():
    global polly
    if polly is None:
        session = Session(profile_name=PROFILE_NAME)
        polly = session.client("polly")
    return polly


def create_file_name(source):
    timestamp = datetime.now().isoformat()
    return f'{timestamp}_{source}_{uuid()}.mp3'


def text_to_speech(message):
    polly = get_polly()
    source = json.loads(message).get('source')
    content = json.loads(message).get('message')
    text = f"{source} says {content}"
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                            VoiceId=agent_voices_mapping.get(source, agent_voices[0]),
                                            Engine="neural", LanguageCode="en-US",)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)


    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            file_name = create_file_name(source)
            output = os.path.join(gettempdir(), file_name)

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                print(f"Audio saved as {output}")
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        
    try:
        play_audio(output)
    except:
        print("Could not play audio")

def play_audio(output_file):
    # Play the audio using the platform's default player
    if sys.platform == "win32":
        os.startfile(output)
    else:
        # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, output_file])