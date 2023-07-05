from flask import Flask, render_template, request
import openai
import os 
from dotenv import load_dotenv
load_dotenv()
import regex as re

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize conversation list
conversation = [{'role':'system', 'content':"""
You are a Sentiment analyzer 
Analyse the text and reply whether content is "positive" or "negative" or "mixed"
"""}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    # Get user input from the form
    user_input = request.form['user_input']
    
    # Append user input to conversation
    conversation.append({'role':'user', 'content':f"{user_input}"})
    
    # Get response from OpenAI API
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        temperature=0.0,
        messages = conversation,
    )
    
    # Append OpenAI's response to conversation
    assistant_response = response.choices[0].message["content"]
    

    conversation.append({'role':'assistant', 'content':f"{assistant_response}"})
    
    return {'response': assistant_response}

if __name__ == '__main__':
    app.run(debug=True)

