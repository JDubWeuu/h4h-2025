import wave

def inspect_wav_file(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()  # in bytes
        frame_rate = wav_file.getframerate()      # sample rate in Hz
        n_frames = wav_file.getnframes()
        duration = n_frames / frame_rate
        params = wav_file.getparams()

    print(f"Channels: {n_channels}")
    print(f"Sample Width (bytes): {sample_width}")
    print(f"Frame Rate (Hz): {frame_rate}")
    print(f"Number of Frames: {n_frames}")
    print(f"Duration (seconds): {duration}")
    print(f"Full Parameters: {params}")

# Example usage:
inspect_wav_file("uploads/recording.wav")