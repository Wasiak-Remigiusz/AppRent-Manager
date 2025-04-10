from db import db


class TenantModel(db.Model):
    __tablename__ = 'tenant'
    tenantId=db.Column(db.Integer, primary_key=True)
    tenantFirstName=db.Column(db.String(50))
    tenantLastName=db.Column(db.String(100))
    tenantTelephone =db.Column(db.String(30))
    tenantEmail=db.Column(db.String(80))

    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'tenant')