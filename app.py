from flask import Flask, render_template
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Flag to ensure we only start one background task
thread = None

@app.route('/')
def index():
    return render_template('index_socket.html')

def send_time():
    while True:
        print(time.ctime())
        socketio.emit('timestamp', {'time': time.ctime()})
        socketio.sleep(5)

@socketio.on('connect')
def on_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(send_time)
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1", port=5000)
