import ipaddress

def validate_ip_address(address):
    try:
        ip = ipaddress.ip_address(address)
        return True
    except ValueError:
        return False

def get_req_from_email(message, required_subject):
    mail_subject = message['subject']
    mail_from = message['from']
    mail_content = ''
    if message.is_multipart():
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                mail_content += part.get_payload()
    else:
        mail_content = message.get_payload()
    if mail_subject == required_subject:
        mail_content = mail_content.strip()
        if validate_ip_address(mail_content):
            return ipaddress.ip_address(mail_content)
    return False