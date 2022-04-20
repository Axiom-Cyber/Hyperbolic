from flaskapp import app
from flaskapp.forms import CTFDLoginForm, EntryForm
from flask import url_for, render_template, request
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print(form.data)
    return render_template('entry.html', title='Entry', form=form)

@app.route('/ctfd-scan', methods=['GET', 'POST'])
def ctfd():
    form = CTFDLoginForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('ctfd.html', title='CTFd Scan', form=form)