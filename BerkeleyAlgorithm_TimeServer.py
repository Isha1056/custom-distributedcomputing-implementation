import threading
import time
import requests
import json


lock = threading.Lock()
count = 0


modify_list=[
    {
        "url":"http://127.0.0.1:5001",
        "data":0
    },
    {
        "url":"http://127.0.0.1:5002",
        "data":0
    }
]


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


def get_time():
  global count
  while(1):
    lock.acquire()
    try:
        print('Returned Timer: ', count )
    finally:
        lock.release()
        return count


def modify():
  global count
  while(1):
    lock.acquire()
    try:
        print("Time server: "+ str(count))
        for i in range(len(modify_list)):
            x = requests.get(url = modify_list[i]["url"]+"/poll")
            x = json.loads(x.text)
            modify_list[i]["data"] = x["data"]
            if modify_list[i]["data"]!=count:
                print("Server "+str(i+1)+": "+str(modify_list[i]["data"]))
                x = requests.post(url = modify_list[i]["url"]+"/modify", json = json.dumps({"data":count-modify_list[i]["data"]}))
                x = json.loads(x.text)
                modify_list[i]["data"] = x["data"]
                print("Modified Server "+str(i+1)+": "+str(modify_list[i]["data"]))
    finally:
        lock.release()
        time.sleep(5)
        


t = threading.Thread(name='tick', target=tick)
t1 = threading.Thread(name='modify', target=modify)
t.start()
t1.start()
