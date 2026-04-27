import os
from flask import Flask, render_template, request, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Supabase configuration
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users", methods=["GET"])
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        response = supabase.table("users").insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<id>", methods=["GET"])
def get_user(id):
    try:
        response = supabase.table("users").select("*").eq("id", id).execute()
        if not response.data:
            return jsonify({"error": "User not found"}), 404
        return jsonify(response.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<id>", methods=["PUT"])
def update_user(id):
    try:
        data = request.json
        response = supabase.table("users").update(data).eq("id", id).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        response = supabase.table("users").delete().eq("id", id).execute()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ai", methods=["POST"])
def ai_query():
    try:
        user_question = request.json.get("question")
        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        # Fetch data from Supabase
        response = supabase.table("users").select("*").execute()
        users_data = response.data

        # Construct prompt
        context = json.dumps(users_data, indent=2)
        prompt = f"""
        You are an AI assistant for a CRUD application. 
        Use the following database records (JSON format) to answer the user's question.
        
        Database Records:
        {context}
        
        Rules:
        1. ONLY use the provided database records to answer.
        2. If the answer is not found in the data, return: "Data not available"
        3. Keep answers short, clear, and direct.
        4. You can count records, summarize data, find highest/lowest values, and detect patterns.
        
        User Question: {user_question}
        
        Answer:
        """

        # Call Ollama API
        ollama_url = "http://localhost:11434/api/generate"
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }

        ollama_response = requests.post(ollama_url, json=payload, timeout=120)
        
        if ollama_response.status_code == 200:
            ai_answer = ollama_response.json().get("response", "").strip()
            return jsonify({"answer": ai_answer}), 200
        else:
            print(f"Ollama error: {ollama_response.status_code} - {ollama_response.text}")
            return jsonify({"error": "Failed to get response from Ollama"}), 500

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Ollama is not running. Please start Ollama first."}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Ollama took too long to respond. Try a simpler question."}), 500
    except Exception as e:
        print(f"AI route error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
