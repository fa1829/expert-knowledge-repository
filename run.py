from app import create_app
from app.config import HOST, PORT, APP_NAME, VERSION

if __name__ == "__main__":
    app = create_app()
    print(f"\n🧠 {APP_NAME} v{VERSION}")
    print(f"🌍 Listening on http://0.0.0.0:{PORT}\n")
    app.run(host=HOST, port=PORT, threaded=True)
