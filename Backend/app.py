from flask import Flask
from flask_cors import CORS
from models import init_db  #from models.py

app = Flask(__name__)
CORS(app)

# initialize database + create tables
init_db(app)


@app.route("/api/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
