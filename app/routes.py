from flask import Blueprint

class Planet:
    def __init__(self, id="",name="", description=None, size=0):
        self.id = id
        self.name = name
        self.description = description
        self.size = size

mercury = Planet()
saturn = Planet()
pluto = Planet()
ceres = Planet()
makemake = Planet()
haumea = Planet()
eris = Planet()
