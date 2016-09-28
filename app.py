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

    for row in this_round:
        recipients = emailsGet(row, team_data)
        room = {
            'round' : settings['round'],
            'affirmative' : row['AFF'],
            'negative' : row['NEG'],
            'to' : recipients
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
    return result

"""Return a list of email addresses for everyone in a room."""
def emailsGet(room, team_data):
    emails = []
    try:
        affirmative = room['AFF']
        negative = room['NEG']
    except KeyError:
        return emails
        #TODO: add an error log message

    for row in team_data:
        """ It doesn't matter which team matches because all the addresses go
        into the same array."""
        if row['Team']==affirmative or row['Team']==negative:
            if 'Email 1' in row:
                """Nested if statements are used instead of an "and" operator
                because calling row['Email X'] before verifying its existance
                could throw a Key Error. Try/except can't be used because the
                application should check for the second e-mail address even if
                the first one doesn't exist."""
                if row['Email 1']:
                    emails.append( row['Email 1'] )
            if 'Email 2' in row:
                if row['Email 2']:
                    emails.append( row['Email 2'] )
    return concatenate(emails)

def concatenate( items ):
    result = ''
    first = True
    for item in items:
        #Don't leave a delimiter dangling at the beginning or end
        if not first:
            result += ", "
        else:
            first = False
        result += str(item)
    return result

if __name__ == "__main__":
    main(sys.argv)
