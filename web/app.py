"""
John Doe's Flask API.
"""

import config
import os
from flask import Flask, render_template, send_from_directory, abort

app = Flask(__name__)
DOCROOT = ""

@app.route("/<path:path>")
def serve_file(path):
    full_path = os.path.join(DOCROOT, path)
    if any(forbidden_value in path for forbidden_value in ("~", "..", "//")):
        abort(403)
    elif not path.endswith((".html", ".css")):
        abort(401)
    elif not os.path.isfile(full_path):
        abort(404)
    return send_from_directory(DOCROOT, path)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template("403.html"), 403

def configure_options():
    global DOCROOT
    options = config.configuration()
    DOCROOT = options.DOCROOT

if __name__ == "__main__":
    configure_options()
    app.run(debug=True, host='0.0.0.0')
