csv2mysql
=========

Configurable importer scripts to import CSV data into MySQL data base tables of any schema.

How to use csv2mysql
====================

csv2mysql consists of a number of scripts which can be used to import CSV files into a data
base of any schema.

The provided classes are

* **EmailHandler:** Reads an email and extracts attached CSV files
* **ParseCSV:** Parses passed CSV data into a list
* **Import2DB:** Imports the lists returned by *ParseCSV* into a MySQL database according to a SQL template rule set
* **Notify:** Can be used to send an email to notify someone of an import.

The file _import_controller.py_ has been added as a sample controller for an import. It takes
a list of users and imports them into a user table. The rules used are:


	{'PRE':[{'SEARCH':{'query':'SELECT uid FROM group WHERE title=\'Members\'',
                              'uid_marker':'members_gid'}},
                    {'SEARCH':{'query':'SELECT pid FROM user WHERE usergroup=\'#members_gid#\' LIMIT 1,1',
                              'uid_marker':'members_pid'}},
                    {'INSERT':{'query':'TRUNCATE user'}}],    		  
    	    'IMPORT':[{'SEARCH':{'query':'SELECT uid FROM user WHERE email=\'#email#\' AND pid=\'#members_pid#\' AND usergroup=\'#members_gid#\'',
                                 'uid_marker':'user_uid'}},
                      {'UPDATE':{'query':'UPDATE user SET username=\'#email#\', first_name=\'#first_name#\', last_name=\'#last_name#\', email=\'#email#\' WHERE uid=\'#user_uid#\'',
                                 'uid_marker':'user_uid'}},
                      {'INSERT':{'query':'INSERT INTO user (pid, usergroup, username, password, first_name, last_name, email) VALUES (\'#subscriber_pid#\', \'#members_gid#\', \'#email#\', SUBSTRING(MD5(RAND()) FROM 1 FOR 12), \'#first_name#\', \'#last_name#\', \'#email#\')',
                                 'uid_marker':'user_uid',
                                 'fallback':True}}]}
                                 
What happens is the following:

*PRE*

* The first rule finds the unique id of group "Members"
* The second rule finds the parent id of the first existing user record
* The third rule truncates the user table

*IMPORT*

* The script will first find the unique id of a record with the same email address as the one to be imported.
* If a record was found, it will update this record with the new data.
* Because the *fallback* option is set in the last rule it will insert a new record if either the first or the second rule have failed.

For a full specification of the configuration dictionary, see the header of Import2DB.

If you use the EmailHandler object, you will have to wrap the strings in a pseudo-file yourself to be able to pass them to the ParseCSV object. 

Pull requests welcome.