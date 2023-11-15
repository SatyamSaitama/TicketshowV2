import smtplib
from datetime import datetime, timedelta
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pytz
import requests
from celery import Celery
from jinja2 import Template

from app import Booking, User, ShowBooking, db


def get_movie_poster_url(title):
    api_key = '34ea11c2'
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        return data.get("Poster")
    else:
        return None


celery = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
sender_email = "ticketshow4you@gmail.com"
sender_password = "iyyjmaksvcdxwpkt"
tz = pytz.timezone('Asia/Kolkata')
india_time = datetime.now(tz)
one_week_ago = india_time - timedelta(days=1)
tz = pytz.timezone('Asia/Kolkata')
india_time = datetime.now(tz)
shows = ShowBooking.query.filter(ShowBooking.timing > india_time).limit(5)
booking = Booking.query.filter(Booking.timing > one_week_ago).all()
exception = [book.user_id for book in booking]
subject = "Don't miss out on the best shows!"
# HTML content with Bootstrap and inline CSS
html_body = """
  <html>
<head>
  <style>
    /* You can use custom CSS here */
    .container {
      max-width: 600px;
      margin: 0 auto;
      font-family: Arial, sans-serif;
    }

    .header {
      background-color: #f0f0f0;
      padding: 20px;
      text-align: center;
    }

    .content {
      padding: 20px;
    }

    .footer {
      background-color: #f0f0f0;
      padding: 20px;
      text-align: center;
    }

    .btn {
      display: inline-block;
      background-color: #007bff;
      color: white;
      padding: 10px 20px;
      text-decoration: none;
    }

    .show {
      display: flex;
      align-items: center;
      margin-bottom: 10px;
    }

    .show-img {
      width: 100px;
      height: 100px;
      object-fit: cover;
      border-radius: 10px;
    }

    .show-info {
      margin-left: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Don't miss out on the best shows!</h1>
    </div>
    <div class="content">
      <p>We have a variety of shows to suit your taste and budget. Whether you are looking for comedy, drama, musical, or thriller, we have something for you. But hurry, tickets are running out fast!</p>
      <p>Check out some of the shows below and book your seats today!</p>

      <!-- Use relative URLs to link to the images -->
    
      {% for show in shows %}
        <div class="show">
              {% set poster_url = get_movie_poster_url(show.show_name) %}

          <img src="{{ poster_url }}" alt="{{ show.name }}" class="show-img">
          <div class="show-info">
            <h3>{{ show.show_name }}</h3>
            show_timing: {{ show.timing }}
          </div>
        </div>
      {% endfor %}

      <p><a class="btn" href="localhost:3000">Book Now</a></p>
    </div>
    <div class="footer">
      <p>This email was sent by {{ company }}. If you wish to unsubscribe, please click here.</p>
    </div>
  </div>
</body>
</html>
"""

html_body = Template(html_body).render(shows=shows, company="TicketShow4You",get_movie_poster_url=get_movie_poster_url)


@celery.task
def send_email(sender_email, sender_password, subject, html_body, shows):  # Add 'shows' as an argument
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587  # For Gmail, use port 587

    # Create a secure SSL context
    context = smtplib.SMTP(smtp_server, smtp_port)
    context.starttls()

    try:
        # Log in to the SMTP server
        context.login(sender_email, sender_password)

        # Fetch user emails based on your criteria (user id not in exception and role is 'user')
        user_email = [user.email for user in User.query.all() if user.id not in exception and user.role == 'user']

        for email in user_email:
            try:
                # Create a multipart message and set the headers
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email
                msg['Subject'] = subject

                # Attach the HTML body
                body = MIMEText(html_body, 'html')
                msg.attach(body)

                # Attach images
                for show in shows:
                    image_path = f"C:\\Users\\786sa\\PycharmProjects\\IITM\\TicketShow\\TIcketShow\\static\\{show.venue_id}.{show.show_name}.jpg"  # Use relative URL
                    with open(image_path, "rb") as image_file:
                        image_data = image_file.read()
                        image = MIMEImage(image_data)
                        image.add_header('Content-ID', f'<{show.show_name}>')
                        image_file.close()

                # Send the email
                context.sendmail(sender_email, email, msg.as_string())
                print("Email sent successfully to:", email)
            except Exception as e:
                print(f"Failed to send email to {email}: {e}")
    except Exception as e:
        print(f"Error while connecting to SMTP server: {e}")
    finally:
        # Close the SMTP connection
        context.quit()


