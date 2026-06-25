import os
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for, abort

import hashlib


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-betdown-ctf")

DB_PATH = os.environ.get("DB_PATH", os.path.join(app.root_path, "betdown.sqlite3"))

LOCKDOWN_FILE = "/var/lib/betdown/lockdown"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def emergency_lockdown():
    """
    Quando o script root.sh é executado, ele cria um marcador em
    /var/lib/betdown/lockdown. A aplicação entra em modo de contingência
    e redireciona todos os endpoints para a página final.
    """
    if os.path.exists(LOCKDOWN_FILE):
        if request.endpoint != "final_flag":
            return redirect(url_for("final_flag"))

def init_db():
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                tipo TEXT NOT NULL,
                saldo TEXT,
                historico TEXT,
                observacao TEXT
            )
            """
        )
        count = db.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
        if count == 0:
            db.executemany(
                """
                INSERT INTO users (username, password_hash, tipo, saldo, historico, observacao)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        "fabio",
                        hashlib.md5("bitch1".encode()).hexdigest(),
                        "user",
                        "R$ 250,00",
                        "Apostas recentes em futebol",
                        "sem observações",
                    ),
                    (
                        "maria",
                        hashlib.md5("fatima".encode()).hexdigest(),
                        "user",
                        "R$ 120,00",
                        "Apostas recentes em basquete",
                        "sem observações",
                    ),
                    (
                        "matric",
                        hashlib.md5("miamor".encode()).hexdigest(),
                        "user",
                        "R$ 300,00",
                        "Apostas recentes em tênis",
                        "sem observações",
                    ),
                    (
                        "homeby",
                        hashlib.md5("lover".encode()).hexdigest(),
                        "user",
                        "R$ 80,00",
                        "Apostas recentes em vôlei",
                        "sem observações",
                    ),
                    (
                        "lulab",
                        hashlib.md5("chris1".encode()).hexdigest(),
                        "user",
                        "R$ 500,00",
                        "Apostas recentes em corrida",
                        "sem observações",
                    ),
                    (
                        "fabio",
                        hashlib.md5("password".encode()).hexdigest(),
                        "user",
                        "R$ 45,00",
                        "Apostas recentes em futebol",
                        "sem observações",
                    ),
                    (
                        "mateus",
                        hashlib.md5("252525".encode()).hexdigest(),
                        "user",
                        "R$ 700,00",
                        "Apostas recentes em e-sports",
                        "sem observações",
                    ),
                    (
                        "atenas",
                        hashlib.md5("lalala".encode()).hexdigest(),
                        "admin",
                        "R$ 99999,00",
                        "Acesso interno",
                        "admin principal",
                    ),
                    (
                        "matruza",
                        hashlib.md5("00000000000bloodyboy".encode()).hexdigest(),
                        "admin",
                        "R$ 99999,00",
                        "Acesso interno",
                        "admin secundário",
                    ),
                    (
                        "junior.admin",
                        hashlib.md5("trocarsenhadepois123".encode()).hexdigest(),
                        "admin",
                        "R$ 99999,00",
                        "Acesso interno",
                        "flag{api_column_tampering}",
                    ),
                ],
            )
        db.commit()


@app.route("/image/<path:filename>", methods=["GET"])
def image_asset(filename):
    return send_from_directory(os.path.join(app.root_path, "image"), filename)


@app.route("/", methods=["GET"])
def index():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        password_hash = hashlib.md5(password.encode()).hexdigest()

        with get_db() as db:
            user = db.execute(
                """
                SELECT id, username, tipo
                FROM users
                WHERE username = ? AND password_hash = ? AND tipo = 'admin'
                """,
                (username, password_hash),
            ).fetchone()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["tipo"] = user["tipo"]
            return redirect(url_for("dashboard"))

        error = "Usuário ou senha inválidos."

    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    with get_db() as db:
        user = db.execute(
            "SELECT username, tipo, saldo, historico FROM users WHERE id = ?",
            (session["user_id"],),
        ).fetchone()
        users = []
        if user and user["tipo"] == "admin":
            users = db.execute(
                "SELECT id, username, tipo, saldo, historico FROM users ORDER BY id"
            ).fetchall()

    if user is None:
        session.clear()
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        user_id=session["user_id"],
        username=user["username"],
        tipo=user["tipo"],
        saldo=user["saldo"],
        historico=user["historico"],
        users=users,
    )


@app.route("/api/dashboard", methods=["POST"])
def api_dashboard():
    if "user_id" not in session:
        return jsonify({"error": "auth required"}), 401

    data = request.get_json(silent=True) or {}
    requested_columns = data.get("columns", ["id", "username", "tipo", "saldo", "historico"])

    # CTF INTENCIONAL: API tampering. O backend confia nas colunas enviadas pelo cliente.
    columns = ",".join(requested_columns)
    query = f"SELECT {columns} FROM users ORDER BY id"

    with get_db() as db:
        rows = db.execute(query).fetchall()

    return jsonify({
        "columns": requested_columns,
        "rows": [dict(row) for row in rows],
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/notascomentarios78")
def arquivos():
    diretorio = os.path.join(app.root_path, "arquivos")

    arquivos = [
        nome
        for nome in os.listdir(diretorio)
        if os.path.isfile(os.path.join(diretorio, nome))
    ]

    html = "<h1>Arquivos</h1><ul>"
    for arquivo in arquivos:
        html += f'<li><a href="/notascomentarios78/{arquivo}">{arquivo}</a></li>'
    html += "</ul>"

    return html
@app.route("/notascomentarios78/<path:filename>")
def arquivo(filename):
    diretorio = os.path.join(app.root_path, "arquivos")
    return send_from_directory(diretorio, filename)


@app.route("/final", methods=["GET"])
def final_flag():
    if not os.path.exists(LOCKDOWN_FILE):
        abort(404)

    return render_template("final.html")


init_db()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
