from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    place = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('ShowBooking', backref='venues')
    hosts = db.relationship('User', backref="arena", secondary="association")

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'location': self.location,
            'capacity': self.capacity,
            'shows': [show.to_json() for show in self.shows],
        }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('Booking', backref='user')
    role = db.Column(db.String(50), default='user', nullable=False)

    def get_role(self):
        return self.role

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'bookings': [booking.to_json() for booking in self.bookings],
            'is_active': False
        }


class Association(db.Model):
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ShowBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.String(10), nullable=False)
    timing = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tags = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    yt_link = db.Column(db.String(50), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    seat_available = db.relationship('SeatAvailable', backref='show_booking', uselist=False)

    def to_json(self):
        return {
            'id': self.id,
            'show_name': self.show_name,
            'rating': self.rating,
            'timing': self.timing.isoformat(),
            'tags': self.tags,
            'price': self.price,
            'yt_link': self.yt_link,
            'venue_id': self.venue_id,
            "venues":
                {
                    'id': self.venues.id,
                    'name': self.venues.name,
                    'place': self.venues.place,
                    'location': self.venues.location,
                    'capacity': self.venues.capacity,

                }

        }


class SeatAvailable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, db.ForeignKey('show_booking.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=True)
    available_seats = db.Column(db.Integer, nullable=False, default=0)

    def to_json(self):
        return {
            'id': self.id,
            'show_id': self.show_id,
            'date': self.date.isoformat(),
            'venue_id': self.venue_id,
            'available_seats': self.available_seats,
        }


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show_booking.id'), nullable=False)
    seat_booked = db.Column(db.Integer, db.ForeignKey('seat_available.id'), nullable=False)
    timing = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def to_json(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'seat_booked': self.seat_booked,
            'timing': self.timing,
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    time = db.Column(db.String,nullable=False)

