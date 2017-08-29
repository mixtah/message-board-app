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
import bottle
from bottle import Bottle

from beaker.middleware import SessionMiddleware
from cherrypy import wsgiserver
from cherrypy.wsgiserver.ssl_pyopenssl import pyOpenSSLAdapter
from OpenSSL import SSL

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

#Home page /
# -lists recent topics
# -add topic

#User page /user/<username>
# -lists topics by user if exists
# -add topic

#Topic Page /topic/<topic-id:int>
# -lists messages
# -modify topic
# -delete topic
# -add message
# -modify message
# -delete message


###################################################################################
### Application API Connection
###################################################################################

#Search  Topics GET  /topic
#Create  Topic  POST /topic/add
#Update  Topic  POST /topic/<topic-id:int>/update
#Delete  Topic  POST /topic/<topic-id:int>/delete
#Like    Topic  POST /topic/<topic-id:int>/like
#Dislike Topic  POST /topic/<topic-id:int>/dislike

#Search  Messages GET  /message
#Create  Message  POST /message/add
#Update  Message  POST /message/<message-id:int>/update
#Delete  Message  POST /message/<message-id:int>/delete
#Like    Message  POST /message/<message-id:int>/like
#Dislike Message  POST /message/<message-id:int>/dislike

###################################################################################
### SSL 
###################################################################################

#I've included code to demonstrate that the bottle test server
#can use SSL via CherryPy, you can make this true to secure your
#users connection however you must generate a certificate, otherwise
#the browser will complain that it's not actually secured.
#
#I encourage you to learn how to generate an SSL certificate after
#this tutorial, and apply it.
#
#It's important to know that when hosting a webapp, you usually
#wont need to bother with SSL at this level as you'd usually use
#software like Nginx or Apache to server the webapp and it will handle
#SSL for you.
useSSL = False

# By default, the server will allow negotiations with extremely old protocols
# that are susceptible to attacks, so we only allow TLSv1.2
class SecuredSSLServer(pyOpenSSLAdapter):
    def get_context(self):
        c = super(SecuredSSLServer, self).get_context()
        c.set_options(SSL.OP_NO_SSLv2)
        c.set_options(SSL.OP_NO_SSLv3)
        c.set_options(SSL.OP_NO_TLSv1)
        c.set_options(SSL.OP_NO_TLSv1_1)
        return c

# Create our own sub-class of Bottle's ServerAdapter
# so that we can specify SSL. Using just server='cherrypy'
# uses the default cherrypy server, which doesn't use SSL
class SSLCherryPyServer(bottle.ServerAdapter):
    def run(self, handler):
        server = wsgiserver.CherryPyWSGIServer((self.host, self.port), handler)
        server.ssl_adapter = SecuredSSLServer('keys/cacert.pem', 'keys/privkey.pem')
        try:
            server.start()
        finally:
            server.stop()


###################################################################################
### Application Initialisation
###################################################################################

#Initialize session details
SESSION_OPTIONS = {
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
    if not useSSL:
        bottle.run(app=application, host=ip, port=8000, debug=True)
    else:
        bottle.run(app=application, host=ip, port=8000, debug=True,server=SSLCherryPyServer)
