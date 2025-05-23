
from flask import Flask, request, jsonify, send_file
import csv
import os

app = Flask(__name__)

# Store files in /tmp which is writable in Render and safe for temporary file storage
STORAGE_DIR = "/tmp"
INFO_FILE = os.path.join(STORAGE_DIR, "info_signups.csv")
PARTICIPANT_FILE = os.path.join(STORAGE_DIR, "participant_signups.csv")

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    form_type = request.form.get('form_type')  # "info" or "participant"

    # Choose correct file path
    if form_type == "participant":
        filename = PARTICIPANT_FILE
    else:
        filename = INFO_FILE

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Message'])  # header
        writer.writerow([name, email, message])            # data row

    return jsonify({'status': 'success'}), 200

@app.route('/download/<filename>')
def download_file(filename):
    if filename == 'info_signups.csv':
        path = INFO_FILE
    elif filename == 'participant_signups.csv':
        path = PARTICIPANT_FILE
    else:
        return jsonify({'error': 'File not found'}), 404

    if not os.path.isfile(path):
        return jsonify({'error': 'File not found on server'}), 404

    return send_file(path, as_attachment=True)

@app.route('/')
def index():
    return 'Form backend is running.'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

