#!/usr/bin/env python3

from app import app
from models import db, Plant

with app.app_context():
    # Clear existing data
    db.session.query(Plant).delete()
    db.session.commit()
    
    # Add new plants (let DB auto-generate IDs)
    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50),
        Plant(name="ZZ Plant", image="./images/zz-plant.jpg", price=25.98)
    ]
    db.session.add_all(plants)
    db.session.commit()