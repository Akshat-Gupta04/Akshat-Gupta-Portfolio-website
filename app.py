
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allows your frontend to access the backend from different origins


# Initialize the LLM model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai.api_key)

# Home route to render the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Render index.html from the templates folder

# Route for LLM interaction (handling user input and getting the response)
@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['question']
    
    # Create a prompt using LangChain's PromptTemplate
    prompt = PromptTemplate(input_variables=["question"], template="You are an assistant. Answer: {question}")
    
    # Create an LLMChain with the prompt and model
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Get the response from the LLM
    response = llm_chain.run(question=user_message)
    
    # Return the response in JSON format
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)