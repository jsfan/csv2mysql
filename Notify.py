import smtplib
from email.mime.text import MIMEText

class Notify:
    
    """Sends an email to one or multiple recipients"""

    def send_message(self, msg_from, to, subject, body):

        msg = MIMEText(body)
        
        msg['From'] = msg_from
        msg['To'] = ", ".join(to)
        msg['Subject'] = subject
        
        smtp = smtplib.SMTP('localhost')
        smtp.sendmail(msg_from, to, msg.as_string())
