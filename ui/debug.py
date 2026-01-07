from flask import Blueprint, request

bp = Blueprint("debug", __name__, url_prefix="/debug")


@bp.route("/")
def index():
    env = request.environ
    # format the env as a table
    rows = []
    for key, value in env.items():
        rows.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
    table = "<table>" + "\n".join(rows) + "</table>"
    html_data = f"""
    <html>
    <head><title>Debug Info</title></head>
    <body>
    <h1>Debug Information</h1>
    {table}
    </body>
    </html>
    """

    # return the response with the correct content type
    return html_data, 200, {"Content-Type": "text/html"}
