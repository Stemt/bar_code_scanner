
from flask import Flask
from flask import request
from multiprocessing import Process

app = Flask(__name__)
server = Process(target=app.run)

@app.route('/')
def hello_world():
   return 'Hi'

@app.route('/stop')
def stop():
    server.terminate()
    server.join()

if __name__ == '__main__':
    server.start()
    




