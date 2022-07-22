from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_pymongo import PyMongo
from datetime import datetime


app = Flask(__name__)
# configure socketIO
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# configure PyMongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/eventLogDB"
mongo = PyMongo(app)

if __name__ == '__main__':
    socketio.run(app)

@app.route("/")
def index():
    return render_template("index.html")

# on connection
@socketio.on('connect')
def connect():
    print('connect')

# on disconnection
@socketio.on('disconnect')
def disconnect():
    print('disconnect')

# Log event in mongoDB
@socketio.on("user event", namespace="/log")
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
        print("Insufficient data")
        return
    
    log_id = mongo.db.logs.insert_one(log).inserted_id
    print(log_id)
