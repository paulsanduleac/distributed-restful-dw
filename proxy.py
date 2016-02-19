from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from itertools import cycle
from random import choice
import requests, json
import settings
import redis

#initialize Flask and Flask_Restful
app = Flask(__name__)
api = Api(app)

apps=[] # we will populate this with incoming data
instances=cycle(apps)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

class Article(Resource): # REST resource, mirrors instance behavior
    def get(self, aid):
        URI=next(instances)+'/article/'+str(aid)
        print URI
    	r=requests.get(URI)
        return r.json()

    def post(self, aid):
		atitle=request.form['title']
		url = next(instances)+'/article/'+str(aid)
		payload = {'title': atitle}
		r = requests.post(url, data=payload)
		return r.json()

class OpenInstance(Resource):
    def get(self):
        return 1

    def post(self):
        host=request.form['host']
        port=request.form['port']
        incoming='http://'+host+':'+port
        apps.append(incoming.encode("utf-8")) 
        print 'Received notification of new instance:' + incoming
        print str(apps)           
        return {'status': 'OK'}

class CloseInstance(Resource):
    def get(self):
        return 1

    def post(self):
        host=request.form['host']
        port=request.form['port']
        incoming='http://'+host+':'+port
        apps.remove(incoming.encode("utf-8"))
        print 'Received notification of instance closing:' + incoming
        print '/n'
        print 'Current list of instances:'
        print str(apps)           
        return {'status': 'OK'}

api.add_resource(Article, '/article/<int:aid>')
api.add_resource(OpenInstance, '/openinstance')
api.add_resource(CloseInstance, '/closeinstance')

if __name__ == '__main__':
    app.debug = True
    app.run(host=settings.proxyhost, port=settings.proxyport)