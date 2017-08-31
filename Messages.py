'''
Created on 29 Aug 2017

@author: Michael
'''
from datetime import datetime
import time
import SQLiteAdapter as db
import Topics

class Message(object):
    '''
    classdocs
    '''


    def __init__(self,id=None,username=None,message=None,reply_to=None,topic=None,
                 modified=0,likes=0,dislikes=0,timestamp=datetime.now()):
        '''
        Constructor
        '''
        self.id = id
        self.username = username
        self.message = message
        self.reply_to = reply_to
        self.topic = topic
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
            res = db.QUERY("INSERT INTO messages (username,message,reply_to,topic,modified,likes,dislikes) VALUES (?,?,?,?,?,?,?)",
                           (self.username,self.message,self.reply_to,self.topic,self.modified,self.likes,self.dislikes))
            if res:
                self.id=res
                return True
        else:
            #Update
            res = db.QUERY("UPDATE messages SET username=?,message=?,reply_to=?,topic=?,modified=?,likes=?,dislikes=? WHERE id=?",
                           (self.username,self.message,self.reply_to,self.topic,self.modified,self.likes,self.dislikes,self.id))
            
        if res:
            return True
        else:
            return False
        
    def getMessages(self):
        return getFiltered(filters={'reply_to':self.id})
    
    def getTopic(self):
        if self.topic:
            return Topics.get(self.topic)
        return None
    
    def getParentMessage(self):
        if self.reply_to:
            return get(self.reply_to)
        return None
        
def getCount(filters={}):
    ''' Number of messages in the database given a number of filters'''
    keys = filters.keys()
    values = filters.values()
    query = 'SELECT COUNT(*) AS count FROM messages '
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
    ''' Gets a Message given it's id
    '''
    if id==None:
        return None
    
    res = db.QUERY('SELECT * FROM messages WHERE id=?',(id,))
    if res and len(res)>0:
        return Message(**res[0])
    else:
        return None
    
def getAll(limit=-1):
    ''' Get a list of all Messages '''
    if limit>0:
        res = db.QUERY('SELECT * FROM messages LIMIT ?',(limit,))
    else:
        res = db.QUERY('SELECT * FROM messages')
    rlist = []
    if res:
        for values in res:
            rlist.append(Message(**values))
        return rlist
    return None
    
def getFiltered(filters={}, limit=-1,order_by=None,ascending=True):
    ''' Get a list of filtered Messages '''
    
    keys = filters.keys()
    query = 'SELECT * FROM messages '
    if len(keys)>0:
        query = query + 'WHERE '
        for key in keys:
            if filters[key] is None:
                #Need to do something slightly special as SQLite is weird will NULLs
                query = query + key + ' IS NULL and '
                del filters[key]
            else:
                query = query + key + '=? and '
        query = query[:-4]
    values = filters.values()
    if order_by:
        order_by = order_by if order_by.lower() in ['id','username','message',
                                                    'reply_to','topic','modified',
                                                    'likes','dislikes',
                                                    'timestamp'] else 'id'
        query = query + 'ORDER BY ' + order_by
        if ascending:
            query = query + " ASC "
        else:
            query = query + " DESC "
        values.append(order_by)
    if limit>0:
        values.append(limit)
        res = db.QUERY(query + ' LIMIT ?',tuple(values))
    else:
        res = db.QUERY(query,tuple(values))
    if res:
        rlist = []
        for values in res:
            rlist.append(Message(**values))
        return rlist
    return None

def delete(id=None):
    ''' Deletes a Message given it's id
    '''
    if id==None:
        return None
    res = db.QUERY('DELETE FROM messages WHERE id=?',(id,))
    if res>0:
        return True
    else:
        return False