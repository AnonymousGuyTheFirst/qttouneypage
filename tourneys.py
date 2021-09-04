import requests, json, datetime

url = "https://qttourney.challonge.com/tournaments"

# Only doing this because I've got collaberator access to the QT. Feel free to replace these with your information if you'd like
apiKey = "YFY3aSkSfKcqs8GdwuMueTB1fSQDZk384ZodySki"
uname = "The_Beverage"

def getTourneys():
    # Need to set the request headers user agent to something or Challonge won't even bother accepting the request
    dataJson = json.loads(requests.get("https://api.challonge.com/v1/tournaments.json?api_key=" + apiKey + "&subdomain=qttourney", headers={'Content-Type':'application/json','User-Agent':'python3-requests/' + requests.__version__}).text)

    tourneysArr = [] # Used for sorting
    tourneysDict = {} # Used to store sorted json

    '''
    tourneysArr struct
    0 - Tourney Name
    1 - Creation date
    2 - State of tourney
    3 - url
    '''

    # For every tournament, get the data and put it into the sorting array
    for i in range(0,len(dataJson)):
        tourneyTime = datetime.datetime.strptime(dataJson[i]['tournament']['created_at'].split("T")[0], "%Y-%m-%d")
        tourneysArr.append([dataJson[i]['tournament']['name'], tourneyTime, dataJson[i]['tournament']['state'],dataJson[i]['tournament']['full_challonge_url']])

    tourneysArr.sort(key=lambda e: e[1]) # Sort array on date

    # Put data back into json format
    for i in range(0,len(tourneysArr)):
        tourneysDict[i] = {
            "Name" : tourneysArr[i][0], 
            "Created At" : tourneysArr[i][1].strftime("%Y-%m-%d"),
            "State" : tourneysArr[i][2],
            "url" : tourneysArr[i][3]}

    return tourneysDict