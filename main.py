from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.mp3_model import AudioUploadResponse
from .speech_to_text.speech_from_audio import transcribe_file
import aiofiles
import subprocess
import os
from .browser.lchain import get_flights, checkout_flight


app = FastAPI()

COUNT = 0
DATA = ""
origins = [
    "http://localhost:3000"
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

audio_chunks = []

def convert_mp3_to_wav(mp3_path: str, wav_path: str):
    command = ["ffmpeg", "-i", mp3_path, "-ar", "16000", "-ac", "1", "-f", "wav", wav_path]
    subprocess.run(command, check=True)

@app.websocket("/ws/audio")
async def obtain_speech(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_chunks.append(await websocket.receive_bytes())
            
    except WebSocketDisconnect:
        # disconnect from web socket whenever user finished speaking (pressed button)
        # pass the audio_chunks into the google speech to text
        print("Web Socket disconnected!")
        transcript = speech_processor.transcribe_audio_chunks(audio_chunks)
        audio_chunks.clear()
        print(transcript)

@app.post("/send/wav", status_code=201)
async def uploadMP3(file: UploadFile = File(...)):
    global COUNT, DATA
    try:
        content = await file.read()
        # Define the upload directory within your project
        upload_directory = "uploads"
        
        # Create the directory if it doesn't exist
        os.makedirs(upload_directory, exist_ok=True)
        # Create the full file path. Here we use the original filename,
        # but you can customize this as needed.
        file_path = os.path.join(upload_directory, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            await out_file.write(content)
            res = transcribe_file(file_path)
            text = res.results
            parsed = " ".join([item.alternatives[0].transcript for item in text])
            # print("asdasd",parsed,"asdasd")
            if COUNT == 1:
                output = await checkout_flight(parsed,DATA)
            else:
                output,DATA = await get_flights(parsed)
                COUNT+=1
        return {
            "message": output
        }
    except HTTPException:
        raise HTTPException(
            status_code=404
        )
    
    
    
        
        
