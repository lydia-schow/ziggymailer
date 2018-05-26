import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, UncontrolledAlert } from 'reactstrap';
import settings from 'electron-settings';

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

    this.toggleSettings = this.toggleSettings.bind(this);
    this.submitSettings = this.submitSettings.bind(this);
    this.change = this.change.bind(this);
    this.canSend = this.canSend.bind(this);
  }

  canSend() {
    return !!settings.get(SENDGRID_KEY);
  }

  toggleSettings(event) {
    if (event) { event.preventDefault(); }
    this.setState({ settingsIsOpen: !this.state.settingsIsOpen });
  }

  submitSettings(event) {
    if (event) { event.preventDefault(); }
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

  render() {
    return (
      <div>
        <div className="container p-5">
          <h1>Ziggy Mailer</h1>
          <form>

            <div className="row">
              <div className="form-group col-sm-6">
                <label htmlFor="from">From</label>
                <input
                  name="from"
                  type="text"
                  id="from"
                  className="form-control"
                  value={this.state.form.from}
                  onChange={this.change}
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
                  onChange={this.change}
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
                onChange={this.change}
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
                onChange={this.change}
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
                  onChange={this.change}
                />
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="round-file">Round File</label>
                <input
                  name="roundFile"
                  type="file"
                  id="round-file"
                  value={this.state.form.roundFile}
                  className="form-control"
                />
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="team-file">Team File</label>
                <input
                  name="teamFile"
                  type="file"
                  id="team-file"
                  className="form-control"
                  value={this.state.form.teamFile}
                  onChange={this.change}
                />
              </div>

            </div>

            <button className="btn btn-link btn-block" onClick={this.toggleSettings}>Settings</button>
            <button type="submit" className="btn btn-primary btn-block" disabled={!this.canSend()}>Send Emails</button>
          </form>
        </div>

        <Modal isOpen={this.state.settingsIsOpen}>
          <form onSubmit={this.submitSettings}>
            <ModalHeader toggle={this.toggleSettings}>Settings</ModalHeader>
            <ModalBody>
              {this.state.error && <UncontrolledAlert color="danger">{this.state.error}</UncontrolledAlert>}
              <div className="form-group">
                <label htmlFor="sendgrid-key">Sendgrid API Key</label>
                <input
                  type="password"
                  name="sendgridKey"
                  id="sendgrid-key"
                  onChange={this.change}
                  value={this.state.form.sendgridKey}
                  className="form-control"
                />
                <small className="help-text">I won&apos;t be able to send email without it.</small>
              </div>
            </ModalBody>
            <ModalFooter>
              <Button color="link" onClick={this.toggleSettings}>Cancel</Button>
              <Button color="primary" type="submit">Set Key</Button>{' '}
            </ModalFooter>
          </form>
        </Modal>

      </div>
    );
  }

}
