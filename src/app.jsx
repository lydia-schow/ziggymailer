/*
✓ Feedback (error, success)
○ Copy and paste
○ HTML

○ Ziggy app icon
○ Move "settings" button to a better place
○ Show success/failure for individual messages
○ Show sendgrid status for individual messages
○ Cancel submissions that are taking a long time
○ Security https://electronjs.org/docs/tutorial/security
○ Upgrade to latest node version
○ Fix jsx-a11y warnings
○ reset settings to defaults (except sendgrid and template key)
*/

import settings from 'electron-settings';
import fs from 'fs';
import { EOL } from 'os';
import path from 'path';
import csv from 'csv';
import { remote } from 'electron';
import React from 'react';
import { UncontrolledAlert, Modal, ModalHeader, ModalBody } from 'reactstrap';
import { find, values, defaultsDeep, uniq } from 'lodash';
import mail from '@sendgrid/mail';
import flat from 'flat';

const { dialog, Menu } = remote;

/**
 * Add context menus to all inputs
 * source: https://github.com/electron/electron/issues/4068#issuecomment-170911307
 */
const InputMenu = Menu.buildFromTemplate([{
  label: 'Undo',
  role: 'undo',
}, {
  label: 'Redo',
  role: 'redo',
}, {
  type: 'separator',
}, {
  label: 'Cut',
  role: 'cut',
}, {
  label: 'Copy',
  role: 'copy',
}, {
  label: 'Paste',
  role: 'paste',
}, {
  type: 'separator',
}, {
  label: 'Select all',
  role: 'selectall',
},
]);

document.body.addEventListener('contextmenu', (e) => {
  e.preventDefault();
  e.stopPropagation();

  let node = e.target;

  while (node) {
    if (node.nodeName.match(/^(input|textarea)$/i) || node.isContentEditable) {
      InputMenu.popup(remote.getCurrentWindow());
      break;
    }
    node = node.parentNode;
  }
});

// Create a promise that resolves in <ms> milliseconds
const timeout = ms =>
  new Promise((resolve, reject) => {
    const id = setTimeout(() => {
      clearTimeout(id);
      resolve(new Error(`Timed out in ${ms} ms.`));
    }, ms);
  });

/* Regex source: http://emailregex.com/ */
const emailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const isEmail = value => emailRegex.test(value);

export default class App extends React.Component {
  static openFile(title = 'Open file', callback) {
    const options = {
      title,
      filters: [{ name: 'CSV', extensions: ['csv'] }],
    };
    dialog.showOpenDialog(options, (filenames) => {
      if (!filenames) return;
      const filename = filenames[0];
      fs.readFile(filename, (error, rawData) => {
        if (error) {
          dialog.showErrorBox('I had trouble opening the file.', error);
          App.log(error);
          return;
        }
        /* Auto-detect columns http://csv.adaltas.com/parse/ */
        const parseOptions = { columns: true };
        const parseCallback = (_error, data) => {
          if (_error) {
            dialog.showErrorBox('I had trouble parsing the file. It might not be a valid CSV.', _error);
            App.log(error);
            return;
          }
          callback({ data, filename });
        };
        csv.parse(rawData, parseOptions, parseCallback);
      });
    });
  }

  static log(...args) {
    console.error(...args);
    /* `EOL` stands for `end of line`. I'm using it because Windows and Unix use
    different line endings */
    const date = Date.now().toString();
    const message = [...args].join(' ');
    const data = `${date} - ${message}${EOL}`;
    fs.appendFile('error.log', data, (_error) => {
      if (_error) console.error('Couldn\'t write error log.');
    });
  }

