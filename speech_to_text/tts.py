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
            input=texttospeech.StreamingSynthesisInput(text="How can I help you today?")
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
