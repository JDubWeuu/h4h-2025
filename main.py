from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()

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
        
        
