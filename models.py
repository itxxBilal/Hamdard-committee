from app import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    father_name = db.Column(db.String(50), nullable=False)
    cnic = db.Column(db.String(13), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    cnic_pic = db.Column(db.String(100), nullable=False)
    profile_pic = db.Column(db.String(100), nullable=False)
