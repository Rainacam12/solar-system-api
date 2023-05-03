from flask import Blueprint, jsonify, abort, make_response, request
from .models.planet import Planet
from app import db


# class Planet:
#     def __init__(self, id="",name="", description=None, size=0):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.size = size


# planets = [
#     Planet(1, "Pluto", "Heart-shaped glacier", "Dwarf"),
#     Planet(2, "Ceres", "Named for Roman Goddess of corn and harvests", "Dwarf"),
#     Planet(3, "Makemake", "Bright and donut-shaped", "Dwarf")
# ]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

# create endpoint to get resources
# @planet_bp.route("", methods=["GET"])

# def handle_planets():
#     planet_response = []
#     for planet in planets:
#         planet_response.append({
#             "id": planet.id,
#             "name": planet.name,
#             "description": planet.description,
#             "size": planet.size
#         })

#     return jsonify(planet_response)

# define route for creating a planet
@planet_bp.route("", methods=['POST'])
def handle_planets():
    request_body = request.get_json()

    new_planet = Planet(
        name = request_body["name"],
        description = request_body["description"],
        size = request_body["size"]
    )

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)

# define a route for getting all planet 
@planet_bp.route("", methods=['GET'])
def read_all_planets():
    planets_response = []

    planet_name_query = request.args.get("name")
    planet_description_query = request.args.get("description")

    if planet_name_query:
        planets = Planet.query.filter_by(name=planet_name_query)
    elif planet_description_query: 
        planets = Planet.query.filter_by(description=planet_description_query)
    else: 
        planets = Planet.query.all()

    # add each planet to the response body
    for planet in planets:
        planets_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "size": planet.size
        })
    return jsonify(planets_response)

def validate_planet(planet_id): 
    try: 
        planet_id = int(planet_id)
    except: 
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))
        
    planet = Planet.query.get(planet_id) 

    if not planet: 
        abort(make_response({"message":f"planet {planet_id} not found"}, 404))

    return planet
        
@planet_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    planet = validate_planet(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "size": planet.size,
    }

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id): 
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size = request_body["size"]

    db.session.commit()

    return make_response(f"planet #{planet.id} successfully updated")


@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id): 
    planet = validate_planet(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"planet #{planet.id} successfully deleted")


# What's the difference between returning make_response and not returning it? 
    # Make response returns HTML and not JSON
    # can be used as confirmation that something was deleted or returned back to us

# use commit() for when we are updating/making changes to the data

# db mgrate and flask upgrade commits everything that's been added to the model to the database table