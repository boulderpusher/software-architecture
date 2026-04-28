#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.sqlite3'
db = SQLAlchemy(app)

class ImageData(db.Model):
    query = db.Column(db.String, nullable=False)
    href = db.Column(db.String, primary_key=True, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    
def get_images(url, query):
    response = requests.get(url, params={'q': query})
    items = response.json()['collection']['items']
    return items

if __name__ == "__main__":
    url = "https://images-api.nasa.gov/search"
    query = 'artemis'
    images = get_images(url, query)
    with app.app_context():
        db.create_all()
        for image in images:
            link = next((link for link in image['links'] if link['rel'] == 'canonical'), image['links'][0])
            href, width, height = link['href'], link['width'], link['height']
            entry = ImageData(query=query, href=href, width=width, height=height)
            db.session.add(entry)
        db.session.commit()