import React from 'react';
import { Button, Modal, ModalBody, ModalFooter, UncontrolledAlert } from 'reactstrap';
import settings from 'electron-settings';

export default class Settings extends React.Component {

  constructor(props) {
    super(props);
    this.toggle = this.toggle.bind(this);
    this.open = this.open.bind(this);
    this.close = this.close.bind(this);
    this.save = this.save.bind(this);
    this.input = this.input.bind(this);
    this.state = {
      isOpen: false,
      sendgridKey: '',
      error: '',
    };
  }

  componentDidMount() {
    if (!settings.has('sendgrid.key')) {
      this.open();
    }
  }

  open() {
    this.setState({
      ...this.state,
      isOpen: true,
    });
  }

  close() {
    this.setState({
      ...this.state,
      isOpen: false,
    });
  }

  toggle() {
    this.setState({
      ...this.state,
      isOpen: !this.state.isOpen,
    });
  }

  save() {
    if (this.state.sendgridKey) {
      settings.set('sendgrid.key', this.state.sendgridKey);
      this.close();
    } else {
      this.setState({
        ...this.state,
        error: 'An API key is required. Cancel if you don\'t want to provide one',
      });
    }
  }

  input(event) {
    this.setState({
      ...this.state,
      sendgridKey: event.target.value,
    });
  }

  render() {
    const isOpen = this.state.isOpen;
    const toggle = this.toggle;
    const save = this.save;
    const input = this.input;
    return (
      <Modal isOpen={isOpen}>
        <ModalBody>
          {this.state.error
            && <UncontrolledAlert color="danger">{this.state.error}</UncontrolledAlert>}
          <div className="form-group">
            <label htmlFor="sendgrid-key">Sendgrid API Key</label>
            <input name="sendgrid.key" className="form-control" onInput={input} />
            <small className="help-text">I won&apos;t be able to send email without it.</small>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button color="link" onClick={toggle}>Cancel</Button>
          <Button color="primary" onClick={save}>Set Key</Button>{' '}
        </ModalFooter>
      </Modal>
    );
  }
}
