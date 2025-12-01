from flask import request


def register():
    if request.method == "GET":
        return "form"
    else:
        pid = request.form.get("pid")
        return f"registered {pid}"