def generate_report(id):
    booking = Booking.query.filter_by(user_id=id).all()
    shows = [ShowBooking.query.get(book.id) for book in booking]
    temp = """<!DOCTYPE html>
<html>
<head>
    <title>Monthly Entertainment Report</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        .container {
            max-width: 600px;
            margin: 0 auto;
            font-family: Arial, sans-serif;
        }
        
        table {
            font-size: 14px;
            font-family: "Arial", sans-serif;
            border-radius: 10px;
            border: 1px solid #ccc;
            width: 100%;
        }

        th, td {
            padding: 10px;
            text-align: center;
        }

        th {
            background-color: #007bff;
            color: white;
        }

        tr:nth-child(odd) {
            background-color: #f0f0f0;
        }

        .genre-icon {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Monthly Entertainment Report</h1>
        <p class="text-center">Here is a summary of your entertainment activities for the month.</p>  
        <table class="table table-striped table-hover table-dark">
            <thead>
                <tr>
                    <th>Movie</th>
                    <th>Genre</th>
                    <th>Rating</th>
                    <th>Booked On</th>
                    <th>Paid</th>
                </tr>
            </thead>
            <tbody>
                {% for show in shows %}
                <tr>
                    <td>{{ show.show_name }}</td>
                    <td>
                        {% if show.tags == "Comedy" %}
                         😅 comedy
                        {% elif show.tags == "Drama" %}
                         🎭 Drama
                        {% elif show.tags == "Action" %}
                         🎬 Action
                        {% elif show.tags == "Adventure" %}
                        🥾 Adventure
                        {% elif show.tags == "Horror" %}
                        👻 Horror
                        {% else %}
                        {{ show.tags }}
                        {% endif %}
                    </td>
                    <td>{{ show.rating }}</td>
                    <td>{{ show.timing }}</td>
                    <td>{{ show.price }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        
    </div>
</body>
</html>

"""
    html_report = Template(temp).render(shows=shows)
    return html_report


@celery.task
def send_report():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    context = smtplib.SMTP(smtp_server, smtp_port)
    context.starttls()

    try:
        # Log in to the SMTP server
        context.login(sender_email, sender_password)

        users = User.query.filter(User.role == 'user').all()

        for user in users:
            try:
                # Create a multipart message and set the headers
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = user.email
                msg['Subject'] = "Montly Report"

                # Attach the HTML body
                body = MIMEText(generate_report(user.id), 'html')
                msg.attach(body)

                # Attach images

                # Send the email
                context.sendmail(sender_email, user.email, msg.as_string())
                print("Email sent successfully to:", user.email)
            except Exception as e:
                print(f"Failed to send email to {user.email}: {e}")
    except Exception as e:
        print(f"Error while connecting to SMTP server: {e}")
    finally:
        # Close the SMTP connection
        context.quit()


@celery.task
def dynamic_pricing():
    current_time = datetime.now()

    topBookings = Booking.query.order_by(Booking.seat_booked.desc()).limit(5).all()
    topShows = [ShowBooking.query.get(book.show_id) for book in topBookings]
    for show in topShows:
        if (show.timing - current_time).seconds < 21600:
            show.price += 10
            db.session.commit()

    bottomBookings = Booking.query.order_by(Booking.seat_booked.asc()).limit(5).all()
    bottomShows = [ShowBooking.query.get(book.show_id) for book in bottomBookings]
    for show in bottomShows:
        if (show.timing - current_time).seconds < 21600:
            show.price -= 10
            db.session.commit()
