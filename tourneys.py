import requests, json, datetime

url = "https://qttourney.challonge.com/tournaments"

# TODO Maybe implement a check that looks for an 'ignoretourneys' json file to take out any tourneys being listed... Or could just remove them manually from tourneys.json

# Only doing this because I've got collaberator access to the QT. Feel free to replace these with your information if you'd like
apiKey = "YFY3aSkSfKcqs8GdwuMueTB1fSQDZk384ZodySki"
uname = "The_Beverage"
localTourneys = {} # Used to hold the current listings stored in the machine. used for inserting the new tourneys if there are any

def getTourneys():

    # Need to set the request headers user agent to something or Challonge won't even bother accepting the request
    # Check if tourney file exists, if so then grab the first tourneys creation date and look for any new tourneys after that
    try:
        with open('./tourneys.json', 'r') as tourneys:
            data = json.load(tourneys)
            lastTourneyDate = str(json.dumps(data[list(data.keys())[0]]['created At'], indent=4))[1::]
            lastTourneyDate = lastTourneyDate[:-1:]
            
            dataJson = json.loads(requests.get("https://api.challonge.com/v1/tournaments.json?api_key=" + apiKey + "&subdomain=qttourney&created_after=" + lastTourneyDate, headers={'Content-Type':'application/json','User-Agent':'python3-requests/' + requests.__version__}).text)
            print(len(dataJson))
            print(lastTourneyDate)
    
            for tourney in data: # For every tourney stored locally
                localTourneys[tourney] = data[tourney] # (Store that tourney in memory for a moment)
                for newTourney in dataJson: # and every new tourney from challonge
                    if(data[tourney]['id'] == newTourney['tournament']['id']): # Check if the new tourney has already been entered locally
                        dataJson.remove(newTourney) # If it has, then remove it from the update list.

    except FileNotFoundError: # If no tourney file is found, get all of them. This will take a while but after doing it once, I can't imagine this will be used again
        dataJson = json.loads(requests.get("https://api.challonge.com/v1/tournaments.json?api_key=" + apiKey + "&subdomain=qttourney", headers={'Content-Type':'application/json','User-Agent':'python3-requests/' + requests.__version__}).text)

    tourneysArr = [] # Used for sorting
    tourneysDict = {} # Used to store sorted json

    '''
    tourneysArr struct
    0 - Tourney Name
    1 - Creation date
    2 - State of tourney
    3 - url
    4 - Participants
    5 - id
    '''

    # For every tournament, get the data and put it into the sorting array
    for i in range(0,len(dataJson)):
        tourneyTime = datetime.datetime.strptime(dataJson[i]['tournament']['created_at'].split("T")[0], "%Y-%m-%d")

        print("Fetching participant data for: " + dataJson[i]['tournament']['name'])
        
        # Get participant listings for each tourney
        dataJsonParticipants = json.loads(requests.get("https://api.challonge.com/v1/tournaments/qttourney-" + dataJson[i]['tournament']['url'] + "/participants.json?api_key=" + apiKey, headers={'Content-Type':'application/json','User-Agent':'python3-requests/' + requests.__version__}).text)
        
        # Get ready to process the tourney details. Get what we want from the challonge response and add it here.
        tourneysArr.append([dataJson[i]['tournament']['name'], tourneyTime, dataJson[i]['tournament']['state'],dataJson[i]['tournament']['full_challonge_url'], [], dataJson[i]['tournament']['id']])

        # Apparently some people are too cool for usernames, display names and even regular names
        for j in range(0, len(dataJsonParticipants)):
            if(dataJsonParticipants[j]['participant']['username'] != None):
                tourneysArr[i][4].append([dataJsonParticipants[j]['participant']['username'], dataJsonParticipants[j]['participant']['final_rank']])
            elif(dataJsonParticipants[j]['participant']['display_name'] != None):
                tourneysArr[i][4].append([dataJsonParticipants[j]['participant']['display_name'], dataJsonParticipants[j]['participant']['final_rank']])
            elif(dataJsonParticipants[j]['participant']['name'] != None):
                tourneysArr[i][4].append([dataJsonParticipants[j]['participant']['name'], dataJsonParticipants[j]['participant']['final_rank']])
            else:
                tourneysArr[i][4].append(['Anonymous', dataJsonParticipants[j]['participant']['final_rank']])

    tourneysArr.sort(key=lambda e: e[1]) # Sort array on date
    tourneysArr.reverse() # Just so we get the latest QT at the top of the list

    # Put data back into json format
    for i in range(0,len(tourneysArr)):

        try:
            tourneysArr[i][4].sort(key=lambda e: e[1]) # Sort each participant listing by their final rank
        except:
            pass

        tourneysDict[i] = {
            "id": tourneysArr[i][5],
            "name" : tourneysArr[i][0], 
            "created At" : tourneysArr[i][1].strftime("%Y-%m-%d"),
            "state" : tourneysArr[i][2],
            "url" : tourneysArr[i][3],
            "participants" : tourneysArr[i][4]}

    print(len(tourneysArr))
    if(len(tourneysArr) > 0): # If there are tourneys that need to be updated to the local file
        for tourney in localTourneys: # For every tourney stored locally
            tempTourney = localTourneys[tourney] # temporarily store a single tourney
            tourneysDict[int(tourney)] = tempTourney # add it into the end of the dictionary to be stored locally

        # Update local tourney listings
        with open('./tourneys.json', 'w') as json_file:
            json.dump(tourneysDict, json_file, indent=4)
    else:
        tourneysDict = localTourneys

    return json.dumps(tourneysDict)