'''
Created on 28 Aug 2017

@author: Michael Bauer

@sumary: A basic web application built to demonstrate simple web 
         application built in bottle and how to secure again a
         couple common security threats. 
         This application is a simple messageboard app where users
         can create a topic and post messages under the topic.
'''

import sys,os
import socket
import json
import bottle
from bottle import Bottle

from beaker.middleware import SessionMiddleware

import Topics
import Messages

#Initialize webapp
app = Bottle()

###################################################################################
### Serve Static Files
###################################################################################

@app.route('/styles/<filename>')
def serve_style(filename):
    '''Loads static files from /styles. Store all .css files there.'''
    return bottle.static_file(filename, root='./static/styles')

@app.route('/media/<filename>')
def serve_media(filename):
    '''Loads static files from /media. Store all User uploaded files there.'''
    return bottle.static_file(filename, root='./static/media')

@app.route('/js/<filename>')
def send_static(filename):
    '''Loads static files from /js. Store all .js files there.'''
    return bottle.static_file(filename, root='./static/js/')

###################################################################################
### Application Main Pages
###################################################################################

#Home page / + Filter pages /popular /liked /disliked
# -lists recent topics
# -add topic
@app.route('/')
def home():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    return bottle.template('page-home', 
                           topics=Topics.getFiltered(limit=50, order_by='id',ascending=False),
                           alert=session.pop('alert',''))

@app.route('/liked')
def liked():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    return bottle.template('page-home', 
                           topics=Topics.getFiltered(limit=25, order_by='likes', ascending=False),
                           alert=session.pop('alert',''))

@app.route('/disliked')
def disliked():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    return bottle.template('page-home', 
                           topics=Topics.getFiltered(limit=25, order_by='dislikes', ascending=False),
                           alert=session.pop('alert',''))

@app.route('/popular')
def popular():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    results = {}
    topics = Topics.getAll()
    for topic in topics:
        results[topic] = Messages.getCount({'topic':topic.id})+topic.likes+topic.dislikes
    
    sortedresults = sorted(results,key=results.get, reverse=True)
    
    return bottle.template('page-home', 
                           topics=sortedresults,
                           alert=session.pop('alert',''))

#User page /user/<username>
# -lists topics by user if exists

