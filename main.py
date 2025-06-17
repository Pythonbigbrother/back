from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import random
import os

app = FastAPI()

# Allow CORS from any origin or replace with your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DownloadRequest(BaseModel):
    url: str
    format: str  # 'mp4' or 'mp3'

# Optional proxy list
FREE_PROXIES = [
    "142.93.162.127:3128",
    "64.225.8.107:9981",
    "159.203.61.169:8080",
    "51.222.13.193:10084",
    "45.77.157.167:3128"
]

@app.post("/download")
async def download_media(req: DownloadRequest):
    proxy = random.choice(FREE_PROXIES)
    cmd = [
        "yt-dlp",
        "--proxy", f"http://{proxy}",
        "--cookies", "youtube_cookies.txt",
        "-f", req.format,
        "-o", "downloads/%(title)s.%(ext)s",
        req.url
    ]

    try:
        subprocess.run(cmd, check=True)
        return {"success": True, "proxy": proxy}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr or str(e), "proxy": proxy}
