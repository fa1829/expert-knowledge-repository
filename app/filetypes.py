from .config import VIDEO_EXT, AUDIO_EXT, IMAGE_EXT, DOC_EXT, TEXT_EXT

def classify(ext):
    if ext in VIDEO_EXT: return "video"
    if ext in AUDIO_EXT: return "audio"
    if ext in IMAGE_EXT: return "image"
    if ext == ".pdf": return "pdf"
    if ext in DOC_EXT: return "doc"
    if ext in TEXT_EXT: return "text"
    return None
