import csv
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from app import Venue, User  

celery = Celery(__name__, broker='redis://localhost:6379/1', backend='redis://localhost:6379/1')


@celery.task
def export_venue_details_task(venue_id):
    try:
        venue = Venue.query.get(venue_id)

        venue_data = [["id", "name", "place", "location", "capacity"],
                      [str(venue.id), venue.name, venue.place, venue.location, str(venue.capacity)]]

        with open("venue.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(venue_data)

        show_data = [["id", "show_name", "rating", "timing", "tags", "price", "ytlink"]]
        for show in venue.shows:
            show_data.append(
                [str(show.id), show.show_name, show.rating, show.timing, show.tags, show.price, show.yt_link])

        with open("shows.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(show_data)

        return "done"
    except Exception as e:
        print(f"CSV Export for venue ID {venue_id} failed: {str(e)}")


@celery.task
def send_email(sender_email, sender_password, subject, html_body, csv_files, id):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    context = smtplib.SMTP(smtp_server, smtp_port)
    context.starttls()

    try:
        context.login(sender_email, sender_password)

        email = User.query.get(id).email
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = subject

            body = MIMEText(html_body, 'html')
            msg.attach(body)

            for csv_file in csv_files:
                with open(csv_file, 'rb') as file:
                    csv_content = file.read()
                    csv_attachment = MIMEApplication(csv_content)
                    csv_attachment.add_header('Content-Disposition', 'attachment', filename=csv_file)
                    msg.attach(csv_attachment)

            context.sendmail(sender_email, email, msg.as_string())
            print("Email sent successfully to:", email)
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")

    except Exception as e:
        print(f"Error while connecting to SMTP server: {e}")
    finally:
        context.quit()
