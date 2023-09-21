# Import necessary libraries and models
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db.init_app(app)

# Route to create a new baked good via POST request
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form  # Get form data from the request

    # Extract relevant data for creating a new baked good
    name = data.get("name")
    price = data.get("price")
    bakery_id = data.get("bakery_id")

    # Create a new baked good object
    new_baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)

    # Add the new baked good to the database
    db.session.add(new_baked_good)
    db.session.commit()

    # Return the newly created baked good as JSON with a 201 status code (Created)
    response_data = new_baked_good.to_dict()
    return jsonify(response_data), 201

# Route to update an existing bakery's name via PATCH request
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    bakery = Bakery.query.get(id)  # Find the bakery by its ID

    if not bakery:
        # Return a 404 response if the bakery doesn't exist
        return jsonify({"error": "Bakery not found"}), 404

    data = request.form  # Get form data from the request

    # Update the bakery's name based on the data in the request
    if "name" in data:
        bakery.name = data["name"]

    # Commit the changes to the database
    db.session.commit()

    # Return the updated bakery as JSON with a 200 status code (OK)
    response_data = bakery.to_dict()
    return jsonify(response_data), 200

# Route to delete an existing baked good via DELETE request
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)  # Find the baked good by its ID

    if not baked_good:
        # Return a 404 response if the baked good doesn't exist
        return jsonify({"error": "Baked good not found"}), 404

    # Delete the baked good from the database
    db.session.delete(baked_good)
    db.session.commit()

    # Return a success message as JSON with a 200 status code (OK)
    response_data = {"message": "Baked good deleted successfully"}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(port=5555)
