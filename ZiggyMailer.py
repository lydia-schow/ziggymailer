# coding=utf-8
import os
import csv
import configparser as cfg
from urllib.error import HTTPError

import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import sendgrid
from sendgrid.helpers.mail import *

class Parameter(dict):
    def __missing__(self, key):
        return '{' + key + '}'

class ZiggyMailer:
    def __init__(self, root):
        """Initialize the GUI application"""
        # Load defaults
        config = cfg.ConfigParser()
        config.read('settings.ini')
        default = {
            'from_email' : config['values']['FromEmail'],
            'reply_to' : config['values']['ReplyTo'],
            'subject' : config['values']['Subject'],
            'body' : config['values']['Body'],
            'round_number' : config['values']['RoundNumber'],
            'round_file' : config['values']['RoundFile'],
            'team_file' : config['values']['TeamFile']
        }
        # Initialize GUI
        self.root = root
        self.root.wm_title('Ziggy Mailer')
        # Left column
        self.leftFrame = tk.Frame(root)
        self.leftFrame.grid(row=0, column=0, sticky='NW', padx=(10,5))
        # From Input
        value = tk.StringVar(root, default['from_email'])
        self.fromLabel = tk.Label(self.leftFrame, text='From')
        self.fromEntry = tk.Entry(self.leftFrame, textvariable=value)
        self.fromLabel.grid(sticky='W',pady=(5,0),padx=(0,5),column=0,row=0)
        self.fromEntry.grid(sticky='WE',pady=(0,5),padx=(0,5),column=0,row=1)
        #Reply-to Input
        value = tk.StringVar(root, default['reply_to'])
        self.replyToLabel = tk.Label(self.leftFrame, text='Reply To')
        self.replyToEntry = tk.Entry(self.leftFrame, textvariable=value)
        self.replyToLabel.grid(sticky='W',pady=(5,0),padx=(5,0),column=1,row=0)
        self.replyToEntry.grid(sticky='WE',pady=(0,5),padx=(5,0),column=1,row=1)
        # Subject Input
        value = tk.StringVar(root, default['subject'])
        self.subjectLabel = tk.Label(self.leftFrame, text='Subject')
        self.subjectEntry = tk.Entry(self.leftFrame, textvariable=value)
        self.subjectLabel.grid(sticky='W', pady=(5,0), columnspan=2)
        self.subjectEntry.grid(sticky='WE', pady=(0,5), columnspan=2)
        #Body Input
        self.bodyLabel = tk.Label(self.leftFrame, text='Body')
        self.bodyText = tk.Text(self.leftFrame, )
        self.bodyLabel.grid(sticky='W', pady=(5,0), columnspan=2)
        self.bodyText.grid(sticky='WE', pady=(0,5), columnspan=2)
        for line in default['body'].split('\\n'):
            self.bodyText.insert( 'end', line + '\n')
        # Right column
        self.rightFrame = tk.Frame(root)
        self.rightFrame.grid(row=0, column=1, sticky='NW', padx=(5, 10))
        # Round Number Input
        value = tk.StringVar(root, default['round_number'])
        self.roundLabel = tk.Label(self.rightFrame, text='Round Number')
        self.roundEntry = tk.Entry(self.rightFrame, textvariable=value)
        self.roundLabel.grid(row='0', sticky='W', pady=(5,0), columnspan=2)
        self.roundEntry.grid(row='1', sticky='WE', pady=(0,5), columnspan=2)
        # Round File Input
        value = tk.StringVar(root, default['round_file'])
        self.roundFileLabel = tk.Label(self.rightFrame, text='Round File (.csv)')
        self.roundFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.setfilename(self.roundFileEntry))
        self.roundFileEntry = tk.Entry(self.rightFrame, state='disabled',
            textvariable=value)
        self.roundFileLabel.grid(row='2', sticky='W', pady=(5,0), columnspan=2)
        self.roundFileButton.grid(row='3', column=0)
        self.roundFileEntry.grid(row='3', column=1, sticky="NSEW")
        # Team File Input
        value = tk.StringVar(root, default['team_file'])
        self.teamFileLabel = tk.Label(self.rightFrame, text='Team File (.csv)')
        self.teamFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.setfilename(self.teamFileEntry))
        self.teamFileEntry = tk.Entry(self.rightFrame, state='disabled',
            textvariable=value)
        self.teamFileLabel.grid(row='4', sticky='W', pady=(5,0), columnspan=2)
        self.teamFileButton.grid(row='5', column=0)
        self.teamFileEntry.grid(row='5', column=1, sticky="NSEW")
        # Submit button
        self.submitButton = tk.Button(root, text='Send', command=self.submit )
        self.submitButton.grid(stick='WE', row=1,columnspan=2, padx=10, pady=10)

    def setfilename(self, target):
        """Update a file name input"""
        # TODO: assert that 'target' is an instance of tk.Entry
        filename = askopenfilename(filetypes=[('Comma Separated Values', '*.csv')])
        target.configure(state = 'normal') # text can't be edited if it's disabled
        target.delete(0, 'end')
        target.insert(0, filename)
        target.xview('end')
        target.configure(state = 'disabled')

    def submit(self):
        """Send postings to each room."""
        from_email = self.fromEntry.get()
        reply_to = self.replyToEntry.get()
        subject = self.subjectEntry.get()
        body = self.bodyText.get('1.0', 'end')
        round_number = int(self.roundEntry.get())
        round_file = self.roundFileEntry.get()
        team_file = self.teamFileEntry.get()

        try:
            assert from_email, 'There is no "From" address. Please specify one.'
            assert subject, 'The subject is empty. Please write a suject line.'
            assert len(subject) < 78, 'The subject must be fewer than 78 characters long. Please shorten it.'  # Required by the SendGrid API
            assert round_number, 'There is no round number. Please specify one.'

            mail = Mail( from_email = Email(from_email),
                         subject = subject,
                         to_email = Email('user@server.com','Firstname Lastname'), # This is a work around. The API malfunctions if you set this to "none".
                         content = Content('text/plain', body )
                        )

            this_round = Round(round_number, round_file, team_file)

            assert this_round.countRooms() <= 1000, 'There are %i rooms, but the SendGrid API only allows up to 1,000 at once. Reduce the number of rooms.' % this_round.countRooms()

            for room in this_round.rooms:
                pers = Personalization()
                for participant in room.participants:
                    pers.add_to(participant)
                pers.add_substitution( Substitution('[aff]', room.affirmative) )
                pers.add_substitution( Substitution('[neg]', room.negative) )
                pers.add_substitution( Substitution('[round]', str(this_round.number) ) )
                mail.add_personalization(pers)
            del mail.personalizations[0]  # Remove the dummy address from the workaround.

            response = sg.client.mail.send.post(request_body=mail.get())
            if __debug__:
                print(response.status_code)
                print(response.body)
                print(response.headers)

            room_count = len(this_round.rooms)
            tk.messagebox.showinfo( 'Message Sent', 'The message was sent to %i rooms and %i participants.' % ( this_round.countRooms(), this_round.countParticipants() ) )

        except AssertionError as error:
            tk.messagebox.showerror('Error', error)
        except HTTPError as error:
            tk.messagebox.showerror('Error', '%s (HTTP %i)' % (error.msg, error.code) )
        except Exception as error:
            tk.messagebox.showerror('Error', error )

