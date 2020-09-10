from flask import Flask, jsonify, request, abort
import os
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)
    # Resource-Specific Usage
    # CORS(app, resources={r"*/api/*": {origins: '*'}})
    
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    # )

    # if test_config is None:
    #     # load the instance config, it if exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # a simple page that says hello
    # @app.route('/')
    # Route-Specific Usage
    # @cross_origin
    # def hello():
    #     return jsonify({'message': 'HELLO WORLD'})

    @app.route('/smiley')
    def smiley():
        return ':)'

    @app.route('/plants', methods=['GET'])
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page -1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success':True,
            'plants': formatted_plants[start:end],
            'total_plants': len(formatted_plants)
        })

    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:    
            return jsonify({
                'success':True,
                'plants': plant.format()
            })

    @app.route('/plants/<int:plant_id>', methods=['POST'])
    def create_plant():
        body = request.get_json()

        try:
            plant_name = body.get('name')
            plant_scientific = body.get('scientific_name')
            plant_color = body.get('primary_color')
            plant_poisonous = body.get('is_poisonous')

            new_plant = Plant(
                name = plant_name,
                scientific_name = plant_scientific,
                primay_color = plant_color,
                is_poisonous = plant_poisonous
            )

            new_plant.insert()

            return jsonify({
                'success': True,
                'id': new_plant.id
            })

        except:
            abort(422)


    @app.route('/plants/<int:plant_id>', methods=['DELETE'])
    def delete_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)
        else:
            plant.delete()

            return jsonify({
                'success': True,
                'id': plant_id,
            })

    @app.route('/plants/<int:plant_id>', methods=['PATCH'])
    def modify_plant(plant_id):
        body = request.get_json()
        
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        if plant is None:
            abort(404)

        else:
            try:
                new_name = body.get('name', None)
                new_scientific = body.get('scientific_name', None)
                new_color = body.get('primary_color', None)
                new_poisonous = body.get('is_poisonous', None)

                plant.name = new_name or plant.name
                plant.scientific_name = new_scientific or plant.scientific_name
                plant.primary_color = new_color or plant.primary_color
                if new_poisonous:
                    plant.is_poisonous = bool(new_poisonous)

                plant.update()

                return jsonify({
                    'success': True,
                    'id': plant.id
                })
            
            except:
                abort(422)
            
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app