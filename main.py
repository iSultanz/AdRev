from typing import Union

from fastapi import FastAPI, File, UploadFile

from services.model import analyze_text, analyze_images, transcribe_audio_with_whisper

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/upload/voice")
async def upload_voice(audio_file: UploadFile = File(...)):
    file_extension = audio_file.filename.split('.')[-1].lower()
    if file_extension not in ["mp3", "wav"]:
        return {"error": "Invalid file format. Only mp3 and wav are allowed."}
    text = transcribe_audio_with_whisper(audio_file)
    # generate results
    analysis = analyze_text(text)
    return {"analysis": analysis}

@app.post("/upload/image")
async def upload_image(image_file: UploadFile = File(...)):
    file_extension = imageFile.filename.split('.')[-1].lower()
    if file_extension not in ["jpg", "jpeg", "png"]:
        return {"error": "Invalid file format. Only jpg, jpeg, and png are allowed."}
    analysis = analyze_images(image_file)
    return {"analysis": analysis}

@app.post("/upload/text")
async def upload_image(text: str):
    if not text:
        return {"error": "Text is empty."}
    analysis = analyze_text(text)
    return {"analysis": analysis}
