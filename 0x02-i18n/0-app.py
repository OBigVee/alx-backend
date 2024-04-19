from flask import Flask
from flask import render_template
"""simple flask app"""

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("0-index.html")


if __name__ == "__main__":
    app.run(debug=True)
