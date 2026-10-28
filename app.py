from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory database representing library books
BOOKS_DATABASE = [
    {"id": 1, "title": "The Phoenix Project", "author": "Gene Kim", "available": True},
    {"id": 2, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "available": True}
]

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the University Library Book Management System API!",
        "version": "1.0.0"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": BOOKS_DATABASE}), 200

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json() or {}
    if not data.get("title") or not data.get("author"):
        return jsonify({"error": "Missing title or author"}), 400
    
    new_book = {
        "id": len(BOOKS_DATABASE) + 1,
        "title": data["title"],
        "author": data["author"],
        "available": True
    }
    BOOKS_DATABASE.append(new_book)
    return jsonify({"message": "Book added successfully", "book": new_book}), 201

@app.route('/books/issue', methods=['POST'])
def issue_book():
    data = request.get_json() or {}
    book_id = data.get("id")
    if not book_id:
        return jsonify({"error": "Missing book ID"}), 400
        
    for book in BOOKS_DATABASE:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                return jsonify({"message": f"Book '{book['title']}' has been successfully issued.", "book": book}), 200
            else:
                return jsonify({"error": "Book is already issued and currently unavailable."}), 400
                
    return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
