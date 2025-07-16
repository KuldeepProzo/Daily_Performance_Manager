from flask import Flask
import threading
import main  # Your updated main.py must have a run() function

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Performance Emailer is deployed."

@app.route("/trigger")
def trigger():
    def background_task():
        try:
            print("🚀 Trigger received, running performance script...")
            main.run()
        except Exception as e:
            print(f"❌ Error in performance run: {e}")

    threading.Thread(target=background_task).start()
    return "🚀 Triggered performance script!", 200
