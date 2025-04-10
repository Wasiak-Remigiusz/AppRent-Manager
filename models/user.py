import binascii
import hashlib
import random
import string
from datetime import date

from db import db


class UserModel(db.Model):
    __tablename__ = 'user'
    userId=db.Column(db.Integer, primary_key=True)
    firstName=db.Column(db.String(50))
    lastName=db.Column(db.String(100))
    userName=db.Column(db.String(50))
    email=db.Column(db.String(100))
    isActive=db.Column(db.Boolean)
    isAdmin=db.Column(db.Boolean)
    password=db.Column(db.Text)

    # apartment = db.relationship('Apartment', backref  = 'user', lazy='dynamic')
    apartment = db.relationship('ApartmentModel', back_populates= 'user', lazy='dynamic')
    rental_agreement = db.relationship('RentalAgreementModel', back_populates= 'user', lazy='dynamic')

    def __repr__(self):
        return 'User: {}/{}'.format(self.userId, self.firstName)
    


class UserPass:
    def __init__(self, first_name = '', last_name='', user_name='', password='', user_email =''):
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.password = password
        self.user_email = user_email
        self.is_valid = False   # Checks if the user account exists in the database, the password is correct, and the account is active.
        self.is_admin = False 
     


    def hash_password(self):
        """Hash a password for storing."""
        # the value generated using os.urandom(60)
        os_urandom_static = b"ID_\x12p:\x8d\xe7&\xcb\xf0=H1\xc1\x16\xac\xe5BX\xd7\xd6j\xe3i\x11\xbe\xaa\x05\xccc\xc2\xe8K\xcf\xf1\xac\x9bFy(\xfbn.`\xe9\xcd\xdd'\xdf`~vm\xae\xf2\x93WD\x04"
        salt = hashlib.sha256(os_urandom_static).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', self.password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        """Verify a stored password against one provided by user"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'),  100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def get_random_user_pasword(self):
        # random_user = ''.join(random.choice(string.ascii_lowercase)for i in range(3))
        # self.user = random_user
        self.first_name = 'Operator_FirstName'
        self.last_name = 'Operator_LastName'
        self.user_name = 'LastName_Operator'

        password_characters = string.ascii_letters #+ string.digits + string.punctuation
        random_password = ''.join(random.choice(password_characters)for i in range(3))
        self.password = random_password

    def login_user(self):
        user_record = UserModel.query.filter(UserModel.userName == self.user_name).first()

        if user_record != None and self.verify_password(user_record.password, self.password):
            return user_record
        else:
            self.user = None
            self.password = None
            return None
        
    def get_user_info(self):
        db_user = UserModel.query.filter(UserModel.userName == self.user_name).first()

        if db_user == None:
            self.is_valid = False
            self.is_admin = False
            self.user_email = ''
        elif db_user.isActive !=1:
            self.is_valid = False
            self.is_admin = False
            self.user_email = db_user.email
        else:
            self.is_valid = True
            self.is_admin = db_user.isAdmin
            self.user_email = db_user.email

