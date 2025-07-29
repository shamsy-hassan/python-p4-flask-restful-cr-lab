import pytest
from app import app
from models import db, Plant

@pytest.fixture(autouse=True)
def setup_db():
    """Fixture to set up and tear down the database for each test"""
    with app.app_context():
        # Create all tables
        db.create_all()
        yield
        # Clean up
        db.drop_all()

class TestPlant:
    """Plant model in models.py"""

    def test_can_be_instantiated(self):
        '''can be instantiated with a name.'''
        p = Plant(name="Douglas Fir")
        assert p.name == "Douglas Fir"

    def test_can_be_created(self):
        '''can create records that can be committed to the database.'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()
            assert p.id is not None

    def test_can_be_retrieved(self):
        '''can be used to retrieve records from the database.'''
        with app.app_context():
            # Add test data first
            p = Plant(name="Test Plant")
            db.session.add(p)
            db.session.commit()
            
            plants = Plant.query.all()
            assert len(plants) > 0

    def test_can_be_serialized(self):
        '''can create records with a to_dict() method for serialization.'''
        with app.app_context():
            p = Plant(name="Douglas Fir")
            db.session.add(p)
            db.session.commit()
            
            plant_dict = p.to_dict()
            assert isinstance(plant_dict, dict)
            assert 'id' in plant_dict
            assert 'name' in plant_dict