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

    def to_dict(self):
        # dictionary = {}
        # for column in self.__table__.columns:
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


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
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all')
def get_all_cafes():
    cafe_object_list = Cafe.query.all()
    details_of_cafes_list = [cafe.to_dict() for cafe in cafe_object_list]
    print(details_of_cafes_list)
    return jsonify(cafe=details_of_cafes_list)


@app.route('/search')
def search_for_cafe():
    pass

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
