from db import db


class RentalAgreementModel(db.Model):
    __tablename__ = 'rental_agreement'
    agreementId = db.Column(db.Integer, primary_key=True)
    agreementName = db.Column(db.String(20))
    userId=db.Column(db.Integer, db.ForeignKey('user.userId'))
    apartmentId = db.Column(db.Integer, db.ForeignKey('apartment.apartmentId'))
    tenantId = db.Column(db.Integer, db.ForeignKey('tenant.tenantId'))
    startDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    currencyId = db.Column(db.Integer, db.ForeignKey('currency.currencyId'))
    paymentDueDate = db.Column(db.Integer)
    depositAmount =  db.Column(db.Float)
    monthlyRentPayment = db.Column(db.Float)
    isBillsSettlement = db.Column(db.Boolean)
    monthlyBillsAmount = db.Column(db.Float)
    aditionalInformation = db.Column(db.Text)


    user = db.relationship('UserModel', back_populates= 'rental_agreement') 
    apartment  = db.relationship('ApartmentModel', back_populates= 'rental_agreement')
    currency  = db.relationship('CurrencyModel', back_populates= 'rental_agreement') 
    tenant  = db.relationship('TenantModel', back_populates= 'rental_agreement') 
    monthly_rent_payment  = db.relationship('MonthlyRentPaymentModel', back_populates= 'rental_agreement') 
    bill  = db.relationship('BillModel', back_populates= 'rental_agreement') 

    bill_settlement  = db.relationship('BillSettlementModel', back_populates= 'rental_agreement') 
    

    def __repr__(self):
        return 'Rental agreement: {}/{}'.format(self.agreementId, self.agreementName)