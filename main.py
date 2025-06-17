from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import subprocess
import random
import os

app = FastAPI()

# CORS (update with your frontend domain if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class DownloadRequest(BaseModel):
    url: str
    format: str  # 'mp4' or 'mp3'

# Optional: List of free proxies (you can rotate or skip)
PROXIES = [
    "142.93.162.127:3128",
    "64.225.8.107:9981",
    "159.203.61.169:8080",
    "51.222.13.193:10084",
    "45.77.157.167:3128"
]

@app.post("/download")
async def download_media(req: DownloadRequest):
    url = req.url
    fmt = req.format.lower()
    proxy = random.choice(PROXIES)

    # Common output path
    output_path = "downloads/%(title)s.%(ext)s"

    # Start building yt-dlp command
    cmd = ["yt-dlp", "-o", output_path]

    # Apply proxy (optional)
    if proxy:
        cmd += ["--proxy", f"http://{proxy}"]

    # Apply format
    if fmt == "mp3":
        cmd += ["-x", "--audio-format", "mp3"]
    else:
        cmd += ["-f", "best"]

    # Detect YouTube (for cookies)
    if "youtube.com" in url or "youtu.be" in url:
        if os.path.exists("youtube_cookies.txt"):
            cmd += ["--cookies", "youtube_cookies.txt"]

    cmd.append(url)

    try:
        subprocess.run(cmd, check=True)
        return {"success": True, "message": "Download started", "proxy": proxy}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e), "proxy": proxy}
