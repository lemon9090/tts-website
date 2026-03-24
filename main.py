from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import edge_tts
import asyncio
import uuid
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate(text: str = Form(None), file: UploadFile = File(None), voice: str = Form(...)):
    if file:
        content = await file.read()
        text = content.decode("utf-8")

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    tts = edge_tts.Communicate(text, voice)
    await tts.save(filepath)

    return FileResponse(filepath, media_type="audio/mpeg", filename="output.mp3")
