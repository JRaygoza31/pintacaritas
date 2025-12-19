from flask import Blueprint, render_template_string, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from models import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Usuario.query.filter_by(
            username=request.form["username"]
        ).first()

        if user and check_password_hash(user.password, request.form["password"]):
            login_user(user)

            # 🔑 AQUÍ ESTÁ LA MAGIA
            next_page = request.args.get("next")
            return redirect(next_page or url_for("home"))

        flash("Usuario o contraseña incorrectos", "error")

    return render_template_string("""
    <html>
    <head>
        <title>Login</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100 flex items-center justify-center h-screen">
        <form method="POST" class="bg-white p-8 rounded shadow w-96">
            <h1 class="text-2xl font-bold mb-6 text-center">🔐 Acceso</h1>

            <input name="username" placeholder="Usuario"
                   class="w-full mb-3 p-2 border rounded">

            <input name="password" type="password" placeholder="Contraseña"
                   class="w-full mb-4 p-2 border rounded">

            <button class="w-full bg-blue-600 text-white py-2 rounded">
                Entrar
            </button>
        </form>
    </body>
    </html>
    """)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
