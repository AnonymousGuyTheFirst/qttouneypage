import tourneys, json, os.path, time
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    dayLater = False

    with open('playercount.txt') as countfile:
        data = countfile.readlines()[0].strip()

    # Holy shit, there's gotta be a better way to check the last time there was a request to challonge
    if os.path.isfile('lastchecked'):
        with open('lastchecked', 'r+') as f:
            if(int(time.time()) > (int(float(f.read())) + 86400)): # Check if current time is a day later
                f.truncate(0)
                f.write(str(time.time()))
                dayLater = True
    else:
        with open('lastchecked', 'w') as f:
            f.write(str(time.time()))
            dayLater = True
            print("Hello")
    
    # Try pulling tourney information from challonge, if not then fallback on the tourney listing saved onto machine
    try:
        if(dayLater):
            print("Pulling from challonge...")
            tournaments = json.loads(tourneys.getTourneys())
        else:
            print("Pulling from local file...")
            tournaments = json.load(open('./tourneys.json'))
    except Exception as e:
        print(e)
        print("Pulling from local file...")
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