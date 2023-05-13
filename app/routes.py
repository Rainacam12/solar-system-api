from flask import Blueprint, jsonify, abort, make_response, request
from app.models.planet import Planet
from app.models.moon import Moon
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
moon_bp = Blueprint("moons", __name__, url_prefix="/moons" )

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
def validate_model(cls, model_id): 
    try: 
        model_id = int(model_id)
    except: 
        abort(make_response({"message":f"{model_id} invalid type ({type(model_id)})"}, 400))
        
    model = cls.query.get(model_id) 

    if not model: 
        abort(make_response({f"message":f"{cls.__name__.lower()} {model_id} not found"}, 404))

    return model

@planet_bp.route("", methods=['POST'])
def create_planet():
    request_body = request.get_json()

    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return jsonify(f"Planet {new_planet.name} successfully created"), 201

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
        planets_response.append(planet.to_dict())
    return jsonify(planets_response)

        
@planet_bp.route("/<planet_id>", methods=["GET"])
def read_one_planet(planet_id):
    # query our db to grab the crystal that has the id we want
    planet = validate_model(Planet, planet_id)
    
    return planet.to_dict(), 200

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id): 
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.size = request_body["size"]

    db.session.commit()

    return planet.to_dict(), 200


@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_planet(planet_id): 
    planet = validate_model(planet_id)

    db.session.delete(planet)
    db.session.commit()

    return make_response(f"planet #{planet.id} successfully deleted")

# Planet's Nested Routes: Create Moon on Planet ID
@planet_bp.route("/<planet_id>/moons", methods=["POST"])
def create_moon_by_id(planet_id): 
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    new_moon = Moon(
        name=request_body["name"],
        planet=planet
    )

    db.session.add(new_moon)
    db.session.commit()

    return jsonify(f"Moon {new_moon.name}")

@planet_bp.route("/<planet_id>/moons", methods=["GET"])
def get_all_moons_with_id(planet_id): 
    planet = validate_model(Planet, planet_id)

    moon_response = []
    for moon in planet.moons: 
        moon_response.append(moon.to_dict())
    return jsonify(moon_response), 200


# moons Routes
@moon_bp.route("", methods=['POST'])
# define a route for creating a crystal resource
def create_moon():
    request_body = request.get_json()
    
    new_moon = Moon(
        name=request_body["name"]
    )
    
    db.session.add(new_moon)
    db.session.commit()
    
    return jsonify(f"Moon {new_moon.name} successfully created!"), 201

@moon_bp.route("", methods=['GET'])
def read_all_moons():
    moons = Moon.query.all()

    moons_response = []

    for moon in moons:
        moons_response.append({"name": moon.name, "id": moon.id})

    return jsonify(moons_response)

