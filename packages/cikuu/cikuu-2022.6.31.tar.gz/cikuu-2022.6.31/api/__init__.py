# 2022.9.2
from dm import * 
from wget import * 
from es import * 

def walk():
	import os
	for root, dirs, files in os.walk(".",topdown=False):
		for file in files: 
			if file.endswith(".py") and not file.startswith("_"): 
				file = file.split(".")[0]
				__import__(file, fromlist=['*']) #			importlib. 

if __name__	== '__main__': 
	print (cloze()) 
