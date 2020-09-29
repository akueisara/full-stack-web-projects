import json
import unittest
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor

casting_assistant_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDQ5NTI3MTkwNjc4OTMwMTI0NzciLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxMzg3ODI0LCJleHAiOjE2MDEzOTUwMjQsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.hnngrrMkTdk1zAVgWLJ_clIKfLlTLr0HS99UwnhN5jHue6Ty7sVMTE7n9GVQWwF0deiVphmWa2B1cly1REPMS88zk92A-jNsWvvg8INmgGS8lEpbFTr3q3SflWK71D3usbPupHmhGVpixguF9Y_-HMBa82Y3yF5OBTYrZircHj7tFIU5FWXknb_JEi0buEFJ_w_R4nOtVcVNl6Rzkr1TpbTQpVQMUVStsxajhisrk0vzbhYwmAZxXAxJwzpMqc_kPmaCMxBQXLFnbGn06gTH_MGpmpeCRyhi2_27C5aQpMLVno6kCc86E51vIZZnMFTzUcyZfbiwdVBfTMiBJoKZrw"
}

casting_director_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg3MjE3NjY0OTc5MTQ0MzAxMjEiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxMzg3NzcyLCJleHAiOjE2MDEzOTQ5NzIsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.puISiJvGXczbDhfeEgclw4fzIXqot65P0JY8BeCJBocrAypMJfmgHiG_E96WQzVNi92YuQxyZOp-tKMzMhHKHuVoqCcRmjyevcaeG1z6s8TroZRAFmhz4yrr1VFtGtDg8oAYtBGhWPrpti4vWPC1Kq2RRoyid6KpNFSTliuQCrDfRTzq71TbQtcehVr_aI25Dmd_JXFVk4sH_AhozMQinhG54rHFLTN95HIWVXvjFQdrPQ8aqD2bksKkwWwWGaUYbsfcKfxeyQ6oAwB4Pys_pR8DCdcDeuLyoVhsj7J_0Z9mdS4IGnAMjH91a4K8PGCJEGngTJaQfWH7dpfP84QEqA"
}

executive_producer_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg4MTEzMTk4NDExMjQxODUwNDgiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAxMzg3NjQ2LCJleHAiOjE2MDEzOTQ4NDYsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.DVP6SZxbX8pMYKtF69Tg5HmIyAEAJuOzmz7dkf0NxAmNlINN6gBosjNNI_P7XRmYVfw_8kzwh0SfZ3n3ejqWvc_0zV_U5623ennj7ss2Daax7KHYJ21BSLrjUQX9_x97v5BfIisYFcui2BcyNxW2be7LsfN_0FvP5n7c0a7dv6NMU_jD9aFNITSL2ZNM8E7elzTDy9YdyFQwO5xbMjj6yxtqXu2Mc4YWzP_kiPt5S87BtZxuhX5VYPHtJyi0vlEnas_a-35lX79gvvlaBupLOwWbiQuaWTJEYdyeptXI6BTcnfiLeCqcI0-8sBpAC4-iuN3GSBZCW7hN2rysfh8r1Q"
}

class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_movie = {
            "title": "New Movie",
            "release_date": "2020-09-27"
        }

        self.updated_movie = {
            "title": "New Movie Updated",
            "release_date": "2020-09-28"
        }

        self.new_actor = {
            "name": "New Actor",
            "age": 20,
            "gender": "female"
        }

        self.updated_actor = {
            "name": "New Actor Updated",
            "age": 22,
            "gender": "male"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_movie(self):
        res = self.client().post('/movies', headers=executive_producer_auth_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['movies']))

    def test_401_create_movie(self):
        res = self.client().post('/movies', headers=casting_assistant_auth_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_get_movies(self):
        res = self.client().get('/movies', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_update_movie(self):
        res = self.client().patch('/movies/2', headers=casting_director_auth_header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_404_update_movie(self):
        res = self.client().patch('/movies/1000', headers=casting_director_auth_header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_movies'])
        self.assertTrue(len(data['movies']))
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(movie, None)

    def test_404_delete_movie_if_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_movie_no_permission(self):
        res = self.client().delete('/movies/1000', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_create_actor(self):
        res = self.client().post('/actors', headers=executive_producer_auth_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['actors']))

    def test_405_if_actor_creation_not_allowed(self):
        res = self.client().post('/actors/45', headers=casting_director_auth_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_get_actors(self):
        res = self.client().get('/actors', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_405_get_actors_not_allowed(self):
        res = self.client().get('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_update_actor(self):
        res = self.client().patch('/actors/2', headers=casting_director_auth_header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_404_update_actor_not_found(self):
        res = self.client().patch('/actors/245', headers=casting_director_auth_header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=executive_producer_auth_header)
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_actors'])
        self.assertTrue(len(data['actors']))
        self.assertEqual(data['deleted'], 1)
        self.assertEqual(actor, None)

    def test_401_delete_actor_no_permission(self):
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()