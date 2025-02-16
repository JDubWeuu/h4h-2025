from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import speech_processor


app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(CORSMiddleware, allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

audio_chunks = []

@app.websocket("ws/audio")
async def obtain_speech(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_chunks.append(await websocket.receive_bytes())
            
    except WebSocketDisconnect:
        # disconnect from web socket whenever user finished speaking (pressed button)
        # pass the audio_chunks into the google speech to text
        print("Web Socket disconnected!")
        await websocket.close()
        transcript = speech_processor.transcribe_audio_chunks(audio_chunks)
        audio_chunks.clear()
        print(transcript)
        
        
