from db import db


class CountryModel(db.Model):
    __tablename__ = 'country'
    countryId=db.Column(db.Integer, primary_key=True)
    countryName=db.Column(db.String(100))


    apartment = db.relationship('ApartmentModel', back_populates= 'country')
