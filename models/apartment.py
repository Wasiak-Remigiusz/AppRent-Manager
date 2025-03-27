from db import db


class ApartmentModel(db.Model):
    __tablename__ = 'apartment'
    apartmentId=db.Column(db.Integer, primary_key=True)
    apartmentName=db.Column(db.String(50))
    userId=db.Column(db.Integer, db.ForeignKey('user.userId'))
    city=db.Column(db.String(100))
    street=db.Column(db.String(100))
    streetNumber=db.Column(db.String(20))
    apartmentNumber=db.Column(db.Integer)
    countryId=db.Column(db.Integer, db.ForeignKey('country.countryId'))

    user = db.relationship('UserModel', back_populates= 'apartment') 
    country  = db.relationship('CountryModel', back_populates= 'apartment') 
    

    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'apartment', lazy='dynamic')
    monthly_rent_payment = db.relationship('MonthlyRentPaymentModel', back_populates= 'apartment', lazy='dynamic')
    bill = db.relationship('BillModel', back_populates= 'apartment', lazy='dynamic')

    bill_settlement = db.relationship('BillSettlementModel', back_populates= 'apartment', lazy='dynamic')
   

    def __repr__(self):
        return 'Apartment: {}/{}'.format(self.apartmentId, self.apartmentName)