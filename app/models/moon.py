from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    planet = db.relationship("Planet", back_populates="moons")
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))

    # create function to turn response into dict
    # no decorator needed bc we are using this on an object
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }