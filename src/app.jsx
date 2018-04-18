import React from 'react';

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

        <div className="modal fade" tabIndex="-1" role="dialog"
          id="settings">
          <div className="modal-dialog" role="document">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Settings</h5>
                <button type="button" className="close" data-dismiss="modal"
                  aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div className="modal-body">
                <div className="form-group">
                  <label htmlFor="sendgrid-key">Sendgrid API Key</label>
                  <input id="zd-settings-sendgrid-key" className="form-control" />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-link"
                  data-dismiss="modal">Cancel</button>
                <button type="button" className="btn btn-primary"
                // onClick={$('#settings').trigger('zd.settings.save')}
                >Set Key</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// import { app, dialog } from 'electron';
// import settings from 'electron-settings';

// module.exports = () => {
//     settings.deleteAll();
//     if (!settings.has('sendgrid.key')) {
//         dialog.showMessageBox({
//             type: "question",
//             title: "Set Sendgrid API Key",
//             message: "Hi, I need your Sendgrid API key to send emails.",
//             detail: "I won't be able to send email without it.",
//             buttons: ['Set Key', 'Cancel']
//         }, response => {
//             if (response === 0) {
//                 dialog.showMessageBox({
//                     type: "error",
//                     message: "Oopsie!",
//                     detail: "I don't have this feature yet. Hopefully I'll have it soon!"
//                 });
//             }
//         });
//     }
// }