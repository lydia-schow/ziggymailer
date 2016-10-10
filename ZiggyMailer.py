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

    def readCSV(self, file_name):
        """Load a CSV file into a Python data structure"""
        result = []
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for room in reader:
                result.append(room)
        return result

    def submit(self):

        """Gather the form's inputs and send emails"""
        from_email = self.fromEntry.get()
        reply_to = self.replyToEntry.get()
        subject = self.subjectEntry.get()
        body = self.bodyText.get('1.0', 'end')
        round_number = int(self.roundEntry.get())
        round_file = self.roundFileEntry.get()
        team_file = self.teamFileEntry.get()

        try:
            result = self.sendmail(from_email, reply_to, subject, body,
            round_number, round_file, team_file )
        except AssertionError as error:
            tk.messagebox.showerror('Error', error)
        except HTTPError as error:
            message = error.msg
            if error.code == 401:
                message = 'SendGrid rejected your request. Make sure you are using a valid API key.'
            elif error.code == 404:
                message = 'SendGrid\'s server could not be found. Check if their servers are down for maintenance.'
            tk.messagebox.showerror('Error', message)
        tk.messagebox.showinfo( 'Message Sent', 'The message was sent to %i rooms and %i participants.'
            % (result[0], result[1]) )

    def sendmail( self, from_email, reply_to, subject, body, round_number,
        round_file, team_file ):
        """Send postings to each participant in each room."""
        #Assertions
        assert os.path.isfile(team_file), 'The Team Data file does not exist. Make sure one is selected.'
        assert os.path.isfile(round_file), 'The Round File does not exist. Make sure one is selected.'
        assert from_email, 'There is no "From" address. Please specify one.'
        assert subject, 'The subject is empty. Please write a suject line.'
        assert len(subject) < 78, 'The subject must be fewer than 78 characters long. Please shorten it.'  # Required by the SendGrid API
        assert round_number, 'There is no round number. Please specify one.'
        # Read CSV files
        team_data = self.readCSV( team_file )
        round_data = self.readCSV( round_file )
        keys = ["Team", "Email 1", "Email 2"]
        for key in keys:
            assert key in team_data[0], 'The team data file is not formatted correctly. Make sure it contains this column (case-sensitive): "%s"' % key
        keys = ["AFF", "NEG"]
        for key in keys:
            assert key in round_data[0], 'The round data file is not formatted correctly. Make sure it contains this column (case-sensitive): "%s"' % key
        room_count = len( round_data )
        assert( room_count < 3000 )
        # Parse CSV files and send messages
        participant_count = 0
        for room in round_data:
            recipients = []
            for row in team_data:
                if row['Team']==room['AFF'] or row['Team']==room['NEG']:
                    keys = ['Email 1', 'Email 2']
                    for key in keys:
                        # Don't add blank email addresses
                        if row[key]: recipients.append( row[key] )
                        participant_count += 1
            assert len(recipients) > 0, 'There are no recipients. Double check the Team File and Round File for errors.'
            assert len(recipients) < 10000, 'There must be fewer than 10,000 recipients per room.'
            to_emails = str(recipients).strip('[]').replace('\'', '')
            # Format the message
            parameters = {
                'round' : round_number,
                'aff' : room['AFF'],
                'neg' : room['NEG'],
            }
            message = body.format_map(Parameter(parameters))
            # Send the message
            mail = Mail( from_email = Email(from_email),
                         subject = subject,
                         to_email = Email(to_emails),
                         content = Content('text/plain', message )
                        )
            if reply_to: mail.set_reply_to( Email(reply_to) )
            response = sg.client.mail.send.post(request_body=mail.get())
            if __debug__:
                print('\n\n------')
                print('\nPARAMETERS')
                for key in parameters:
                    print('%s : %r' % (str(key), parameters[key] ),
                        logfile )
                print('\nRECIPIENTS:')
                for item in recipients: print(item)
                print('\nRESPONSE:')
                print(response.status_code)
                print(response.body)
                print(response.headers)
        return (room_count, participant_count)


"""Main Loop"""
config = cfg.ConfigParser()
config.read('settings.ini')
sg = sendgrid.SendGridAPIClient(apikey=config['general']['APIKey'])
root = tk.Tk()
app = ZiggyMailer(root)

root.mainloop()
