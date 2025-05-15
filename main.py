from flask import Flask, request, jsonify, send_file
import csv
import os

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    form_type = request.form.get('form_type')  # "info" or "participant"

    # Choose CSV file
    if form_type == "participant":
        filename = "participant_signups.csv"
    else:
        filename = "info_signups.csv"

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(['Name', 'Email', 'Message'])  # header
        writer.writerow([name, email, message])            # data row

    return jsonify({'status': 'success'}), 200

@app.route('/download/<filename>')
def download_file(filename):
    # Only allow valid CSV files to be downloaded
    if filename in ['info_signups.csv', 'participant_signups.csv']:
        return send_file(filename, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/')
def index():
    return 'Form backend is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


if __name__ == '__main__':
    # Use the PORT provided by the hosting platform (like Render)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
