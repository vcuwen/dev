import sys
import socket

class ParseIncomMsg(object):
    """
    This class takes the control of incomming messages. The correct way to code the software is by 
    socket, in wich one client sends data to our server/app, but for the purpose of the exercise
    a file with data will be used to show the report.
    """
    
    def __init__(self, host=None, port=None):
	""" 
	In the correct approach there is another application sending messages through the
	network by the specified port. In that port we will be waiting to receive the message.

	To make it easier, user may not initialize any socket, and the app works too  
	"""

	self.dic   = {}	 # dictionary to store shares and amounts
	self.opDic = {}  # dictionary to store operations over shares
	self.conn  = None

	if host != None and port != None:
		self.conn = socket.socket(
		        socket.AF_INET, socket.SOCK_STREAM)
		
		self.conn.connect((host, port))

	
    def recvMsg(self):
	""" 
	The incoming message (by socket client or by file) format is a list with four possible fields for
	message type 1 and 2 --> product|sales|price|typeMsg and for message type 3 with this 
	structure --> product|amount|operation|typeMsg 

	The software will check if it works by network or by file
	"""

	if self.conn != None:
		print ">> Receiving data from client"
		return self.conn.recv(512)

		
    def parsePrintRep(self):
	"""
	Method that process and print the data. 
	"""

	cont10 = 1
	cont50 = 1
	
	"""
	As I said the proper way is code by socket but port could be closed depending of the 
	network, thus to test the program, message is received across data file (inputMsg.dat)
	"""
	if self.conn == None: f = open('inputMsg.dat', 'r')

	while 1:
		# the socket way incoming messages
		if self.conn != None:
			data = recvMsg() 

		# the file way 
		else:
			data = f.readline().rstrip()
			# When the eof is reached the application ends
			if data == '': break

		fields = data.split('|')
		product = fields[0]

		"""check if the product (fields[0]) exists yet in 
		the dictionary, if not it'll be add """

		if self.dic.get(product) == None:
			self.dic[product] = [0, 0] # [sales, totalvalue]
			# this is just to store the total amount
			self.dic[product].append(0) 
			# to log the adjustements have been made
			self.opDic[product] = {'+': 0, '-': 0, '*': 0}

		# Ask for the type of message (1 or 2)
		if fields[3] == '1' or fields[3] == '2':
			self.dic[product][0] += int(fields[1]) # sales
			#self.dic[product][1] += int(self.dic[product][0]) * int(self.dic[product][1]) # total amount
			self.dic[product][1] += int(fields[1])*int(fields[2]) # total value
			
		# Type message 3
		elif fields[3] == '3':
			if fields[2] == '+':
				self.dic[product][1] = int(self.dic[product][1]) + int(self.dic[product][0])*int(fields[1])
				self.opDic[product]['+'] += 1
			elif fields[2] == '-':
				self.dic[product][1] = int(self.dic[product][1]) - int(self.dic[product][0])*int(fields[1])
				self.opDic[product]['-'] += 1
			elif fields[2] == '*':
				
				self.dic[product][1] = int(self.dic[product][1]) * int(self.dic[product][0])*int(fields[1])
				self.opDic[product]['*'] += 1
		else: 		
			raise RuntimeError("Socket transmision error. Message format incorrect") 
		
		#print self.dic
		if cont10 == 10:
			print '###############################'
			print 'TEMPORAL REPORT (10th)'
			for share in self.dic:
				print '>>> SHARE: ', share + ' Sales: ' + str(self.dic[share][0]) + ' TOTAL: ' + str(self.dic[share][1]) + 'p'
			cont10 = 1;
			print '###############################'
			print ''

		if cont50 == 50:
			print '###############################'
			print 'REPORTING OPERATION ACTIVITY'
			for share in self.opDic:
				print '>>> SHARE: ', share
				print 'Adding operations: ', self.opDic[share]['+']
				print 'Substract operations: ', self.opDic[share]['-']
				print 'Multiply operations: ', self.opDic[share]['*']
				print '----------------------------'
			print '###############################'
			print ''
				
			cont50 = 0

			inp = raw_input(">>> Application is paused. Press enter to keep geting new messages")

		cont10 += 1
		cont50 += 1



obj = ParseIncomMsg()
obj.parsePrintRep()



	

