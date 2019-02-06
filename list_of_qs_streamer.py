# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:41:07 2019

@author: Armaan Puri 
"""

import os
import multiprocessing
import glob
import time
import sched
import configparser
from multiprocessing import Event 

class Streamer():
    
    def __init__(self, directory, latest_files):
        self.directory = directory
    
    def simpler(self, stream_name, f_q,  wait, ml, list_length):
        known_latest = []           #
        print(multiprocessing.current_process())
        path = stream_name.get()
        l = multiprocessing.Lock()
        # count = 0   
        try:
            while True:
                newest_file = max(glob.glob(path+"/*"), key=os.path.getctime)
                if len(known_latest)<list_length:
                    if str(newest_file) not in known_latest:         #
                        ml.acquire()
                        l.acquire()
                        known_latest.append(str(newest_file))
                        # output.put(newest_file)
                        f_q.put(newest_file)
                        print("writing to queues done, releasing lock")
                        print("here's output", f_q)
                        l.release()
                        ml.release()
                    else:
                        print("waiting for file now...")
                        # print(latest_files.get())
                        # print("The output queue is empty?",latest_files.empty())
                        time.sleep(wait)
                        continue
                else:
                    known_latest=[]
        except KeyboardInterrupt:
            print("Stopped by user")

    def repeater(self, return_num):
        # while True:
        return_num.value = len(os.listdir(self.directory))
        Timer(10,repeater, [return_num]).start()


            # print("written*************************")
            # print("repeater_output*******************************: ", return_num.value)
            # time.sleep(30)
    def dump_queue(self,queue):
        """
        Empties all pending items in a queue and returns them in a list.
        """
        result = []

        for i in iter(queue.get, 'STOP'):
            result.append(i)
        # time.sleep(.1)
        return result

if __name__=='__main__':
    config = configparser.ConfigParser()
    config.read('./config.ini')

    path_to_rec = config["DEFAULT"]["path_to_rec"]
    wait = int(config["DEFAULT"]["wait_time"])
    list_length = int(config["DEFAULT"]["list_length"])

    myResults = multiprocessing.Manager().list()
    streamer = Streamer(path_to_rec, myResults)
    myStreams = multiprocessing.Queue()

    main_lock = multiprocessing.Lock()
    # lock = multiprocessing.Lock()
    for stream in glob.glob(os.path.join(path_to_rec+"/*")):
        myStreams.put(stream)

    n = len(os.listdir(streamer.directory))   #for each stream, a process would be started 
    final_q = [multiprocessing.Queue()] * n    # initializing n queues, for each stream, this list is the final OUTPUT

    workers = []
    processes = {}
    m=0
    
    # n=int(return_num.value)

    for i in range(n):
        work = multiprocessing.Process(target=streamer.simpler, args=(myStreams,final_q[i], wait,main_lock, list_length))
        work.name
        work.start()
        # work.join()
        # work.daemon = True
        processes[n] = (work, i)
        m+=1
        workers.append(work)
    
    # for each in workers:
    #     print("Let's join workers")
    #     each.join()

    # while len(processes) > 0:
    #     for x in processes.keys():
    #         (p, a) = processes[x]
    #         time.sleep(0.5)
    #         if p.exitcode is None and not p.is_alive(): # Not finished and not running
    #              # Do your error handling and restarting here assigning the new process to processes[n]
    #              print(a, 'is gone as if never born!')
    #         elif p.exitcode < 0:
    #             print ('Process Ended with an error or a terminate', a)
    #             # Handle this either by restarting or delete the entry so it is removed from list as for else
    #         else:
    #             print (a, 'finished')
    #             p.join() # Allow tidyup
    #             del processes[x] # Removed finished items from the dictionary 
    #             # When none are left then loop will end

    # for worker in workers:
    #     check = multiprocessing.Process(target=streamer.check_status, args=(worker,))
    #     check.start()
  
    # for i in range(n):
    #     print("Final queue containing queues for each stream: ", final_q.get())

    for worker in workers:
        if worker.is_alive() == False:
            worker.start()
            continue
        else:
            pass
