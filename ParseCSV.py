import StringIO
import csv

class ParseCSV:
    
    """Parses CSV from string and returns a pseudo-file object"""

    def parse_csv(self, csv_buffer, delimiter):
        csv_pseudo_file = StringIO.StringIO(csv_buffer)
        csv_contents = csv.reader(csv_pseudo_file, delimiter=delimiter)

        return csv_contents          
