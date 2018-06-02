import settings from 'electron-settings';
import fs from 'fs';
import { remote } from 'electron';
import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, UncontrolledAlert } from 'reactstrap';

const { dialog } = remote;
const SENDGRID_KEY = 'form.sendgridKey';

export default class App extends React.Component {

  constructor(...args) {
    super(...args);

    this.state = {
      form: Object.assign({
        from: 'ziggyonlinedebate@gmail.com',
        replyTo: 'ziggyonlinedebate@gmail.com',
        body: 'Hello,\nYour debate round [roud] pairing is as follows:\nAffirmative [aff] vs. Negative [neg]',
        subject: 'Ziggy Debate - Postings',
        roundNumber: '1',
        roundFile: '',
        teamFile: '',
        sendgridKey: '',
      }, settings.get('form')),
      settingsIsOpen: !this.canSend(),
    };
  }

  submit (event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    console.log('Email ALL THE THINGS');
  }

  canSend() {
    return !!settings.get(SENDGRID_KEY);
  }

  toggleSettings(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    this.setState({ settingsIsOpen: !this.state.settingsIsOpen });
  }

  submitSettings(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    settings.set(SENDGRID_KEY, this.state.form.sendgridKey);
    this.toggleSettings();
  }

  change(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    settings.set(`form.${name}`, value);
    this.setState({
      form: {
        [name]: value,
      },
    });
  }

  openFile(callback) {
    const options = {
      filters: [{ name: 'CSV', extensions: ['csv'] }],
    };
    dialog.showOpenDialog(options, (filenames) => {
      if (!filenames) return;
      fs.readFile(filenames[0], (error, data) => {
        if (error) {
          dialog.showErrorBox('I had trouble opening the file.', error);
          return;
        }
        callback(data);
      });
    });
  }

  openTeamFile(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    this.openFile(console.dir);
  }

  openRoundFile(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }
    this.openFile(console.dir);
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
                  value={this.state.form.from}
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
                  value={this.state.form.replyTo}
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
                value={this.state.form.subject}
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
                value={this.state.form.body}
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
                  value={this.state.form.roundNumber}
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
                <p>{this.state.form.roundFile}</p>
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
                <p>{this.state.form.teamFile}</p>
              </div>

            </div>

            <button className="btn btn-link btn-block" onClick={this.toggleSettings}>Settings</button>
            <button type="submit" className="btn btn-primary btn-block" disabled={!this.canSend()}>Send Emails</button>
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
                  value={this.state.form.sendgridKey}
                  className="form-control"
                />
                <small className="help-text">I won&apos;t be able to send email without it.</small>
              </div>
            </ModalBody>
            <ModalFooter>
              <Button color="link" onClick={e => this.toggleSettings(e)}>Cancel</Button>
              <Button color="primary" type="submit">Set Key</Button>{' '}
            </ModalFooter>
          </form>
        </Modal>

      </div>
    );
  }

}
