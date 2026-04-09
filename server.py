from flask import Flask, render_template, request
from flask_cors import CORS
from main import InstaBot  # importa la classe dal main.py
import threading

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/")
def home():
    return render_template("index.html")  # mostra il template HTML con CSS/JS

@app.route("/start", methods=["POST"])
def start():
    data = request.get_json()
    username = data['username']
    password = data['password']

    def run_bot():
        bot = InstaBot(username, password)
        bot.get_unfollowers()

    threading.Thread(target=run_bot).start()
    return "Bot avviato bro 🚀"

@app.route("/track", methods=["POST", "OPTIONS"])
def track():
    data = request.json  # prendi il JSON inviato
    if data:
        # apri/crea track_log.txt e aggiungi la roba
        with open("track_log.txt", "a") as f:
            f.write(str(data) + "\n")  # scrive una riga per ogni POST
    return "ok"

if __name__ == "__main__":
    app.run(debug=True)