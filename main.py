#!/usr/bin/python3
from hello import Runner
from threading import Thread

r = Runner()
runner = Thread(target=r.run)
runner.setDaemon(True)
runner.start()

try:
    while True:
        r.recv()
except KeyboardInterrupt:
    r.stop()
    print("-------\nAll done")