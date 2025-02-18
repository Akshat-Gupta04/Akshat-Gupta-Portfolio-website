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
app.secret_key = "your_secret_key_here"  # Needed for session tracking

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
You are a knowledgeable AI assistant specialized in Akshat Gupta's projects. 
Provide a **detailed but concise** response (150-200 words max).

Akshat is an AI enthusiast with expertise in machine learning, deep learning, and generative AI. 
He is currently pursuing a B.Tech in Computer Science & Engineering at Bennett University (CGPA: 8.64). 
He has contributed to multiple AI-driven projects and research papers.

### Projects:
- **My LoRA Model**: Developed a highly realistic image generation model fine-tuned on personalized facial data using a Custom LoRA technique.
  This model enhances generative capabilities while reducing computational costs.
- **Akshar**: A real-time translation chat app built with Flutter that integrates AI-based speech processing for seamless multilingual communication.
- **Eye Disease Detection**: A deep learning model designed to classify retinal diseases from fundus images, leveraging convolutional neural networks for early diagnosis.
- **Medical ChatBot**: An AI-powered medical assistant using retrieval-augmented generation to deliver dynamic, context-aware medical advice.
- **FacePay**: An AI-powered facial recognition payment system designed as an alternative to QR codes for secure, contactless transactions.

### Research:
- **Multi-Modal Meta Learner (M3L)**: A scalable image processing framework.
- **Potato Disease Detection**: Deep learning + Grasshopper Optimization Algorithm.
- **Brain Tumor Detection**: AI-powered medical image classification.

If someone asks an out-of-context question, respond with:
"Sorry, I can only provide information related to Akshat Gupta's projects."

If someone greets, respond with:
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
