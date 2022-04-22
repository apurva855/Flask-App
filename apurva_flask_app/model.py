from apurva_flask_app import db,login_manager
from flask_login import UserMixin
from enum import unique

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    role=db.Column(db.String(10),nullable=False)
    username=db.Column(db.String(100),unique=True,nullable=False)
    firstName=db.Column(db.String(50),nullable=False)
    lastName=db.Column(db.String(50),nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable=False)

class Offices(db.Model):
    officecode=db.Column(db.Integer,primary_key=True)
    city=db.Column(db.String(60),nullable=False)
    phone=db.Column(db.String(60),nullable=False)
    addressline1=db.Column(db.String(60),nullable=False)
    addressline2=db.Column(db.String(60),nullable=False)
    state=db.Column(db.String(60),nullable=False)
    country=db.Column(db.String(60),nullable=False)
    postalcode=db.Column(db.String(60),nullable=False)
    territory=db.Column(db.String(60),nullable=False)

    def serialize(self):
            return {"officeCode": self.officecode,
                    "city": self.city,
                    "phone": self.phone,
                    "addressline1": self.addressline1,
                    "addressline2": self.addressline2,
                    "country": self.country,
                    "postalcode": self.postalcode,
                    "territory": self.territory}

class Employees(db.Model):
    employeeNumber=db.Column(db.Integer,primary_key=True)
    lastName=db.Column(db.String(60),nullable=False)
    firstName=db.Column(db.String(60),nullable=False)
    extension=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(60),nullable=False)
    officeCode=db.Column(db.Integer,nullable=False)
    reportsTo=db.Column(db.String(60),nullable=False)
    jobTitle=db.Column(db.String(60),nullable=False)

    def serialize(self):
            return {"employeeNumber": self.employeeNumber,
                    "lastName": self.lastName,
                    "firstName": self.firstName,
                    "extension": self.extension,
                    "email": self.email,
                    "officeCode": self.officeCode,
                    "reportsTo": self.reportsTo,
                    "jobTitle": self.jobTitle}


    #def __repr__(self):
        #return f"User('{self.username}', '{self.email}')"

db.create_all()