from __future__ import annotations
import os
from pathlib import Path

APP_NAME = "Expert Knowledge Repository"
APP_TAGLINE = "Self-hosted knowledge platform for experts, mentors, and researchers"
VERSION = "0.5.0"

# OpenStack-safe port
HOST = "0.0.0.0"
PORT = int(os.getenv("EKR_PORT", "7000"))

SECRET_KEY = os.getenv("EKR_SECRET_KEY", "change-this-now")
ADMIN_TOKEN = os.getenv("EKR_ADMIN_TOKEN", "")

# Root knowledge folders (CHANGE THESE)
REPOSITORIES = {
    "Knowledge": "/data/knowledge",
    "Courses": "/data/courses",
    "Research": "/data/research",
}

VIDEO_EXT = {".mp4", ".mkv", ".avi", ".mov", ".webm"}
AUDIO_EXT = {".mp3", ".wav", ".flac", ".aac"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg"}
DOC_EXT   = {".pdf", ".docx", ".pptx", ".xlsx"}
TEXT_EXT  = {".txt", ".md", ".py", ".json", ".yaml"}

MAX_INLINE_TEXT_BYTES = 300_000
SEARCH_DEBOUNCE_MS = 400
SKIP_DEFAULT_SECONDS = 10
SKIP_ALT_SECONDS = 30
