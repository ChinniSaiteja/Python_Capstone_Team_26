from flask import Flask, render_template

from Hometaskassignment3.database import get_waste_items
from Hometaskassignment3.exceptions import DatabaseError

app = Flask(__name__)


@app.route("/")
def home():
    items = get_waste_items()
    return render_template("index.html", items=items)


@app.errorhandler(DatabaseError)
def handle_database_error(error):
    return render_template(
        "error.html",
        message="The database service is currently unavailable."
    ), 500


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    return render_template(
        "error.html",
        message="An unexpected error occurred."
    ), 500


if __name__ == "__main__":
    app.run(debug=True)