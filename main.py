from fastapi import FastAPI, WebSocket


app = FastAPI()


@app.websocket("/query/ws")
def obtain_speech(websocket: WebSocket):
    pass
