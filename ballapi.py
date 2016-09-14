from urllib.request import urlopen, Request, URLError
import requests
import os
import csv
import collections
import time


api_key = 'z61uEjPdOSvBWAYteq5xaKypM7VG3r4b'

json_teams = []

# call each function, return the keys of the object as well as the object,
# can I then aggregate all of these things together in one object??


def get_teams(api_key):

    try:
            ############ GET TEAM OBJECT #########
        team_payload = {'api_key': api_key}
        teams = requests.post(
            'http://api.probasketballapi.com/team', data=team_payload)

        # create json object from http request for teams (actually a
        # list)
        json_teams = teams.json()

            # list with keys for teams
        team_keys = []

        for key in json_teams[0].keys():
            team_keys.append(key)

        teams = collections.namedtuple('Teams', ['keys', 'object'])
        team_items = teams(team_keys, json_teams)

    except:
        print('error')

    return team_items

def get_players(api_key):


    player_payload_setup = {'api_key': api_key}
    players = requests.post(
        'http://api.probasketballapi.com/player', data=player_payload_setup)

    json_players = players.json()
    
        # list with keys for players
    player_keys = []

        # set fieldnames for each key, append to fieldnames array

    for key in json_players[0].keys():
        player_keys.append(key)

    players = collections.namedtuple('Players', ['keys', 'object'])
    player_items = players(player_keys, json_players)

    return player_items     

def write_to_file(team_items, fieldnames):
    ########### CSV WRITER #########
        # set csv variable for fileName
    csvfile = open('names.csv', 'a', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()

    ########## GET TEAMS AND PLAYERS AND PRINT IN CSV FILE #########
    for team in team_items[1]:
        #writer.writerow({'Team ID': team['id'], 'Team Name': team['team_name'], 'City': team[
         #              'city'], 'Abbreviation': team['abbreviation']})

        player_payload = {'api_key': api_key, 'team_id': team['id']}
        players = requests.post(
            "http://api.probasketballapi.com/player", data=player_payload)

                # set json object for players
        json_player = players.json()
        for player in json_player:
                # write the data. Match the data with the fieldName
                # as of now, there are seven keys that come from the team
                # object.
                #as of now, there are seven keys coming from the player object as well

            #print(player['player_name'])

            writer.writerow({'player_name': player['player_name'], 'last_name': player['last_name'], 'first_name': player['first_name'],
                             'birth_date': player['birth_date'], 'position': player['position'], 'team_id': player['team_id'], 'id': player['id'],
                             'dk_position': player['dk_position'], 'dk_id': player['dk_id'], 'team_name': team['team_name'], 'abbreviation': team['abbreviation'],
                             'city': team['city'], 'created_at': team['created_at'], 'updated_at': team['updated_at'], 'dk_id': team['dk_id']})


    #call functions
team_items = get_teams(api_key)
player_items = get_players(api_key)

    # create array with headers
field_headers = []

#print (player_items.keys, team_items.keys)

    # append headers to the field header array
field_headers += player_items.keys
field_headers += team_items.keys

write_to_file(team_items, field_headers)







        #writer.writerow({team_keys[0]: team[team_keys[0]], team_keys[1]: team[team_keys[1]], team_keys[2]: team[
         #   team_keys[2]], team_keys[3]: team[team_keys[3]], team_keys[4]: team[team_keys[4]], team_keys[5]: team[team_keys[5]], team_keys[6]: team[team_keys[6]],
          #  player_keys[0]: player[player_keys[0]], player_keys[1]: player[player_keys[1]], player_keys[2]: player[player_keys[2]], player_keys[3]: player[player_keys[3]], 
           # player_keys[4]: player[player_keys[4]], player_keys[5]: player[player_keys[5]], player_keys[6]: player[player_keys[6]]})

# the idea here is to dynamically write a row according to the number of headers that are in the file.
# also need to be able to dynamically write the items according to how many headers come from the team resource and how
# many come from the players resource.
