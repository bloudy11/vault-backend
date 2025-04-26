from flask import Flask, request, jsonify
from flask_cors import CORS
from cryptography.fernet import Fernet
import base64
import hashlib
import os

app = Flask(__name__)
CORS(app)

# Простая "псевдо-база" в памяти
database = {
    "notes": [],
    "passwords": [],
    "reflections": []
}

# Функция генерации ключа шифрования
def derive_key(master_password: str, salt: str = "vault_salt") -> bytes:
    return base64.urlsafe_b64encode(hashlib.sha256((master_password + salt).encode()).digest())

# Функция для шифрования текста
def encrypt(text: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

# Функция для расшифровки текста
def decrypt(token: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

# --- ROUTE для сохранения данных ---
@app.route('/api/save', methods=['POST'])
def save_item():
    data = request.json
    item_type = data.get("type")  # 'notes', 'passwords', 'reflections'
    encrypted_data = data.get("encrypted_data")

    if item_type not in database:
        return jsonify({"status": "error", "message": "Invalid data type."}), 400

    item = {
        "id": len(database[item_type]) + 1,  # уникальный ID
        "data": encrypted_data
    }
    database[item_type].append(item)
    return jsonify({"status": "success", "item": item}), 201

# --- ROUTE для получения всех данных ---
@app.route('/api/get', methods=['GET'])
def get_items():
    item_type = request.args.get("type")
    if item_type not in database:
        return jsonify({"status": "error", "message": "Invalid data type."}), 400

    return jsonify({
        "status": "success",
        "data": database[item_type]
    }), 200

# --- ROUTE для удаления записи ---
@app.route('/api/delete', methods=['POST'])
def delete_item():
    data = request.json
    item_type = data.get("type")
    item_id = data.get("id")

    if item_type not in database:
        return jsonify({"status": "error", "message": "Invalid data type."}), 400

    before = len(database[item_type])
    database[item_type] = [item for item in database[item_type] if item["id"] != item_id]

    if len(database[item_type]) == before:
        return jsonify({"status": "error", "message": "Item not found."}), 404

    return jsonify({"status": "success"}), 200

# --- Тестовый маршрут (например для твоего App.js) ---
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Vault backend is running!"})



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
#if __name__ == '__main__':
    #app.run(port=5001, debug=True)

