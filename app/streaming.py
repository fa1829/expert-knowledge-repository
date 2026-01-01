from flask import request, abort, send_file
from pathlib import Path
import mimetypes
from .config import REPOSITORIES
from .utils import is_safe

def stream(repo, subpath):
    base = REPOSITORIES[repo]
    if not is_safe(base, subpath):
        abort(403)

    f = Path(base) / subpath
    if not f.exists():
        abort(404)

    mime = mimetypes.guess_type(str(f))[0]
    return send_file(f, mimetype=mime)
