"""TaskFlow: a very small to-do list app. Main routes live here."""
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from auth import authenticate
from utils import login_required

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

# In-memory task storage: {username: [{"id": int, "title": str, "done": bool}]}
_tasks = {}
_next_task_id = 1


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        success, error = authenticate(username, password)
        if success:
            session["username"] = username
            return redirect(url_for("view_tasks"))
        flash(error)
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def view_tasks():
    username = session["username"]
    tasks = _tasks.get(username, [])
    return render_template("tasks.html", tasks=tasks, username=username)


@app.route("/tasks/add", methods=["POST"])
@login_required
def add_task():
    global _next_task_id
    username = session["username"]
    title = request.form.get("title", "").strip()
    if title:
        _tasks.setdefault(username, []).append({"id": _next_task_id, "title": title, "done": False})
        _next_task_id += 1
    return redirect(url_for("view_tasks"))


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
@login_required
def complete_task(task_id):
    username = session["username"]
    for task in _tasks.get(username, []):
        if task["id"] == task_id:
            task["done"] = True
            break
    return redirect(url_for("view_tasks"))


@app.route("/api/tasks/count")
@login_required
def task_count():
    username = session["username"]
    return jsonify({"count": len(_tasks.get(username, []))})


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
