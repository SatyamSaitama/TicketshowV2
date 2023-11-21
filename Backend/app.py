import re
from collections import OrderedDict
from datetime import timedelta

import bcrypt
import pytz
from flask import *
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
from flask_restful import Resource, reqparse, Api, fields, marshal, abort
from flask_swagger_ui import get_swaggerui_blueprint

from model import *
# from test import *

app = Flask(__name__)
"""===============================================================CONFIGS=========================================================="""
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///venue.sqlite3"
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)
"""===================================================Initializations==============================================================================="""
CORS(app)
db.init_app(app)
api = Api(app)
cache = Cache(app)
app.secret_key = '123'
jwt = JWTManager(app)
SWAGGER_URL = '/api/docs'

API_URL = '/static/api.yml'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,

    API_URL,
    config={
        'app_name': "My API",

    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

app.app_context().push()
"""==============================================================METHODS============================================================================="""


def is_valid_password(password):
    # Check for at least 8 characters, at least 1 uppercase letter, at least 1 lowercase letter,
    # and at least 1 number
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$"
    return re.match(pattern, password) is not None


"""===========================================================UTILS====================================================================================="""


@jwt.user_identity_loader
def user_identity_lookup(member):
    return member.to_json()


@app.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_x = User.query.filter_by(email=email).first()
    if user_x:
        # login the user
        role = user_x.role
        stored_hashed_password = user_x.password
        is_password_correct = bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)
        if is_password_correct:
            access_token = create_access_token(identity=user_x)
            return jsonify({'message': 'success', "access_token": access_token, 'role': role})
        else:
            return jsonify({'error': 'Invalid credentials', 'message': 'failure'})
    return jsonify({'email': email, 'password': password})


@app.route('/logout')
def logout():
    # this has to done with frontend by  making the token invalid
    return jsonify({'message': 'You have been logged out!'})


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == "POST":
        data = request.get_json()
        name = data.get('username')
        email = data.get('email')
        password = data.get('password')

        role = data.get('role')

        confirm_password = data.get('confirm_password')

        USER = User.query.filter_by(email=email).first()
        if USER:
            return jsonify({'message': 'Email already exists.'})
        if password != confirm_password:
            return jsonify({'message': 'Password does not match'})
        if not is_valid_password(password):
            return jsonify(
                {'message': 'Password must be at least 8 characters long and contain uppercase letters and numbers.'})
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode('utf-8'), salt)
        if role == 'admin':
            # noinspection PyArgumentList
            USER = User(name=name, email=email, password=password, role=role)
        else:
            # noinspection PyArgumentList
            USER = User(name=name, email=email, password=password)
        db.session.add(USER)
        db.session.commit()
        return jsonify({'success': 'registered successfully'})

    return jsonify({'message': 'Signup endpoint reached'})


class SearchResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self, query):
        venues = [venue.to_json() for venue in Venue.query.all()]
        bookings = Booking.query.all()
        ratings = {}

        for booking in bookings:
            if booking.show_id not in ratings:
                ratings[booking.show_id] = []
            ratings[booking.show_id].append(booking.rating)

        for show_id in ratings:
            avg_rating = round(sum(ratings[show_id]) / len(ratings[show_id]), 1)

            ratings[show_id] = avg_rating
        place = [city.location for city in Venue.query.all()]
        shows = ShowBooking.query.filter(ShowBooking.show_name.ilike('%' + query + '%')).all()
        current_time = datetime.now()
        shows = [show for show in shows if show.timing > current_time]

        return jsonify({'results': [show.to_json() for show in shows], "location": list(set(place)), "ratings": ratings,
                        "venues": venues})

    def post(self):
        location_result = []
        venues = [venue.to_json() for venue in Venue.query.all()]
        rating_result = []
        tag_result = []
        venue_result = []
        bookings = Booking.query.all()
        ratings = {}

        for booking in bookings:
            if booking.show_id not in ratings:
                ratings[booking.show_id] = []
            ratings[booking.show_id].append(booking.rating)

        for show_id in ratings:
            avg_rating = round(sum(ratings[show_id]) / len(ratings[show_id]), 1)

            ratings[show_id] = avg_rating
        data = request.get_json()
        tags = data.get('tags')
        _location = data.get('location')
        venue = data.get('venues')
        _rating = data.get('rating')
        if _location:
            results = [ShowBooking.query.join(Venue).filter(Venue.location.ilike(x)).all() for x in _location]
            location_result = [y for x in results for y in x]

        if tags:
            results = [ShowBooking.query.filter(ShowBooking.tags.ilike(x)).all() for x in tags]
            tag_result = [y for x in results for y in x]

        if venue:
            results = [ShowBooking.query.filter(ShowBooking.venue_id == x).all() for x in venue]
            venue_result = [y for x in results for y in x]
            print(results, venue_result, 'venue', venue)

        if _rating:
            results = [ShowBooking.query.filter(ShowBooking.rating.ilike(x)).all() for x in _rating]
            rating_result = [y for x in results for y in x]

        if _location and tags and _rating and venue:
            results = list(
                set(location_result).intersection(tag_result).intersection(rating_result).intersection(venue_result))
        elif _location and tags and venue:
            results = list(set(location_result).intersection(tag_result).intersection(venue_result))
        elif _location and tags and _rating:
            results = list(set(location_result).intersection(tag_result).intersection(rating_result))
        elif _location and venue and _rating:
            results = list(set(location_result).intersection(venue_result).intersection(rating_result))
        elif tags and _rating and venue:
            results = list(set(tag_result).intersection(rating_result).intersection(venue_result))
        elif _location and tags:
            results = list(set(location_result).intersection(tag_result))
        elif _location and venue:
            results = list(set(location_result).intersection(venue_result))
        elif _location and _rating:
            results = list(set(location_result).intersection(rating_result))
        elif tags and _rating:
            results = list(set(tag_result).intersection(rating_result))
        elif tags and venue:
            results = list(set(tag_result).intersection(venue_result))
        elif venue and _rating:
            results = list(set(venue_result).intersection(rating_result))
        else:
            results = list(OrderedDict.fromkeys(location_result + tag_result + venue_result + rating_result))

        return jsonify({'results': [result.to_json() for result in results], 'ratings': ratings,
                        'location': list(set([v['location'] for v in venues])), 'venues': venues})


"""=============================================================VENUE-SHOW-CRUD========================================================================="""
venue_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'place': fields.String,
    'location': fields.String,
    'capacity': fields.Integer
}

show_booking_fields = {
    'id': fields.Integer,
    'show_name': fields.String,
    'rating': fields.String,
    'yt_link': fields.String,
    'timing': fields.DateTime,
    'tags': fields.String,
    'price': fields.Float,
}


class VenueResource(Resource):
    @jwt_required()
    def get(self, id=None):
        if get_jwt_identity()['role'] == 'admin':
            if id:
                venue = Venue.query.get(id)
                if not venue:
                    abort(404, message='Venue not found')
                return venue.to_json()
            else:
                venues = Venue.query.all()
                return [venue.to_json() for venue in venues]
        return jsonify({'error': 'User not authorized'})

    @jwt_required()
    def post(self):
        if get_jwt_identity()['role'] == 'admin':
            res = reqparse.RequestParser()
            res.add_argument('name', required=True)
            res.add_argument('place', required=True)
            res.add_argument('location', required=True)
            res.add_argument('capacity', required=True, type=int)
            data = res.parse_args()
            venue = Venue(name=data['name'], place=data['place'], location=data['location'], capacity=data['capacity'])
            db.session.add(venue)
            db.session.commit()
            association = Association(venue_id=venue.id, admin_id=get_jwt_identity()['id'])
            db.session.add(association)
            db.session.commit()
            return marshal(venue, venue_fields), 201
        return jsonify({'error': 'User not authorized'})

    @jwt_required()
    def put(self, id):
        res = reqparse.RequestParser()
        res.add_argument('name')
        res.add_argument('place')
        res.add_argument('location')
        res.add_argument('capacity', type=int)
        data = res.parse_args()
        venue = Venue.query.get(id)
        if not venue:
            abort(404, message='Venue not found')
        if data['name']:
            venue.name = data['name']
        if data['place']:
            venue.place = data['place']
        if data['location']:
            venue.location = data['location']
        if data['capacity'] or data['capacity'] == 0:
            venue.capacity = data['capacity']
        db.session.commit()
        return marshal(venue, venue_fields)

    @jwt_required()
    def delete(self, id):
        if get_jwt_identity()['role'] == 'admin':
            venue = Venue.query.get(id)
            if not venue:
                abort(404, message='Venue not found')
            for x in venue.shows:
                booking = Booking.query.filter_by(show_id=x.id).all()
                for y in booking:
                    db.session.delete(y)

                db.session.delete(x.seat_available)
                db.session.delete(x)
            db.session.delete(venue)
            db.session.commit()
            return '', 204

        return jsonify({'error': 'User not authorized'})


