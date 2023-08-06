# 2022.9.2
import requests,os,re,itertools
import pandas as pd
eshost	= os.getenv('eshost', 'es.corpusly.com:9200')

iphrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()['hits']['total']['value']
iterm  = lambda term="NOUN:force", cp='en', field='kps':requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "term": { field: term    }   } } ).json()['hits']['total']['value']
sntsum = lambda cp='clec': requests.post(f"http://{eshost}/_sql", json={"query":f"select count(*) from {cp} where type='snt'"}).json()['rows'][0][0]
match_phrase = lambda hyb="_be in force", cp='en', field='postag': requests.post(f"http://{eshost}/{cp}/_search", json={   "query": {  "match_phrase": { field: hyb    }   } } ).json()
phrase_snt = lambda hyb="_be in force", cp='en', field='postag': [ ar['_source']['snt']  for ar in match_phrase(hyb,cp,field)['hits']['hits'] ]

rows = lambda query, fetch_size=1000: requests.post(f"http://{eshost}/_sql",json={"query": query,"fetch_size": fetch_size}).json().get('rows',[]) #rows("select s,i from dic where s like 'dobj:VERB_open:NOUN_%'")
si = lambda pattern, cp='en', sepa='_': [ (row[0].split(sepa)[-1], int(row[1]) )  for row in rows(f"select s,i from {cp} where s like '{pattern}' order by i desc")]

def keyness(data_src, data_tgt): 
	''' return (src, tgt, src_sum, tgt_sum, keyness),2022.8.25 '''
	from util import likelihood
	df = pd.DataFrame({'src': dict(data_src), 'tgt': dict(data_tgt)}).fillna(0)
	df['src_sum'] = sum([i for s,i in data_src])
	df['tgt_sum'] = sum([i for s,i in data_tgt])
	df['keyness'] = [ likelihood(row['src'],row['tgt'],row['src_sum'],row['tgt_sum']) for index, row in df.iterrows()] 
	return df.sort_values(df.columns[-1], ascending=True) 

def cands_product(q='one two/ three/'):
    ''' {'one three', 'one two', 'one two three'} '''
    arr = [a.strip().split('/') for a in q.split()]
    res = [' '.join([a for a in ar if a]) for ar in itertools.product( * arr)]
    return set( [a.strip() for a in res if ' ' in a]) 

def compare(q="_discuss about/ the issue", cp='en'):
    cands = cands_product(q)
    return [ (cand, iphrase(cand, cp))  for cand in cands]

addpat	= lambda s : f"{s}_[^ ]*" if not s.startswith('_') else f"[^ ]*{s}[^ ]*"   # if the last one, add $ 
rehyb   = lambda hyb: ' '.join([ addpat(s) for s in hyb.split()])  #'the_[^ ]* [^ ]*_NNS_[^ ]* of_[^ ]*'
heads   = lambda chunk:  ' '.join([s.split('_')[0].lower() for s in chunk.split()])		#the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
def hybchunk(hyb:str='the _NNS of', index:str='en', size:int= -1, topk:int=10):
	''' the _NNS of -> {the books of: 13, the doors of: 7} , added 2021.10.13 '''
	from collections import Counter
	sql= { "query": {  "match_phrase": { "postag": hyb  } },  "_source": ["postag"], "size":  size}
	res = requests.post(f"http://{eshost}/{index}/_search/", json=sql).json()
	si = Counter()
	repat = rehyb(hyb)
	for ar in res['hits']['hits']: 
		postag =  ar["_source"]['postag']
		m= re.search(repat,postag) #the_the_DT_DET adventures_adventure_NNS_NOUN of_of_IN_ADP
		if m : si.update({ heads(m.group()):1})
	return si.most_common(topk)

if __name__ == '__main__': 
	print ( hybchunk()) 