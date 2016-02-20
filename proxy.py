from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from itertools import cycle
from random import choice
from redis import Redis
import requests, json
import settings


#initialize Flask and Flask_Restful
app = Flask(__name__)
api = Api(app)
redis=Redis("localhost")

apps=[] # we will populate this with incoming data
instances=cycle(apps)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

class Article(Resource): # REST resource, mirrors instance behavior
    def get(self, aid):
        try:
            URI=next(instances)+'/article/'+str(aid)
            print URI
        except StopIteration:
            pass
        except UnboundLocalError:
            r="Please set an instance first."
        cache=redis.get(aid)
        print cache

        if cache==None:
            r=requests.get(URI)
            r=r.json()
            title=r['title']
            redis.setex(aid,title,5)
        else:
            r={"aid": aid, "title": cache, "cached": "1"}
        return r

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
        print '\n'
        return {'status': 'OK'}

class CloseInstance(Resource):
    def get(self):
        return 1

    def post(self):
        host=request.form['host']
        port=request.form['port']
        incoming='http://'+host+':'+port
        print 'Received notification of instance closing:' + incoming
        print '\n'
        try:
            apps.remove(incoming.encode("utf-8"))
        except ValueError:
            print 'Tried to remove an instance, but could not find it in the list.'
            print '\n'
        if apps == None:
            print "No instances"
        else: 
            print 'Current list of instances:'
            print str(apps) 
        print '\n'  
        return {'status': 'OK'}

class CacheClear(Resource):
    def get(self):
        redis.flushdb()
        return 1

api.add_resource(Article, '/article/<int:aid>')
api.add_resource(OpenInstance, '/openinstance')
api.add_resource(CloseInstance, '/closeinstance')
api.add_resource(CacheClear, '/cacheclear')

if __name__ == '__main__':
    app.debug = True
    app.run(host=settings.proxyhost, port=settings.proxyport)