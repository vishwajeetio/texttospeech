from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess

session = Session(profile_name="adminuser")
polly = session.client("polly")

OUTPUT_FORMAT = 'mp3'
TEXT_TYPE = 'ssml'
VOICE_ENGINE = 'neural'  # Make sure that your AWS region supports Neural voice

myssml = '<speak> \
    Hahahahaha.<break time="1s"/> Thank God \
        Ayy, ayy <sub alias="Ive been codin golang and poppin pillies">W3C</sub> Man, I feel just like a rockstar (ayy, ayy), \
            All my brothers got that gas, And they always be smokin like a Rasta. <break time="1s"/> codin with me, call up on a Uzi \
                <amazon:effect name="whispered">"And show up, man, them the shottas,"</amazon:effect> \
                    When my homies pull up on your block. \
                        <prosody rate="80%">They make that thing go grrra-ta-ta-ta</prosody> \
                            </speak>'

spoken_text = polly.synthesize_speech(Text=myssml, TextType=TEXT_TYPE, OutputFormat=OUTPUT_FORMAT, VoiceId='Matthew', Engine=VOICE_ENGINE)

with closing(spoken_text["AudioStream"]) as stream:
    output = "data/speech.mp3"
    with open(output, "wb") as file:
        file.write(stream.read())
        print("saved")

# Open the mp3 player and play the audio(optional):ss
if sys.platform == "win32":
    output = "data\speech.mp3"
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])