# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 10:16:19 2019

@author: Armaan Puri 
"""
import os
import multiprocessing
import glob

class Streamer():
	
	def __init__(self, directory):
		self.directory = directory
	
	def latest_provider(self, stream_name):
		# get latest files, if any.
		files_sent=[]
		try:
			while True:
				if len(files_sent)<100:
					latest_file = max(glob.glob(stream_name.get()+"/*"), key=os.path.getctime)
					if str(latest_file) not in files_sent:
						files_sent.append(str(latest_file))
						self.latest_provider.q.put(latest_file)                                         #put latest files in a queue for FRAMER
						print(1)
					else:
						continue
				else:   
					files_sent=[]
					print(2)
					continue
		except KeyboardInterrupt:
			print("Stopped by User")
		# do something if condition not satisfied. Also start process again once condition satisfies

	def simpler_init(self, q):
		self.simpler.q = q
		
	def simpler(self, l, stream_name):
		known_latest = []           #
		print(multiprocessing.current_process())
		path = stream_name.get()
		# count = 0   
		try:
			while True:
				newest_file = max(glob.glob(path+"/*"), key=os.path.getctime)
				# print(newest_file)
				# print(path)
				# count+=1
				# print("Finding newest_file", count)
				if len(known_latest)<100:
					if str(newest_file) not in known_latest:         #
						l.acquire()
						known_latest.append(str(newest_file))
						self.simpler.q.put(newest_file)
						print("written to queue, releasing lock")
						l.release()
					else:
						print("waiting for file now...")
						# print(latest_files.get())
						# print("The output queue is empty?",latest_files.empty())
						time.sleep(5)
						continue
				else:
					known_latest=[]
		except KeyboardInterrupt:
			print("Stopped by user")

	def get_streams(self): #os.listdir("recordings")                           ###### check how to output multiprocessing stream output
		q = multiprocessing.Queue()
		p = multiprocessing.Pool(len(os.listdir(self.directory)), self.simpler_init, [q])    ###### add handle for process dying.sum(os.path.isdir(i) for i in os.listdir(path))
		streams = p.imap(self.simpler, (glob.glob(os.path.join(self.directory+"/*")),))
		p.close()

		for i in range(len(os.listdir(self.directory))):
			print(q.get())
			print(streams.next())
		
		# put retrieved streams in a queue
	
	def check_latest(stream_name):
		pass
		

if __name__=='__main__':
	directory = "/mnt/f/IISc_Big/recordings"
	streamer = Streamer(directory)
	streamer.get_streams()

