from app import db

# create our model
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    size = db.Column(db.Integer)

    @classmethod
    # in class methods, cls must come first. it's a reference to the class itself
    def from_dict(cls, planet_data):
        new_planet = Planet(
            name=planet_data["name"],
            description=planet_data["description"],
            size=planet_data["size"],
        )

        return new_planet

    # create function to turn response into dict
    # no decorator needed bc we are using this on an object
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "size": self.size
        }