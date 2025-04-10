from db import db


class BillTypeModel(db.Model):
    __tablename__ = 'bill_type'
    billTypeId = db.Column(db.Integer, primary_key=True)
    billTypeName =  db.Column(db.String(35))


    bill = db.relationship('BillModel', back_populates= 'bill_type')


    def __repr__(self):
        return 'Bill type: {}/{}'.format(self.billId, self.billTypeName)