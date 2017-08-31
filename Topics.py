'''
Created on 29 Aug 2017

@author: Michael
'''
from datetime import datetime
import time
import SQLiteAdapter as db
import Messages

class Topic(object):
    '''
    classdocs
    '''


    def __init__(self,id=None,username=None,subject=None,description=None,
                 modified=0,likes=0,dislikes=0,timestamp=datetime.now()):
        '''
        Constructor
        '''
        self.id = id
        self.username = username
        self.subject = subject
        self.description = description
        self.modified = modified
        self.likes = likes
        self.dislikes = dislikes
        self.timestamp = timestamp
        
    def save(self):
        '''
            Adds this object to the database if no id exists, otherwise it updates.
            This must be called after any direct modification to this object in order to 
            make it permanent.
        '''
        if self.id==None:
            #Add                
            res = db.QUERY("INSERT INTO topics (username,subject,description,modified,likes,dislikes) VALUES (?,?,?,?,?,?)",
                           (self.username,self.subject,self.description,self.modified,self.likes,self.dislikes))
            if res:
                self.id=res
                return True
        else:
            #Update
            res = db.QUERY("UPDATE topics SET username=?,subject=?,description=?,modified=?,likes=?,dislikes=? WHERE id=?",
                           (self.username,self.subject,self.description,self.modified,self.likes,self.dislikes,self.id))
            
        if res:
            return True
        else:
            return False
        
    def getMessages(self):
        return Messages.getFiltered(filters={'topic':self.id,'reply_to':None})

def getCount(filters={}):
    ''' Number of topics in the database given a number of filters'''
    keys = filters.keys()
    values = filters.values()
    query = 'SELECT COUNT(*) AS count FROM topics '
    if len(keys)>0:
        query = query + 'WHERE '
        for key in keys:
            query = query + key + '=?, '
        query = query[:-2]
    res = db.QUERY(query,tuple(values))
    if res:
        return res[0]['count']
    return 0
        
def get(id=None):
    ''' Gets a Topic given it's id
    '''
    if id==None:
        return None
    
    res = db.QUERY('SELECT * FROM topics WHERE id=?',(id,))
    if res and len(res)>0:
        return Topic(**res[0])
    else:
        return None
    
def getAll(limit=-1):
    ''' Get a list of all Topics '''
    if limit>0:
        res = db.QUERY('SELECT * FROM topics LIMIT ?',(limit,))
    else:
        res = db.QUERY('SELECT * FROM topics')
    rlist = []
    if res:
        for values in res:
            rlist.append(Topic(**values))
        return rlist
    return None
    
def getFiltered(filters={}, limit=-1,order_by=None,ascending=True):
    ''' Get a list of filtered Topics '''
    
    keys = filters.keys()
    values = filters.values()
    query = 'SELECT * FROM topics '
    if len(keys)>0:
        query = query + 'WHERE '
        for key in keys:
            query = query + key + '=? and '
        query = query[:-4]
    if order_by:
        order_by = order_by if order_by.lower() in ['id','username','subject',
                                                    'description','modified',
                                                    'likes','dislikes',
                                                    'timestamp'] else 'id'
        query = query + 'ORDER BY '+order_by
        if ascending:
            query = query + " ASC "
        else:
            query = query + " DESC "
    #if limit>0:
    #    values.append(limit)
    #    res = db.QUERY(query + ' LIMIT ?',tuple(values))
    #else:
    res = db.QUERY(query,tuple(values))
    if res:
        rlist = []
        for values in res:
            rlist.append(Topic(**values))
        return rlist
    return None

def delete(id=None):
    ''' Deletes a Topic given it's id '''
    if id==None:
        return None
    res = db.QUERY('DELETE FROM topics WHERE id=?',(id,))
    if res>0:
        return True
    else:
        return False