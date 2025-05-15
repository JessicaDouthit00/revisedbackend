from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)  # Allow requests from other domains (e.g., your GitHub Pages site)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    form_type = request.form.get('form_type')  # "info" or "participant"

    # Choose the appropriate CSV file
    if form_type == "participant":
        filename = "participant_signups.csv"
    else:
        filename = "info_signups.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Message'])
        writer.writerow([name, email, message])

    return jsonify({'status': 'success'}), 200

@app.route('/')
def index():
    return 'Form backend is running.'

if __name__ == '__main__':
    # Use the PORT provided by the hosting platform (like Render)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
