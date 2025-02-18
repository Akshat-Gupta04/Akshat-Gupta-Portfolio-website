from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key_here"  # Needed for session tracking

# Initialize the LLM model (GPT-3.5-turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

# Define project details
project_docs = [
    """My LoRA Model: Developed a highly realistic image generation model fine-tuned on personalized facial data using a Custom LoRA technique.
    This model enhances generative capabilities while reducing computational costs.""",
    """Akshar: A real-time translation chat application built with Flutter that integrates AI-based speech processing for seamless multilingual communication.
    This app allows instant voice and text translation across multiple languages.""",
    """Eye Disease Detection: A deep learning model designed to classify retinal diseases from fundus images, leveraging convolutional neural networks for early diagnosis.
    The model improves early detection rates and supports ophthalmologists in accurate diagnosis.""",
    """Medical ChatBot: An AI-powered medical assistant using retrieval-augmented generation to deliver dynamic, context-aware medical advice.
    It provides initial medical guidance, symptom analysis, and basic health recommendations.""",
    """FacePay: An AI-powered facial recognition payment system designed as an alternative to QR codes.
    This solution ensures secure, contactless transactions with high accuracy and fraud prevention."""
]

# Create embeddings and load FAISS index safely
embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
faiss_index_path = "faiss_index"

if os.path.exists(faiss_index_path):
    vector_store = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
else:
    vector_store = FAISS.from_texts(project_docs, embeddings)
    vector_store.save_local(faiss_index_path)

# Set API usage limit per session
MAX_REQUESTS_PER_USER = 10

# Home route: Render the main HTML page
@app.route('/')
def home():
    session["request_count"] = 0  # Reset API count for each new session
    return render_template('index.html')
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/ask', methods=['POST'])
def ask():
    if "request_count" not in session:
        session["request_count"] = 0

    if session["request_count"] >= MAX_REQUESTS_PER_USER:
        return jsonify({'response': "⚠️ Sorry, to maintain fair use, a limit of 10 questions per session is applied. Please wait before making more requests."})

    user_message = request.json.get('question', '')

    # Define a controlled-length response prompt
    custom_template = """
You are a knowledgeable AI assistant specialized in Akshat Gupta's projects. 
Provide a **detailed but concise** response (150-200 words max).

Akshat is an AI enthusiast with expertise in machine learning, deep learning, and generative AI. 
He is currently pursuing a B.Tech in Computer Science & Engineering at Bennett University (CGPA: 8.64). 
He has contributed to multiple AI-driven projects and research papers.

### Projects:
- **My LoRA Model**: Fine-tuned image generation model using a Custom LoRA technique for personalized facial data.
- **Akshar**: Real-time translation chat app built with Flutter and AI-driven speech processing.
- **Eye Disease Detection**: CNN-based model for classifying retinal diseases from fundus images.
- **Medical ChatBot**: AI-powered assistant using retrieval-augmented generation for medical guidance.
- **FacePay**: Facial recognition payment system for secure, contactless transactions.

### Research:
- **Multi-Modal Meta Learner (M3L)**: A scalable image processing framework.
- **Potato Disease Detection**: Deep learning + Grasshopper Optimization Algorithm.
- **Brain Tumor Detection**: AI-powered medical image classification.

if someone ask out of context question then answer will be:
Sorry, I can only provide information related to Akshat Gupta's projects.


and if someone greets then answer will be:
Hello! How can I assist you today? 
### Answer the following:
**{query}**
    """
    prompt = PromptTemplate(input_variables=["query"], template=custom_template)

    # Retrieve documents from FAISS
    retrieved_docs = vector_store.similarity_search(user_message)
    context = "\n".join([doc.page_content for doc in retrieved_docs]) if retrieved_docs else "No relevant context found."

    # Create LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate AI response
    response = llm_chain.invoke({"query": user_message})

    # Update session request count
    session["request_count"] += 1

    return jsonify({'response': response["text"]})

if __name__ == '__main__':
    app.run(debug=True)
