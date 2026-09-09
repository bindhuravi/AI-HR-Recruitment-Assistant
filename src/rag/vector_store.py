"""Local keyword retrieval; no API key or vector database service required."""
import os,re
from config import KB_DIR,JD_DIR
from src.utils.file_loader import load_text_from_file
class Doc:
    def __init__(self,page_content,metadata): self.page_content=page_content; self.metadata=metadata
def similarity_search(query,k=4,collection_name='hr_knowledge'):
    words=set(re.findall(r'\b[a-zA-Z]{3,}\b',query.lower())); docs=[]
    for directory in (KB_DIR,JD_DIR):
        if not os.path.isdir(directory): continue
        for fn in os.listdir(directory):
            p=os.path.join(directory,fn)
            if os.path.isfile(p):
                txt=load_text_from_file(p); score=sum(txt.lower().count(w) for w in words)
                if score: docs.append((score,Doc(txt,{'source':fn})))
    docs.sort(key=lambda x:x[0],reverse=True); return [d for _,d in docs[:k]]
def add_documents(texts,metadatas=None,collection_name='hr_knowledge'): return None
