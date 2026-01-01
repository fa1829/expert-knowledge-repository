from flask import Blueprint, render_template, request, redirect, jsonify
from pathlib import Path
from .config import *
from .indexer import search, build_index
from .streaming import stream
from .filetypes import classify

bp = Blueprint("main", __name__)

@bp.route("/")
def home():
    return render_template("index.html", repos=REPOSITORIES.keys())

@bp.route("/search")
def do_search():
    q = request.args.get("q", "")
    return render_template("index.html", results=search(q), q=q)

@bp.route("/browse/<repo>/<path:subpath>")
def browse(repo, subpath):
    return stream(repo, subpath)

@bp.route("/admin/reindex", methods=["POST"])
def reindex():
    if ADMIN_TOKEN and request.headers.get("X-Admin-Token") != ADMIN_TOKEN:
        return "Unauthorized", 401
    return jsonify({"indexed": build_index()})
