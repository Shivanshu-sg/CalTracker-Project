from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Dishes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    country = db.Column(db.String(80), nullable=False)
    main_ingredient = db.Column(db.String(80), nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    time_spent = db.Column(db.Integer, nullable=False)
    calories_burn = db.Column(db.Integer, nullable=False)
