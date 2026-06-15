import os
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-betdown-ctf")

DB_PATH = os.environ.get("DB_PATH", os.path.join(app.root_path, "betdown.sqlite3"))


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


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
                        "player01",
                        "123456",
                        "user",
                        "R$ 250,00",
                        "Apostas recentes em futebol",
                        "sem observações",
                    ),
                    (
                        "junior.admin",
                        "admin123",
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

        with get_db() as db:
            user = db.execute(
                """
                SELECT id, username, tipo
                FROM users
                WHERE username = ? AND password_hash = ? AND tipo = 'admin'
                """,
                (username, password),
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


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
