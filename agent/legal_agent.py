import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Load the reference links once at the top
with open(os.path.join("data", "state_links.json"), "r") as f:
    reference_links = json.load(f)

# Helper function to fetch legal reference links
def get_reference_link(question):
    question_lower = question.lower()
    for state, topics in reference_links.items():
        if state.lower() in question_lower:
            for topic, link in topics.items():
                topic_words = topic.lower().split()
                if all(word in question_lower for word in topic_words):
                    return link
    return None

# Main agent function
def get_legal_answer(question):
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "You are a helpful legal assistant for civic housing rights. Help with questions about heirs' property, title issues, and stability strategies."},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
        )
        answer = response.choices[0].message.content

        # Generalized logic to append a link
        link = get_reference_link(question)
        if link:
            answer += f"\n\n🔗 For more info, see: {link}"

        return answer
    except Exception as e:
        return f"Error: {e}"