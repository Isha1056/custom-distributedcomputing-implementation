import threading
import time
import requests
import json
from flask import Flask, request
import random


app=Flask(__name__) 


lock = threading.Lock()
count=0
node=1


modify_list=[
    {
        "url":"http://127.0.0.1:5001",
        "node":2
    },
    {
        "url":"http://127.0.0.1:5002",
        "node":3
    }
]


def tick():
  global count
  while(1):
    lock.acquire()
    try:
        count += 6
        print("Time: "+str(count))
    finally:
        lock.release()
        time.sleep(1)


def get_time():
  global count
  while(1):
    lock.acquire()
    try:
        pass
    finally:
        lock.release()
        return count


def modify(x):
  global count
  while(1):
    lock.acquire()
    try:
        print('\nReceived timer: ', x )
        print('Current timer: ', count )
        count = max(count, x+1)
        print('Modified timer: ', count )
        print()
    finally:
        lock.release()
        break


def message():
    global count
    while(1):
        time.sleep(5)
        lock.acquire()
        try:
            x = requests.post(url = modify_list[random.randint(0,1)]["url"]+"/modify", json = json.dumps({"data":count, "node": modify_list[random.randint(0,1)]["node"]}))
        finally:
            lock.release()


t = threading.Thread(name='tick', target=tick)
t1 = threading.Thread(name='message', target=message)
t.start()
t1.start()


@app.route('/modify', methods = ['POST']) 
def func1(): 
    if request.method == 'POST':
        data = request.json
        data = json.loads(data)
        modify(data['data'])
        x = get_time()
        return json.dumps({"data":x})


if __name__=='__main__':  
    app.run(port=5000, debug=True, use_reloader=False)
