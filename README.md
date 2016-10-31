# Ziggy Mailer
Automate e-mail postings for an online debate tournament.

## Legal
This project is offered as-is without warranty.
Elijah Schow © 2016

## Installation
1. Install the latest version of Python 3 from [Python.org](https://www.python.org/)
2. Install [pip for Python 3](https://pip.pypa.io/en/stable/installing/)
3. Install the sendgrid api module through pip
    > python3 -m pip install sendgrid

4. Run ZiggyMailer.py from the terminal, Python Launcher, or IDLE

## Settings.ini
This program will not work without a valid SendGrid API key. Before running it,
create a settings.ini file and add your API key. Also populate the "values"
section to set default values for the form inputs.

```
[general]
APIKey =

[values]
FromEmail =
ReplyTo =
Subject =
Body =
RoundNumber =
RoundFile = data/Example Round.csv
TeamFile = data/Example Team Data.csv
```
