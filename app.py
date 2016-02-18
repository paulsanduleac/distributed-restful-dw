from cassandra.cluster import Cluster
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
import socket
import requests
import settings
import os
import atexit

app = Flask(__name__)
api = Api(app)
cluster = Cluster()
dbsession = cluster.connect('dev')

@app.errorhandler(404)
def not_found(error):  # handles any 404 requests to the instance
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

class Article(Resource): # REST resource
    def get(self, aid):
    	single = dbsession.execute("SELECT aid, title FROM articles WHERE aid=%s", [aid])
        return {'aid': single[0][0],
        		'title': single[0][1]}

    def post(self, aid):
    	atitle=request.form['title']
    	single = dbsession.execute("INSERT INTO articles(aid, title) VALUES (%s,%s)", [aid,atitle])
        return {'status': 'OK'}
api.add_resource(Article, '/article/<int:aid>') # add resource and create REST endpoint

def findport(): # find an open port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket magic to find a free port
    sock.bind(('localhost', 0))
    openport = sock.getsockname()[1]
    sock.close() # closing the socket, we know the port is free
    return openport

def open_instance(host, port): # notify proxy of the new instance
    try:
        response = 1
        url = 'http://' + settings.proxyhost + ':' + str(settings.proxyport) + '/openinstance'
        payload = {'host': host,'port': port}
        r=requests.post(url, data=payload)
        response = r.status_code
    except requests.exceptions.MissingSchema:
        print 'The proxy was not notified of the new instance. Please re-check the URL in settings.py.'
    except requests.exceptions.ConnectionError as error:
        print 'Could not connect to proxy: ' + str(error)    
    else:
        print 'Instance open - proxy notification sent, response: %d' % response
    return response

def close_instance(host, port): # notify proxy of instance closing
    try:
        response = 1
        url = 'http://' + settings.proxyhost + ':' + str(settings.proxyport) + '/closeinstance'
        payload = {'host': host,'port': port}
        r=requests.post(url, data=payload)
        response = r.status_code
    except requests.exceptions.MissingSchema:
        print 'The proxy was not notified of instance closing. Please re-check the URL in settings.py.'
    except requests.exceptions.ConnectionError as error:
        print 'Could not connect to proxy: ' + str(error)    
    else:
        print 'Instance closing, proxy notification sent, response: %d' % response
    return response

if __name__ == '__main__':
    settings.instanceport=findport()  #comment this line to use the default port from settings.py
    print(open_instance(settings.instancehost, settings.instanceport))   
    app.run(host=settings.instancehost, port=settings.instanceport)

atexit.register(close_instance, settings.instancehost, settings.instanceport)