class ShowBookingResource(Resource):
    def get(self, id=None):
        if id:
            show = ShowBooking.query.get(id)
            if not show:
                abort(404, message='Show not found')
            return show.to_json()
        else:
            shows = ShowBooking.query.all()
            return [show.to_json() for show in shows]

    @jwt_required()
    def post(self):
        if get_jwt_identity()['role'] == 'admin':

            res = reqparse.RequestParser()
            res.add_argument('show_name', required=True)
            res.add_argument('rating', required=True)
            res.add_argument('yt_link', required=True)
            res.add_argument('timing', required=True, )
            res.add_argument('tags', required=True)
            res.add_argument('price', required=True, type=float)
            res.add_argument('venue_id', required=True, type=int)
            data = res.parse_args()
            data['timing'] = datetime.strptime(data['timing'], '%Y-%m-%dT%H:%M')

            venue = Venue.query.get(data['venue_id'])
            if not venue:
                abort(404, message='Venue not found')
            show = ShowBooking(show_name=data['show_name'], rating=data['rating'], timing=data['timing'],
                               tags=data['tags'], price=data['price'], venue_id=data['venue_id'],
                               yt_link=data['yt_link'])
            seat_available = SeatAvailable(available_seats=100, date=data['timing'], show_booking=show,
                                           venue_id=data['venue_id'])
            db.session.add(show)
            db.session.add(seat_available)
            db.session.commit()
            return marshal(show, show_booking_fields), 201
        return jsonify({'error': 'User not authorized'})

    @jwt_required()
    def put(self, id):
        if get_jwt_identity()['role'] == 'admin':

            response = reqparse.RequestParser()
            response.add_argument('show_name')
            response.add_argument('rating')
            response.add_argument('yt_link')
            response.add_argument('timing')
            response.add_argument('tags')
            response.add_argument('price', type=float)
            data = response.parse_args()
            show = ShowBooking.query.get(id)
            data['timing'] = datetime.strptime(data['timing'], '%Y-%m-%dT%H:%M')

            if not show:
                abort(404, message='Show not found')
            if data['show_name']:
                show.show_name = data['show_name']
            if data['rating']:
                show.rating = data['rating']
            if data['timing']:
                show.timing = data['timing']
                show.seat_available.date = data['timing']
            if data['tags']:
                show.tags = data['tags']
            if data['price']:
                show.price = data['price']
            if data['yt_link']:
                show.yt_link = data['yt_link']
            db.session.commit()
            return marshal(show, show_booking_fields)
        return jsonify({'error': 'User not authorized'})

    @jwt_required()
    def delete(self, id):
        if get_jwt_identity()['role'] == 'admin':

            show = ShowBooking.query.get(id)

            if not show:
                abort(404, message='Show not found')
            booking = Booking.query.filter_by(show_id=show.id).all()
            for x in booking:
                db.session.delete(x)
            db.session.delete(show.seat_available)
            db.session.delete(show)
            db.session.commit()
            return '', 204
        return jsonify({'error': 'User not authorized'})


"""====================================================BOOKING-MANAGEMENT============================================================================="""
parser = reqparse.RequestParser()
parser.add_argument('rating', type=float, required=False, help='Rating of the booking')
parser.add_argument('user_id', type=int, required=True, help='User ID')
parser.add_argument('show_id', type=int, required=True, help='Show ID')
parser.add_argument('seat_booked', type=int, required=True, help='Seat booked ID')
parser.add_argument('timing', type=str, help='Timing in the format "YYYY-MM-DD HH:MM:SS"')


