from flaskapp import app
from flask import url_for, render_template

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html', title='Home')