@app.route('/user/<username>')
def users(username=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    return bottle.template('page-user', 
                           username=username,
                           alert=session.pop('alert',''))

#Topic Page /topic/<topic_id:int>
# -lists messages
# -modify topic
# -delete topic
# -add message
# -modify message
# -delete message

@app.route('/topic/<topic_id:int>')
def topic(topic_id=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    return bottle.template('page-topic', 
                           topic=Topics.get(int(topic_id)),
                           alert=session.pop('alert',''))

###################################################################################
### Application API Connection
###################################################################################

#Search  Topics GET  /topic
#Create  Topic  POST /topic/add
#Update  Topic  POST /topic/<topic-id:int>/update
#Delete  Topic  POST /topic/<topic-id:int>/delete
#Like    Topic  POST /topic/<topic-id:int>/like
#Dislike Topic  POST /topic/<topic-id:int>/dislike

@app.get('/topic')
def search_topics():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    query = bottle.request.query
    #Here we use pop because we want to remove the value from the query
    limit = query.pop('limit',-1)
    order_by = query.pop('orderby','id')
    ascending = query.pop('asc','FALSE').upper()=='TRUE' #To make sure this is a boolean
    
    #This is a trick to get the list of variables that
    #exist within the Topic class.
    allowed_query = Topics.Topic().__dict__.keys()
    
    new_query = dict(query)
    for item in new_query:
        #remove any unwanted query fields
        if not query.get(item) in allowed_query:
            query.pop(item)
            
    topics = Topics.getFiltered(query, limit=limit, order_by=order_by, ascending=ascending)
    
    #We're returning json
    bottle.response.content_type = 'application/json'
    
    #We don't want to send back a json array, it must start with a key-value
    #This is due to a subtle json vulnerability, read more on:
    # http://haacked.com/archive/2009/06/25/json-hijacking.aspx/
    # http://haacked.com/archive/2008/11/20/anatomy-of-a-subtle-json-vulnerability.aspx/
    res = {'results':[]}
    
    if topics:
        for i in topics:
                i = i.__dict__
                res['results'].append(i)
    return json.dumps(res)

@app.post('/topic/add')
def add_topic():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    form = bottle.request.forms
    
    required = ['username','subject','description']
    for r in required:
        if not r in form or len(form.get(r))==0:
            session['alert'] = 'Failed to add Topic. Missing '+r
            bottle.redirect('/')
    
    topic = Topics.Topic(username=form.get('username'),
                         subject=form.get('subject'),
                         description=form.get('description')
                         )
    if topic.save():
        session['alert'] = 'Successfully added Topic'
        bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = 'Failed to add Topic'
    bottle.redirect('/')
    
@app.route('/topic/<topic_id:int>/like')
def like_topic(topic_id=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    topic = Topics.get(int(topic_id))
    if topic:
        topic.likes = topic.likes + 1
        if not topic.save():
            session['alert'] = 'Failed to like Topic'
        bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = "Failed to like Topic, doesn't exist"
    bottle.redirect('/')
    
@app.route('/topic/<topic_id:int>/dislike')
def dislike_topic(topic_id=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    topic = Topics.get(int(topic_id))
    if topic:
        topic.dislikes = topic.dislikes + 1
        if not topic.save():
            session['alert'] = 'Failed to dislike Topic'
        bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = "Failed to dislike Topic, doesn't exist"
    bottle.redirect('/')

#Search  Messages GET  /message
#Create  Message  POST /message/add
#Update  Message  POST /message/<message-id:int>/update
#Delete  Message  POST /message/<message-id:int>/delete
#Like    Message  POST /message/<message-id:int>/like
#Dislike Message  POST /message/<message-id:int>/dislike

@app.post('/message/add')
def add_message():
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    form = bottle.request.forms
    
    required = ['username','message','topic']
    for r in required:
        if not r in form or len(form.get(r))==0:
            session['alert'] = 'Failed to add Topic. Missing '+r
            bottle.redirect('/')
    
    topic = Topics.get(id=int(form.get('topic')))
    if topic:
        message = Messages.Message(username=form.get('username'),
                             message=form.get('message'),
                             reply_to=form.get('reply_to',None),
                             topic=topic.id
                             )
        if message.save():
            session['alert'] = 'Successfully added Reply'
            bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = 'Failed to add Message'
    bottle.redirect('/')

@app.route('/message/<message_id:int>/like')
def like_message(message_id=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    message = Messages.get(int(message_id))
    if message:
        topic = message.getTopic()
        if topic:
            message.likes = message.likes + 1
            if not message.save():
                session['alert'] = 'Failed to like Message'
            bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = "Failed to like Message, doesn't exist"
    bottle.redirect('/')
    
@app.route('/message/<message_id:int>/dislike')
def dislike_message(message_id=''):
    session = bottle.request.environ.get('beaker.session')  #@UndefinedVariable
    
    message = Messages.get(int(message_id))
    if message:
        topic = message.getTopic()
        if topic:
            message.dislikes = message.dislikes + 1
            if not message.save():
                session['alert'] = 'Failed to dislike Message'
            bottle.redirect('/topic/'+str(topic.id))
    session['alert'] = "Failed to dislike Message, doesn't exist"
    bottle.redirect('/')



###################################################################################
### Application Initialisation
###################################################################################

#Initialize session details
SESSION_OPTIONS = {
    'session.auto': True,
    'session.cookie_expires': False,
    #This is a security risk if this is false as it means that if 
    #anyone gets access to your session cookie or just uses your
    #computer while your away, they'll be able to access your
    #account details.
    #
    #There is usually a balance between usability and security
    #as it will be annoying to login too often.
    #
    #for the purpose of this tutorial, I'm leaving it as false.
}

#Add Beakers Session management
application = SessionMiddleware(app, SESSION_OPTIONS)

if __name__ == '__main__':
    #Actually start running the application. If run from here, it will be using
    #the debug server. Run this module externally and use 'application' to start.
    
    print "Starting Message Board App..."    
    
    if len(sys.argv)>1:
        if sys.argv[1]=='--init-db':
            #We're going to drop tables if they exists
            #then create them.
            #This will reset all topics and messages
            import SQLiteAdapter
            SQLiteAdapter.initialize_db()
            
    
    #Here I'm deciding how I should launch the application
    #The application can be started with:
    # python app.py 
    #
    #It will automatically find your ip address automatically and host
    #it on your local network.
    ip = socket.gethostbyname(socket.gethostname())
    bottle.run(app=application, host=ip, port=8000, debug=True)
