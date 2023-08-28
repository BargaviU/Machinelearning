import os
from flask import Flask, render_template, request, flash, redirect, url_for
from transformers import BartTokenizer, BartForConditionalGeneration
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

app = Flask(__name__)
app.config.from_object('config')
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(pdf_path)
            summary = summarize_pdf(pdf_path)
            os.remove(pdf_path)
        else:
            flash('Invalid file format. Only PDF files are allowed.')
            return redirect(request.url)
    return render_template('index.html', summary=summary)


def summarize_pdf(pdf_path):
    try:
        # Open the PDF using the appropriate encoding
        with open(pdf_path, 'rb') as pdf_file:
            # Read PDF using PdfReader
            pdf_reader = PdfReader(pdf_path)
            pdf_text = ''
            for page_num in range(len(pdf_reader.pages)):
                pdf_text += pdf_reader.pages[page_num].extract_text()

        # Summarize the PDF text using the BART model
        inputs = tokenizer.encode("summarize: " + pdf_text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = model.generate(inputs, max_length=400, min_length=100, length_penalty=2.0, num_beams=4,
                                     early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return summary
    except UnicodeDecodeError:
        # Handle the UnicodeDecodeError
        error_message = "Error: Unable to decode the PDF content."
        return error_message
    except Exception as e:
        return f"An error occurred: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)
