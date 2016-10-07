# Ziggy Mailer

## Installation
1. Install python 3: https://www.macobserver.com/tmo/article/how-to-upgrade-your-mac-to-python-3
    A. Download the installer from python.org
    B. Double click the file you downloaded.
    C. Allow third party apps: System Preferences > Security and Privacy > General
    D. Right click "Python.mpkg" and select Open With > Installer.app

2. Install dependancies
    A. Open the terminal
    B. Upgrade pip for python3
        > python3 pip install -U pip

    C. Install sendgrid for python3
        > python3 pip install sendgrid

    D. Install pyinstaller
        > python3 pip install pyinstaller

    E. If these commands don't work, run them as an administrator by adding "sudo" to the beginning. You will probably be asked to enter your password.

    e.g. this:
        > python3 pip install -U pip

    becomes this:
        > sudo python3 pip install -U pip

5. Download and Build ZiggyMailer
    A. Download the project and extract it somewhere convenient
    B. Open the terminal and navigate to the extracted project
    C. Run pyinstaller to generate a .app file
    > pyinstaller ZiggyMailer.py -F

6. Test the application
    A. Open file exporer and find the project's folder
    B. Go to the "dist" subfolder (short for "distribution")
    C. Double-click the .app file

7. If you're happy with the application, find a convenient place to put it.


## Spreadsheet Changes
  1. Add "Email 1" and "Email 2" to the "Team Data" sheet.
  2. Export each sheet as a .CSV (comma separated) file.
