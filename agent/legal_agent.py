import os
import json
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from utils.state_list import US_STATES

load_dotenv()

# Load public blob links for source documents
with open(os.path.join("data", "source_links.json"), "r") as f:
    source_links = json.load(f)

# Load curated law links
with open(os.path.join("data", "state_links.json"), "r") as f:
    reference_links = json.load(f)

# ---------- Helper functions ----------


def is_generic_doc(filename):
    return not re.search(r"-[a-z]{2}-\d{4}", filename.lower())
    

def get_reference_link(question):
    question_lower = question.lower()
    for state, topics in reference_links.items():
        if state.lower() in question_lower:
            for topic, link in topics.items():
                topic_words = topic.lower().split()
                if all(word in question_lower for word in topic_words):
                    return link
    return None
    

def extract_state(question):
    for state in US_STATES:
        if re.search(rf"\b{state}\b", question, re.IGNORECASE):
            return state.lower()
    return None

# ---------- Setup functions (deferred until called) ----------


def get_openai_client():
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def get_embeddings():
    return AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    )


def get_chat_llm():
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    )


# ---------- Prompt Template ----------


custom_prompt_text = (
    "You are a legal assistant helping someone understand how to resolve "
    "heirs' property issues.\n\n"
    "Use the following documents to give a detailed and actionable response, "
    "including:\n"
    "- Steps the person should take\n"
    "- Names of organizations, contact info, and websites if available\n"
    "- Legal terms or state laws if mentioned in the documents\n\n"
    "If you don't find information in the documents, say \"I don't know\".\n\n"
    "Context:\n{context}\n\nQuestion: {question}"
)
custom_prompt = PromptTemplate.from_template(custom_prompt_text)


# ---------- Main Function ----------


def get_legal_answer(question):
    try:
        state = extract_state(question)
        embedding_model = get_embeddings()
        vectorstore = FAISS.load_local(
            "data/indexes/legal_docs_index",
            embeddings=embedding_model,
            allow_dangerous_deserialization=True
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
        llm = get_chat_llm()
        docs = retriever.get_relevant_documents(question)

        # Filter documents
        filtered_docs = []
        if state:
            for doc in docs:
                content = doc.page_content.lower()
                source = doc.metadata.get("source", "").lower()
                if state in content or state in source:
                    filtered_docs.append(doc)
        else:
            for doc in docs:
                filename = os.path.basename(doc.metadata.get("source", "")).lower()
                if is_generic_doc(filename):
                    filtered_docs.append(doc)

        if filtered_docs:
            chain = load_qa_chain(llm, chain_type="stuff", prompt=custom_prompt)
            answer = chain.run(input_documents=filtered_docs, question=question)
            result = {"result": answer, "source_documents": filtered_docs}
        else:
            result = {"source_documents": []}
            answer = llm.invoke(question).content

        if "i don't know" in answer.lower() or len(answer.strip()) < 40:
            answer = llm.invoke(question).content

        sources = set()
        for doc in result["source_documents"]:
            filename = os.path.basename(doc.metadata.get("source", ""))
            link = source_links.get(filename)
            if link:
                sources.add(f"[{filename}]({link})")
            else:
                sources.add(filename)

        if sources:
            source_list = "\n".join(f"🔹 {src}" for src in sorted(sources))
            answer += "\n\n📄 Source Documents Used:\n" + source_list

        curated_link = get_reference_link(question)
        if curated_link:
            answer += f"\n\n🔗 For more info, see: {curated_link}"

        return answer

    except Exception as e:
        return f"❌ Error: {e}"
