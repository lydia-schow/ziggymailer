import sys
import csv
import os
import sendgrid
from sendgrid.helpers.mail import *

import tkinter as tk
from tkinter.filedialog import askopenfilename

sg = sendgrid.SendGridAPIClient(apikey='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')

class ZiggyMailer:
    # Define the GUI
    def __init__(self, root):
        # Left column
        self.leftFrame = tk.Frame(root)
        self.leftFrame.grid(row=0, column=0, sticky='NW', padx=(10,5))
        #From Input
        self.fromLabel = tk.Label(self.leftFrame, text='From')
        self.fromEntry = tk.Entry(self.leftFrame)
        self.fromLabel.grid(sticky='W', pady=(5,0))
        self.fromEntry.grid(sticky='WE', pady=(0,5))
        # Subject Input
        self.subjectLabel = tk.Label(self.leftFrame, text='Subject')
        self.subjectEntry = tk.Entry(self.leftFrame)
        self.subjectLabel.grid(sticky='W', pady=(5,0))
        self.subjectEntry.grid(sticky='WE', pady=(0,5))
        #Information Input
        self.informationLabel = tk.Label(self.leftFrame, text='Information')
        self.informationText = tk.Text(self.leftFrame)
        self.informationLabel.grid(sticky='W', pady=(5,0))
        self.informationText.grid(sticky='WE', pady=(0,5))
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
        self.roundFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.setfilename(self.roundFileEntry))
        self.roundFileEntry = tk.Entry(self.rightFrame, state='disabled')
        self.roundFileLabel.grid(row='2', sticky='W', pady=(5,0), columnspan=2)
        self.roundFileButton.grid(row='3', column=0)
        self.roundFileEntry.grid(row='3', column=1, sticky="NSEW")
        # Team File Input
        self.teamFileLabel = tk.Label(self.rightFrame, text='Team File (.csv)')
        self.teamFileButton = tk.Button(self.rightFrame, text="Open",
            command=lambda:self.setfilename(self.teamFileEntry))
        self.teamFileEntry = tk.Entry(self.rightFrame, state='disabled')
        self.teamFileLabel.grid(row='4', sticky='W', pady=(5,0), columnspan=2)
        self.teamFileButton.grid(row='5', column=0)
        self.teamFileEntry.grid(row='5', column=1, sticky="NSEW")
        # Submit button
        self.submitButton = tk.Button(root, text='Send', command=self.submit)
        self.submitButton.grid(stick='WE', row=1,columnspan=2, padx=10, pady=10)

    # Update a file name input
    def setfilename(self, target):
        # TODO: assert that 'target' is an instance of tk.Entry
        filename = askopenfilename(filetypes=[('Comma Separated Values', '*.csv')])
        target.configure(state = 'normal') # text can't be edited if it's disabled
        target.delete(0, 'end')
        target.insert(0, filename)
        target.xview('end')
        target.configure(state = 'disabled')

    # Load a CSV file into a Python data structure
    def readCSV(self, file_name):
        result = []
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for room in reader:
                result.append(room)
        return result

    # Gather the form's inputs and send emails
    def submit(self):
        #TODO: assert assumptions about input.

        from_email = self.fromEntry.get()
        subject = self.subjectEntry.get()
        information = self.informationText.get('1.0', 'end')
        round_number = int(self.roundEntry.get())
        round_file = self.roundFileEntry.get()
        team_file = self.teamFileEntry.get()

        self.sendmail(from_email, subject, information, round_number,
            round_file, team_file )

    # E-mail postings to all the participants
    def sendmail( self, from_email, subject, information, round_number,
        round_file, team_file ):
        #TODO: assert assumptions about input.
        team_data = self.readCSV( team_file )
        this_round = self.readCSV( round_file )
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
            message = '<!DOCTYPE html><html><head><meta charset="UTF-8"></head>\
                       <body>\
                            <p>Hello,</p>\
                            <p>Your debate round %i pairing is as follows: \
                            Affirmative %s vs. Negative %s.</p>\
                            <p>%s</p>\
                        </body></html>'\
                        % (round_number, room['AFF'], room['NEG'], information)

            # Send the message
            mail = Mail( Email(from_email), subject, Email(recipients),
                Content('text/html', message ) )
            response = sg.client.mail.send.post(request_body=mail.get())
            if __debug__:
                print(response.status_code)
                print(response.body)
                print(response.headers)

"""Main Loop"""
root = tk.Tk()
app = ZiggyMailer(root)
root.mainloop()
