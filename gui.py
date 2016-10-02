from tkinter import *

root = Tk()

# Left column
leftFrame = Frame(root)
leftFrame.grid(row=0, column=0, sticky='NW', padx=(10,5))

fromLabel = Label(leftFrame, text='From')
fromEntry = Entry(leftFrame)
fromLabel.grid(sticky='W', pady=(5,0))
fromEntry.grid(sticky='WE', pady=(0,5))

subjectLabel = Label(leftFrame, text='Subject')
subjectEntry = Entry(leftFrame)
subjectLabel.grid(sticky='W', pady=(5,0))
subjectEntry.grid(sticky='WE', pady=(0,5))

informationLabel = Label(leftFrame, text='Information')
informationText = Text(leftFrame)
informationLabel.grid(sticky='W', pady=(5,0))
informationText.grid(sticky='WE', pady=(0,5))

# Right column
rightFrame = Frame(root)
rightFrame.grid(row=0, column=1, sticky='NW', padx=(5, 10))

roundLabel = Label(rightFrame, text='Round Number')
roundEntry = Entry(rightFrame)
roundLabel.grid(sticky='W', pady=(5,0))
roundEntry.grid(sticky='WE', pady=(0,5))

roundFileLabel = Label(rightFrame, text='Round File (.csv)')
roundFileFrame = Frame(rightFrame)
roundFileButton = Button(roundFileFrame, text="Open")
roundFileEntry = Entry(roundFileFrame)
roundFileEntry.configure(state='disabled')
roundFileLabel.grid(sticky='W', pady=(5,0))
roundFileFrame.grid(sticky='WE', pady=(0,5))
roundFileButton.grid(row=0, column=0)
roundFileEntry.grid(row=0, column=1, sticky="NSEW")

teamFileLabel = Label(rightFrame, text='Team File (.csv)')
teamFileFrame = Frame(rightFrame)
teamFileButton = Button(teamFileFrame, text="Open")
teamFileEntry = Entry(teamFileFrame)
teamFileEntry.configure(state='disabled')
teamFileLabel.grid(sticky='W', pady=(5,0))
teamFileFrame.grid(sticky='WE', pady=(0,5))
teamFileButton.grid(row=0, column=0)
teamFileEntry.grid(row=0, column=1, sticky="NSEW")

submitButton = Button(root, text='Send')
submitButton.grid(stick='WE', row=1,columnspan=2, padx=10, pady=10)

root.mainloop()
