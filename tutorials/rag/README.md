# RAG: Retrieval Augmented Generation


## Basic RAG

<p align='center'><img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/rag/basic_rag.png' width=60% alt='basic_rag'></p>

---

###  RAG Steps 
- Load and parse documents.
- Chunk the text into manageable pieces.
- Create vector embeddings and store in vector database (e.g., FAISS).
- Retrieve relevant chunks for summarization based on input query.
- Generate a concise summary using LLM (e.g., QwenChat).
- Print the summary output to the console.

### Example

#### Script
[basic_rag_qwen.py](https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/rag/basic_rag_qwen.py)

#### Features
- The pipeline currently uses "sentence-transformers/all-MiniLM-L6-v2" embedding model for chunk vectorization.
- Uses FAISS DB for efficient approximate nearest neighbor search and vector indexing of document embeddings.
- Both chunk_size and chunk_overlap parameters in split_documents can be modified for different chunking behavior.
- Supports `.pdf`,`.docx`, `.md`, and `.txt ` documents (single files or directories).
- QwenChat model requires GPU with float16 support for best performance.


#### Requirements

```
Python 3.12+
```

#### Installation 

```
pip install langchain transformers accelerate sentence-transformers faiss-cpu
pip install langchain-community langchain-huggingface
pip install "unstructured[all-docs]"
```

#### Input Query

```
"Summarize the following document by providing key points"
```

#### Prompt Template

```
prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that summarizes documents into concise bullet points describing key takeaways only."),
        ("human", "{input_query}:\n\n{context}")
    ])
```

#### Input Document

```
Building Retrieval-Augmented Generation (RAG) pipelines can seem daunting, with lots of moving parts and custom logic. In this tutorial, you'll learn how to quickly set up RAG agents using Contextual AI’s managed platform. You'll also get hands-on with several of the agent's core components—like the Parser, Reranker, Grounded Language Model, and LMUnit—so you can see how each part works in practice.

By completing this tutorial, you'll learn how to leverage agentic RAG to solve more complex queries. The agentic nature lies in the system's ability to autonomously analyze incoming queries, determine what reformulation strategy is needed, and execute that strategy without explicit user instruction.

Traditional RAG systems take queries as-is, often leading to poor retrievals for ambiguous, context-lacking, or complex queries. Agentic RAG intelligently preprocesses queries to bridge this gap. In the query path, the primary agentic step is query reformulation, comprising multi-turn, query expansion, or query decomposition. This query reformulation step is critical to obtaining the most robust RAG results, and is one component of a system engineered to generate the most accurate query responses.

In query reformulation, context is added or queries are restructured from the original input: for multi-turn, adding iterative dialogue context; for query expansion, adding additional context to help a short query return optimal results; for query decomposition, taking complex multi-faceted queries that require reasoning across several unrelated documents, and breaking them down into several sub-queries that help obtain the most relevant retrievals. This agentic component handles all of this reformulation autonomously, augmenting the user's query to help obtain the response they need.
```


#### Output Response

```
 - **Query Reformulation**: Agentic RAG enhances original queries by autonomously adding context or restructuring them through three key methods:  
  - *Multi-turn*: Incorporates iterative dialogue context.  
  - *Query expansion*: Adds relevant context to improve short query performance.  
  - *Query decomposition*: Breaks down complex, multi-faceted queries into sub-queries for better document-level reasoning.  

- **Autonomous Processing**: The agentic component independently analyzes queries, determines the optimal reformulation strategy, and executes it without user intervention.  

- **Improved Retrieval**: Traditional RAG systems fail with ambiguous or complex queries; agentic RAG overcomes this by intelligently preprocessing queries to yield more accurate and relevant results.  

- **RAG Pipeline Simplification**: Contextual AI’s managed platform enables rapid setup of agentic RAG pipelines with minimal custom code.  

- **Core Components**: Hands-on exploration of key components—Parser, Reranker, Grounded Language Model, and LMUnit—demonstrates how each contributes to effective query response generation.  

- **Key Takeaway**: Agentic RAG significantly enhances response accuracy by autonomously reformulating queries to better match retrieval needs, making it ideal for complex, context-rich, or ambiguous user inputs.
```

