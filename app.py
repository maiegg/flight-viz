from flask import Flask, render_template
from flask_socketio import SocketIO
import time
from flight_data import * 

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Flag to ensure we only start one background task
thread = None

@app.route('/')
def index():
    return render_template('index_socket.html')

def send_flight_data():
    while True:
        print(time.ctime())

        flights = fetch_flights()
        if flights:
            flights_parsed = parse_flights(flights['states'])

        socketio.emit('timestamp', {'data': flights_parsed})
        socketio.sleep(5)

@socketio.on('connect')
def on_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(send_flight_data)
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)