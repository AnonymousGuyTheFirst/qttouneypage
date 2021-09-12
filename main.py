from flask import Flask, render_template, jsonify
import tourneys, json

app = Flask(__name__)

@app.route('/')
def index():
    with open('playercount.txt') as countfile:
        data = countfile.readlines()[0].strip()
    
    # Try pulling tourney information from challonge, if not then fallback on the tourney listing saved onto machine
    try:
       tournaments = json.loads(tourneys.getTourneys())
    except:
        tournaments = json.load(open('./tourneys.txt'))

    return render_template("index.html", playercount=data, tournaments=tournaments, len=len(tournaments["0"]))

@app.route('/players/')
def players():
    return render_template("players.html")

@app.route('/api/tourneys-json')
def getTournets():
    #data = json.loads(tourneys.getTourneys())
    return jsonify(tourneys.getTourneys())