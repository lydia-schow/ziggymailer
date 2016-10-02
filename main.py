import sys
import csv
import os
import sendgrid
from sendgrid.helpers.mail import *


"""Settings"""
sg = sendgrid.SendGridAPIClient(apikey='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')
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
    for room in this_round:
        recipients = recipientsGet(room, team_data)
        message = messageGet(room, settings)
        messageSend (message, recipients, settings)

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
def recipientsGet(room, team_data):
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


"""Convert a list into a comma-separated string"""
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


"""Build the email's body"""
def messageGet(row, settings):
    return '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>\
                    <p>Hello,</p>\
                    <p>Your debate round %s pairing is as follows: \
                    Affirmative %s vs. Negative %s.</p>\
                    <p>%s</p>\
                </body></html>'\
                % (settings['round'], row['AFF'],\
                row['NEG'], settings['information'])

"""Make a request to the sendgrid API"""
def messageSend(message, recipients, settings):
    mail = Mail( Email(settings['from']), settings['subject'],\
                 Email(recipients), Content('text/html', message ) )
    response = sg.client.mail.send.post(request_body=mail.get())
    if __debug__:
        print(response.status_code)
        print(response.body)
        print(response.headers)
    return response


"""..."""
if __name__ == "__main__":
    main(sys.argv)
