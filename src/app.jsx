import React from 'react';
import Settings from './settings';

export default class App extends React.Component {

  render() {
    return (
      <div>
        <div className="container p-5">
          <h1>Ziggy Mailer</h1>
          <form>

            <div className="row">
              <div className="form-group col-sm-6">
                <label htmlFor="from">From</label>
                <input type="text" id="from" className="form-control" />
              </div>
              <div className="form-group col-sm-6">
                <label htmlFor="reply-to">Reply to</label>
                <input type="text" id="reply-to" className="form-control" />
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="subject">Subject</label>
              <input type="text" id="subject" className="form-control" />
            </div>

            <div className="form-group">
              <label htmlFor="message-body">Body</label>
              <textarea id="message-body" rows="8" className="form-control" />
            </div>

            <div className="row">

              <div className="form-group col-sm-4">
                <label htmlFor="round-number">Round Number</label>
                <input type="number" id="round-number" className="form-control" />
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="round-file">Round File</label>
                <input type="file" id="round-file" className="form-control" />
              </div>

              <div className="form-group col-sm-4">
                <label htmlFor="team-file">Team File</label>
                <input type="file" id="team-file" className="form-control" />
              </div>

            </div>

            <button type="submit" className="btn btn-primary btn-block" disabled>Send
            Emails</button>
          </form>
        </div>
        <Settings />
      </div>
    );
  }

}
