#!/usr/bin/env python

from boto.sqs.connection import SQSConnection
from boto.sqs.message import Message
conn = SQSConnection('AKIAIFNNIT7VXOXVFPIQ', 'stNtF2dlPiuSigHNcs95JKw06aEkOAyoktnWqXq+')
q = conn.get_queue('dwpTestQueue')

def writeToSQS(messageBody):
	# Note that messages are base64 encoded.
	m1 = Message()
	m1.set_body(messageBody)
	q.write(m1)

def pingSQS():
	print 'OMF message count:', q.count()

def peakSingleMessage():
	print [m.get_body() for m in q.get_messages(1)]

def eatSingleMessage():
	pull = q.get_messages(1)
	if len(pull) == 0:
		return False
	else:
		m = pull[0]
		q.delete_message(m)
		return m.get_body()

def endlessPinging():
	from threading import Timer
	def repeating():
		pingSQS()
		Timer(2, repeating).start()
	repeating()

if __name__ == '__main__':
	# writeToSQS('Test message!')
	# endlessPinging()
	print eatSingleMessage()



'''
One queue, stores tuples (analysisName, requestType). Or maybe have two queues, whatever.

Adding jobs.
	Put (analysisName, 'toRun') on the queue.
	If that analysis is already on the queue, return failed.
	Update the DB to say queued.
Running jobs.
	Every 1(?) second, all nodes check the queue.
	If there's a toRun there, and we're not full, pop one.
	Start the job.
	Update DB to say queued.
Canceling jobs.
	Every 1(?) second, all nodes check the queue.
	If there's a toKill there, and we're running that analysisName, pop one.
	Kill the PID.

Queue limits?


We need to handle two cases:
1. Filesystem case. Just have a dumb fileQueue class that has no limits, etc.?
2. S3 cluster case. Have a cluterQueue class, and also have a daemon.

'''

from threading import Timer
import multiprocessing

JOB_LIMIT = 1

class backgroundProc(multiprocessing.Process):
	def __init__(self, backFun, funArgs):
		self.name = 'omfWorkerProc'
		self.backFun = backFun
		self.funArgs = funArgs
		self.myPid = os.getpid()
		multiprocessing.Process.__init__(self)
	def run(self):
		self.backFun(*self.funArgs)

class LocalQueue:
	def __init__(self):
		pass
	def executeAnalysis(self, jobOb):
		pass
	def terminateAnalysis(self, jobOb):
		pass

class ClusterQueue:
	def __init__(self, userKey, passKey, workQueueName, terminateQueueName):
		self.runningJobs = 0
		self.conn = SQSConnection(userKey, passKey)
		self.workQueue = self.conn.get_queue(workQueueName)
		self.terminateQueue = self.conn.get_queue(terminateQueueName)
	def queueWork(self, analysisName):
		m = Message()
		m.set_body(analysisName)
		status = self.workQueue.write(m)
		return status
	def queueTerminate(self, analysisName):
		m = Message()
		m.set_body(analysisName)
		status = self.terminateQueue(m)
		return status

def monitorClusterQueue():
	#TODO: what all do we have to import to run this stuff?
	conn = SQSConnection(USERKEY, PASSKEY)
	jobQueue = conn.get_queue('crnOmfJobQueue')
	terminateQueue = conn.get_queue('crnOmfTerminateQueue')
	runningJobs = 0
	def endlessLoop():
		if runningJobs < JOB_LIMIT:
			mList = jobQueue.get_messages(1)
			if len(mList) == 1:
				anaName = mList[0].get_body()
				# Get analysis stuff from storage, run it here.
		if runningJobs > 0:
			# Get the termination going here.
			pass
		Timer(2, repeating).start()
	endlessLoop()

if __name__ == '__main__':
	# If we're running this module directly, go into daemon mode:
	monitorClusterQueue()