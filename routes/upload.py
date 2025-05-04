# routes/upload.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
import os

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file and uploaded_file.filename != '':
            save_path = os.path.join('uploads', uploaded_file.filename)
            os.makedirs('uploads', exist_ok=True)
            uploaded_file.save(save_path)
            flash(f"✅ File '{uploaded_file.filename}' uploaded successfully.", 'success')
            # You can send file to ChatGPT next here
            return redirect(url_for('upload.upload'))
        else:
            flash('⚠️ No file selected.', 'error')

    return render_template('main/upload.html', active_page='upload')

