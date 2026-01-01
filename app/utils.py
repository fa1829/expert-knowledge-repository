from pathlib import Path
import html

def is_safe(base, path):
    base = Path(base).resolve()
    target = (base / path).resolve()
    return base in target.parents or base == target

def escape(s):
    return html.escape(s)
