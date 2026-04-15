import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient, exceptions
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cosmos DB Setup
endpoint = os.environ.get("COSMOS_URI")
key = os.environ.get("COSMOS_KEY")
client = CosmosClient(endpoint, key)
database = client.get_database_client(os.environ.get("COSMOS_DATABASE"))
container = database.get_container_client(os.environ.get("COSMOS_CONTAINER"))

@app.route('/')
def home():
    return "<h1>Blog API is Live</h1><p>Use /posts to see data.</p>"

@app.route('/posts', methods=['GET'])
def get_posts():
    # Fetch all posts (Note: In production, use pagination for large datasets)
    query = "SELECT * FROM c"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return jsonify(items), 200

@app.route('/posts/<id>', methods=['GET'])
def get_post(id):
    # Since we use /author as partition key, we must query rather than direct read 
    # unless we also have the author name. Querying is safer for a simple ID lookup.
    query = f"SELECT * FROM c WHERE c.id = '{id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not items:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(items[0]), 200

@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    if not all(k in data for k in ("title", "content", "author")):
        return jsonify({"error": "Missing fields"}), 400

    new_post = {
        "id": str(uuid.uuid4()),
        "title": data['title'],
        "content": data['content'],
        "author": data['author'],
        "timestamp": datetime.utcnow().isoformat()
    }
    
    container.create_item(body=new_post)
    return jsonify(new_post), 201

@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    # Important: In Cosmos DB, to delete you usually need the Partition Key (author)
    # We'll find the item first to get the author, then delete.
    query = f"SELECT c.id, c.author FROM c WHERE c.id = '{id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    
    if not items:
        return jsonify({"error": "Post not found"}), 404
        
    container.delete_item(item=items[0]['id'], partition_key=items[0]['author'])
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)