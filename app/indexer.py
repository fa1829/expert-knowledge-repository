from pathlib import Path
from threading import Lock
from .config import REPOSITORIES
from .filetypes import classify

INDEX = []
LOCK = Lock()

def build_index():
    global INDEX
    temp = []
    for repo, root in REPOSITORIES.items():
        root = Path(root)
        if not root.exists(): continue
        for f in root.rglob("*"):
            if f.is_file():
                t = classify(f.suffix.lower())
                if t:
                    temp.append({
                        "repo": repo,
                        "name": f.name,
                        "rel": f.relative_to(root).as_posix(),
                        "type": t,
                        "url": f"/browse/{repo}/{f.relative_to(root)}"
                    })
    with LOCK:
        INDEX = temp
    return len(INDEX)

def search(q):
    q = q.lower()
    with LOCK:
        return [i for i in INDEX if q in i["name"].lower()]
