from flask import *
import requests
import random
import time
import threading
import json


import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


app = Flask(__name__)


coordinator = 4
cur = 0
port = 5000
lock = threading.Lock()


bully_list=("http://127.0.0.1:5000/","http://127.0.0.1:5001/","http://127.0.0.1:5002/","http://127.0.0.1:5003/","http://127.0.0.1:5004/")


def election():
    global coordinator
    f = False
    print("Holding Election!")
    for i in range(cur+1, len(bully_list)):
        try:
            x = requests.get(url=bully_list[i]+"election")
            if x.status_code == 200:
                f=True
                print("Node "+str(i)+" is active!")
        except:
            print("Node "+str(i)+" is inactive!")
            continue
    if f==False:
        lock.acquire()
        coordinator=cur
        print("New Coordinator: "+str(coordinator))
        lock.release()
        for i in range(len(bully_list)):
            if i!=cur:
                try:
                    requests.post(url=bully_list[i]+"coordinator", json=json.dumps({"data":str(cur)}))
                    break
                except:
                    print("Node "+str(i)+" is inactive!")
                    continue
        
def run():
    global coordinator
    ch = list(range(0,len(bully_list)))
    ch.remove(cur)
    while(1):
        lock.acquire()
        urlidx = random.choice(ch)
        try:
            state = requests.get(bully_list[urlidx])
            print("Node "+str(cur)+":",state.content.decode("UTF-8"))
            response = state.content.decode("UTF-8")
            lock.release()
        except:
            print("Connection failed with Node "+str(urlidx)+"!")
            if urlidx == coordinator:
                lock.release()
                threading.Thread(name='election', target=election).start()
            else:
                lock.release()
        finally:
            time.sleep(3)


def setcoordinator(x):
    lock.acquire()
    global coordinator
    coordinator=x
    print("New Coordinator: "+str(coordinator))
    lock.release()


@app.route("/", methods=['GET'])
def default_cordinator():
    return str(cur)


@app.route("/election", methods=['GET'])
def electionfunction():
    threading.Thread(name='election', target=election).start()
    return str(cur)


@app.route("/coordinator", methods=['POST'])
def coordinatorfunction():
    global coordinator
    data = request.json
    data = json.loads(data)
    setcoordinator(int(data["data"]))
    return str(cur)


if __name__ == '__main__':
    t = threading.Thread(name='run', target=run)
    t.start() 
    app.run(debug=True, use_reloader=False, port=port)
