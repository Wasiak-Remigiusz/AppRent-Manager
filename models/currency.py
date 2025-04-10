from db import db


class CurrencyModel(db.Model):
    __tablename__ = 'currency'
    currencyId=db.Column(db.Integer, primary_key=True)
    currencySymbol = db.Column(db.String(5))

    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'currency')
    bill = db.relationship('BillModel', back_populates= 'currency')