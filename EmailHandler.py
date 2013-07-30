from email import parser as EmailParser
import sys

class EmailHandler:
    
    """ Takes an email from stdin and extracts attached CSV files"""

    def __init__(self):
        parse_email = EmailParser.Parser()
        self.email_obj = parse_email.parse(sys.stdin)
        self.email_from = self.email_obj.get('From')
        self.email_to = self.email_obj.get('To')
        self.email_subject = self.email_obj.get('Subject')

    def get_from(self):
        return self.email_from

    def get_to(self):
        return self.email_to

    def get_subject(self):
        return self.email_subject

    def get_parts(self):
        decode = True
        if self.email_obj.is_multipart():
            decode = False
        return self.email_obj.get_payload(decode=decode)
            

    def get_csv_attachments(self):
        csvs = []
        for part in self.get_parts():
            if not part.is_multipart() \
                and 'content-type' in part \
                and part['content-type'] == 'text/csv':
                csvs.append(part.get_payload(decode=True))

        return csvs