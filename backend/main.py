# backend/main.py

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image, ExifTags
import os
from io import BytesIO
from datetime import datetime


app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/stretch")
async def stretch_image(file: UploadFile, ratio: float = Form(...)):
    try:
        # Read uploaded image
        contents = await file.read()
        img = Image.open(BytesIO(contents))

        # Extract EXIF metadata (creation date)
        exif = img._getexif()
        creation_date = None

        if exif:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag)
                if decoded == "DateTimeOriginal":
                    creation_date = value
                    break

        # Format the date nicely
        if creation_date:
            creation_date = creation_date.split(" ")[0].replace(":", "-")
        else:
            creation_date = datetime.today().strftime("%Y-%m-%d")  # fallback

        # Get original dimensions
        width, height = img.size
        print(f"Original size: {width}x{height}, stretch ratio: {ratio}")

        # Determine which dimension to stretch
        if width >= height:
            # Stretch width only
            new_width = int(width * ratio)
            new_height = height
        else:
            # Stretch height only
            new_width = width
            new_height = int(height * ratio)

        # Resize image with new dimensions
        stretched_img = img.resize((new_width, new_height), Image.LANCZOS)

        # Ensure output directory exists
        os.makedirs("images", exist_ok=True)

        # Build output filename (same as original but prefixed)
        output_path = f"images/stretched_{file.filename}"

        # Save new image in same format
        # Use high-quality save settings (especially for JPEG)
        if img.format == "JPEG":
            stretched_img.save(output_path, format="JPEG", quality=95, subsampling=0, optimize=False)
        else:
            stretched_img.save(output_path, format=img.format)

        print(f"Saved stretched image as: {output_path}")
        return JSONResponse(content={
            "status": "ok",
            "filename": file.filename,
            "date": creation_date
        })

    except Exception as e:
        print(f"Error stretching image: {e}")
        return JSONResponse(status_code=500, content={"status": "error", "details": str(e)})
