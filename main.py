from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import edge_tts
import uuid
import os

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ CREATE templates FIRST
templates = Jinja2Templates(directory="templates")

# ✅ THEN modify cache
templates.env.cache = {}

# Output folder
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Home route
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

# Generate audio
@app.post("/generate")
async def generate(
    request: Request,
    text: str = Form(None),
    file: UploadFile = File(None),
    voice: str = Form(...)
):
    # DEBUG PRINT (important)
    print("TEXT:", text)
    print("FILE:", file)

    # Handle file first
    if file and file.filename:
        content = await file.read()
        text = content.decode("utf-8")

    # Clean text
    if not text or text.strip() == "":
        return {"error": "Please enter text or upload a file"}

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    tts = edge_tts.Communicate(text, voice)
    await tts.save(filepath)

    return FileResponse(filepath, media_type="audio/mpeg", filename="output.mp3")
