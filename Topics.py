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
            if self.timestamp == None or len(self.timestamp)==0:
                self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                
            res = db.QUERY("INSERT INTO topics (username,subject,description,modified,likes,dislikes) VALUES (?,?,?,?,?,?)",
                           (self.username,self.subject,self.description,self.modified,self.likes,self.dislikes))
            if res:
                self.id=res
                return True
        else:
            #Update
            res = db.QUERY("UPDATE topics SET username=?,subject=?,description=?,modified=?,likes=?,dislikes=? WHERE id=?)",
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
    query = 'SELECT COUNT(*) AS count FROM topics WHERE '
    for key in keys:
        query = query + key + '=?, '
    query = query[:-2]
    res = db.QUERY(query,tuple(values))
    return res[0]['count']
        
def get(id=None):
    ''' Gets a Topic given it's id
    '''
    if id==None:
        return None
    
    res = db.QUERY('SELECT FROM topics WHERE id=?',(id,))
    if len(res)>0:
        return Topic(**res[0])
    else:
        return None
    
def getAll(limit=-1):
    ''' Get a list of all Topics '''
    if limit>0:
        res = db.QUERY('SELECT FROM topics LIMIT ?',(limit))
    else:
        res = db.QUERY('SELECT FROM topics')
    rlist = []
    for values in res:
        rlist.append(Topic(**values))
    return rlist
    
def getFiltered(filters={}, limit=-1):
    ''' Get a list of filtered Topics '''
    
    keys = filters.keys()
    values = filters.values()
    query = 'SELECT FROM topics WHERE '
    for key in keys:
        query = query + key + '=?, '
    query = query[:-1]
    if limit>0:
        res = db.QUERY(query + ' LIMIT ?',(limit))
    else:
        res = db.QUERY(query,tuple(values))
    rlist = []
    for values in res:
        rlist.append(Topic(**values))
    return rlist

def delete(id=None):
    ''' Deletes a Topic given it's id '''
    if id==None:
        return None
    res = db.QUERY('DELETE FROM topics WHERE id=?',(id,))
    if res>0:
        return True
    else:
        return False