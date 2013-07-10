#{'PRE':[{'SEARCH':{'query':<query>,'uid_marker':'<markername>'},
# 	     'UPDATE':{'query':<query>,'uid_marker':'<markername>'},
# 	     'INSERT':{'query':<query>,'uid_marker':'<markername>','fallback':<True|False>}},
#	    ...],
# 'IMPORT':[{'SEARCH':{'query':<query>,'uid_marker':'<markername>'},
# 	     'UPDATE':{'query':<query>,'uid_marker':'<markername>'},
# 	     'INSERT':{'query':<query>,'uid_marker':'<markername>','fallback':<True|False>}},
#	    ...]
#{'POST':[{'SEARCH':{'query':<query>,'uid_marker':'<markername>'},
# 	     'UPDATE':{'query':<query>,'uid_marker':'<markername>'},
# 	     'INSERT':{'query':<query>,'uid_marker':'<markername>','fallback':<True|False>}},
#	    ...],
#}

import re
import MySQLdb as mysql

class Import2DB:

    def __init__(self, server, dbname, username, passwd):
        self.db = mysql.connect(host=server, user=username, passwd=passwd, db=dbname)
        self.cursor = self.db.cursor()
        self.updated = False

    def run_query(self,query):
        # catch warnings
        import warnings
        with warnings.catch_warnings():
#            warnings.simplefilter('error', mysql.Warning)
            res = False
            try:
                res = self.cursor.execute(query)
            except mysql.Error, e:
                raise e
            finally:
                return res
        
    def write2db(self, fields, mandatory, import_data, query_mapping):

        data = {}

        # run the "pre-queries" which are global to the set
        self.updated = False
        try:
            for query in query_mapping['PRE']:
                data = self.process_query(query, data)
        except KeyError:
            print 'No pre-queries.'

        data_backup = data.copy()

        self.updated = False
        for record in import_data:
            idx = 0
            assoc_list = []
            all_mandatory = True
            for field in fields:
                assoc_list.append((field, record[idx]))
                
                # check if field is mandatory and filled if it is
                if any(x in [ field ] for x in mandatory) and not record[idx]:
                    all_mandatory = False

                idx += 1

            data = dict(data_backup.items() + dict(assoc_list).items())

            # run the import queries
            for query in query_mapping['IMPORT']: 
                if all_mandatory:
                    data = self.process_query(query, data)

        # run the "post-queries" which are global to the set
        self.updated = False
        data = data_backup
        try:
            for query in query_mapping['POST']:
                data = self.process_query(query, data)

        except KeyError:
            print 'No post-queries.'


    def process_query(self, query, data):
        
        try:
            search_query = query['SEARCH']
            if 'uid_marker' in search_query:
                data[search_query['uid_marker']] = self.check_exists(search_query['query'], data)
        except KeyError:
            try:
                update_query = query['UPDATE']
                if 'uid_marker' in update_query and update_query['uid_marker'] in data and data[update_query['uid_marker']] != None:
                    update_ret = self.replace_markers(update_query['query'], data)
                    try:
                        self.run_query(update_ret)
                    except mysql.Warning:
                        print 'Warning'
                    finally:
                        self.updated = True
            except KeyError:
                insert_query = query['INSERT']
                if not self.updated or 'fallback' not in insert_query or not insert_query['fallback']:
                    insert_ret = self.replaceMarkers(insert_query['query'], data)
                    try:
                        self.run_query(insert_ret)
                    except mysql.Warning:
                        print 'Warning'
                    finally:
                        if 'uid_marker' in insert_query:
                            data[insert_query['uid_marker']] = self.db.insert_id()
                else:
                    self.updated = False

        return data

    def check_exists(self, search_template, data):

        search_query = self.replaceMarkers(search_template, data)
#        print searchQuery
        try:
            self.run_query(search_query)
        except mysql.Warning:
            print 'Warning'
        res = self.cursor.fetchone()
        if not res:
            return None
        else:
            # assume first column of fetched row is uid
            return res[0]

    def replace_markers(self, query_template, data):

        query = query_template
        markers = re.findall('#([^#]+)#', query)
        for marker in markers:
            value=''
            if marker in data:
                value = str(data[marker]).replace("'", "\\'")
            new_query = re.subn('#' + marker + '#', value, query)
            query = new_query[0]

        return query
