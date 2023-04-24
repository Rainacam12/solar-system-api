from flask import Blueprint, jsonify, abort, make_response

class Planet:
    def __init__(self, id="",name="", description=None, size=0):
        self.id = id
        self.name = name
        self.description = description
        self.size = size


planets = [
    Planet(1, "Pluto", "Heart-shaped glacier", "Dwarf"),
    Planet(2, "Ceres", "Named for Roman Goddess of corn and harvests", "Dwarf"),
    Planet(3, "Makemake", "Bright and donut-shaped", "Dwarf")
]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

# create endpoint to get resources
@planet_bp.route("", methods=["GET"])
def handle_planets():
    planet_response = []
    for planet in planets:
        planet_response.append({
            "id": planet.id,
            "name": planet.name,
            "description": planet.description,
            "size": planet.size
        })

    return jsonify(planet_response)

def validate_planet(planet_id): 
    try:
        planet_id = int(planet_id)
    except:
        abort(make_response({"message":f"planet {planet_id} invalid"}, 400))

    for planet in planets: 
        if planet.id == planet_id: 
            return planet

    abort(make_response({"message":f"planet {planet_id} not found"}, 404))

# create endpoint to get single resource, with validation
@planet_bp.route("/<planet_id>", methods=["GET"])
def handle_planet(planet_id): 
    planet = validate_planet(planet_id)
    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "size": planet.size
    }
