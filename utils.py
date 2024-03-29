import constants

# Convert keys like "s1", "s2" to human readable "Kills", "Assists"
def convertMatchKeys(match: object) -> object:
    copy_match = match.copy()
    for key in copy_match:
        if key in constants.FaceitIndex:
            match[constants.FaceitIndex[key]] = match[key]
            del match[key]
    return match

# Filtr matches by maps
def filterMatchesByMap(matches: list, map_name: str) -> list:
    return [match for match in matches if match['Map'] == map_name]

# Simple averaging function
def average(array: list) -> list:
    return round(sum(array) / len(array), 2) if len(array) > 0 else 0

def getPlayersFromMatch(match: object, merge=False) -> list:
    """
    Returns list or object of players as \n
    {
        "faction1": [id, id...],
        "faction2": [id, id...]
    }
    """
    data = {}
    players = []
    for faction in match['teams']:
        if merge:
            players.extend([player['id'] for player in match['teams'][faction]['roster']])
        else:
            data[faction] = [player['id'] for player in match['teams'][faction]['roster']]
    if merge:
        return players
    else:
        return data

# Get average stats of matches
def getAverageOfMatches(matches: list) -> object:
    match_average = {}
    for key in constants.AVERAGE_ALLOWED:
        match_average[key] = average([float(match[key]) for match in matches])
    return match_average 

# Compare taems and give prediction ("faction1", "faction2" or "tie")
def predict(data: object, MAP:str) -> str: 
    faction1_points = faction2_points = 0
    for key in constants.AVERAGE_ALLOWED:
        if (data['faction1'][MAP][key] > data['faction2'][MAP][key]):
            faction1_points+=1
        elif (data['faction1'][MAP][key] < data['faction2'][MAP][key]):
            faction2_points+=1
        else:
            faction1_points+=1
            faction2_points+=1
    
    if faction1_points > faction2_points:
        return "faction1"
    elif faction2_points > faction1_points:
        return "faction2"
    else:
        return "tie"

# Returns the integer difference of final match score; requires 'score' key
def getScoreDifference(match: object) -> int:
    score = [int(score.strip()) for score in match['score'].split('/')]
    return abs(score[0] - score[1])

def stripMatch(match: object) -> object:
    """Remove unused keys from match object"""
    for key in match.copy():
        if key in constants.KEYS_TO_KEEP:
            if key == 'teams' and 'id' in match[key]['faction1']:
                for team in match[key]:
                    match[key][team] = [player['id'] for player in match[key][team]['roster']]
            elif key == 'id':
                match['_id'] = match[key]
        else:
            del match[key]
    return match

def stripPlayerMatch(match: object) -> object:
    """Removes unused keys in player match object"""
    matchCopy = match.copy()
    for key in match:
        if key not in constants.AVERAGE_ALLOWED:
            del matchCopy[key]
    return matchCopy

def stripManually(obj: object, allowed_keys: list) -> object:
    """Removes unused keys in given object"""
    objCopy = obj.copy()
    for key in obj:
        if key not in allowed_keys:
            del objCopy[key]
    return objCopy