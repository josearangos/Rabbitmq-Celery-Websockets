from stomp import *

c = stomp.Connection([('127.0.0.1', 5672)])
c.start()
c.connect('gues', 'gues', wait=True)


stomp -H localhost -P 5672
