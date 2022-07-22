""" 
    Project to test logging user events using socketIO, mongoDB, Flask
    User client connects to socketio
    User clicks a button (blue/red)
        triggering client to emit event to namespace '/log'
        example of data received from client:
        `{ 'event': 'button click', 'data': { name: 'Blue Button' } }`
    Server saves event information to local mongoDB 
        database 'eventLogDB', collection 'logs'
            {
                _id: ObjectId,
                user: { type: ObjectId, ref: 'users' },
                created: Date,
                event: String,
                data: Object,
            }
"""

from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from datetime import datetime


app = Flask(__name__)
# configure socketIO
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# configure PyMongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/eventLogDB'
mongo = PyMongo(app)

if __name__ == '__main__':
    socketio.run(app)

@app.route('/')
def index():
    return render_template('index.html')

# on connection
@socketio.on('connect')
def connect():
    print('connect')

# on disconnection
@socketio.on('disconnect')
def disconnect():
    print('disconnect')

# Log event in mongoDB
@socketio.on('user event', namespace='/log')
def log_event(data):
    print(data)
    try:
        log = {
            #TODO: add user info
            'created': datetime.utcnow(),
            'event': data['event'],
            'data': data['data'],
        }
    except KeyError:
        print('Insufficient data')
        return
    
    log_id = mongo.db.logs.insert_one(log).inserted_id
    print(log_id)
