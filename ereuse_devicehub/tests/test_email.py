from smtplib import SMTPRecipientsRefused

from ereuse_devicehub.mails.mails import suppressAndLogSendingException
from ereuse_devicehub.tests import TestStandard
from flask_mail import Message


class TestEmail(TestStandard):
    def test_suppressAndLogSendingException(self):
        self.app.config['MAIL_DEBUG'] = False
        self.app.config['MAIL_SUPPRESS_SEND'] = False
        with self.app.app_context():
            message = Message('foobar', recipients=['foo@bar.com'])
            with suppressAndLogSendingException(message):
                # This error should be catch and logged
                raise SMTPRecipientsRefused(recipients=['foo@bar.com'])