  constructor(...args) {
    super(...args);

    // Load defaults from the application state
    this.state = defaultsDeep(
      settings.get('state'),
      {
        sendgridKey: '',
        from: 'ziggyonlinedebate@gmail.com',
        replyTo: 'ziggyonlinedebate@gmail.com',
        body: '<p>Hello,</p><p>Your debate round {{Round}} pairing is as follows:</p><p>Affirmative {{AFF.Team}} vs. Negative {{NEG.Team}}</p>',
        subject: 'Ziggy Debate - Postings',
        roundNumber: '1',
        teamFile: '',
        teamData: [],
        roundFile: '',
        roundData: [],
        settingsIsOpen: true,
        templateId: 'c4ca7f9b-e077-4cd9-a4b3-ebf8752c1879',
      },
    );
    this.state.settingsIsOpen = this.state.sendgridKey.length === 0;
    this.state.status = 'idle'; // "idle" | "loading" | "success" | "error"
  }

  componentDidUpdate(props, state) {
    settings.set('state', state);
  }

  submit(event) {
    this.setState(state => ({ ...state, status: 'loading' }));

    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    const rounds = this.state.roundData;
    const teams = this.state.teamData;
    const Round = this.state.roundNumber;
    const roundPromises = rounds.map((round) => {
      const AFF = find(teams, ({ Team }) => Team && Team === round.AFF);
      const NEG = find(teams, ({ Team }) => Team && Team === round.NEG);
      if (!AFF) {
        return Promise.reject(new Error(`Could not find AFF team ${round && round.AFF}. Make sure they match in the round and team file.`));
      }
      if (!NEG) {
        return Promise.reject(new Error(`Could not find NEG team ${round && round.NEG}. Make sure they match in the round and team file.`));
      }

      /* Extract all unique email addresses from both teams */
      const emails = uniq(values(NEG).concat(values(AFF)).filter(isEmail));
      if (emails.length === 0) {
        return Promise.rejeect(new Error(`I did not find email addresses for ${AFF && AFF.Team} and ${NEG && NEG.Team}. Add some then try again.`));
      }

      const message = {
        from: this.state.from,
        to: emails,
        /* SendGrid doesn't support reply-to multiple addresses:
        https://github.com/sendgrid/sendgrid-csharp/issues/339 */
        // replyTo: emails,
        subject: this.state.subject,
        html: this.state.body,
        templateId: this.state.templateId,
        substitutions: flat({
          Round,
          AFF,
          NEG,
        }),
      };

      mail.setApiKey(this.state.sendgridKey);
      return mail.send(message);
      // return timeout(100000); // this is for testing without spamming the API
    });

    Promise.all(roundPromises)
      .then((success) => {
        this.setState(state => ({
          ...state,
          status: 'success',
          success,
        }));
      })
      .catch((error) => {
        this.setState(state => ({
          ...state,
          status: 'error',
          error,
        }));
        App.log(error);
      });
  }

  canSubmit() {
    return this.state.sendgridKey
      && this.state.sendgridKey.length > 0
      && this.state.roundData.length > 0
      && this.state.teamData.length > 0;
  }

  toggleSettings(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    this.setState({ settingsIsOpen: !this.state.settingsIsOpen });
  }

  change(event) {
    const { target, name } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    this.setState(state => ({
      ...state,
      [name]: value,
    }));
  }

  openTeamFile(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    App.openFile('Team file', ({ data, filename }) => this.setState(state => ({
      ...state,
      teamFile: filename,
      teamData: data,
    })));
  }

  openRoundFile(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    App.openFile('Round file', ({ data, filename }) => this.setState(state => ({
      ...state,
      roundFile: filename,
      roundData: data,
    })));
    // TODO: throw an error if columns are missing
  }

  isIdle() {
    return this.state.status === 'idle';
  }

  isLoading() {
    return this.state.status === 'loading';
  }

  isError() {
    return this.state.status === 'error';
  }

  isSuccess() {
    return this.state.status === 'success';
  }

