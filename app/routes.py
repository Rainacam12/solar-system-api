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
    # query.all gets planet from db
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