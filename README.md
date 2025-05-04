# STRETCHED 📸

A local Python + Docker application to stretch anamorphic images using FastAPI and a custom UI.

## Features
- Drag & drop image interface
- Stretch images by 1.33x or 1.5x along the largest dimension
- Output to same folder with `stretched_` prefix
- EXIF-based date display
- High-quality JPEG export (95%, no chroma subsampling)

## Run with Docker
```bash
docker-compose up --build
