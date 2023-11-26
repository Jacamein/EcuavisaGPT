import openai
import requests
import os
from flask import Flask, request, jsonify

# Cargar las variables de entorno
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
google_cse_id = os.getenv('GOOGLE_CSE_ID')

# Verificar que las claves de API están disponibles
if not all([openai_api_key, google_api_key, google_cse_id]):
    raise ValueError("API keys are not set in the environment variables.")

app = Flask(__name__)

@app.route('/generate_search_query', methods=['POST'])
def generate_search_query():
    data = request.json
    prompt = data['prompt']
    
    openai.api_key = openai_api_key
    
    response = openai.Completion.create(
        model="gpt-4-1106-preview",  # Asegúrate de usar el modelo más reciente de GPT disponible.
        prompt=prompt,  # Prompt que le pides al modelo que complete
        max_tokens=60  # Ajusta según sea necesario
    )
    
    search_query = response.choices[0].text.strip()
    return jsonify(search_query)

@app.route('/perform_web_search', methods=['GET'])
def perform_web_search():
    query = request.args.get('query')
    
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': google_api_key,
        'cx': google_cse_id,
        'num': 10
    }
    
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify(f"Error: {response.status_code}, {response.text}")

if __name__ == "__main__":
    app.run()

