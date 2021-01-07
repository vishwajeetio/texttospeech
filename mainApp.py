from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="adminuser")
polly = session.client("polly")

SSML_START = '<speak>'
SSML_END = '</speak>'
SSML_PAUSE = '<break time="1s"/>'
OUTPUT_FORMAT = 'mp3'
TEXT_TYPE = 'ssml'
VOICE_ENGINE = 'neural'  # Make sure that your AWS region supports Neural voice
AUDIO_STREAM = 'AudioStream'
TEMP_FILE_PREFIX = 'temp_'
FINAL_FILE_PREFIX = 'final_'
SLEEP = 0.2


myssml = '<speak> \
    He was caught up in the game.<break time="1s"/> In the middle of the \
        10/3/2014 <sub alias="World Wide Web Consortium">W3C</sub> meeting, \
            he shouted, "Nice job!" quite loudly. When his boss stared at him, he repeated \
                <amazon:effect name="whispered">"Nice job,"</amazon:effect> in a \
                    whisper. \
                        </speak>'




spoken_text = polly.synthesize_speech(Text=myssml, TextType=TEXT_TYPE, OutputFormat=OUTPUT_FORMAT, VoiceId='Matthew', Engine=VOICE_ENGINE)

    # The API response is rich and contains tons of information. 'AudioStream' is what holds the actual speech
    # recording. This is what we are writing to disk as a binary file.
#     with open(dir_to_store_output_files_abs_path + f'/%s' % temp_name, 'wb') as f:
#         f.write(spoken_text[AUDIO_STREAM].read())
#         f.close()





# response = polly.synthesize_speech(Text="Hello Overdosed SSH! Can I call you odssh", OutputFormat="mp3",
#                                         VoiceId="Matthew")
with closing(spoken_text["AudioStream"]) as stream:
    output = "speech.mp3"
    with open(output, "wb") as file:
        file.write(stream.read())
        print("saved")


if sys.platform == "win32":
    os.startfile(output)
else:
    # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    subprocess.call([opener, output])