from controller.database import db
from datetime import datetime
class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement = True )
    user_email = db.Column(db.String(100), unique = True , nullable = False)
    user_password = db.Column(db.String(250), nullable = False)
    user_name = db.Column(db.String(50), nullable = False)
    user_address = db.Column(db.String(250), nullable = True)
    user_pincode = db.Column(db.String(10), nullable = True)
    
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable = True)
    role = db.relationship('Role', backref='user', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True )
    name = db.Column(db.String(50), unique = True, nullable = False)





class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    prime_location_name = db.Column(db.String(100), nullable = False)
    address = db.Column(db.String(250), nullable = False)
    pincode = db.Column(db.String(10), nullable = False)
    maximum_number_of_spots = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    spot = db.relationship('ParkingSpot', backref='parking_lot', lazy=True,uselist=False)
    reserve = db.relationship('ReserveParkingSpot', backref='parking_lot', lazy=True, uselist=False)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable = False)
    status = db.Column(db.String(20), nullable = False)  

class ReserveParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'))
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'))
    vehicle_no = db.Column(db.String, nullable=False)
    address = db.Column(db.String(250), nullable = False)
    pincode = db.Column(db.String(10), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    parking_timestamp = db.Column(db.DateTime, nullable = False)
    leaving_timestamp = db.Column(db.DateTime)
    parking_cost = db.Column(db.Float, nullable = False)
    spot = db.relationship('ParkingSpot', backref='reserve_parking_spot', lazy=True, uselist=False)

