import sys
import csv
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='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')

"""Settings"""
ROUND_FILE_NAME = "Round 1.csv"
TEAM_DATA_FILE_NAME = "Team Data.csv"

FROM_EMAIL = "ziggyonlinedebate@gmail.com"
SUBJECT = "Ziggy Online Debate"
INFORMATION = "This is a test e-mail."
ROUND = 1

DEBUG = False

"""Main Entry Point"""
def main(argv):
    team_data = readCSV( TEAM_DATA_FILE_NAME )
    this_round = readCSV( ROUND_FILE_NAME )

    if DEBUG:
        print( team_data )
        print( this_round )

    for row in this_round:
        room = {
            'round' : ROUND,
            'affirmative' : row['AFF'],
            'negative' : row['NEG'],
            'to' : emailsGet(row, team_data)
        }
    print(room)


"""Load a CSV file into an array of dictionaries"""
def readCSV(file_name):
    result = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
    if DEBUG: print(result)
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

    if DEBUG:
        print(emails)
    return emails

if __name__ == "__main__":
    main(sys.argv)




"""
this_round = [
    {
        'affirmative' : 'Bob Smith',
        'negative' : 'John Doe'
    }
]

room = {
    'round' : '1',
    'affirmative' : 'Bob Smith',
    'negative' : 'John Doe',
    'to' : 'elijah.schow@gmail.com, mr.glasses.aux@gmail.com, elijah.schow@ethosdebate.com, webmaster@elegantevidence.org'
}

message = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>\
                <p>Hello,</p>\
                <p>Your debate round %s pairing is as follows:<br>\
                Affirmative %s vs. Negative %s.</p>\
                <p>%s</p>\
            </body></html>'\
            % (room['round'], room['affirmative'], room['negative'],\
            INFORMATION)

mail = Mail( Email(FROM_EMAIL), SUBJECT, Email(room['to']),\
    Content('text/html', str(message) ) )
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)
"""
