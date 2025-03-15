from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)
app.secret_key = "1234qazx"  # Needed for session tracking

# Initialize the LLM model (GPT-3.5-turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

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

    # Define a controlled-length response prompt with project details
    custom_template = """
You are a knowledgeable AI assistant specialized in Akshat Gupta's projects. Provide a detailed but concise response (50-120 words max).

Akshat Gupta is an AI enthusiast with expertise in machine learning, deep learning, and generative AI. Currently pursuing a B.Tech in Computer Science & Engineering at Bennett University (CGPA: 8.64), he has developed several innovative projects and contributed to research papers.

### Projects:
- **My LoRA Model**: A personalized, fine-tuned LoRA model that generates realistic images with reduced computational costs.
- **Akshar**: A real-time chat app built with Flutter for seamless multilingual text and audio translation.
- **Eye Disease Detection**: A deep learning model leveraging CNNs to classify retinal diseases from fundus images.
- **Medical ChatBot**: An AI-powered medical assistant using retrieval-augmented generation to deliver context-aware advice.
- **FacePay**: A facial recognition payment system offering secure, contactless UPI transactions.
- **Teacher-Student Distillation on IMDB**: A robust sentiment analysis pipeline that distills a large teacher model into a compact student model.
- **Vision Transformer for MNIST**: A Vision Transformer built from scratch for MNIST image classification.
- **Krishi Sanrakshan**: A deep learning model for detecting diseases in livestock and plants.
- **English-Hindi Translation**: A transformer model built from scratch to translate English text to Hindi, demonstrating core NLP and deep learning techniques.

If asked an out-of-context question, respond with:
"Sorry, I can only provide information related to Akshat Gupta and his projects."

If greeted, respond with:
"Hello! How can I assist you today?"

### Answer the following:
**{query}**
"""
    prompt = PromptTemplate(input_variables=["query"], template=custom_template)

    # Create LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Generate AI response
    response = llm_chain.invoke({"query": user_message})

    # Update session request count
    session["request_count"] += 1

    return jsonify({'response': response["text"]})

if __name__ == '__main__':
    app.run(debug=True)