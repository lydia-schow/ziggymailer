import sys
import csv
import os
import sendgrid
from sendgrid.helpers.mail import *

"""Main Entry Point"""
def main(argv):

    # Load settings
    sg = sendgrid.SendGridAPIClient(apikey='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')
    settings = {
        'from' : "ziggyonlinedebate@gmail.com",
        'subject': "Ziggy Online Debate",
        'information' : "This is a test e-mail.",
        'round' : '1',
        'round_file' : 'data/Round 1.csv',
        'team_file' : 'data/Team Data.csv'
    }

    # Load data files
    team_data = readCSV( settings['team_file'] )
    this_round = readCSV( settings['round_file'] )

    for room in this_round:

        # Find the e-mails of everyone in this room
        recipients = ""
        first = True
        for row in team_data:
            if not first:
                recipients += ","
            else:
                if row['Team']==room['AFF'] or row['Team']==room['NEG']:
                    if 'Email 1' in row:
                        if row['Email 1']:
                            recipients += row['Email 1']
                    if 'Email 2' in row:
                        if row['Email 2']:
                            recipients += row['Email 2']
                first = False

        # Format the message
        message = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head><body>\
                        <p>Hello,</p>\
                        <p>Your debate round %s pairing is as follows: \
                        Affirmative %s vs. Negative %s.</p>\
                        <p>%s</p>\
                    </body></html>'\
                    % (settings['round'], room['AFF'],\
                    room['NEG'], settings['information'])

        # Send the message
        mail = Mail( Email(settings['from']), settings['subject'],\
                     Email(recipients), Content('text/html', message ) )
        response = sg.client.mail.send.post(request_body=mail.get())
        if __debug__:
            print(response.status_code)
            print(response.body)
            print(response.headers)

    return 0


"""Load a CSV file into a Python data structure"""
def readCSV(file_name):
    result = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for room in reader:
            result.append(room)
    return result


"""..."""
if __name__ == "__main__":
    main(sys.argv)
