from flask import Flask, render_template, request
from flask_cors import CORS
from main import InstaBot  # importa la classe dal main.py
import threading
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return render_template("index.html")  # mostra il template HTML con CSS/JS

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    # leggi username/password dal form del browser, oppure usa variabili d'ambiente
    username = data.get('username') or os.environ.get("INSTA_USERNAME")
    password = data.get('password') or os.environ.get("INSTA_PASSWORD")

    def run_bot():
        bot = InstaBot(username, password)
        bot.get_unfollowers()

    threading.Thread(target=run_bot).start()
    return "Bot avviato bro 🚀"

@app.route("/track", methods=["POST", "OPTIONS"])
def track():
    data = request.json  # prendi il JSON inviato
    if data:
        # scrive su track_log.txt
        with open("track_log.txt", "a") as f:
            f.write(str(data) + "\n")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
