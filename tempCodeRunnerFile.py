from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
import os
import csv
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = 'images'  # Updated folder name
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            print(f'Saving file to {file_path}')
            file.save(file_path)
            
            # Run the detect.py script
            result_csv = os.path.join(app.config['UPLOAD_FOLDER'], 'results', 'predictions.csv')
            subprocess.run(['python', 'detect.py', '--source', file_path, '--save-txt', '--project', app.config['UPLOAD_FOLDER'], '--name', 'results'], check=True)
            
            # Load results from CSV
            results = []
            if os.path.exists(result_csv):
                with open(result_csv, newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        results.append(row)
                    
            return render_template('results.html', filename=filename, results=results)
    
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
