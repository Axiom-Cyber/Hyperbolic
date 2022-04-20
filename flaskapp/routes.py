from flaskapp import app
from flaskapp.forms import CTFDLoginForm, EntryForm
from flask import url_for, render_template, request

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    form = EntryForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('entry.html', title='Entry', form=form)

@app.route('/ctfd-scan', methods=['GET', 'POST'])
def ctfd():
    form = CTFDLoginForm()
    if form.validate_on_submit():
        print(form.data)
    return render_template('ctfd.html', title='CTFd Scan', form=form)