from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv
import requests
import os

app = Flask(__name__)
load_dotenv('.env')
# Environment variables for security
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTHORIZATION_URL = os.getenv('AUTHORIZATION_URL')
TOKEN_URL = os.getenv('TOKEN_URL')
REDIRECT_URI = os.getenv('REDIRECT_URI')

@app.route('/')
def home():
    return 'Welcome to the OAuth example for Power BI'

@app.route('/login')
def login():
    # Redirect user to the OAuth provider's authorization page
    return redirect(f'{AUTHORIZATION_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}')

@app.route('/callback')
def callback():
    # Get the authorization code from the callback
    auth_code = request.args.get('code')

    # Exchange the authorization code for an access token
    # token_response = requests.post(TOKEN_URL, data={
    #     'grant_type': 'authorization_code',
    #     'code': auth_code,
    #     'redirect_uri': REDIRECT_URI,
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET
    # })

    # token_json = token_response.json()
    # access_token = token_json.get('access_token')
    # refresh_token = token_json.get('refresh_token')

    # Store the tokens securely (e.g., in a database)
    # For demonstration, we'll just return them
    return auth_code
# jsonify({
#         'access_token': access_token,
#         'refresh_token': refresh_token
#     })

@app.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.form['refresh_token']
    token_response = requests.post(TOKEN_URL, data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    new_refresh_token = token_json.get('refresh_token')

    # Store the new tokens securely (e.g., in a database)
    # For demonstration, we'll just return them
    return jsonify({
        'access_token': access_token,
        'refresh_token': new_refresh_token
    })

if __name__ == '__main__':
    app.run(debug=True)
