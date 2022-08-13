from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

# Create Flask Object
app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
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


# HTTP GET - Read Record
@app.route('/search')
def search_for_cafes():
    query_location = request.args.get("loc")

    cafe = Cafe.query.filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


# HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def add_cafe():
    print('In add_cafe')
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get('map_url'),
        img_url=request.form.get('img_url'),
        location=request.form.get('location'),
        has_sockets=bool(request.form.get('has_sockets')),
        has_toilet=bool(request.form.get('has_toilet')),
        has_wifi=bool(request.form.get('has_wifi')),
        can_take_calls=bool(request.form.get('can_take_calls')),
        seats=request.form.get('seats'),
        coffee_price=request.form.get('coffee_price')
    )

    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


# HTTP PUT/PATCH - Update Record
@app.route('/update-price/<int:cafe_id>')
def update_record(cafe_id):
    cafe = Cafe.query.filter_by(id=cafe_id).first()
    if cafe:
        cafe.coffee_price = request.args.get('new_price')
        db.session.commit()
        return jsonify(response={'success': 'Successfully updated the price.'})
    else:
        return jsonify(error={'Not Found': 'Sorry a cafe with that id was not found in the database.'})


if __name__ == '__main__':
    app.run(debug=True)
