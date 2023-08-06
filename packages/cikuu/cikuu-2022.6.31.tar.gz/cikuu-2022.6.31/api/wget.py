# 2022.9.2 
import time, requests ,json, platform,os,re,builtins
from collections import Counter,defaultdict
apihost	= os.getenv('apihost', 'cpu76.wrask.com:8000')

def cloze(snt:str="The quick fox * over the lazy dog.", model:str='native', topk:int=10):
	''' [{name,word,score}] '''
	#http://cpu76.wrask.com:8000/unmasker?q=The%20goal%20of%20life%20is%20%2A.&model=native&topk=10&verbose=false
	return requests.get(f"http://{apihost}/unmasker", params={"q":snt, "model":model, "topk":topk}).json()

if __name__	== '__main__': 
	print (cloze())