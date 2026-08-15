import os
from dotenv import load_dotenv
load_dotenv()
from langchain_huggingface import HuggingFaceEndpointEmbeddings

hf_token = os.getenv("HF_TOKEN")
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=hf_token
)

res = embeddings.embed_query("Hello world")
print(f"Embedding length: {len(res)}")
