import json
import unittest
from app import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor

casting_assistant_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJod"
                     "HRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDQ5NTI3MTkwNjc4OTMwMTI0Nz"
                     "ciLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA"
                     "xMzk4ODkwLCJleHAiOjE2MDE0MDYwOTAsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUi"
                     "OiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.HC0ZXGjX"
                     "ZY165lqTFxl_YNpUGc6YDLR6XPV49gf_JQis-lTNEc0uT41yN5PUMZBP_kxWLN7TwyWkrKrF_VcgXvPVGQLkHe9RXSnNzvl4W"
                     "D3poicNsBNvSh3YA7saO-oKKYbMBKjOQJmZ7YPFpl4256NN6l3NHHJUr6kGNgGVFSiofx9cOw9pdWplHGDOqm2OYzVY83k2Y-"
                     "_XmcYKqFmCDIh9wFYrjewnVI5VX81O6pXFfuNC3OKSNMZxZLFPnl3YwWnbSrhd0F7GktbYvbgHNYdEc7ooObTnM50UV25dNHT"
                     "mscYRsrJOK0BJLcpdYQ9xk3SxKaCbEnVmfqMaMXhTUg"
}

casting_director_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJod"
                     "HRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg3MjE3NjY0OTc5MTQ0MzAxMj"
                     "EiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA"
                     "xMzk4ODIzLCJleHAiOjE2MDE0MDYwMjMsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUi"
                     "OiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0O"
                     "m1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.BJTfmiGThUHBxHIJaRf7VsLPx"
                     "U2q_bPlm-7luu0BqHn4rTKnHzoT4xXX8m5ctNLo7ocnEbNzYnOHiw9DFbSfkAvX6aAxZfjY5vkIDlCly6y3QVVBlhD0dcHyKB"
                     "22WXekOEkKQfDjddCO6GNB77102MbQ-9GzndsNm7TnkgK7TkWz1dDBqMElSzce6sH0sk-IJALAEmXljhrjcufZGr1q_013g8p"
                     "VrILFyIWYm0Jym5rph3jEY0vGH1_qeWA_MOIETvX6S6ecn3UEUkGLxnTxgx8NgVAYAbchkMvoLJFGYUSoov9j-eoJFubta6VX"
                     "wDT4Vd1yeBZjM3MLsUud4ejrKg"
}

executive_producer_auth_header = {
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjRHU1A0YlMxa0tmSUgwajhlb3dOWSJ9.eyJpc3MiOiJod"
                     "HRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDg4MTEzMTk4NDExMjQxODUwND"
                     "giLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL2FrdWVpc2FyYS51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjA"
                     "xMzk4NzYzLCJleHAiOjE2MDE0MDU5NjMsImF6cCI6IlQ5N05SODdGdVVlcWxaZWN5bFF3OEE4WW5vdWxHSmU2Iiwic2NvcGUi"
                     "OiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ"
                     "2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3"
                     "Q6bW92aWVzIl19.uA49-W0bC3OMOdqp3QpOxyVYZXcXfkLpRkf411UDUeddhOirbokCkq2BHKe6Ltp5d2trAj9CG68mabiWQ6"
                     "SfJsDGMBM-tmXF52tF3xbsN3Nkox_4G1tj5oqHT9zFr6mG5iEy8T4xCNTc-w-RVjIq356G3JvlvlolU71AD_j31lE7QBi8eDV"
                     "onU1RgRMSeV4HFWC-CTKDU_9AokBnZe-erKu8a_h4ccJ-KGYH0ygoL0_u9J0EXPuoPjCLMmY_ZYTGO9SV8cB-VOnRp4wiz8VG"
                     "vpBYYU8gA-Xsjz5LuXYDrBeMAHirkPh6ZqAg7U4DoJrF3nDpiQT3liw9h2bAq3LlKA"
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