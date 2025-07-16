# app.py
import threading
from flask import Flask
import subprocess
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Daily Performance Manager is live."

@app.route("/run")
def trigger_main():
    def run_script():
        try:
            print("🚀 Running main.py...")
            subprocess.run(["python", "main.py"], check=True)
            print("✅ Script completed.")
        except Exception as e:
            print(f"❌ Error: {e}")

    threading.Thread(target=run_script).start()
    return "🚀 main.py started in background. Server returning instantly.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