# Helper function to get a booking by ID
def get_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        abort(404, message='Booking not found')
    return booking


# API Resource for individual bookings
class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):

        booking = get_booking(booking_id)
        return {
                   'id': booking.id,
                   'rating': booking.rating,
                   'user_id': booking.user_id,
                   'show_id': booking.show_id,
                   'seat_booked': booking.seat_booked,
                   'timing': f'{booking.timing}'
               }, 200

    @jwt_required()
    def delete(self, booking_id):
        booking = get_booking(booking_id)
        db.session.delete(booking)
        db.session.commit()
        return '', 204

    @jwt_required()
    def put(self, booking_id):
        booking = Booking.query.filter_by(user_id=get_jwt_identity()['id'], show_id=booking_id).first()

        booking = get_booking(booking.id)
        args = request.get_json()
        print(args)
        if 'rating' in args:
            booking.rating = args['rating']
        if 'user_id' in args:
            booking.user_id = args['user_id']
        if 'show_id' in args:
            booking.show_id = args['show_id']
        if 'seat_booked' in args:
            booking.seat_booked = args['seat_booked']
        db.session.commit()
        return {
                   'id': booking.id,
                   'rating': booking.rating,
                   'user_id': booking.user_id,
                   'show_id': booking.show_id,
                   'seat_booked': booking.seat_booked,
                   'timing': f'{booking.timing}'

               }, 200


# API Resource for a list of bookings and creating new bookings
class BookingListResource(Resource):
    @jwt_required()
    def get(self):
        bookings = Booking.query.all()

        return [{
            'id': booking.id,
            'rating': booking.rating,
            'user_id': booking.user_id,
            'show_id': booking.show_id,
            'seat_booked': booking.seat_booked,
            'timing': f'{booking.timing}'
        } for booking in bookings], 200

    @jwt_required()
    def post(self):
        args = parser.parse_args()
        print(args.timing)
        timing_str = args.timing
        timing_format = "%m/%d/%Y, %I:%M:%S %p"

        timing_datetime = datetime.strptime(timing_str, timing_format)
        booking = Booking(
            rating=args.rating,
            user_id=args.user_id,
            show_id=args.show_id,
            seat_booked=args.seat_booked,
            timing=timing_datetime
        )

        previousOrders = Booking.query.filter_by(show_id=booking.show_id, user_id=booking.user_id).first()
        if previousOrders:
            previousOrders.seat_booked = booking.seat_booked + previousOrders.seat_booked
            db.session.commit()
            return {"seat_booked": "updated"}

        db.session.add(booking)
        db.session.commit()
        return {
                   'id': booking.id,
                   'rating': booking.rating,
                   'user_id': booking.user_id,
                   'show_id': booking.show_id,
                   'seat_booked': booking.seat_booked,
                   'timing': f'{booking.timing}'
               }, 201


class UserShowsResource(Resource):
    @jwt_required()
    def get(self, user_id):
        bookings = Booking.query.filter_by(user_id=user_id).all()
        shows = [ShowBooking.query.get(booking.show_id) for booking in bookings]
        shows = list(set(shows))
        return [show.to_json() for show in shows], 200

    @jwt_required()
    def put(self, show_id):
        booking = Booking.query.filter_by(user_id=get_jwt_identity()['id'], show_id=show_id).first()
        args = parser.parse_args()
        if 'rating' in args:
            booking.rating = args['rating']
        if 'user_id' in args:
            booking.user_id = args['user_id']
        if 'show_id' in args:
            booking.show_id = args['show_id']
        if 'seat_booked' in args:
            booking.seat_booked = args['seat_booked']
        db.session.commit()
        return {
                   'id': booking.id,
                   'rating': booking.rating,
                   'user_id': booking.user_id,
                   'show_id': booking.show_id,
                   'seat_booked': booking.seat_booked,
                   'timing': f'{booking.timing}'

               }, 200


