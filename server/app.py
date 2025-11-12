from fastapi import FastAPI, WebSocket
app = FastAPI()

@app.get('/health')
def health():
    return {'ok': True}

@app.websocket('/ws')
async def ws(ws: WebSocket):
    await ws.accept()
    await ws.send_json({'hello': 'world', 'note':'encrypt on client, store ciphertexts only'})
    await ws.close()
