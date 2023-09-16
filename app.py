from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Global variables for Cognitive Services
cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
cog_key = os.getenv('COG_SERVICE_KEY')

def get_language(text):
    credential = AzureKeyCredential(cog_key)
    client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)
    detected_language = client.detect_language(documents=[text])[0]
    return detected_language.primary_language.name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_text = request.form['user_text']
        if user_text.lower() != 'quit':
            language = get_language(user_text)
            return render_template('result.html', language=language)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