class Round:
    """Represents one debate round in the tournament"""
    def __init__(self, number, round_file, team_file):
        self.number = number

        assert os.path.isfile(round_file), 'The Round File does not exist. Make sure one is selected.'
        round_data = readCSV(round_file)
        assert 'AFF' in round_data[0] and\
               'NEG' in round_data[0],\
               'The round data file is not formatted correctly. Make sure it contains these columns (case-sensive): "AFF", and "NEG".'

        assert os.path.isfile(team_file), 'The Round File does not exist. Make sure one is selected.'
        team_data = readCSV(team_file)
        assert 'Team' in team_data[0] and\
               'First Name 1' in team_data[0] and\
               'Last Name 1' in team_data[0] and\
               'Email 1' in team_data[0] and\
               'First Name 2' in team_data[0] and\
               'Last Name 2' in team_data[0] and\
               'Email 2' in team_data[0],\
               'The team data file is not formatted correctly. Make sure it contains these columns (case-sensive): "Team", "First Name 1", "Last Name 1", "Email 1", "First Name 2", "Last Name 2", "Email 2".'

        self.rooms = []
        for round_row in round_data:
            affirmative = round_row['AFF']
            negative = round_row['NEG']
            participants = []
            for team_row in team_data:
                if team_row['Team'] == affirmative or team_row['Team'] == negative:
                    name1 = team_row['First Name 1'] + ' ' + team_row['Last Name 1']
                    email1 = team_row['Email 1']
                    if email1: participants.append( Email(email1, name1) )
                    name2 = team_row['First Name 2'] + ' ' + team_row['Last Name 2']
                    email2 = team_row['Email 2']
                    if email2: participants.append( Email(email2, name2) )
            room = Room(affirmative, negative, participants)
            self.rooms.append(room)

    def countRooms(self):
        return len(self.rooms)

    def countParticipants(self):
        result = 0
        for room in self.rooms:
            result += len(room.participants)
        return result


class Room:
    """Represents a single room in a round."""
    def __init__(self, affirmative, negative, participants):
        self.affirmative = affirmative
        self.negative = negative
        self.participants = participants


def readCSV(file_name):
    """Load a CSV file into a Python data structure"""
    result = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
        file.close()
    return result

"""Main Loop"""
config = cfg.ConfigParser()
config.read('settings.ini')
sg = sendgrid.SendGridAPIClient(apikey=config['general']['APIKey'])
root = tk.Tk()
app = ZiggyMailer(root)

root.mainloop()
