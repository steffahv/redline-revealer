import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA

load_dotenv()

# Set up OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Load curated law links
with open(os.path.join("data", "state_links.json"), "r") as f:
    reference_links = json.load(f)

# Helper to find curated link from JSON
def get_reference_link(question):
    question_lower = question.lower()
    for state, topics in reference_links.items():
        if state.lower() in question_lower:
            for topic, link in topics.items():
                topic_words = topic.lower().split()
                if all(word in question_lower for word in topic_words):
                    return link
    return None

# Setup RAG (FAISS + LangChain)
embedding_model = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
)
vectorstore = FAISS.load_local(
    "data/indexes/legal_docs_index",
    embeddings=embedding_model,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
)

# Custom detailed prompt
custom_prompt = PromptTemplate.from_template("""
You are a legal assistant helping someone understand how to resolve heirs' property issues.

Use the following documents to give a detailed and actionable response, including:
- Steps the person should take
- Names of organizations, contact info, and websites if available
- Legal terms or state laws if mentioned in the documents

If you don't find information in the documents, say "I don't know".

Context:
{context}

Question: {question}
""")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False,
    chain_type_kwargs={"prompt": custom_prompt},
)

# Main agent function
def get_legal_answer(question):
    try:
        # 1. Run the QA chain with vector search
        result = qa_chain(
            {"query": question},
            return_only_outputs=True
        )
        answer = result["result"]

        # 2. If RAG gives weak answer, fallback to raw LLM
        if "i don't know" in answer.lower() or len(answer.strip()) < 40:
            answer = llm.invoke(question).content  # Call GPT directly (no vector context)

        # 3. Add sources used (filenames)
        if "source_documents" in result:
            sources = set()
            for doc in result["source_documents"]:
                metadata = doc.metadata
                if "source" in metadata:
                    sources.add(os.path.basename(metadata["source"]))
            if sources:
                answer += "\n\n📄 Sources: " + ", ".join(sorted(sources))

        # 4. Add curated law link if relevant
        curated_link = get_reference_link(question)
        if curated_link:
            answer += f"\n\n🔗 For more info, see: {curated_link}"

        return answer

    except Exception as e:
        return f"❌ Error: {e}"