  render() {
    return (
      <div>
        <div className="container p-5">
          <h1>Ziggy Mailer</h1>
          <form onSubmit={e => this.submit(e)}>

            <div className="row">
              <div className="form-group col-sm-6">
                <label htmlFor="from">From</label>
                <input
                  name="from"
                  type="text"
                  id="from"
                  className="form-control"
                  value={this.state.from}
                  onChange={e => this.change(e)}
                />
              </div>
              <div className="form-group col-sm-6">
                <label htmlFor="reply-to">Reply to</label>
                <input
                  name="replyTo"
                  type="text"
                  id="reply-to"
                  className="form-control"
                  value={this.state.replyTo}
                  onChange={e => this.change(e)}
                />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject</label>
              <input
                name="subject"
                type="text"
                id="subject"
                className="form-control"
                value={this.state.subject}
                onChange={e => this.change(e)}
              />
            </div>

            <div className="form-group">
              <label htmlFor="message-body">Body</label>
              <textarea
                name="body"
                id="message-body"
                rows="8"
                className="form-control"
                value={this.state.body}
                onChange={e => this.change(e)}
              />
            </div>

            <div className="row">

              <div className="form-group col-sm-4">
                <label htmlFor="round-number">Round Number</label>
                <input
                  name="roundNumber"
                  type="number"
                  id="round-number"
                  className="form-control"
                  value={this.state.roundNumber}
                  onChange={e => this.change(e)}
                />
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="round-file">Round File</label>
                <button
                  id="round-file"
                  className="btn btn-block"
                  type="button"
                  onClick={e => this.openRoundFile(e)}
                >
                  Open
                </button>
                <p>{path.basename(this.state.roundFile)}</p>
                {this.state.roundData.length > 0 &&
                  <p>{this.state.roundData.length} room(s)</p>}
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="team-file">Team File</label>
                <button
                  id="team-file"
                  className="btn btn-block"
                  type="button"
                  onClick={e => this.openTeamFile(e)}
                >
                  Open
                </button>
                <p>{path.basename(this.state.teamFile)}</p>
                {this.state.teamData.length > 0 &&
                  <p>{this.state.teamData.length} teams(s)</p>}
              </div>

            </div>

            <button className="btn btn-link btn-block" onClick={e => this.toggleSettings(e)}>Settings</button>
            <button type="submit" className="btn btn-primary btn-block" disabled={!this.canSubmit() || this.isLoading()}>
              Send Emails
              &nbsp;{this.isLoading() && <div className="loader" />}
            </button>
            {this.isError() &&
              <UncontrolledAlert color="danger">
                <strong>I had a problem</strong>
                {(this.state.error && `: ${this.state.error.message}`) || ', but I don\'t know what it was 🤔'}
              </UncontrolledAlert>}
            {this.isSuccess() &&
              <UncontrolledAlert color="success">
                <strong>I sent {this.state.success.length} emails. </strong>
                Check your sendgrid dashboard for more details.
              </UncontrolledAlert>
            }
          </form>
        </div>

        <Modal isOpen={this.state.settingsIsOpen}>
          <form onSubmit={this.submitSettings}>
            <ModalHeader toggle={e => this.toggleSettings(e)}>Settings</ModalHeader>
            <ModalBody>
              {this.state.error && <UncontrolledAlert color="danger">{this.state.error}</UncontrolledAlert>}
              <div className="form-group">
                <label htmlFor="sendgrid-key">Sendgrid API Key</label>
                <input
                  type="password"
                  name="sendgridKey"
                  id="sendgrid-key"
                  onChange={e => this.change(e)}
                  value={this.state.sendgridKey}
                  className="form-control"
                />
                <small className="help-text">
                  {this.canSubmit()
                    ? <span>I automatically saved your key.</span>
                    : <span>I won&apos;t be able to send email without it.</span>
                  }
                </small>
              </div>
              <div className="form-group">
                <label htmlFor="sendgrid-template-id">Sendgrid Template ID (optional)</label>
                <input
                  type="text"
                  name="templateId"
                  id="sendgrid-template-id"
                  onChange={e => this.change(e)}
                  value={this.state.templateId}
                  className="form-control"
                />
              </div>
            </ModalBody>
          </form>
        </Modal>

      </div>
    );
  }
}
