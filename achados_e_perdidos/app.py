from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "achados_perdidos.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "troque-esta-chave-em-producao"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL CHECK(kind IN ('perdido', 'encontrado')),
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                contact TEXT NOT NULL,
                image TEXT,
                status TEXT NOT NULL DEFAULT 'aberto'
                    CHECK(status IN ('aberto', 'resolvido')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    filtro = request.args.get("tipo", "todos")
    busca = request.args.get("q", "").strip()
    query = "SELECT * FROM items WHERE 1=1"
    params = []
    if filtro in ("perdido", "encontrado"):
        query += " AND kind = ?"
        params.append(filtro)
    if busca:
        query += " AND (name LIKE ? OR description LIKE ? OR location LIKE ?)"
        termo = f"%{busca}%"
        params.extend([termo, termo, termo])
    query += " ORDER BY status ASC, created_at DESC"
    with get_db() as conn:
        items = conn.execute(query, params).fetchall()
    return render_template("index.html", items=items, filtro=filtro, busca=busca)

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    kind = request.form.get("kind", "")
    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()
    location = request.form.get("location", "").strip()
    contact = request.form.get("contact", "").strip()
    image = request.files.get("image")
    if kind not in ("perdido", "encontrado") or not all([name, description, location, contact]):
        flash("Preencha todos os campos obrigatórios.", "erro")
        return redirect(url_for("index"))

    image_name = None
    if image and image.filename:
        if not allowed_file(image.filename):
            flash("Formato de imagem não permitido. Use PNG, JPG, JPEG, GIF ou WEBP.", "erro")
            return redirect(url_for("index"))
        # Nome gerado pelo banco evita depender do nome original enviado.
        ext = image.filename.rsplit(".", 1)[1].lower()
        import uuid
        image_name = f"{uuid.uuid4().hex}.{ext}"
        upload_dir = BASE_DIR / "static" / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        image.save(upload_dir / image_name)

    with get_db() as conn:
        conn.execute(
            "INSERT INTO items (kind, name, description, location, contact, image) VALUES (?, ?, ?, ?, ?, ?)",
            (kind, name, description, location, contact, image_name)
        )
    flash("Item cadastrado com sucesso!", "sucesso")
    return redirect(url_for("index"))

@app.route("/resolver/<int:item_id>", methods=["POST"])
def resolver(item_id):
    with get_db() as conn:
        cursor = conn.execute("UPDATE items SET status = 'resolvido' WHERE id = ?", (item_id,))
    if cursor.rowcount:
        flash("Item marcado como devolvido/resolvido.", "sucesso")
    else:
        flash("Item não encontrado.", "erro")
    return redirect(url_for("index"))

@app.route("/reabrir/<int:item_id>", methods=["POST"])
def reabrir(item_id):
    with get_db() as conn:
        conn.execute("UPDATE items SET status = 'aberto' WHERE id = ?", (item_id,))
    flash("Item reaberto.", "sucesso")
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
