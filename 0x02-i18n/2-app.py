#!/usr/bin/env python3
"""Basic Babel Setup"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """Configuration for Babel integration."""

    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)

app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Get the locale from request or default to config"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/")
def index():
    """Render the index template with translated text."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
