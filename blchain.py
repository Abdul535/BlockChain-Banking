import datetime
import hashlib
import string
from flask import Flask, request, render_template

class Block:
	blockNo = 0
	data = None
	next = None
	hash = None
	nonce = 0
	previous_hash = 0*0
	timestamp = datetime.datetime.now()
	
	def __init__(self, data, name):
		self.data = data
		self.blockName = name
		
	def hash(self):
		h = hashlib.sha256()
		h.update(
		str(self.nonce).encode('utf8')+
		str(self.data).encode('utf8')+
		str(self.previous_hash).encode('utf8')+
		str(self.timestamp).encode('utf8')+
		str(self.blockName).encode('utf8'))
		
		return h.hexdigest()
		
	def __str__(self):
		return "Block Hash: " + str(self.hash()) + "\nBlockName: " + str(self.blockName)+ "\nBlock Data: " + str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"


class Blockchain:
	diff = 10
	maxNonce = 2**32
	target = 2**(256-diff)
	
	block = Block("Genesis text", "Genesis")
	dummy = head = block
	
	def add(self, block):
		block.previous_hash = self.block.hash() 
		self.block.next = block
		self.block = self.block.next
	
	def mine(self, block):
		for n in range(self.maxNonce):
			if int(block.hash(), 16) <= self.target:
				self.add(block)
				# print("Hello i am ")
				print(block)
				# print("Hello i am 222 ")
				return block.blockName,block.data,str(block.hash()),str(block.previous_hash)
			else:
				block.nonce += 1
	
	
app = Flask(__name__)
blockchain = Blockchain()
my_dict = []

@app.route('/')
def my_form():
	return render_template('index.html',content = "")

@app.route('/',methods=['POST', 'GET'])
def my_form_post():
	PayeeName = request.form['PayeeName']
	AmountTransfer = request.form['AmountTransfer']
	
	nm, tx, bh, ph = blockchain.mine(Block(PayeeName, AmountTransfer))
	my_dict.append([nm,tx,bh,ph])
	return render_template('index.html', name_list = my_dict)

if __name__=="__main__":
	app.run(debug=True)