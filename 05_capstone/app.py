from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

DATA_PER_PAGE = 10

def paginate_data(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DATA_PER_PAGE
    end = start + DATA_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(jwt):
        selection = Movie.query.order_by(Movie.id).all()
        current_movies = paginate_data(request, selection)

        if len(current_movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': current_movies,
            'total_movies': len(Movie.query.all())
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()

        new_title = body.get('title')
        new_release_date = body.get('release_date')

        try:
            movie = Movie(new_title, new_release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.id,
                'movies': [movie.format()]
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()
            selection = Movie.query.order_by(Movie.id).all()
            current_movies = paginate_data(request, selection)

            return jsonify({
                'success': True,
                'deleted': movie_id,
                'movies': current_movies,
                'total_movies': len(Movie.query.all())
            })

        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        body = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)

        try:
            if body.get("title"):
                movie.title = body.get('title')
            if body.get("release_date"):
                movie.release_date = body.get('release_date')

            movie.update()

            return jsonify({
                'success': True,
                'movies': [movie.format()]
            })

        except:
            abort(400)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(jwt):
        selection = Actor.query.order_by(Actor.id).all()
        current_actors = paginate_data(request, selection)

        if len(current_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': current_actors,
            'total_actors': len(Actor.query.all())
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()

        name = body.get('name')
        age = body.get('age', None)
        gender = body.get('gender', None)

        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.id,
                'actors': [actor.format()]
            })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            actor.delete()
            selection = Actor.query.order_by(Actor.id).all()
            current_actors = paginate_data(request, selection)

            return jsonify({
                'success': True,
                'deleted': actor_id,
                'actors': current_actors,
                'total_actors': len(Actor.query.all())
            })

        except:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if actor is None:
            abort(404)

        try:
            if body.get("name"):
                actor.name = body.get('name')
            if body.get("age"):
                actor.age = body.get('age')
            if body.get("gender"):
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actors': [actor.format()]
            })

        except:
            abort(400)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def not_auth(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error.get('description')
        }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)