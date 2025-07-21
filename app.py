from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("title")
    if title:
        tasks = load_tasks()
        tasks.append({"title": title})
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for("index"))

@app.route('/edit/<int:index>', methods=["GET", "POST"])
def edit(index):
    tasks = load_tasks()
    if request.method == "POST":
        new_title = request.form.get("title")
        if new_title:
            tasks[index]["title"] = new_title
            save_tasks(tasks)
            return redirect(url_for("index"))
    return render_template("edit.html", index=index, task=tasks[index])

if __name__ == '__main__':
    app.run(debug=True)
