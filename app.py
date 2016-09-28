import sys
import csv
import os

settings = {
    'from' : "ziggyonlinedebate@gmail.com",
    'subject': "Ziggy Online Debate",
    'information' : "This is a test e-mail.",
    'round' : '1',
    'round_file' : 'data/Round 1.csv',
    'team_file' : 'data/Team Data.csv'
}

"""Main Entry Point"""
def main(argv):
    team_data = readCSV( settings['team_file'] )
    this_round = readCSV( settings['round_file'] )

    if __debug__:
        print( team_data )
        print( this_round )

    for row in this_round:
        room = {
            'round' : settings['round'],
            'affirmative' : row['AFF'],
            'negative' : row['NEG'],
            'to' : emailsGet(row, team_data)
        }

    print(room)

    q=raw_input("press close to exit")

    return 0

"""Load a CSV file into an array of dictionaries"""
def readCSV(file_name):
    result = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
    if __debug__: print(result)
    return result

"""..."""
def emailsGet(room, team_data):
    emails = []
    try:
        affirmative = room['AFF']
        negative = room['NEG']
    except KeyError:
        return emails
        #TODO: add an error log message

    for row in team_data:
        #All the addresses go into the same array, so we don't care which team matched
        if row['Team']==affirmative or row['Team']==negative:
            if 'Email 1' in row:
                #I used nested if statements instead of an "and" operator because calling row['Email X'] before verifying its existance could throw a Key Error. I can't use a try/except block because I want to check for the second e-mail address even if the first one failes.
                if row['Email 1']:
                    emails.append( row['Email 1'] )
            if 'Email 2' in row:
                if row['Email 2']:
                    emails.append( row['Email 2'] )

    if __debug__:
        print(emails)

    return emails

if __name__ == "__main__":
    main(sys.argv)
