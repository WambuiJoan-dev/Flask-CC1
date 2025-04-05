from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String, ForeignKey

db = SQLAlchemy() 

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    super_name = Column(String)
    hero_powers = db.relationship("HeroPower", back_populates="hero")
    serialize_rules = ('-hero_powers.hero',)

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    hero_powers = db.relationship("HeroPower", back_populates="power")
    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long.")
        return description

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = Column(Integer, primary_key=True)
    strength = Column(String)
    hero_id = Column(Integer, ForeignKey('heroes.id'), nullable=False)
    power_id = Column(Integer, ForeignKey('powers.id'), nullable=False)
    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return value