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
            'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6IjJvajR4MnR5MmIiLCJ0b2tlbiI6eyJpdiI6ImQ2YWI2NTMyNzQ0ZDI0NTc3MTRmYjQ5YmI3NzViODUxIiwiY29udGVudCI6IjgxNjYyYjNhMmQyZDQ5NDhmOTdhNTQzOGYxMTk1N2Y3MGI0YjhmNmMyZTVjZDQwZTBlOGQ5MTc2NGYzMDAxNzI0NzVjOThmOGNiODM0NDU2NzI1OWYxNmNjOTVjODVhYWVmZjUyZjAyM2Q2MTZkN2UwMWQxYjRlZWZlZmYzYmE0NjAyYzc1MjNlNDI0YTAwNzAyNTNmZTY3ZGQ3NTQwYzA5YTc1Y2FkNmJiZDI5YTM5MTAxYzYyMWNkN2Y0YTk4ZmFhZDkyYzhhNDVmOWRjMWUxZGNjYmM0MGUwMDZlYWNhOGFhOGZjNjFhODUxN2E4NzdmODdmZmVmMmU5OTkxNGE5NzUyNzRjYzUxMGM1Nzc3ZDQ0ZjZhYzJkY2M4NTFlNmYzNmJiNjk4OWJjMGNhNDJmM2RlZDdlNjgxMTgwNjQ1NzkwNjczYmNhYWRjNWUxOTAyNGIwMDJkMDc5NDZiYmUxOTQyY2E2MGQ4MGY2MDVhM2U5NjBjNzYwMmQxYjY3YjM3OWMwYjQzMzhiZTEyNjI5YmFiZWNhNGVmMDMyNWVlOWUyMjNjYzAyNjJiZDU0NDM3ZTM3N2YzYjc0YTM2NTk4ODkwYzc3MzE1YWE0ZDEwZWIwOGVhNmJjYzQ3MmI3OGIwNjA3ODE1NDc1Njk2OTVhY2QwYTQxNDRlMGM2NTIyMGVlOTBkY2IzNzA0MTVlN2YxMTUyZDA2ZTRhY2Q0YmE3ODA4NjFhOTU3ZWExY2NlNzYwZDdhNzc2NzQxNWEyOWM2MjIxOTc5ZTE5NzU4NjFiNGI5ZTdhNjhiOGI5YmQxYmI0NmU1YmI0MmI3ZTMzY2ZlNjhkNWUwNTAwNmUzYTBiZWQ0NWYxZTYwZmVmNzgwMzYxMDY4In0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiJkNmFiNjUzMjc0NGQyNDU3NzE0ZmI0OWJiNzc1Yjg1MSIsImNvbnRlbnQiOiJiMjUzMzIyYTI3MjIwMDU5ODY2MTU4NDhmYzM0NGRmZTIxNGRiZTViM2YwMmU0NTIyNGEzYTIwZDUzNmQzMjQxN2I3MmI4YWQ4NmQyNWI3YTU0NzhlMDUyIn0sImp0aSI6ImE2OTQyY2E0LTM0MTYtNDAzYS04YTVjLTRkZGExYmRhMTRlNSIsImlhdCI6MTY2ODM1Njk0OSwiZXhwIjoxNjY4MzYwNTQ5fQ.rAUnQ_UAJthavlguBY5gfj3kXrk7kV6tKM2VEXnfcVs'
            }
    output = requests.request("GET", url2, headers=headers).json()

    return render_template('results.html', info=output)
