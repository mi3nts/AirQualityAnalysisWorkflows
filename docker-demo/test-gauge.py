from prometheus_client import start_http_server, Gauge
import numpy as np
import time

start_http_server(8000)


g = Gauge("my_sin_function", "The function sin(x) updated with a dx of pi/200 every second")

dx = np.pi/200
x = 0
g.set(x)

while True:
    x += dx
    g.set(np.sin(x))
    print("Current value is {}".format(np.sin(x)))
    time.sleep(0.5)
