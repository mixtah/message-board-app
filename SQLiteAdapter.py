'''
Created on 28 Aug 2017

@author: Michael
'''
import sqlite3
from datetime import datetime

DB_NAME = 'message-board.db'


def QUERY(query,params=None):
    '''
        Provides direct access to the SQLite Database. Given a query it will
        run it and return a result depending on the query.
        @param query: The SQL query to be run
        @type query: str
        @param params: A tuple of parameters to be inserted into the query in
                    order to prevent SQLInjection
        @return: list of dictionaries, each dictionary containing keys as 
                column names and values as the row value.
        @rtype: list
    '''
    try:
        print query.replace('?','%s') % tuple(params)
    except:
        print query
        
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        
        #Hint: I would not normally do this, why not?
        spl = query.split(';')
        if len(spl)>1:
            for q in spl:
                if params:
                    cur.execute(q,params)
                    params = None
                    conn.commit()
                else:
                    cur.execute(q)
                    conn.commit()
        else:
            if params:
                cur.execute(query,params)
            else:
                cur.execute(query)
        
        #Check if we were given a select statement
        #If so we want to return the results,
        #otherwise we want to return the last row that was updated
        if query.lstrip().lower().startswith('select'):
            result = []
            
            for row in cur.fetchall():
                cols = []
                fixedRow = []
                for i in range(len(row)):
                    if isinstance(row[i], datetime):
                        fixedRow.append(row[i].strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        fixedRow.append(row[i])
                for i in cur.description:
                    cols.append(i[0])
                result.append(dict(zip(cols,fixedRow)))
            return result
        else:
            cid = cur.lastrowid
            conn.commit()
            if not cid:
                return True
            return cid 
    except Exception as err:
        print "Exception: ",err
        return None
    finally:
        #Is run no matter what, even if there is an error.
        #perfect place to close connections
        conn.close()

def initialize_db():
    
    
    QUERY('''DROP TABLE IF EXISTS topic''')
    QUERY('''DROP TABLE IF EXISTS messages''')
    
    with open('create-tables.sql', 'r') as script:
        queries = script.read().split(';')
        for query in queries:
            QUERY(query)
    
    
    return True



if __name__ == '__main__':
    initialize_db()
    
    print('Insert Data')
    print(QUERY('''INSERT INTO messages (username,message) VALUES (?,?)''',('myusername','<h3>mymessage</h3>')))
    
    print('Select Data')
    print(QUERY('''SELECT * FROM messages WHERE username=?''',('myusername',)))
    
    print('Deleting Data')
    print(QUERY('''DELETE FROM messages WHERE username=?''',('myusername',)))
