import { app, dialog } from 'electron';
import settings from 'electron-settings';

module.exports = () => {
    settings.deleteAll();
    if (!settings.has('sendgrid.key')) {
        dialog.showMessageBox({
            type: "question",
            title: "Set Sendgrid API Key",
            message: "Hi, I need your Sendgrid API key to send emails.",
            detail: "I won't be able to send email without it.",
            buttons: ['Set Key', 'Cancel']
        }, response => {
            if (response === 0) {
                dialog.showMessageBox({
                    type: "error",
                    message: "Oopsie!",
                    detail: "I don't have this feature yet. Hopefully I'll have it soon!"
                });
            }
        });
    }
}