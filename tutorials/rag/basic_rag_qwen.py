import os
import torch
from typing import List, Optional, Any
from pydantic import Field, PrivateAttr
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.language_models import BaseLanguageModel
from langchain_core.language_models.llms import LLM
from langchain.prompts.chat import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# pip install langchain transformers accelerate sentence-transformers faiss-cpu
# pip install langchain-community langchain-huggingface
# pip install "unstructured[all-docs]"


# Load LLM Model
class QwenChatLLM(LLM):
    model_name: str = Field(default="Qwen/Qwen3-4B-Instruct-2507")
    max_new_tokens: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9

    _tokenizer: Any = PrivateAttr()
    _model: Any = PrivateAttr()

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-4B-Instruct-2507",
        max_new_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ):
        super().__init__(
            model_name=model_name,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs
        )

        self._tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        self._model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            device_map="auto",
            dtype=torch.float16,
        )
        self._model.eval()

    @property
    def _llm_type(self) -> str:
        return "qwen-chat"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        messages = [{"role": "user", "content": prompt}]
        chat_text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(chat_text, return_tensors="pt").to(self._model.device)

        output = self._model.generate(
            **inputs,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            do_sample=True,
            eos_token_id=self._tokenizer.eos_token_id,
        )

        generated_tokens = output[0][inputs["input_ids"].shape[-1]:]
        return self._tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()

def load_qwen_llm() -> BaseLanguageModel:
    return QwenChatLLM()


# Step 1: Load Documents
def load_documents(path):
    documents = []
    # Single file
    if os.path.isfile(path):
        if path.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif path.endswith(".docx"):
            loader = Docx2txtLoader(path)
        elif path.endswith(".md"):
            loader = UnstructuredMarkdownLoader(path)
        else:
            loader = TextLoader(path)
        documents.extend(loader.load())
    # Directory (load all supported files)
    elif os.path.isdir(path):
        for filename in os.listdir(path):
            full_path = os.path.join(path, filename)
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(full_path)
            elif filename.endswith(".docx"):
                loader = Docx2txtLoader(full_path)
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(full_path)
            elif filename.endswith(".txt"):
                loader = TextLoader(full_path)
            else:
                continue
            documents.extend(loader.load())
    else:
        raise ValueError("Provided path is neither a file nor a directory.")
    return documents


# Step 2: Split Documents
def split_documents(documents, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(documents)


# Step 3: Generate document embedding chunks and store in FAISS db
def create_vector_store(docs):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    return db


# Step 4: Create Retriever and Summary Chain
def create_retriever(db):
    retriever = db.as_retriever()
    docs = retriever.invoke("Summarize the key points of the document.")
    return docs

def create_summary_chain(llm):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarizes documents into concise bullet points describing key takeaways only."),
        ("human", "{input_query}:\n\n{context}")
    ])

    chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    return chain


# Step 5: Run summarization query
def summarize(file_path, input_query):
    docs = load_documents(file_path)
    chunks = split_documents(docs)
    db = create_vector_store(chunks)
    docs = create_retriever(db)
    llm = load_qwen_llm()
    summary_chain = create_summary_chain(llm)
    response = summary_chain.invoke({"input_query": input_query, "context": docs})
    print("\nOutput Summary:\n\n", response)


# Example Usage
if __name__ == "__main__":
    # file_or_dir_path = "my_docs/"
    file_or_dir_path = "example.md" 
    input_query = "Summarize the following document by providing key points"
    summarize(file_or_dir_path, input_query)
