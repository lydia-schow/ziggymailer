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

class ZiggyMailer:
    def __init__(self):
        """Set up the GUI and load default settings"""
        # Window Title
        root.wm_title('Ziggy Mailer')
        # Left column
        self.leftFrame = tk.Frame(root)
        self.leftFrame.grid(row=0, column=0, sticky='NW', padx=(10,5))
        # From Input
        self.fromLabel = tk.Label(self.leftFrame, text='From')
        self.fromEntry = tk.Entry(self.leftFrame)
        self.fromLabel.grid(sticky='W',pady=(5,0),padx=(0,5),column=0,row=0)
        self.fromEntry.grid(sticky='WE',pady=(0,5),padx=(0,5),column=0,row=1)
        #Reply-to Input
        self.replyToLabel = tk.Label(self.leftFrame, text='Reply To')
        self.replyToEntry = tk.Entry(self.leftFrame)
        self.replyToLabel.grid(sticky='W',pady=(5,0),padx=(5,0),column=1,row=0)
        self.replyToEntry.grid(sticky='WE',pady=(0,5),padx=(5,0),column=1,row=1)
        # Subject Input
        self.subjectLabel = tk.Label(self.leftFrame, text='Subject')
        self.subjectEntry = tk.Entry(self.leftFrame)
        self.subjectLabel.grid(sticky='W', pady=(5,0), columnspan=2)
        self.subjectEntry.grid(sticky='WE', pady=(0,5), columnspan=2)
        #Body Input
        self.bodyLabel = tk.Label(self.leftFrame, text='Body')
        self.bodyText = tk.Text(self.leftFrame, )
        self.bodyLabel.grid(sticky='W', pady=(5,0), columnspan=2)
        self.bodyText.grid(sticky='WE', pady=(0,5), columnspan=2)
        # Right column
        self.rightFrame = tk.Frame(root)
        self.rightFrame.grid(row=0, column=1, sticky='NW', padx=(5, 10))
        # Round Number Input
        self.roundLabel = tk.Label(self.rightFrame, text='Round Number')
        self.roundEntry = tk.Entry(self.rightFrame)
        self.roundLabel.grid(row='0', sticky='W', pady=(5,0), columnspan=2)
        self.roundEntry.grid(row='1', sticky='WE', pady=(0,5), columnspan=2)
        # Round File Input
        self.roundFileLabel = tk.Label(self.rightFrame, text='Round File (.csv)')
        self.roundFileEntry = tk.Entry(self.rightFrame, state='disabled')
        self.roundFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.set_filename(self.roundFileEntry))
        self.roundFileLabel.grid(row='2', sticky='W', pady=(5,0), columnspan=2)
        self.roundFileButton.grid(row='3', column=0)
        self.roundFileEntry.grid(row='3', column=1, sticky="NSEW")
        # Team File Input
        self.teamFileLabel = tk.Label(self.rightFrame, text='Team File (.csv)')
        self.teamFileEntry = tk.Entry(self.rightFrame, state='disabled')
        self.teamFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.set_filename(self.teamFileEntry))
        self.teamFileLabel.grid(row='4', sticky='W', pady=(5,0), columnspan=2)
        self.teamFileButton.grid(row='5', column=0)
        self.teamFileEntry.grid(row='5', column=1, sticky="NSEW")
        # Submit button
        self.submitButton = tk.Button(root, text='Send', command=self.submit )
        self.submitButton.grid(stick='WE', row=1,columnspan=2, padx=10, pady=10)

        # Load settings
        if not os.path.isfile('settings.ini'):
            tk.messagebox.showerror('Error', 'Ziggy Mailer requires a file called settings.ini to run. Read README.md for details.' )
            root.destroy()
        config = cfg.ConfigParser()
        config.read('settings.ini')
        values = config['values']
        general = config['general']
        default = {
                'from_email'    :   values.get('FromEmail'),
                'reply_to'      :   values.get('ReplyTo'),
                'subject'       :   values.get('Subject'),
                'body'          :   values.get('Body'),
                'round_number'  :   values.get('RoundNumber'),
                'round_file'    :   values.get('RoundFile'),
                'team_file'     :   values.get('TeamFile')
        }

        # Create sendgrid client
        self.sg = sendgrid.SendGridAPIClient(apikey=general.get('APIKey', ''))

        # Set default values
        # From Input
        value = tk.StringVar(root, default.get('from_email'))
        self.fromEntry.configure(textvariable = value)
        # Reply-to Input
        value = tk.StringVar(root, default.get('reply_to'))
        self.replyToEntry.configure(textvariable = value)
        # Subject Input
        value = tk.StringVar(root, default.get('subject'))
        self.subjectEntry.configure(textvariable = value)
        # Round Number Input
        value = tk.StringVar(root, default.get('round_number'))
        self.roundEntry.configure(textvariable = value)
        # Body Input
        for line in default.get('body').split('\\n'):
            self.bodyText.insert( 'end', line + '\n')
        # Round File Input
        value = tk.StringVar(root, default.get('round_file'))
        self.roundFileEntry.configure(state = 'normal')  # entry can't be edited if it's disabled
        self.roundFileEntry.configure(textvariable = value)
        self.roundFileEntry.configure(state = 'disabled')
        # Team Data Input
        self.teamFileEntry.configure(state = 'normal')  # entry can't be edited if it's disabled
        value = tk.StringVar(root, default.get('team_file'))
        self.teamFileEntry.configure(textvariable = value)
        self.teamFileEntry.configure(state = 'disabled')

    def set_filename(self, target):
        """Update a file name input"""
        assert isinstance(target, tk.Entry), 'The target of set_filename() must be an instance of tk.Entry.'
        
        filename = askopenfilename(filetypes=[('Comma Separated Values', '*.csv')])
        if filename:
            target.configure(state = 'normal') # text can't be edited if it's disabled
            target.delete(0, 'end')
            target.insert(0, filename)
            target.xview('end')
            target.configure(state = 'disabled')

    def submit(self):
        """Build and send postings to each room."""
        from_email = self.fromEntry.get()
        reply_to = self.replyToEntry.get()
        subject = self.subjectEntry.get()
        body = self.bodyText.get('1.0', 'end')
        round_number = str(self.roundEntry.get())
        round_file = self.roundFileEntry.get()
        team_file = self.teamFileEntry.get()

        try:
            assert from_email, 'There is no "From" address. Please specify one.'
            assert subject, 'The subject is empty. Please write a suject line.'
            assert len(subject) < 78, 'The subject must be fewer than 78 characters long. Please shorten it.'  # The SendGrid API will not accept subjects that are longers than 78 characters
            assert round_number, 'There is no round number. Please specify one.'

            this_round = Round(round_number, round_file, team_file)

            assert this_round.count_rooms() <= 1000, 'There are %i rooms, but the SendGrid API only allows up to 1,000 at once. Reduce the number of rooms.' % this_round.count_rooms() # The SendGrid API will not accept more than 1,000 personalizations

            mail = Mail( from_email = Email(from_email),
                         subject = subject,
                         to_email = Email('user@server.com','Firstname Lastname'),  # The API malfunctions if this field is "none", so a dummy address is inserted. It will be removed before the message is sent.
                         content = Content('text/plain', body )
                        )
            for room in this_round.rooms:
                pers = Personalization()
                for participant in room.participants:
                    pers.add_to(participant)
                pers.add_substitution( Substitution('[aff]', room.affirmative) )
                pers.add_substitution( Substitution('[neg]', room.negative) )
                pers.add_substitution( Substitution('[round]', this_round.number ) )
                mail.add_personalization(pers)
            del mail.personalizations[0]  # Remove the dummy address

            # Send an API request to SendGrid
            response = self.sg.client.mail.send.post(request_body=mail.get())
            if __debug__:
                print('Mail Object:')
                print(mail.__dict__)
                print('Room Object')
                print(room.__dict__)
                print(response.status_code)
                print(response.body)
                print(response.headers)

            # Tell the user that the request was successful
            room_count = len(this_round.rooms)
            tk.messagebox.showinfo( 'Message Sent', 'The message was sent to %i rooms and %i e-mail addresses.' % ( this_round.count_rooms(), this_round.count_emails() ) )

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
        round_data = read_csv(round_file)
        assert 'AFF' in round_data[0] and\
               'NEG' in round_data[0],\
               'The round data file is not formatted correctly. Make sure it contains these columns (case-sensive): "AFF", and "NEG".'

        assert os.path.isfile(team_file), 'The Round File does not exist. Make sure one is selected.'
        team_data = read_csv(team_file)
        assert 'Team' in team_data[0] and\
               'First Name 1' in team_data[0] and\
               'Last Name 1' in team_data[0] and\
               'Email 1' in team_data[0] and\
               'First Name 2' in team_data[0] and\
               'Last Name 2' in team_data[0] and\
               'Email 2' in team_data[0] and\
               'Email 3' in team_data[0] and\
               'Email 4' in team_data[0],\
               'The team data file is not formatted correctly. Make sure it contains these columns (case-sensive): "Team", "First Name 1", "Last Name 1", "Email 1", "First Name 2", "Last Name 2", "Email 2", "Email 3", and "Email 4".'

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
                    # Emails 3 and 4 are for parents
                    email3 = team_row['Email 3']
                    if email3: participants.append( Email(email3) )
                    email4 = team_row['Email 4']
                    if email4: participants.append( Email(email4) )

            room = Room(affirmative, negative, participants)
            self.rooms.append(room)

    def count_rooms(self):
        """Count the number of rooms in a round."""
        return len(self.rooms)

    def count_emails(self):
        """Count the number of e-mail addresses that this room's postings will
        be sent to."""
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


def read_csv(file_name):
    """Load a CSV file into a Python data structure"""
    result = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
        file.close()
    return result

"""Main Loop"""
global root

root = tk.Tk()
ZiggyMailer()
root.mainloop()
