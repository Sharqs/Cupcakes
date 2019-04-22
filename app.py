from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)


@app.route('/')
def display_cupcakes():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/cupcakes')
def show_cupcakes():
    """Display all cupcakes"""

    cupcakes = Cupcake.query.all()

    cupcake_list = [cupcake.serialize_to_dict() for cupcake in cupcakes]

    return jsonify(cupcake_list)


@app.route('/cupcakes', methods=['POST'])
def add_cupcake():
    """Create a new cupcake pass it to DB"""

    new_cupcake = request.json

    cupcake_obj = Cupcake(flavor=new_cupcake['flavor'],
                          size=new_cupcake['size'],
                          rating=new_cupcake['rating'],
                          image=new_cupcake['image'] or None)

    db.session.add(cupcake_obj)
    db.session.commit()

    return (jsonify(cupcake_obj.serialize_to_dict()), 201)


@app.route('/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake pass to db return updated cupcake from db as json"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    new_values = request.json

    cupcake.flavor = new_values['flavor']
    cupcake.size = new_values['size']
    cupcake.rating = new_values['rating']
    cupcake.image = new_values['image']

    db.session.commit()

    return jsonify(cupcake.serialize_to_dict())


@app.route('/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"message": "Deleted"})