class DeleteBookingResource(Resource):
    @jwt_required()
    def delete(self, show_id, user_id):
        booking = Booking.query.filter_by(show_id=show_id, user_id=user_id).first()
        if booking:
            show = ShowBooking.query.get(show_id)
            show.venues.capacity = show.venues.capacity + booking.seat_booked
            db.session.delete(booking)

            db.session.commit()
            return "deleted successfully"
        return '', 204


class HomeResource(Resource):
    @cache.cached(timeout=60)  # Cache the response for 60 seconds
    def get(self):
        bookings = Booking.query.all()
        ratings = {}
        for booking in bookings:
            if booking.show_id not in ratings:
                ratings[booking.show_id] = []
            ratings[booking.show_id].append(booking.rating)

        for show_id in ratings:
            avg_rating = round(sum(ratings[show_id]) / len(ratings[show_id]), 1)
            ratings[show_id] = avg_rating

        tz = pytz.timezone('Asia/Kolkata')
        india_time = datetime.now(tz)
        shows = ShowBooking.query.filter(ShowBooking.timing > india_time).all()
        shows_json = [show.to_json() for show in shows]

        return jsonify({'shows': shows_json, 'ratings': ratings})

    def post(self):
        bookings = Booking.query.all()
        ratings = {}
        for booking in bookings:
            if booking.show_id not in ratings:
                ratings[booking.show_id] = []
            ratings[booking.show_id].append(booking.rating)

        for show_id in ratings:
            avg_rating = round(sum(ratings[show_id]) / len(ratings[show_id]), 1)
            ratings[show_id] = avg_rating

        tz = pytz.timezone('Asia/Kolkata')
        india_time = datetime.now(tz)
        shows = ShowBooking.query.filter(ShowBooking.timing > india_time).all()
        data = request.get_json()
        city = data.get('city')
        shows_json = [show.to_json() for show in shows if show.venues.location == city]
        return jsonify({'shows': shows_json, 'ratings': ratings})


"""=====================================================ROUTES======================================================================================"""


@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    if get_jwt_identity()['role'] == 'admin':
        adm = User.query.get(get_jwt_identity()['id'])
        venues = [venue.to_json() for venue in adm.arena]
        return jsonify({'venues': venues, 'id': get_jwt_identity()['id']})
    return jsonify({'error': 'User not authorized'})


@app.route('/set_venue', methods=['GET'])
@jwt_required()
def set_venue_data():
    if get_jwt_identity()['role'] == 'admin':
        obj = User.query.get(get_jwt_identity()['id'])
        rows = [venue.to_json() for venue in obj.arena]
        return jsonify({'rows': rows})

    return jsonify({'error': 'User not authorized'})


@app.route("/user", methods=['GET'])
@jwt_required()
def userx():
    return get_jwt_identity()


# @app.route('/export/<int:venue_id>')
# @jwt_required()
# def export(venue_id):
#     export_venue_details_task.delay(venue_id)
#     sender_email = "ticketshow4you@gmail.com"
#     sender_password = "iyyjmaksvcdxwpkt"
#     html_body = """<!DOCTYPE html>
# <html>
# <head>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             background-color: #f9f9f9;
#             margin: 0;
#             padding: 0;
#         }
#         .header {
#             background-color: #007bff;
#             color: white;
#             text-align: center;
#             padding: 20px 0;
#         }
#         .content {
#             max-width: 600px;
#             margin: 0 auto;
#             padding: 20px;
#             background-color: white;
#             border-radius: 5px;
#             box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
#         }
#         .message {
#             font-size: 16px;
#             line-height: 1.6;
#             color: #333;
#         }

#         .footer {
#             text-align: center;
#             margin-top: 20px;
#             color: #777;
#         }
#     </style>
# </head>
# <body>
#     <div class="header">
#         <h1>Your CSV Files</h1>
#     </div>
#     <div class="content">
#         <p class="message">Hello,</p>
#         <p class="message">Here are your requested CSV files.
#         <p class="message">Thank you for your interest.</p>
#     </div>
#     <div class="footer">
#         <p>&copy; 2023 TicketShow. All rights reserved.</p>
#     </div>
# </body>
# </html>

