import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from FlagEmbedding import BGEM3FlagModel
import faiss
faiss.omp_set_num_threads(1)

import numpy as np
import json

from .utils import DataLoader
class SimilarityChecker:
    def __init__(self,texts):
        #vars
        self.database=None
        self.emb=None


        self.encoding_model=BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)  
        self.build_database(texts)
        self.dehash=texts
    def search_texts(self,texts,k=5):
        if self.database is None:
            print("need init before use")
            return
        if isinstance(texts,str):
            texts=[texts]
        vector=self._encode_text(texts)
        return self.database.search(vector,k)
        
    def build_database(self,texts):
        emb=self._encode_text(texts)
        self.database = faiss.IndexFlatIP(emb.shape[1])
        self.database.add(emb)

    def self_search(self,k=5):
        if self.database is None:
            print("need init before use")
            return [None]
        scores,rankings=self.database.search(self._encode_text(self.dehash),k)
        res=self._visible_result(scores,rankings)
        pairs=[]
        l=0
        for i in res:
            for j in i:
                if l!=j:
                    pairs.append({"pair":(l,j),"score":i[j]})
            l+=1
        return sorted(pairs,key=lambda x:x["score"],reverse=True)

    def _encode_text(self,texts):
        out = self.encoding_model.encode(texts, batch_size=32, max_length=2048)
        emb = out["dense_vecs"]
        emb = np.ascontiguousarray(emb, dtype="float32")
        if emb.ndim == 1:  # a single string gives shape (dim,); FAISS needs (n, dim)
            emb = emb.reshape(1, -1)
        return emb
    def _visible_result(self,scores,rankings):
        results=[]
        for i in range(len(rankings)):
            template={}
            for j in range(len(rankings[i])):
                #name=self.dehash[rankings[i][j]]
                name=int(rankings[i][j])
                score=float(scores[i][j])
                template[name]=score
            results.append(template)
        return results

def check_problems():
    data=DataLoader("data_generation/dataset")
    problems=[]
    for i in data:
        problems.append(i.problem)
    sc=SimilarityChecker(problems)
    res=sc.self_search()
    with open("similar.txt","w+") as fp:
        json.dump(res,fp)
    return
if __name__ == "__main__":
    check_problems()
    #texts=["dog","cat","car","book","motorbike"]
    #sc=SimilarityChecker(texts)
    #sc.search_texts(["bike","sleep"])
    #sc.self_search()

