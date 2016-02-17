# Proof of concept for JSON response on GET
from flask import Flask, jsonify, make_response

app = Flask(__name__)

users = [
    {
        'id': 1,
        'first_name': u'Lisa',
        'last_name': u'Doe', 
        'allowed': 1
    },
    {
        'id': 2,
        'first_name': u'John',
        'last_name': u'Doe', 
        'allowed': 0
    }
]

@app.route('/api/get')
def get_users_data():
	return jsonify({'users': users})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'Error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
