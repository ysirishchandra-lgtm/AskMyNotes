from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import io
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

app = FastAPI(title="AskMyNotes RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from dotenv import load_dotenv
load_dotenv()

# Global variables for vector store and LLM
vector_store = None
llm = None
full_pdf_text = ""

from langchain_huggingface import HuggingFaceEndpointEmbeddings

# Initialize Hugging Face Endpoint embeddings
embeddings = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=os.environ.get("HF_TOKEN")
)

# Initialize cloud LLM via HuggingFace API (Massive model, zero local processing)
try:
    print("Connecting to Hugging Face API...")
    from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
    endpoint = HuggingFaceEndpoint(
        repo_id="Qwen/Qwen2.5-72B-Instruct",
        huggingfacehub_api_token=os.environ.get("HF_TOKEN"),
        max_new_tokens=2048,
        temperature=0.3
    )
    llm = ChatHuggingFace(llm=endpoint)
    print("API Connected successfully.")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error loading models: {e}")


class QuestionRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global vector_store, full_pdf_text
    try:
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
                
        if not text:
            return {"error": "Could not extract text from PDF."}

        full_pdf_text = text

        # Chunk text into smaller pieces for much faster AI processing
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
        chunks = text_splitter.split_text(text)

        # Create embeddings and vector store
        vector_store = FAISS.from_texts(chunks, embeddings)

        return {"message": "File uploaded and processed successfully."}
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask")
async def ask_question(data: QuestionRequest):
    global vector_store, llm, full_pdf_text
    if not vector_store:
        return {"error": "Please upload a PDF first."}
    if not llm:
        return {"error": "AI model is still loading or failed to load."}
    
    try:
        question_lower = data.question.lower()
        if "summary" in question_lower or "summarize" in question_lower:
            # For summarization, provide the whole text (up to 20000 chars to stay within context limits safely)
            context = full_pdf_text[:20000]
        else:
            # Retrieve a massive context to maximize response detail
            docs = vector_store.similarity_search(data.question, k=10)
            context = "\n".join([doc.page_content for doc in docs])
        
        # Generate answer using Cloud LLM
        from langchain_core.messages import HumanMessage
        prompt = (
            f"You are the world's most intelligent AI assistant. Your goal is to provide a '10/10 rating' masterclass response based ONLY on the provided notes.\n\n"
            f"Notes Context: {context}\n\n"
            f"User Question: {data.question}\n\n"
            f"Instructions for a 10/10 response:\n"
            f"1. Be incredibly detailed, comprehensive, and exhaustive.\n"
            f"2. Use markdown formatting beautifully (bolding key terms, using bullet points, creating clear paragraphs).\n"
            f"3. Structure the answer logically with an introduction, detailed body paragraphs, and a clear conclusion.\n"
            f"4. Leave absolutely no stone unturned.\n\n"
            f"Generate your 10/10 response now:"
        )
        response = llm.invoke([HumanMessage(content=prompt)])
            
        return {"answer": response.content.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.get("/status")
def status():
    return {"status": "online", "models_loaded": llm is not None}

# Serve the static frontend files
import os
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'Frontend')
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{filename}")
def serve_static(filename: str):
    file_path = os.path.join(frontend_path, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse(os.path.join(frontend_path, "index.html"))
