from email import parser as EmailParser
import sys.stdin
import re

class EmailHandler:

    def __init__(self):
        parse_email = EmailParser.Parser()
        self.email_obj = parse_email.parse(sys.stdin)
        self.email_from = self.email_obj.get('From')
        self.email_to = self.email_obj.get('To')
        self.emailSubject = self.email_obj.get('Subject')

    def get_from(self):
        return self.email_from

    def get_to(self):
        return self.email_to

    def get_subject(self):
        return self.email_subject

    def get_parts(self):
        return self.email_obj.get_payload(decode=True)

    def get_csv_attachments(self):
        csvs = []
        for part in self.get_parts:
            csv = re.search('\.csv$', part, flags=re.IGNORECASE)
            if not csv: #found
                csv = csvs.append(csv)

        return csvs