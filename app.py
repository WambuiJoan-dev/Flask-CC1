from flask import Flask, jsonify, request
from flask_migrate import Migrate, upgrade
from models import Hero, Power, HeroPower, db  
from flask.cli import with_appcontext

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify(hero.to_dict())
    return jsonify({'error': 'Hero not found'}), 404


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])


@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify(power.to_dict())
    return jsonify({'error': 'Power not found'}), 404


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        except ValueError as e:
            return jsonify({'errors': [str(e)]}), 422
    else:
        return jsonify({'errors': ['Missing description in request body']}), 400


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    try:
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']

        power = Power.query.get(power_id)
        hero = Hero.query.get(hero_id)

        if not power or not hero:
            errors = []
            if not power:
                errors.append(f"Power with id {power_id} not found")
            if not hero:
                errors.append(f"Hero with id {hero_id} not found")
            return jsonify({'errors': errors}), 404

        new_hero_power = HeroPower(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify(new_hero_power.to_dict(include=('id', 'hero_id', 'power_id', 'strength', 'hero', 'power'))), 201
    except KeyError as e:
        return jsonify({'errors': [f'Missing required field: {e}']}), 400
    except ValueError as e:
        return jsonify({'errors': [str(e)]}), 422


if __name__ == '__main__':
    app.run(debug=True)