from db import db


class MonthlyRentPaymentModel(db.Model):
    __tablename__ = 'monthly_rent_payment'
    rentPaymentId = db.Column(db.Integer, primary_key=True)
    apartmentId = db.Column(db.Integer, db.ForeignKey('apartment.apartmentId'))
    agreementId = db.Column(db.Integer, db.ForeignKey('rental_agreement.agreementId'))
    monthBillingPeriod = db.Column(db.Date)
    paymentDueDate = db.Column(db.Date)
    amountPayment = db.Column(db.Float)
    monthlyRentPayment = db.Column(db.Float)
    monthlyBillsAmount = db.Column(db.Float)
    paymentDate =  db.Column(db.Date)
    isBillsSettlement = db.Column(db.Boolean)
    isPaid = db.Column(db.Boolean)
    monthlyRentPaymentDesc = db.Column(db.Text)

    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'monthly_rent_payment')
    apartment  = db.relationship('ApartmentModel', back_populates= 'monthly_rent_payment')
    
    bill_settlement  = db.relationship('BillSettlementModel', back_populates= 'monthly_rent_payment') 

    def __repr__(self):
        return 'Monthly rent payment: {}/{}'.format(self.rentPaymentId, self.apartmentId)

