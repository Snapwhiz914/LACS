import imaplib
import email

class MailManager:
    def __init__(self, server, port, addr, password):
        self.server = server
        self.port = port
        self.addr = addr
        self.password = password
    
    def get_new_messages_periodic(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.server, self.port)
            self.mail.login(self.addr, self.password)
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
            print("Status is not OK after mail search.")
        except TimeoutError:
            print("(ignorable) Mail Connection timed out. If this happens freqently, check if your mail service is up and working.")
        except ConnectionError as e:
            print(f"Connection error to mail server occurred with error number {e.errno}")
        self.mail.close()
        self.mail = None
        return []