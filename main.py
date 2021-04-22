from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    with open('playercount.txt') as countfile:
        data = countfile.readlines()[0].strip()
    return render_template("index.html", playercount=data)

@app.route('/players/')
def players():
    return render_template("players.html")
