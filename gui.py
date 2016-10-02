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
roundLabel.grid(row='0', sticky='W', pady=(5,0), columnspan=2)
roundEntry.grid(row='1', sticky='WE', pady=(0,5), columnspan=2)

roundFileLabel = Label(rightFrame, text='Round File (.csv)')
roundFileButton = Button(rightFrame, text="Open")
roundFileEntry = Entry(rightFrame)
roundFileEntry.configure(state='disabled')
roundFileLabel.grid(row='2', sticky='W', pady=(5,0), columnspan=2)
roundFileButton.grid(row='3', column=0)
roundFileEntry.grid(row='3', column=1, sticky="NSEW")

teamFileLabel = Label(rightFrame, text='Team File (.csv)')
teamFileButton = Button(rightFrame, text="Open")
teamFileEntry = Entry(rightFrame)
teamFileEntry.configure(state='disabled')
teamFileLabel.grid(row='4', sticky='W', pady=(5,0), columnspan=2)
teamFileButton.grid(row='5', column=0)
teamFileEntry.grid(row='5', column=1, sticky="NSEW")

submitButton = Button(root, text='Send')
submitButton.grid(stick='WE', row=1,columnspan=2, padx=10, pady=10)

root.mainloop()
