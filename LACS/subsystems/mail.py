import imaplib
import email
import syslog

class MailManager:
    def __init__(self, server, email, password):
        self.server = server
        self.email = email
        self.password = password
    
    def get_new_messages_periodic(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.server)
            self.mail.login(email, self.password)
            self.mail.select("inbox")

            status, data = self.mail.search(None, 'UNSEEN')
            assert status == "OK"
            new_mail_messages = []

            mail_ids = []
            for block in data:
                mail_ids += block.split()
            for id in mail_ids:
                status, mail_data = self.mail.fetch(id, '(RFC822)')
                assert status == "OK"
                for response_part in mail_data:
                    if isinstance(response_part, tuple):
                        message = email.message_from_bytes(response_part[1])
                        new_mail_messages.append(message)
            return new_mail_messages
        except AssertionError:
            syslog.syslog(syslog.LOG_ERR, "Status is not OK after mail search.")
        except TimeoutError:
            syslog.syslog(syslog.LOG_WARNING, "(ignorable) Connection timed out")
        except ConnectionError:
            syslog.syslog(syslog.LOG_ERR, "Connection error occurred.")
        return []