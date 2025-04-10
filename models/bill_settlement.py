from db import db


class BillSettlementModel(db.Model):
    __tablename__ = 'bill_settlement'
    billSettlementId = db.Column(db.Integer, primary_key=True)
    apartmentId = db.Column(db.Integer, db.ForeignKey('apartment.apartmentId'))
    agreementId = db.Column(db.Integer, db.ForeignKey('rental_agreement.agreementId'))
    billId = db.Column(db.Integer, db.ForeignKey('bill.billId'))
    rentPaymentId = db.Column(db.Integer, db.ForeignKey('monthly_rent_payment.rentPaymentId'))
    monthBillingPeriod = db.Column(db.Date)
    paymentDate =  db.Column(db.Date)
    toBeRefundedByLandlord =  db.Column(db.Float)
    toBeRefundedByTenant =  db.Column(db.Float)
    isPaid = db.Column(db.Boolean)
    billSettlementDesc = db.Column(db.Text)

    apartment  = db.relationship('ApartmentModel', back_populates= 'bill_settlement')
    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'bill_settlement')
    bill  = db.relationship('BillModel', back_populates= 'bill_settlement') 
    monthly_rent_payment  = db.relationship('MonthlyRentPaymentModel', back_populates= 'bill_settlement') 

    def __repr__(self):
        return 'Monthly rent payment: {}/{}'.format(self.rentPaymentId, self.apartmentId)

