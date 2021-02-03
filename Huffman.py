import heapq
import os

class Huffman:
	def __init__(self,path):
		self.path=path
		self.codes = {}
		self.heap=[]
		self.reverse_mapping = {}

	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other==None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq


	def countfrequency(self,text):
		freq_dict={}
		for key in text:
			if not key in freq_dict:
				freq_dict[key] = 0
			freq_dict[key] += 1
		return freq_dict

	def makeheap(self,freq_dict):
		for key in freq_dict:
			node = self.HeapNode(key,freq_dict[key])
			heapq.heappush(self.heap, node)

	def combineNodes(self):
		while(len(self.heap)>1):
			node1=heapq.heappop(self.heap)
			node2=heapq.heappop(self.heap)
			
			merged=self.HeapNode(None, node1.freq + node2.freq)
			merged.left=node1
			merged.right=node2

			heapq.heappush(self.heap, merged)
		    

	def recur_code(self, root, current_code):
		if(root == None):
			return 

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.recur_code(root.left, current_code + "0")
		self.recur_code(root.right, current_code + "1")
		
	

	def code(self):
		root=heapq.heappop(self.heap)
		current_code = ""
		self.recur_code(root, current_code)

	def encoded_text(self,text):
		encoded=""
		for char in text:
			encoded += self.codes[char]
		return encoded

	def pad_encoded_text(self,encoded):
		extra_encoded=8 - len(encoded) % 8
		for i in range(extra_encoded):
			encoded += "0"
		paded_code= "{0:08b}".format(extra_encoded)
		encoded=paded_code + encoded
		print("encod",paded_code)
		return encoded

	def get_hex_array(self,pad_encoded_text):
		if(len(pad_encoded_text) % 8!=0):
			print("encoding not done properly")
			exit(0)
		
		h=bytearray()

		for i in range(0,len(pad_encoded_text),8):
			hexa=pad_encoded_text[i:i+8]
			#hexa2=pad_encoded_text[i+8:i+16]
			h.append(int(hexa, 2))
		
		return h

	def compress(self):
		filename,fileextension=os.path.splitext(self.path)
		output_file=filename+".bin"

		with open(self.path ,'r+') as file ,open(output_file,'wb') as output:
			text=file.read()
			text=text.rstrip()

			frequency=self.countfrequency(text)
			self.makeheap(frequency)
			self.combineNodes()
			self.code()

			encode=self.encoded_text(text)
			pad_encode=self.pad_encoded_text(encode)

			h=self.get_hex_array(pad_encode)
			output.write(bytes(h))

			print("compressed")
			return output_file


	def rem_pad(self,pad_encoded_text):
		pad_info = pad_encoded_text[:8]
		extra = int(pad_info, 8)

		pad_encoded_text = pad_encoded_text[8:]
		encoded_text = pad_encoded_text[:-1*extra]

		return encoded_text

			

	def decode_text(self,encoded_text):
		current_code=""
		decode_text=""

		for i in encoded_text:
			current_code+=i
			if(current_code in self.reverse_mapping):
				char=self.reverse_mapping[current_code]
				decode_text+=char
				current_code=""
		return decode_text

	def decompress(self,input_path):
		filename,fileextension = os.path.splitext(self.path)
		output_path = filename + "_decompress" +".txt"
		with open(input_path,'rb') as file, open(output_path,'w') as output:
			string=""

			hexa=file.read(1)
			
			while(len(hexa) > 0):
				
				hexa=ord(hexa)
				
				he=hex(hexa)[2:].rjust(8, '0')
				string+=hexa
				hexa=file.read(1)

			encoded_text=self.rem_pad(string)
			decompressed_text=self.decode_text(encoded_text)
			output.write(decompressed_text)

		    
		    
		print("decompressed")
		return output_path	

path=input("enter the path of the file \n")
h=Huffman(path)
h.compress()
i=int(input("do u need to decompress the file \n"))


if (i==1):
	j=input("enter the path of the file to be compressed \n")
	h.decompress(j)

        


		




    
			    

    		

    	

    













