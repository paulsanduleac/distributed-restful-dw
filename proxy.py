from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
#from requests import get, post
import requests
import json, random

app = Flask(__name__)
api = Api(app)

def balancer():
    app1='http://localhost:5001'
    app2='http://localhost:5002'
    instance=random.choice([app1, app2])
    return instance

URI=balancer()+'/article/'+'1'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

class Article(Resource):
    def get(self, aid):
        URI=balancer()+'/article/'+str(aid)
    	r=requests.get(URI)
        return r.json()

    def post(self, aid):
		atitle=request.form['title']
		url = 'http://localhost:5001/article/%d' % aid
		payload = {'title': atitle}
		r = requests.post(url, data=payload)
		return r.json()

api.add_resource(Article, '/article/<int:aid>')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5003)