from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random


app = Flask(__name__)


##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")
    

@app.route('/random')
def get_random_cafe():
    # cafe_list = Cafe.query.all()
    # rand_cafe = random.choice(cafe_list)

    # A faster way to get a random cafe especially when the database is large:
    row_count = Cafe.query.count()
    random_offset = random.randint(0, row_count - 1)
    random_cafe = Cafe.query.offset(random_offset).first()
    print(random_cafe.id)
    return jsonify(cafe={"id": random_cafe.id,
                         "can_take_calls": random_cafe.can_take_calls,
                         "coffee_price": random_cafe.coffee_price,
                         "has_sockets": random_cafe.has_sockets,
                         "has_toilet": random_cafe.has_toilet,
                         "has_wifi": random_cafe.has_wifi,
                         "id": random_cafe.id,
                         "img_url": random_cafe.img_url,
                         "location": random_cafe.location,
                         "map_url": random_cafe.map_url,
                         "name": random_cafe.name,
                         "seats": random_cafe.seats
    })




## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
