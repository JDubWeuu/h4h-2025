#!/usr/bin/env python
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Google Cloud Text-To-Speech API streaming sample application .

Example usage:
    python streaming_tts_quickstart.py
"""


#!/usr/bin/env python
# Plays audio from the Google Cloud Text-to-Speech streaming API on your speakers.

from google.cloud import texttospeech
import itertools
import pyaudio

def run_streaming_tts_quickstart():
    """Synthesizes speech from a stream of input text and plays it on your speakers."""
    client = texttospeech.TextToSpeechClient()

    # Configure voice and audio settings.
    streaming_config = texttospeech.StreamingSynthesizeConfig(
        voice=texttospeech.VoiceSelectionParams(
            name="en-US-Journey-D",
            language_code="en-US"
        ),
    )

    # The first request must contain the configuration.
    config_request = texttospeech.StreamingSynthesizeRequest(
        streaming_config=streaming_config
    )

    # Request generator. Replace these hardcoded chunks with your LLM output if needed.
    def request_generator():
        yield texttospeech.StreamingSynthesizeRequest(
            input=texttospeech.StreamingSynthesisInput(text="Hello there. ")
        )
        yield texttospeech.StreamingSynthesizeRequest(
            input=texttospeech.StreamingSynthesisInput(text="How are you ")
        )
        yield texttospeech.StreamingSynthesizeRequest(
            input=texttospeech.StreamingSynthesisInput(text="today? It's ")
        )
        yield texttospeech.StreamingSynthesizeRequest(
            input=texttospeech.StreamingSynthesisInput(text="such nice weather outside.")
        )

    # Chain the config and text requests.
    streaming_requests = itertools.chain([config_request], request_generator())
    
    # Start streaming synthesis.
    streaming_responses = client.streaming_synthesize(streaming_requests)
    
    # Set up PyAudio to play the audio.
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,  # 16-bit PCM.
        channels=1,              # Mono audio.
        rate=24000,              # Must match the TTS audio_config sample rate.
        output=True
    )
    
    # Play the streamed audio.
    for response in streaming_responses:
        if response.audio_content:
            stream.write(response.audio_content)
    
    # Clean up the PyAudio stream.
    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    run_streaming_tts_quickstart()
