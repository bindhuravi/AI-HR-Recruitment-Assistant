"""Local-only compatibility module. No cloud API is used."""
def get_chat_model(*args,**kwargs): return None
def get_embeddings(): return None
