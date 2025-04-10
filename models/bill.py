from db import db


class BillModel(db.Model):
    __tablename__ = 'bill'
    billId=db.Column(db.Integer, primary_key=True)
    apartmentId = db.Column(db.Integer, db.ForeignKey('apartment.apartmentId'))
    agreementId = db.Column(db.Integer, db.ForeignKey('rental_agreement.agreementId'))  # --> DO be deleted
    currencyId = db.Column(db.Integer, db.ForeignKey('currency.currencyId'))
    monthBillingPeriod = db.Column(db.Date)
    paymentDueDate = db.Column(db.Date)
    amountBill = db.Column(db.Float)
    paymentDate =  db.Column(db.Date)
    billName = db.Column(db.String(20))
    billTypeId =  db.Column(db.Integer, db.ForeignKey('bill_type.billTypeId'))
    isSettlement = db.Column(db.Boolean)
    isPaid = db.Column(db.Boolean)
    mediaBillDesc = db.Column(db.Text)


    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'bill')
    apartment  = db.relationship('ApartmentModel', back_populates= 'bill')
    bill_type  = db.relationship('BillTypeModel', back_populates= 'bill') 
    currency  = db.relationship('CurrencyModel', back_populates= 'bill') 

    bill_settlement  = db.relationship('BillSettlementModel', back_populates= 'bill') 



    def __repr__(self):
        return 'Monthly bill: {}/{}'.format(self.billId, self.apartmentId, self.agreementId, self.monthBillingPeriod)