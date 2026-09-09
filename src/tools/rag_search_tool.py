import os,re
from config import KB_DIR,JD_DIR
from src.utils.file_loader import load_text_from_file
def search_knowledge_base(query:str)->str:
    words=set(re.findall(r'\b[a-zA-Z]{3,}\b',query.lower())); results=[]
    for directory in (KB_DIR,JD_DIR):
        if not os.path.isdir(directory): continue
        for fn in os.listdir(directory):
            p=os.path.join(directory,fn)
            if not os.path.isfile(p): continue
            text=load_text_from_file(p); score=sum(1 for w in words if w in text.lower())
            if score: results.append((score,fn,text))
    results.sort(reverse=True,key=lambda x:x[0])
    return '\n\n'.join(f'[source: {fn}]\n{txt[:1500]}' for _,fn,txt in results[:4]) or 'No relevant documents found in the knowledge base.'
