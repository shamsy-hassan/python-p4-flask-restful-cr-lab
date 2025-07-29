import json
import pytest
from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    @pytest.fixture(autouse=True)
    def setup_db(self):
        """Fixture to set up and tear down the database for each test"""
        with app.app_context():
            db.create_all()
            # Add a test plant that will have ID=1
            test_plant = Plant(
                name="Test Plant",
                image="test.jpg",
                price=9.99
            )
            db.session.add(test_plant)
            db.session.commit()
        yield
        with app.app_context():
            db.drop_all()

    def test_plants_get_route(self):
        '''has a resource available at "/plants".'''
        response = app.test_client().get('/plants')
        assert response.status_code == 200

    def test_plants_get_route_returns_list_of_plant_objects(self):
        '''returns JSON representing Plant objects at "/plants".'''
        response = app.test_client().get('/plants')
        data = json.loads(response.data.decode())
        
        assert isinstance(data, list)
        assert len(data) > 0
        for record in data:
            assert isinstance(record, dict)
            assert 'id' in record
            assert 'name' in record
            assert 'image' in record
            assert 'price' in record

    def test_plants_post_route_creates_plant_record_in_db(self):
        '''allows users to create Plant records through the "/plants" POST route.'''
        response = app.test_client().post(
            '/plants',
            json={
                "name": "Live Oak",
                "image": "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx",
                "price": 250.00,
            }
        )
        
        assert response.status_code == 201
        data = json.loads(response.data.decode())
        assert data['name'] == "Live Oak"
        
        with app.app_context():
            lo = Plant.query.filter_by(name="Live Oak").first()
            assert lo is not None
            assert lo.name == "Live Oak"
            assert lo.image == "https://www.nwf.org/-/media/NEW-WEBSITE/Shared-Folder/Wildlife/Plants-and-Fungi/plant_southern-live-oak_600x300.ashx"
            assert lo.price == 250.00

    def test_plant_by_id_get_route(self):
        '''has a resource available at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        '''returns JSON representing one Plant object at "/plants/<int:id>".'''
        response = app.test_client().get('/plants/1')
        data = json.loads(response.data.decode())
        
        assert isinstance(data, dict)
        assert data["id"] == 1
        assert data["name"] == "Test Plant"
        assert data["image"] == "test.jpg"
        assert data["price"] == 9.99