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
        tournaments = json.load(open('./tourneys.json'))

    return render_template("index.html", playercount=data, tournaments=tournaments)

@app.route('/players/')
def players():
    return render_template("players.html")

@app.route('/api/tourneys-json')
def getTournets():
    #data = json.loads(tourneys.getTourneys())
    return jsonify(tourneys.getTourneys())

@app.template_filter('QTFormat')
def formatTitle(value):
    
    if str(value).find("QT Tourney") != -1:
        t = value.find("(")
        value = value[:t] + "</p><p>" + value[t:]
    else:
        pass

    return value

@app.template_filter('QTMain')
def getPlayersMain(value):
    try:
        return json.load(open('playermains.json', 'r'))[value]
    except:
        return "rand"