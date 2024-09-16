from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from config import db
from datetime import datetime
import re


# USER MODEL

class User(db.Model, SerializerMixin):
    
    __tablename__ = 'users_table'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, nullable=False, unique = True) #database constraints
    email = db.Column(db.String)
    address = db.Column(db.String)
    phone_number = db.Column(db.String)
    age = db.Column(db.Integer)
    vip = db.Column(db.Boolean)
    year_joined = db.Column(db.Integer) # range 

    #decorator for validating
    @validates('year_joined')
    def validate_year_joined(self, key, value):
        #current_year = datetime.now().year
        #if validation doesn't pass raise an error
        if value not in range(2000, datetime.now().year + 1):
            raise ValueError('year_joined must be between 2000 and 2024')
        
        return value
    
    @validates('email')
    def validates_email(self, key,value):
        if value.count('@') != 1:
            raise ValueError('Invalid email format')

        return value
    
    @validates('username')
    def validates_username(self, key, value):
        naughty_list=['heck', 'frack', 'bish']
        for naughty in naughty_list:
            if naughty in value:
                raise ValueError('Username cannot have bad words')
            
        return value
    
    @validates('phone_number')
    def validates_phone_number(self, key, value):
        if len(value) != 12:
            raise ValueError('invalid phone number format')
        
        if re.match('^[a-zA-Z]+$', value):
            raise ValueError('invalid phone number')
        
        return value.strip('-')
    
    @validates('address')
    def validates_address(self, key, value):
        address_words=['Street', 'Avenue', 'Road']
        for word in address_words:
            if word not in value:
                raise ValueError('Invalid address')
            
        if not re.match(r'\d{5}$', value[-5:]):
            raise ValueError('need valid 5 digit zipcode at end')
        
        return value
        
    

