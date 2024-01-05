from flask import Flask, request, jsonify, send_file, Response
from flask_caching import Cache
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL')

app.config['CACHE_REDIS_PORT'] = 6379

# Initialize the cache object
cache = Cache(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///image_database.sqlite3'
db = SQLAlchemy(app)
CORS(app)


class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    data = db.Column(db.LargeBinary)

@app.route('/')
def test():
    return "connected Image Service"
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'message': 'No image part in the request'}), 400

    image_file = request.files['image']
    name = image_file.filename
    data = image_file.read()

    new_image = ImageModel(name=name, data=data)
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Image uploaded successfully'}), 201


@app.route('/download/<int:image_id>', methods=['GET'])
def download_image(image_id):
    image = ImageModel.query.get(image_id)
    if not image:
        return jsonify({'message': 'Image not found'}), 404

    # Save the image to a temporary file before sending
    temp_image_path = 'temp_image.jpg'
    with open(temp_image_path, 'wb') as f:
        f.write(image.data)

    return send_file(temp_image_path, as_attachment=True)


@app.route('/images/<path:name>', methods=['GET'])
@cache.cached(timeout=60)  # Cache the response for 60 seconds
def get_image(name):
    image = name + '.jpg'
    image = ImageModel.query.filter_by(name=image).first()
    if not image:
        return jsonify({'message': 'Image not found'}), 404

    return Response(image.data, content_type='image/jpeg')


if __name__ == '__main__':
    app.run(debug=True)
