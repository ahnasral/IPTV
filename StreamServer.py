#!/usr/bin/env python
from flask import Flask, render_template, Response
from StreamObject import StreamObject
from enumerate_interfaces import all_interfaces, format_ip

app = Flask(__name__)

def select_if():
    print ('All Interfaces:')
    ifs = all_interfaces()
    for i in ifs:
        print "%s->%s" % (i[0], format_ip(i[1]))
    d_if = raw_input('Type which input to select: ')
    for i in ifs:
        if i[0] == d_if:
            return format_ip(i[1])
    print ('Interface selected invalid')
    exit(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/msg')
def sample_msg():
    return 'Hello World'

def gen(StreamObject):
    while True:
        frame = StreamObject.get_frame()
        yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame)

@app.route('/cam_feed')
def cam_feed():
    return Response(gen(StreamObject(0)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/sample_video')
def sample_video():
    return Response(gen(StreamObject(1)), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if_ip = select_if()
    if_port = 5000
    app.run(host = if_ip, port = if_port, threaded = True, debug = True, use_reloader = False)
