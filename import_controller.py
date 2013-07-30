#!/usr/bin/env python

""" Sample controller which imports users to a database"""

import sys

import ParseCSV
import Import2DB
import Notify

# read CSV from stdin
# change this to a file import if necessary
csv = sys.stdin.read()

# initialise CSV parser
csv_parser = ParseCSV.ParseCSV()

# Connect to database
db_obj = Import2DB.Import2DB(server='localhost', dbname='sampledb', username='sampleuser', passwd='thepassword')

# parse the CSV into lists suitable for database import
import_records = csv_parser.parse_csv(csv, ',')

# set names of fields as they appear in CSV file
fields = [ 'first_name', 'last_name', 'email' ]

# set names of mandatory fields
mandatory = [ 'email' ]

# query templates
query_map = {'PRE':[{'SEARCH':{'query':'SELECT uid FROM grouptable WHERE title=\'Members\'',
                              'uid_marker':'members_gid'}},
                    {'SEARCH':{'query':'SELECT pid FROM usertable WHERE usergroup=#members_gid# LIMIT 0,1',
                              'uid_marker':'members_pid'}},
                    {'INSERT':{'query':'TRUNCATE usertable'}}],    		  
    	    'IMPORT':[{'SEARCH':{'query':'SELECT uid FROM usertable WHERE email=\'#email#\' AND pid=#members_pid# AND usergroup=#members_gid#',
                                 'uid_marker':'user_uid'}},
                      {'UPDATE':{'query':'UPDATE usertable SET username=\'#email#\', first_name=\'#first_name#\', last_name=\'#last_name#\', email=\'#email#\' WHERE uid=\'#user_uid#\'',
                                 'uid_marker':'user_uid'}},
                      {'INSERT':{'query':'INSERT INTO usertable (`pid`, `usergroup`, `username`, `password`, `first_name`, `last_name`, `email`) VALUES (#members_pid#, #members_gid#, \'#email#\', SUBSTRING(MD5(RAND()) FROM 1 FOR 12), \'#first_name#\', \'#last_name#\', \'#email#\')',
                                 'uid_marker':'user_uid',
                                 'fallback':True}}]}

# import data from CSV into database
db_obj.write2db(fields, mandatory, import_records, query_map)

# notify someone that import has happened
notification = Notify.Notify()
notification.send_message(msg_from='someone@example.com',
                          to=[ 'someoneelse@example.net' ],
                          subject='csv2mysql has done its magic',
                          body='Just thought you might want to be notified.')