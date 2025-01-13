from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from services.model import analyze_text, analyze_images, transcribe_audio_with_whisper

app = FastAPI()

# Add cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload/voice")
async def upload_voice(audio_file: UploadFile = File(...)):
    file_extension = audio_file.filename.split('.')[-1].lower()
    if file_extension not in ["mp3", "wav"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid file format. Only mp3 and wav are allowed."},
        )

    text = transcribe_audio_with_whisper(audio_file)
    analysis = analyze_text(text)
    return {"analysis": analysis}

@app.post("/upload/image")
async def upload_image(image_file: UploadFile = File(...)):
    file_extension = image_file.filename.split('.')[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png"]:
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid file format. Only jpg, jpeg, and png are allowed."},
        )
    analysis = analyze_images(image_file)
    return {"analysis": analysis}

@app.post("/upload/text")
async def upload_text(text: str):
    if not text:
        return JSONResponse(
            status_code=400, 
            content={"error": "Text is empty."},
        )
    analysis = analyze_text(text)
    return {"analysis": analysis}
