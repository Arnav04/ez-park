import os
import json
from flask import Flask, jsonify, request,render_template,session,redirect,url_for
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, RadioField,
                    IntegerField, SelectField, SubmitField)
from wtforms.validators import DataRequired
import gunicorn
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, support_credentials=True)

db = SQLAlchemy(app)



# form

class InfoForm(FlaskForm):
    loc = StringField(("Where do you want to find parking near? (Address) "), validators=[DataRequired()])
    rad = IntegerField(("Within what radius (meters) should we find parking? "), validators = [DataRequired()])
    time = IntegerField(("How long of a parking period are you looking for? "), validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*')
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['loc'] = form.loc.data
        session['rad'] = form.rad.data
        session['time'] = form.time.data
        return redirect(url_for('results'))
    return render_template('index.html', form=form)

@app.route('/results', methods=['GET', 'POST'])
@cross_origin(origin='*')
def results():
    url = "https://nominatim.openstreetmap.org/search?format=json&q=" + str(session['loc'])
    coords = requests.request("GET", url).json()

    x = coords[0]

    mod_cord = x['lat'] + "%7C" + x['lon']
    print(mod_cord)
    print(mod_cord)
    url2 = "https://api.iq.inrix.com/lots/v3?point=" + str(mod_cord) + "&radius=" + str(session['rad']) + "&limit=10&duration=" + str(session['time'])
    headers = {
    'Content-Type': 'application/json',
    'Authorization':
            'Bearer [bearer token]'
    output = requests.request("GET", url2, headers=headers).json()

    return render_template('results.html', info=output)
