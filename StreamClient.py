#!/usr/bin/env python
import urllib
import cv2
import numpy

# get http server ip, port, and route
server_ip = raw_input('Server IP: ')
port = raw_input('Port: ')
route = raw_input('Route: ')
buf = 1024
cam = 'http://' + server_ip + ':' + port + '/' + route
stream = urllib.urlopen(cam)
bytes = ''
if route != 'cam_feed' and route != 'sample_video':
    bytes = stream.read()
    print bytes
else:
    while True:
        # read motion jpeg frame
        bytes += stream.read(buf)
        # parse the stream and check if entire frame is found between marker
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            # decode the numpy array
            frame = cv2.imdecode(numpy.fromstring(jpg, dtype = numpy.uint8),cv2.IMREAD_COLOR)
            if frame is None:
                print 'Frame from Cam not found'
                break
            else: # we now have frame stored in frame.
                cv2.imshow('Video Display',frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
stream.close()
