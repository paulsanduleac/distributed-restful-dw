from cassandra.cluster import Cluster
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)
cluster = Cluster()
dbsession = cluster.connect('dev')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': '404 Not Found'}), 404)

class Article(Resource):
    def get(self, aid):
    	single = dbsession.execute("SELECT aid, title FROM articles WHERE aid=%s", [aid])
        return {'aid': single[0][0],
        		'title': single[0][1]}

    def post(self, aid):
    	atitle=request.form['title']
    	single = dbsession.execute("INSERT INTO articles(aid, title) VALUES (%s,%s)", [aid,atitle])
        return {'status': 'OK'}

api.add_resource(Article, '/article/<int:aid>')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001) #port 0 lets the OS find an open port