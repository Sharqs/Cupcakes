from app import app
from models import db, connect_db, Cupcake
import unittest

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes-app-test'
connect_db(app)
db.create_all()


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and make new cupcake."""

        Cupcake.query.delete()

        self.client = app.test_client()

        self.new_cupcake = Cupcake(
            flavor='testing', size='small', rating=10)
        db.session.add(self.new_cupcake)
        db.session.commit()

    def test_cupcakes_GET(self):

        with self.client:
            result = self.client.get("/cupcakes")
            self.assertEqual(result.status_code, 200)
            self.assertEqual(len(result.json), 1)
            self.assertEqual(result.json[0]['flavor'], 'testing')

    def test_add_cupcake(self):

        with self.client:
            result = self.client.post('/cupcakes', json={
                "flavor": "testy",
                "size": "cupcake",
                "rating": 3.14,
                "image": ""
            })

            response = result.json

            self.assertEqual(response['flavor'], "testy")
            self.assertEqual(response['size'], "cupcake")
            self.assertEqual(response['rating'], 3.14)
            self.assertEqual(response['image'], "https://tinyurl.com/truffle-cupcake")

            self.assertEqual(result.status_code, 201)

    def test_update_cupcake(self):

        with self.client:
            result = self.client.patch(f'/cupcakes/{self.new_cupcake.id}',
                                       json={
                                             "flavor": "testable",
                                             "size": "mini",
                                             "rating": 5,
                                             "image": "https://truffle-assets.imgix.net/pxqrocxwsjcc_4mlylloieeiqmyecgk0qq8_rose%CC%81-champagne-cupcakes-landscape-no-graphic.jpg"
                                            })

            response = result.json

            self.assertEqual(response['flavor'], "testable")
            self.assertEqual(response['size'], "mini")
            self.assertEqual(response['rating'], 5)
            self.assertEqual(response['image'], "https://truffle-assets.imgix.net/pxqrocxwsjcc_4mlylloieeiqmyecgk0qq8_rose%CC%81-champagne-cupcakes-landscape-no-graphic.jpg")

            self.assertEqual(result.status_code, 200)

    def delete_cupcake(self):

        with self.client:
            result = self.client.delete(f'/cupcakes/{self.new_cupcake.id}')

            self.assertEqual(result.json['message'], "Deleted")
            self.assertEqual(len(result.json), 1)

            self.assertEqual(result.status_code, 200)
