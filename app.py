# app.py
import threading
import os
from flask import Flask
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
            os.system("python3 main.py")
            print("✅ Script completed.")
        except Exception as e:
            print(f"❌ Error running main.py: {e}")

    threading.Thread(target=run_script).start()
    return "🚀 main.py triggered in background.", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
