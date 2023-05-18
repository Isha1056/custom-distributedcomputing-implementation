from flask import Flask, request
import threading
import time
import json


lock = threading.Lock()
count = 0


def tick():
  global count
  while(1):
    lock.acquire()
    try:
        count += 1
        print("Time: "+str(count))
    finally:
        lock.release()
        time.sleep(1)


def modify(x):
  global count
  while(1):
    lock.acquire()
    try:
        print('Current timer: ', count )
        count += x
        print('Modified timer: ', count )
    finally:
        lock.release()
        return


def get_time():
  global count
  while(1):
    lock.acquire()
    try:
        print('Returned Timer: ', count )
    finally:
        lock.release()
        return count


app=Flask(__name__) 


@app.route('/poll', methods = ['GET']) 
def func(): 
    if request.method == 'GET':
        x = get_time()
        return json.dumps({"data":x})


@app.route('/modify', methods = ['POST']) 
def func1(): 
    if request.method == 'POST':
        data = request.json
        data = json.loads(data)
        modify(data['data'])
        x = get_time()
        return json.dumps({"data":x})


if __name__=='__main__': 
    t = threading.Thread(name='tick', target=tick)
    t.start() 
    app.debug=True 
    app.run(port=5001, debug=True, use_reloader=False)
