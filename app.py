"""
Mini project to understand backend systems:
client → HTTP → Flask → API → data → response
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# temporary storage (acts like a fake DB)
students = []

# health check / home
@app.route("/")
def home():
    return "Student server is running"

# GET → read data
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(students)

# POST → add data
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    students.append(data)
    return jsonify({
        "message": "Student added",
        "data": data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

