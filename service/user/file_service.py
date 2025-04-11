import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]

def save_avatar(file_storage):
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed(file_storage.filename):
        raise ValueError("Extensão de imagem não permitida")
    ext = file_storage.filename.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], unique_name)
    os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
    file_storage.save(path)
    return unique_name

def delete_avatar(filename: str):
    if not filename:
        return
    path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    if os.path.exists(path):
        os.remove(path)
