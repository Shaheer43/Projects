import threading
import time
def testy():
    print("Excuting FROM {}".format(threading.current_thread().name))
    time.sleep(2)
THREADS=[]
for i in range(0,5):
    t=threading.Thread(target=testy)
    t.start()#concurrently
    t.join()#linearly