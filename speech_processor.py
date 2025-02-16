from google.cloud import speech

def transcribe_audio_chunks(audio_chunks: list) -> str:
    """
    Combine the audio chunks and transcribe them using Google Speech-to-Text.
    
    Assumes audio_chunks is a list of bytes and that the audio is LINEAR16
    with a sample rate of 16000 Hz.
    """
    client = speech.SpeechClient()

    # Combine the chunks into one continuous byte stream.
    audio_content = b"".join(audio_chunks)
    audio = speech.RecognitionAudio(content=audio_content)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Adjust as needed for your audio.
        language_code="en-US"
    )
    
    # Use the synchronous recognize method
    response = client.recognize(config=config, audio=audio)
    
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    return transcript.strip()