# """
#     subject = "Here is your csv files"
#     csv_files = ["shows.csv", "venue.csv"]
#     send_email.delay(sender_email, sender_password, subject, html_body, csv_files, get_jwt_identity()['id'])
#     return jsonify({"task": "done"})


# ===============================================================================================================================
api.add_resource(SearchResource, '/search', '/search/<string:query>')
api.add_resource(UserShowsResource, '/api/bookings/user/<int:user_id>', '/api/bookings/<int:show_id>/<int:user_id>')
api.add_resource(DeleteBookingResource, '/api/bookings/<int:show_id>/<int:user_id>')
api.add_resource(HomeResource, '/')
api.add_resource(BookingListResource, '/api/bookings')
api.add_resource(BookingResource, '/api/bookings/<int:booking_id>')
api.add_resource(VenueResource, '/api/venues', '/api/venues/<int:id>')
api.add_resource(ShowBookingResource, '/api/shows', '/api/shows/<int:id>')


# ===================================================================================================================================
@app.route('/popularity')
@jwt_required()
def popularity():
    if get_jwt_identity()['role'] == 'admin':
        # retrieve all the shows from the database
        bookings = Booking.query.order_by(Booking.seat_booked.desc()).all()
        shows_sorted = [ShowBooking.query.get(x.show_id) for x in bookings if
                        ShowBooking.query.get(x.show_id) is not None and x.seat_booked > 0]

        # count the number of occurrences of each venue
        venues = [Venue.query.get(x.venue_id).name for x in shows_sorted if x in shows_sorted is not None]
        venue_counts = {}
        for venue in venues:
            if venue in venue_counts:
                venue_counts[venue] += 1
            else:
                venue_counts[venue] = 1
        venues_sorted = sorted(venue_counts.keys())
        venue_popularity = [venue_counts[x] for x in venues_sorted]

        # count the number of occurrences of each show
        titles = [show.show_name for show in shows_sorted]
        show_counts = {}
        for title in titles:
            if title in show_counts:
                show_counts[title] += 1
            else:
                show_counts[title] = 1
        titles_sorted = sorted(show_counts.keys())
        show_popularity = [show_counts[x] for x in titles_sorted]

        # create a list of dictionaries for venue popularity
        venue_data = [{'Venue': venue, 'Popularity': count} for venue, count in zip(venues_sorted, venue_popularity)]

        # create a list of dictionaries for show popularity
        show_data = [{'Title': title, 'Popularity': count} for title, count in zip(titles_sorted, show_popularity)]

        # return the JSON response
        return jsonify({'venue_popularity': venue_data, 'show_popularity': show_data})

    # return an error message if the user is not an admin
    return jsonify({'error': 'Access denied'})


class CommentResource(Resource):
    def get(self, comment_id=None):
        if comment_id is None:
            comments = Comment.query.all()
            comments = [{'id': comment.id, 'user_id': comment.user_id, 'show_id': comment.show_id, 'text': comment.text,
                         'time': comment.time} for comment in comments]
            return comments, 200
        else:
            comments = Comment.query.filter_by(show_id=comment_id).all()
            comments = [{'id': comment.id, 'user_id': comment.user_id, 'show_id': comment.show_id, 'text': comment.text,
                         'time': comment.time} for comment in comments]
            return comments, 200

    def post(self):
        data = request.get_json()
        if 'user_id' in data and 'show_id' in data and 'text' in data and 'time' in data:
            new_comment = Comment(user_id=data['user_id'], show_id=data['show_id'], text=data['text'],
                                  time=data['time'])
            db.session.add(new_comment)
            db.session.commit()
            return {'message': 'Comment created', 'id': new_comment.id}, 201
        else:
            return {'error': 'Invalid data'}, 400

    def delete(self, comment_id):
        comment = Comment.query.get(comment_id)
        if comment:
            db.session.delete(comment)
            db.session.commit()
            return {'message': 'Comment deleted'}, 200
        else:
            return {'error': 'Comment not found'}, 404


api.add_resource(CommentResource, '/comment', '/comment/<int:comment_id>')

# ===============================================================================================================================

if __name__ == '__main__':
    app.run(port=3000, debug=True)
